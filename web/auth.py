#########################
#Authentification module#
#########################

from web import app
from web import login_manager
from flask.ext.login import login_required
import flask.ext.login as flask_login
from functools import wraps
from flask import request, Response
from flask import redirect, url_for
from flask.ext.login import UserMixin
import flask.ext.login as flask_login
from flask import render_template

def get_users():
    return {'admin': {'password': '1234'}}

class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in get_users():
        return

    user = User()
    user.id = email
    return user

#def login_required(f):
#    @wraps(f)
#    def decorated_function(*args, **kwargs):
#        if g.user is None:
#            return redirect(url_for('login', wantsurl = request.path))
#        return f(*args, **kwargs)
#    return decorated_function


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in get_users():
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    users = get_users()
    user.is_authenticated = (request.form['password'] == users[email]['password'])

    return user

@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('Login.html', wantsurl=url_for('index'))

@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        users = get_users()
        if email in users:
            if request.form['password'] == users[email]['password']:
                user = User()
                user.id = email
                flask_login.login_user(user)
                if request.form['wantsurl']:
                    #print "*"*100
                    #request.form['wantsurl']
                    #print "*"*100
                    return redirect(url_for('adminPanel'))
                    
                else:
                    #print "F"*100
                    return redirect(url_for('index'))
    return render_template('Login.html', wantsurl=url_for('index'))

#########################
#Authentification module#
#########################
