from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from app.models.user_model import RegistrationForm, ROLE_ADMIN, ROLE_MANAGER, ROLE_STAFF

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.users.find_one({'username': username})

        if user and check_password_hash(user['password'], password) and user['status'] == 'active':
            session['username'] = username
            next_page = request.args.get('next')
            if user['role'] == ROLE_ADMIN:
                return redirect(next_page or url_for('user.admin_dashboard'))
            elif user['role'] == ROLE_MANAGER:
                return redirect(next_page or url_for('user.manager_dashboard'))
            elif user['role'] == ROLE_STAFF:
                return redirect(next_page or url_for('user.staff_dashboard'))
            else:
                flash('Invalid user role.', 'error')
        else:
            flash('Invalid credentials or account not active.', 'error')
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = generate_password_hash(form.password.data)
        role = form.role.data
        status = 'pending'

        if db.users.find_one({'username': username}):
            flash('Username already exists. Please choose a different username.', 'error')
        else:
            db.users.insert_one({
                'name': name,
                'email': email,
                'username': username,
                'password': password,
                'role': role,
                'status': status
            })
            flash('Registration successful. Awaiting admin approval.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('auth.login'))