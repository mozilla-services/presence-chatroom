import os
from ws4py.client.tornadoclient import TornadoWebSocketClient
import json


class PresenceClient(TornadoWebSocketClient):

    def __init__(self, url, token, onreceive, *args, **kw):
        TornadoWebSocketClient.__init__(self, url, *args, **kw)
        self.onreceive = onreceive
        self.token = token

    def opened(self):
        self.send(json.dumps({'token': self.token,
                              'action': 'auth'}))

    def received_message(self, msg):
        data = json.loads(msg.data)
        if data.get('action') == 'auth':
            # that's the auth ACK
            if data['result'] != 'OK':
                self.close()
        else:
            self.onreceive(data)

    def _cleanup(self):
        pass


class Presence(object):
    def __init__(self, service, appid, token):
        self.statuses = {}
        self.appid = appid
        self.service = service
        self._subs = []
        self._ws = None
        self.token = token
        self.initialize()

    def initialize(self):
        url = os.path.join(self.service, self.appid)
        self._ws = PresenceClient(url, token=self.token,
                                  onreceive=self.update_status)

        self._ws.connect()

    def register(self, callable):
        self._subs.append(callable)

    def unregister(self, callable):
        self._subs.remove(callable)

    def get_status(self, email):
        return self.statuses.get(email, 'unknown')

    # triggered by the presence service via websockets
    def update_status(self, data):
        status = data.get('status')
        user = data.get('user')
        if user is not None and status is not None:
            for sub in self._subs:
                sub(data)
            self.statuses[user] = status
