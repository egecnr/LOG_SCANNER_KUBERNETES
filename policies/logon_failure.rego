package login_failures

default allow = false

alert_message_template = "{userhost} tried to access {dbusername} at {event_timestamp} time for {number_of_attempts} times within 5 minutes. This may indicate a security vulnerability such as a brute-force attack or unauthorized access attempt. Therefore, it requires further examination."

allow_inspection {
    input.action_name == "LOGON"
    input.unified_audit_policies == "ORA_LOGON_FAILURES"
}

alert[msg] {
    allow_inspection
    input.number_of_attempts >= 5
    msg = sprintf(alert_message_template, [input.userhost, input.dbusername, input.event_timestamp, input.number_of_attempts])
}
