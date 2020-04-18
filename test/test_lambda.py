import lambda_function
import json

ISSUE_CREATED = """ Copy the raw json sent from Jira here """
ISSUE_ASSIGNED = """ Copy the raw json sent from Jira here """
ISSUE_STATUS_CHANGED = """ Copy the raw json sent from Jira here """
ISSUE_LINK_CREATED = """ Copy the raw json sent from Jira here """
COMMENT_CREATED = """ Copy the raw json sent from Jira here """
COMMENT_UPDATED = """ Copy the raw json sent from Jira here """
COMMENT_DELETED = """ Copy the raw json sent from Jira here """

ACTUALLY_HIT_DISCORD = True

def escape_chars(string):
    return string.replace('\r','\\r').replace('\n','\\n')

def json_string_to_obj(string):
    return json.loads(escape_chars(string))

def test_lambda_issue_created():
    lambda_function.lambda_handler(json_string_to_obj(ISSUE_CREATED))
    x = 0

def test_lambda_issue_assigned():
    lambda_function.lambda_handler(json_string_to_obj(ISSUE_ASSIGNED))
    x = 0

def test_lambda_comment_created():
    lambda_function.lambda_handler(json_string_to_obj(COMMENT_CREATED))
    x = 0

def test_lambda_comment_updated():
    lambda_function.lambda_handler(json_string_to_obj(COMMENT_UPDATED))
    x = 0

def test_lambda_comment_deleted():
    lambda_function.lambda_handler(json_string_to_obj(COMMENT_DELETED))
    x = 0

def test_lambda_status_changed():
    lambda_function.lambda_handler(json_string_to_obj(ISSUE_STATUS_CHANGED))
    x = 0

