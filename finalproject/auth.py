import functools
from .models import User, db

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

# from finalproject.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')
ass = Blueprint('auth', __name__, url_prefix='/auth')
ass = Blueprint('hihi', "hihihi", url_prefix="/hi")

@bp.route('/register', methods=('GET', 'POST'))
def register():
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repassword =  request.form['repassword']
        error = None
        if not username or not password:
            error = "Username required"
        if not password:
            error = "Password required"
        if not repassword:
            error = "Repassword required"
        if password != repassword:
            error = "Passwords don't match"
        if User.query.filter_by(username=username).first() is not None:
            error = 'User {} is already registered.'.format(username)
        print(error)
        if error is None:
            new_user = User(username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    print(request.cookies)
    error = None
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if not (username and password):
            error = "Username and password required"
        else:
            user = User.query.filter_by(username=username).first()
            if user is None or not check_password_hash(user.password, password):
                error = "Invalid username or password"
                print(error)
        if error is None:
            print('here')
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('index'))
        flash(error)

    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Login required decorator
def login_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@bp.before_app_request
def get_user():
    print("PRINT BEFORE REQUEST")
    user = session.get('user_id')
    if user is None:
        g.user = None
    else:
        g.user = User.query.get(user)
