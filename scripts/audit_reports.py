#!/usr/bin/env python3

"""Collect audit reports form oci logging search and creates a csv file"""

import argparse
from pathlib import Path

from utils.date_utils import parse_date, validate_date_range
from utils.logging_setup import get_logger, setup_logging
from utils.report_utils import Report
from utils.search_log_utils import generate_csv_from_logs

log = get_logger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--time-start",
        dest="time_start",
        type=parse_date,
        required=True,
    )
    parser.add_argument(
        "--time-end",
        dest="time_end",
        type=parse_date,
        required=True,
    )
    parser.add_argument(
        "--type",
        type=Report,
        choices=list(Report),
        required=True,
        help="Report type"
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        default=Path("reports"),
        help="Output folder for the CSV file (default: ./reports).",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Log level: DEBUG|INFO|WARNING|ERROR|CRITICAL (default: INFO).",
    )
    parser.add_argument(
        "--compartment",
        default=None,
        help="Specify the compartment where an identity domain exists."
    )
    return parser.parse_args()


def main():
    args = parse_args()
    setup_logging(use_rich=True)

    try:
        validate_date_range(
            time_start=args.time_start,
            time_end=args.time_end
        )

        output_dir: Path = args.output_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        out_path = generate_csv_from_logs(
            report_type=args.type,
            time_start=args.time_start,
            time_end=args.time_end,
            output_dir=args.output_dir
        )

        log.info("Done. File: %s", out_path)
        return 0
    except Exception as exc:
        log.exception("Failed: %s", exc)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

