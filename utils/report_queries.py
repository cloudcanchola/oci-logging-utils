
def successful_logins_report(compartment: str) -> str:
    return (
        f" search \"{compartment}\" | "
        "where data.additionalDetails.eventId = 'sso.session.create.success'"
        "| select data.additionalDetails.domainDisplayName as Domain, "
        "data.additionalDetails.actorName as Login, "
        "data.additionalDetails.eventId as Result, "
        "data.additionalDetails.ssoRp as Provider, "
        "time_format(datetime, 'yyyy-MM-dd hh:mm:ss z') as Date"
    )


def failed_logins_report(compartment: str) -> str:
    return (
        f"search \"{compartment}\" | "
        "where data.additionalDetails.eventId = 'sso.authentication.failure' | "
        "select data.additionalDetails.domainDisplayName as Domain, "
        "data.additionalDetails.actorName as User, "
        "data.additionalDetails.eventId as Result, "
        "data.message as Comments, "
        "time_format(datetime, 'yyyy-MM-dd hh:mm:ss z') as Date"
    )


def application_access_report(compartment: str) -> str:
    return (
        f"search \"{compartment}\" | "
        "where data.additionalDetails.eventId = 'sso.session.create.success' "
        "or data.additionalDetails.eventId = 'sso.authentication.failure' "
        "or data.additionalDetails.eventId = 'sso.session.modify.success' | "
        "select data.additionalDetails.domainDisplayName as Domain, "
        "data.additionalDetails.actorDisplayName as User, "
        "data.additionalDetails.actorName as Login, "
        "data.additionalDetails.eventId as \"Success/Failure\", "
        "data.additionalDetails.ssoRp as Application, "
        "time_format(datetime, 'yyyy-MM-dd hh:mm:ss z') as Date"
    )


def audit_log_report(compartment: str) -> str:
    return (
        f"search \"{compartment}\" | "
        "where data.additionalDetails.eventId = 'sso.app.access.success' or "
        "data.additionalDetails.eventId = 'sso.app.access.failure' or "
        "data.additionalDetails.eventId = 'sso.session.create.success' or "
        "data.additionalDetails.eventId = 'sso.authentication.failure' or "
        "data.additionalDetails.eventId = 'sso.session.delete.success' or "
        "data.additionalDetails.eventId = 'sso.session.modify.success' or "
        "data.additionalDetails.eventId = 'admin.user.create.success' or "
        "data.additionalDetails.eventId = 'admin.user.activated.success' or "
        "data.additionalDetails.eventId = 'admin.user.deactivated.success' or "
        "data.additionalDetails.eventId = 'admin.user.update.success' or "
        "data.additionalDetails.eventId = 'admin.user.delete.success' or "
        "data.additionalDetails.eventId = 'admin.user.password.reset.success' or "
        "data.additionalDetails.eventId = 'admin.me.password.reset.success' or "
        "data.additionalDetails.eventId = 'admin.me.password.change.success' or "
        "data.additionalDetails.eventId = 'admin.policy.create.success' or "
        "data.additionalDetails.eventId = 'admin.rule.create.success' or "
        "data.additionalDetails.eventId = 'admin.policy.update.success' or "
        "data.additionalDetails.eventId = 'admin.rule.update.success' or "
        "data.additionalDetails.eventId = 'admin.passwordpolicy.create.success' or "
        "data.additionalDetails.eventId = 'admin.passwordpolicy.update.success' or "
        "data.additionalDetails.eventId = 'admin.grant.create.success' or "
        "data.additionalDetails.eventId = 'admin.grant.delete.success' or "
        "data.additionalDetails.eventId = 'admin.group.create.success' or "
        "data.additionalDetails.eventId = 'admin.group.add.member.success' or "
        "data.additionalDetails.eventId = 'admin.group.remove.member.success' or "
        "data.additionalDetails.eventId = 'admin.group.delete.success' or "
        "data.additionalDetails.eventId = 'admin.app.create.success' or "
        "data.additionalDetails.eventId = 'admin.app.update.success' or "
        "data.additionalDetails.eventId = 'admin.app.delete.success' or "
        "data.additionalDetails.eventId = 'admin.app.activated.success' or "
        "data.additionalDetails.eventId = 'admin.app.deactivated.success' or "
        "data.additionalDetails.eventId = 'notification.delivery.success' or "
        "data.additionalDetails.eventId = 'notification.delivery.failure' or "
        "data.additionalDetails.eventId = 'sso.auth.factor.initiated' or "
        "data.additionalDetails.eventId = 'sso.bypasscode.create.success' or "
        "data.additionalDetails.eventId = 'admin.approle.add.member.success' or "
        "data.additionalDetails.eventId = 'admin.approle.remove.member.success' "
        "| select time_format(datetime, 'yyyy-MM-dd hh:mm:ss z') as Date, "
        "data.additionalDetails.domainDisplayName as Domain, "
        "data.additionalDetails.actorName as Actor, "
        "data.additionalDetails.eventId as \"Event ID\", "
        "data.message as \"Description\", "
        "data.additionalDetails.adminResourceName as Target"
    )


def app_role_assignments_report(compartment: str) -> str:
    return (
        f"search \"{compartment}\" | "
        "where data.additionalDetails.eventId = 'admin.approle.add.member.success' "
        "or data.additionalDetails.eventId = 'admin.approle.remove.member.success' | "
        "select data.additionalDetails.domainDisplayName as Domain, "
        "data.additionalDetails.actorDisplayName as Approver, "
        "data.additionalDetails.adminAppRoleAppName as \"Application Name\", "
        "data.additionalDetails.adminRefResourceName as Beneficiary, "
        "data.additionalDetails.adminRefResourceType as \"User/Group\", "
        "data.additionalDetails.adminResourceName as \"Application Role Name\", "
        "time_format(datetime, 'yyyy-MM-dd hh:mm:ss z') as Date, "
        "data.additionalDetails.eventId as \"Added/Removed\""
    )


def delivery_failure_report(compartment: str) -> str:
    return (
        f"search \"{compartment}\" | "
        "where data.additionalDetails.eventId = 'notification.delivery.failure'"
        "| select time_format(datetime, 'yyyy-MM-dd hh:mm:ss z') as Date, "
        "data.additionalDetails.domainDisplayName as Domain, "
        "data.additionalDetails.actorName as Actor, "
        "data.additionalDetails.eventId as \"Event ID\", "
        "data.message as \"Description\", "
        "data.additionalDetails.adminResourceName as Target"
    )
