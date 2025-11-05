from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash
from app import db
from app.models.user_model import get_current_user, login_required, role_required, ROLE_ADMIN, ROLE_MANAGER, ROLE_STAFF

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/manage_profile', methods=['GET', 'POST'])
@login_required
@role_required(ROLE_ADMIN, ROLE_MANAGER, ROLE_STAFF)
def manage_profile():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = db.users.find_one({'username': session['username']})
        db.users.update_one({'username': session['username']}, {
            '$set': {
                'name': name,
                'email': email,
                'password': generate_password_hash(password) if password else user['password']
            }
        })
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('profile.manage_profile'))
    return render_template('manage_profile.html', user=get_current_user())
