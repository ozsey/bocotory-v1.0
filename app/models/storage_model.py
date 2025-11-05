from flask import session, redirect, url_for, flash
from functools import wraps
from app import db

ROLE_ADMIN = 'admin'
ROLE_MANAGER = 'manager'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def role_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user = db.users.find_one({'username': session['username']})
            if user and user['role'] not in roles:
                flash('You do not have permission to access this page.', 'error')
                return redirect(url_for('auth.login'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper