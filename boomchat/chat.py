import json


class Chat(object):
    def __init__(self):
        self.clients = []

    def get_users(self):
        return [client.get_username() for client in self.clients]

    def add_client(self, client):
        user = client.get_username()
        # make sure we remove a previous connection
        for exclient in self.clients:
            if exclient.get_username() == user:
                self.clients.remove(exclient)

        evt = {'user': client.get_username(),
               'status': 'connected'}
        self.clients.append(client)

    def remove_client(self, client):
        user = client.get_username()
        evt = {'user': user,
               'status': 'disconnected'}

        self.broadcast(client, evt)
        if client in self.clients:
            self.clients.remove(client)

    def broadcast(self, client, message):
        evt = {'user': client.get_username(),
               'message': message}
        evt = json.dumps(evt)
        for c in self.clients:
            try:
                c.write_message(evt)
            except AttributeError:
                pass   #meh
