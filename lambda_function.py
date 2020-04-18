import json
import urllib3

from discord import Payload
from jira import JiraEvent
from settings import CONFIG


def lambda_handler(event):
    http = urllib3.PoolManager()
    e = JiraEvent(event)
    payload = Payload('JIRA', e)
    url = CONFIG["discordWarningWebhookUrl"] if not e.is_handled() else CONFIG["discordWebhookUrl"]

    r = http.request(
        'POST',
        '' if CONFIG["doNotSend"] else url,
        headers={"Content-type": "application/json"},
        body=json.dumps(payload.data).encode("utf-8"))

    return {
        "isBase64Encoded": False,
        "statusCode": r.status,
        "headers": {"headerName": "headerValue"},
        "body": r.data.decode("utf-8")
    }