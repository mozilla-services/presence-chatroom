from bottle import get, view, app, request, redirect, route, abort
from boomchat.user import User


@get('/')
@view('index')
def index():
    return {'title': 'BoomChat',
            'session': request.environ.get('beaker.session'),
            'contacts': _get_contacts()}


def _get_contacts():
    app_session = request.environ.get('beaker.session')
    connected_users = app.chat.get_users()

    if app_session.get('logged_in', False):
        user = User(app_session['email'])

        contacts = {}
        for contact in user.contacts:
            contacts[contact] = app.presence.get_status(contact)

        users = [{'user': user.email, 'status': 'online'}]
        for user, status in contacts.items():
            if user in connected_users:
                users.append({'user': user,
                              'status': 'online'})
            else:
                users.append({'user': user,
                              'status': contacts[user]})
    else:
        users = []
        for user in connected_users:
            users.append({'user': user, 'status': 'online'})

    users.sort()
    return users


@route('/getContacts', method='GET')
def get_contacts():
    return {'contacts': _get_contacts()}


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
