

class Presence(object):
    def __init__(self, presence_service):
        self.statuses = {}
        self.presence_service = presence_service

    def get_status(self, email):
        return self.statuses.get(email, 'unknown')

    def update_status(self, data):
        for status in data:
            self.statuses[status['email']] = status['status']


