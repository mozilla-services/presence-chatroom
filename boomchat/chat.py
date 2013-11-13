import json


class Chat(object):
    def __init__(self):
        self.clients = []

    def add_client(self, client):
        evt = {'user': client.get_username(),
               'status': 'online'}
        self.clients.append(client)
        self.broadcast(client, evt)

    def remove_client(self, client):
        user = client.get_username()
        evt = {'user': user,
               'status': 'offline'}

        self.broadcast(client, evt)
        if client in self.clients:
            self.clients.remove(client)

    def broadcast(self, client, message):
        evt = {'user': client.get_username(),
               'message': message}
        evt = json.dumps(evt)
        for c in self.clients:
            c.write_message(evt)
