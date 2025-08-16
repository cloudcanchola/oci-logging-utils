import csv
import shutil
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterator, Mapping, Any

import oci.config
from oci.exceptions import ServiceError
from oci.loggingsearch import LogSearchClient
from oci.loggingsearch.models import SearchLogsDetails
from rich.progress import track

from utils.logging_setup import get_logger
from utils.report_utils import Report, REPORTS

log = get_logger(__name__)


def generate_logs_per_chunks(
        client: LogSearchClient,
        details: SearchLogsDetails,
) -> Iterator[Mapping[str, Any]]:
    """
    Generator function to iterate paginated results from logging search
    handling 1000 oci pagination limit.
    :return: Iterator
    """
    page_token = None
    response = None
    while True:
        try:
            response = client.search_logs(
                search_logs_details=details,
                limit=1000,  # OCI max value per page
                page=page_token
            )
        except ServiceError as se:
            log.error(
                "Service Error: %s",
                se,
            )
        except Exception as e:
            log.exception("Unexpected error during log pagination", e)

        for entry in response.data.results:
            yield entry.data

        page_token = response.next_page

        if not response.has_next_page:
            break


def generate_csv_from_logs(
        report_type: Report,
        time_start: datetime,
        time_end: datetime,
        output_dir: Path | None,
        compartment: str | None = None,
) -> str:
    """
    Calls generate_logs_per_chunks and creates a csv, handles each call in
    14 days ranges.
    :return: str Path
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".csv", dir=output_dir)
    tmp_file = Path(tmp_path)
    config = oci.config.from_file()

    # Default to root compartment
    if not compartment:
        compartment = config["tenancy"]

    logging_client = LogSearchClient(config=config)

    search_query = REPORTS[report_type]["fn"](compartment)
    report_fields = REPORTS[report_type]["fields"]

    log.info(f"Creating report: {report_type}")

    if not output_dir:
        output_dir = f"reports/{report_type}{datetime.now()}.csv"

    try:
        with open(
                tmp_file, "w",
                newline="",
                encoding="utf-8"
        ) as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=report_fields)
            writer.writeheader()

            chunk_start = time_start
            while chunk_start < time_end:
                chunk_end = min(
                    chunk_start + timedelta(days=14),
                    time_end
                )

                search_details = SearchLogsDetails(
                    time_start=chunk_start,
                    time_end=chunk_end,
                    search_query=search_query,
                    is_return_field_info=False
                )

                for raw in track(generate_logs_per_chunks(
                        client=logging_client,
                        details=search_details,
                ), description=f"Logs from {chunk_start} to {chunk_end}"):
                    row = {col: raw.get(col, "") for col in report_fields}
                    writer.writerow(row)

                chunk_start = chunk_end + timedelta(microseconds=1)

        final_path = output_dir / f"{report_type}-{datetime.now()::%Y%m%d%H%M}.csv"
        shutil.move(str(tmp_file), final_path)
        log.info("Logs written to %s", final_path)

        return str(final_path)

    except Exception as e:
        log.exception("Failed to generate report. Temp file: %s", e)
        tmp_file.unlink(missing_ok=True)  # delete partial file


