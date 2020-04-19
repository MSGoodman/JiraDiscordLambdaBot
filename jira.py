from settings import CONFIG


class JiraEvent:
    def __init__(self, root_json):
        self.raw_data = root_json
        self.event_name = self.get_event_name()
        self.target = self.event_name.split(" ")[0]
        self.verb = self.event_name.split(" ", 1)[1]

        self.user = None
        self.comment = None
        self.ticket = None
        self.changelog = None
        self.attachment = None

        self.__populate_conditional_fields()

    def get_event_name(self):
        # If this is an Issue Event, get the more specific name
        if 'issue_event_type_name' in self.raw_data:
            raw_name = self.raw_data['issue_event_type_name']

            # If this is a generic event, figure out what it should actually be called
            if raw_name == 'issue_generic' and 'changelog' in self.raw_data:
                raw_name = 'issue_status_changed'
        else:
            raw_name = self.raw_data['webhookEvent']

        # Now make it pretty
        return raw_name.replace("_", " ").title()

    def is_handled(self):
        return self.event_name in CONFIG["handledEvents"]

    def is_ignored(self):
        return self.event_name in CONFIG["ignoredEvents"]

    def get_actor(self):
        if self.user:
            return self.user
        elif self.comment:
            return self.comment.update_author
        elif self.ticket:
            return self.ticket.assignee
        elif self.attachment:
            return self.attachment.author

    def title(self):
        if self.ticket:
            return f'{self.ticket.key}: {self.ticket.name}'
        if self.attachment:
            return f'{self.attachment.filename}'

    def url(self):
        if self.target in ['Issue', 'Comment']:
            return f'{CONFIG["jiraRootUrl"]}{self.ticket.key}'
        if self.target == 'Attachment':
            return self.attachment.content_url
        else:
            return ''

    def description(self):
        if self.target == 'Issue':
            # Issue created shouldn't have a description, the title is enough
            if self.verb == 'Created':
                return None
            else:
                return f'{self.changelog.changed_field.title()} changed from {self.changelog.from_value} to {self.changelog.to_value}'

        if self.target == 'Comment':
            # Strikethrough if the comment was deleted
            if self.verb == 'Deleted':
                return f'~~{self.comment.body}~~'
            else:
                return self.comment.body

    def change_details(self):
        return f'{self.target} {self.verb} by {self.get_actor().name}'

    def image_url(self):
        if self.attachment:
            return self.attachment.thumbnail_url
        else:
            return None

    def __populate_conditional_fields(self):
        if 'issue' in self.raw_data:
            self.ticket = JiraTicket(self.raw_data['issue'])
        if 'comment' in self.raw_data:
            self.comment = JiraComment(self.raw_data['comment'])
        if 'changelog' in self.raw_data:
            self.changelog = JiraChangelog(self.raw_data['changelog'])
        if 'user' in self.raw_data:
            self.user = JiraUser(self.raw_data['user'])
        if 'attachment' in self.raw_data:
            self.attachment = JiraAttachment(self.raw_data['attachment'])


class JiraChangelog:
    def __init__(self, changelog_json):
        self.raw_data = changelog_json
        self.changed_field = changelog_json['items'][0]['field']
        self.from_value = changelog_json['items'][0]['fromString']
        self.to_value = changelog_json['items'][0]['toString']


class JiraTicket:
    def __init__(self, ticket_json):
        self.raw_data = ticket_json
        self.key = ticket_json['key']
        self.name = ticket_json['fields']['summary']
        self.type = ticket_json['fields']['issuetype']['name']
        self.assignee = JiraUser(ticket_json['fields']['assignee'])
        self.priority = ticket_json['fields']['priority']['name']
        self.status = ticket_json['fields']['status']['name']


class JiraComment:
    def __init__(self, comment_json):
        self.raw_data = comment_json
        self.author = JiraUser(comment_json['author'])
        self.update_author = JiraUser(comment_json['updateAuthor'])
        self.body = comment_json['body']


class JiraUser:
    def __init__(self, user_json):
        self.raw_data = user_json
        self.name = user_json['displayName']


class JiraAttachment:
    def __init__(self, attachment_json):
        self.raw_data = attachment_json
        self.filename = attachment_json['filename']
        self.author = JiraUser(attachment_json['author'])
        self.content_url = attachment_json['content']
        self.thumbnail_url = attachment_json['thumbnail']
