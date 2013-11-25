import os
import json

DATA_DIR = '/tmp/boomchat/'
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)


# place holder for user info
class User(object):

    def __init__(self, email):
        self.email = email
        self._file = os.path.join(DATA_DIR, email)

        if os.path.exists(self._file):
            with open(self._file) as f:
                data = f.read()
                self._data = json.loads(data)
        else:
            self._data = {}

    def _sync(self):
        with open(self._file, 'w') as f:
            f.write(json.dumps(self._data))

    def set_presence_uid(self, uid):
        self._data['uid'] = uid
        self._sync()

    def get_presence_uid(self):
        return self._data.get('uid')

    @property
    def name(self):
        return self.email

    @property
    def contacts(self):
        return self._data.get('contacts', [])

    def add_contact(self, contact):
        contacts = self._data.get('contacts', [])
        if contact not in contacts:
            contacts.append(contact)
        self._data['contacts'] = contacts
        self._sync()
