import os
from ws4py.client.tornadoclient import TornadoWebSocketClient
import json


DATA_DIR = '/tmp/boomchat/'
if not os.path.exists(DATA_DIR):
    os.mkdir(DATA_DIR)


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
        print 'recieved from presence: %s' % str(data)

        if data.get('action') == 'auth':
            # that's the auth ACK
            if data['result'] != 'OK':
                self.close()
        else:
            self.onreceive(data)

    def _cleanup(self):
        pass


class Presence(object):
    def __init__(self):
        self.prefs_file = os.path.join(DATA_DIR, 'prefs')

        if not os.path.exists(self.prefs_file):
            prefs = {'appid': '8592e6f9-a696-4892-95da-bb68b8b58f56',
                     'service': 'ws://localhost:8282/myapps/',
                     'token': 'ce3ee269-dd41-4039-964b-e5eb23e43927'}

        else:
            with open(self.prefs_file) as f:
                prefs = json.loads(f.read())

        self.appid = prefs['appid']
        self.service = prefs['service']
        self.token = prefs['token']
        self.sync()

        self.statuses = {}
        self._subs = []
        self._ws = None
        self.initialize()

    def sync(self):
        prefs = {'appid': self.appid,
                 'service': self.service,
                 'token': self.token}

        with open(self.prefs_file, 'w') as f:
            f.write(json.dumps(prefs))

    def initialize(self):
        if self._ws is not None and not self._ws.terminated:
            self._ws.close()

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

        # XXX needs to convert uid to user here
        user = data.get('uid')
        data['user'] = user


        if user is not None and status is not None:
            for sub in self._subs:
                sub(data)
            self.statuses[user] = status

    def notify(self, source, target, message):
        self._ws.send(json.dumps({'token': self.token,
                                  'action': 'notify',
                                  'source': source,
                                  'target': target,
                                  'message': message}))
