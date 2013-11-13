from bottle import get, view, app, request, redirect, route, abort
from boomchat.user import User


@get('/')
@view('index')
def index():
    app_session = request.environ.get('beaker.session')
    if not app_session.get('logged_in', False):
        contacts = []
    else:
        user = User(app_session['email'])
        def _status(contact):
            return {'user': contact, 'status': app.presence.get_status(contact)}

        contacts = [_status(contact) for contact in user.contacts]

    return {'title': 'BoomChat',
            'session': request.environ.get('beaker.session'),
            'users': app.chat.get_users(),
            'contacts': contacts}


@route('/getContacts', method='GET')
def get_contacts():
    app_session = request.environ.get('beaker.session')
    if not app_session.get('logged_in', False):
        abort(401, "Sorry, access denied.")

    def _status(contact):
        return {'user': contact, 'status': app.presence.get_status(contact)}

    user  = User(app_session['email'])
    return {'contacts': [_status(contact) for contact in user.contacts]}


@route('/addContact', method='GET')
def add_contact():
    app_session = request.environ.get('beaker.session')
    if not app_session.get('logged_in', False):
        abort(401, "Sorry, access denied.")

    user  = User(app_session['email'])
    user.add_contact(request.GET['contact'])
    return {'status': 'OK'}

@route('/login', method='POST')
def login():
    assertion = request.POST['assertion']
    try:
        data = app.verifier.verify(assertion, '*')
        email = data['email']
        app_session = request.environ.get('beaker.session')
        app_session['logged_in'] = True
        app_session['email'] = email
        app_session['assertion'] = assertion
        app_session.save()
    except ValueError, UnicodeDecodeError:
        # need to raise a auth
        pass
    return {'email': email}


@route('/logout', method='POST')
def logout():
    app_session = request.environ.get('beaker.session')
    app_session['logged_in'] = False
    app_session['email'] = None
    redirect("/")
