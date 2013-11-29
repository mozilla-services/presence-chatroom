from json import dumps, loads
import os
import browserid
import beaker.middleware
import json

from bottle import ServerAdapter
import bottle
from bottle import *
from bottle.ext.tornadosocket import TornadoWebSocketServer
import tornado.web
import tornado.websocket

from boomchat.chat import Chat
from boomchat.user import User
from boomchat.presence import Presence


STATIC = os.path.join(os.path.dirname(__file__), 'static')
bottle.TEMPLATE_PATH = [os.path.join(os.path.dirname(__file__),
                                     'views')]

debug(True)

session_opts = {
    'session.type': 'file',
    'session.data_dir': './session/',
    'session.auto': True,
    }

STATIC = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))



class ChatHandler(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kw):
        tornado.websocket.WebSocketHandler.__init__(self, *args, **kw)
        self._user = None
        app.presence.register(self._presence_update)

    def _presence_update(self, data):
        data['presence'] = True
        user = data['user']

        for client in app.chat.clients:
            cuser = User(client.get_username())
            if user in cuser.contacts:
                client.write_message(dumps(data))

    def get_username(self):
        if self._user is None:
            return None
        return self._user.name

    def on_message(self, message):
        message = loads(message)
        self._user = user = User(message['user'])
        action = message.get('action')

        print 'received from js chat box ' + str(message)

        if 'status' in message:
            action = 'status'
            status = message['status']

            if status == 'connected':
                app.chat.add_client(self)
            elif status == 'disconnected':
                app.chat.remove_client(self)

            message = {'status': status,
                       'presence': True,
                       'user': message['user']}

        if action in ('chat', 'status'):
            app.chat.broadcast(self, message)
        elif action == 'notification':
            # we're sending to the presence server the live
            # notification
            app.presence.notify(user.email,
                                message['target'],
                                message['message'])

    def on_close(self):
        app.chat.remove_client(self)
        app.presence.unregister(self._presence_update)

class TornadoWebSocketServer(ServerAdapter):
    def run(self, handler): # pragma: no cover
        import tornado.wsgi, tornado.httpserver, tornado.ioloop
        wsgiapp = beaker.middleware.SessionMiddleware(handler[0])
        wsgi_handler = tornado.wsgi.WSGIContainer(wsgiapp)

        default_handlers = [
            (r".*", tornado.web.FallbackHandler, {'fallback': wsgi_handler})
        ]

        if self.options['handlers'] is not None and isinstance(self.options['handlers'], list):
            handlers = list(self.options['handlers']) + list(default_handlers)
        else:
            handlers = default_handlers

        tornado_app = tornado.web.Application(handlers)
        tornado.httpserver.HTTPServer(tornado_app).listen(self.port)
        tornado.ioloop.IOLoop.instance().start()


def main(port=8080, reloader=True):
    tornado_handlers = [
        (r"/chat", ChatHandler),
        (r"/css/(.*)", tornado.web.StaticFileHandler,
         {"path": os.path.join(STATIC, 'css')}),
        (r"/js/(.*)", tornado.web.StaticFileHandler,
         {"path": os.path.join(STATIC, 'js')}),
        (r"/images/(.*)", tornado.web.StaticFileHandler,
         {"path": os.path.join(STATIC, 'images')}),

    ]

    app.presence = Presence()
    app.chat = Chat()
    app.verifier = browserid.LocalVerifier(['*'])

    from boomchat import views

    run(port=port, reloader=reloader, app=app,
        server=TornadoWebSocketServer, handlers=tornado_handlers)
