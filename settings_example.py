CONFIG = {
    'jiraRootUrl':  "", # The root url of your Jira organization, e.g. https://developerorganizations.atlassian.net/browse
    'discordWarningWebhookUrl': "", # The webhook url for integration failures (should be things not yet implemented), e.g. https://discordapp.com/api/webhooks/999999999999999999/ABCdefghijklmonpqrstu-vwxyz12345667810111213141516171819202122212400
    'discordWebhookUrl': "", # The webhook url for jira notifications, e.g. https://discordapp.com/api/webhooks/999999999999999999/ABCdefghijklmonpqrstu-vwxyz12345667810111213141516171819202122212400
    'colorNotification': 4245067, # The color you want the embeds for notifications to be
    'colorWarning': 12268107, # The color you want the embeds for warnings to be
    'useEmbed': True, # If you would like notifications to show up as embeds
    'useContent': False, # If you would like notifications to show up as content (basically a normal post); this looks worse but if helpful because embeds don't show up if your personal settings disable link unfolding for some reason
    'doNotSend': False, # If you don't want anything to actually send to the webhook, just makes it easier to turn it off for whatever reason if you don't want to disable the webhook in Jira
    # These are the events I've set up for this to handle so far
    'handledEvents': ['Issue Created',
                      'Issue Updated',
                      'Issue Assigned',
                      'Issue Status Changed',
                      'Comment Created',
                      'Comment Updated',
                      'Comment Deleted'],
    # These are events I'm just not going to handle
    'ignoredEvents': ['Issue Property Set']
}