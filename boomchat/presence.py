from ws4py.client.tornadoclient import TornadoWebSocketClient
import json


class PresenceClient(TornadoWebSocketClient):

    def __init__(self, url, onreceive, *args, **kw):
        TornadoWebSocketClient.__init__(self, url, *args, **kw)
        self.onreceive = onreceive

    def received_message(self, msg):
        self.onreceive(json.loads(msg.data))

    def _cleanup(self):
        pass


class Presence(object):
    def __init__(self, presence_service):
        self.statuses = {}
        self.presence_service = presence_service
        self._ws = PresenceClient(presence_service,
                                  onreceive=self.update_status)
        self._ws.connect()
        self._subs = []

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
