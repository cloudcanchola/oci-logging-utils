from enum import Enum

from utils.report_queries import successful_logins_report, failed_logins_report, \
    application_access_report, audit_log_report, app_role_assignments_report, \
    delivery_failure_report

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"


class Report(str, Enum):
    audit = "audit"
    roles = "roles"
    access = "access"
    fail = "fail"
    success = "success"
    delivery_failure = "delivery_failure"


REPORTS = {
    "success": {
        "fn": successful_logins_report,
        "fields": ["Domain", "Login", "Result", "Provider", "Date"]
    },
    "fail": {
        "fn": failed_logins_report,
        "fields": ["Domain", "Login", "Result", "Comments", "Date"]
    },
    "access": {
        "fn": application_access_report,
        "fields": [
            "Domain", "User", "Login", "Success/Failure", "Application", "Date"
        ]
    },
    "audit": {
        "fn": audit_log_report,
        "fields": [
            "Date", "Domain", "Actor", "Event ID", "Description", "Target"
        ]
    },
    "roles": {
        "fn": app_role_assignments_report,
        "fields": [
            "Domain",
            "Approver",
            "Application Name",
            "Beneficiary",
            "User/Group",
            "Application Role Name",
            "Date",
            "Added/Removed"
        ]
    },
    "delivery_failure": {
        "fn": delivery_failure_report,
        "fields": [
            "Date", "Domain", "Actor", "Event ID", "Description", "Target"
        ]
    },
}



