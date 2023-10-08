package login_failures

default allow = false

alert_message =  "ALERT !!!!  %s tried to access %s at %s time for %d times within 5 minutes. This may indicate a security vulnerability such as a brute-force attack or unauthorized access attempt. Therefore, it requires further examination."

allow_inspection {
    input.action_name == "LOGON"
    input.unified_audit_policies == "ORA_LOGON_FAILURES"
}

attempts_limit_passed {
    input.number_of_attempts >= 5
}

attempts_limit_not_passed {
    input.number_of_attempts <5
}

alert[msg] {
    allow_inspection
    attempts_limit_passed
    msg = sprintf(alert_message, [input.userhost, input.dbusername, input.event_timestamp, input.number_of_attempts])
}

minor_threat_message = "INFORMATION %s has tried to access %s %d times. This action still poses a minor threat since it is less than 5 times in the last five minutes. More attempts will lead to an alert in the future."

alert[msg] {
    allow_inspection
    attempts_limit_not_passed
    msg = sprintf(minor_threat_message, [input.userhost, input.dbusername, input.number_of_attempts])
}