from flask import Blueprint, render_template, request, jsonify
from werkzeug.security import generate_password_hash
from app import db
from app.models.user_model import login_required, role_required, ROLE_ADMIN, ROLE_MANAGER, ROLE_STAFF, get_current_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/admin_dashboard')
@login_required
@role_required(ROLE_ADMIN)
def admin_dashboard():
    return render_template('base.html', user=get_current_user())

@user_bp.route('/manager_dashboard')
@login_required
@role_required(ROLE_MANAGER)
def manager_dashboard():
    return render_template('base.html', user=get_current_user())

@user_bp.route('/staff_dashboard')
@login_required
@role_required(ROLE_STAFF)
def staff_dashboard():
    return render_template('base.html', user=get_current_user())

@user_bp.route('/manage_user', methods=['GET'])
@login_required
@role_required(ROLE_ADMIN)
def manage_user():
    users = list(db.users.find({}, {'password': 0}))
    return render_template('manage_user.html', users=users)

@user_bp.route('/add_user', methods=['POST'])
@login_required
@role_required(ROLE_ADMIN)
def add_user():
    data = request.form
    name = data['name']
    email = data['email']
    username = data['username']
    password = generate_password_hash(data['password'])
    role = data['role']
    status = data['status']
    
    if db.users.find_one({'username': username}):
        return jsonify({'message': 'Username already exists. Please choose a different username.'}), 400
    
    db.users.insert_one({
        'name': name,
        'email': email,
        'username': username,
        'password': password,
        'role': role,
        'status': status
    })
    return jsonify({'message': 'User added successfully.'}), 200

@user_bp.route('/update_user/<username>', methods=['POST'])
@login_required
@role_required(ROLE_ADMIN)
def update_user(username):
    data = request.form
    name = data['name']
    email = data['email']
    password = generate_password_hash(data['password'])
    role = data['role']
    status = data['status']
    
    db.users.update_one({'username': username}, {
        '$set': {
            'name': name,
            'email': email,
            'password': password,
            'role': role,
            'status': status
        }
    })
    return jsonify({'message': 'User updated successfully.'}), 200

@user_bp.route('/delete_user/<username>', methods=['POST'])
@login_required
@role_required(ROLE_ADMIN)
def delete_user(username):
    db.users.delete_one({'username': username})
    return jsonify({'message': 'User deleted successfully.'}), 200

@user_bp.route('/manage_staff')
@login_required
@role_required(ROLE_ADMIN, ROLE_MANAGER)
def manage_staff():
    staff = list(db.users.find({'role': ROLE_STAFF}, {'password': 0}))  # Exclude password field
    return render_template('manage_staff.html', staff=staff)

@user_bp.route('/update_staff_status/<username>', methods=['POST'])
@login_required
@role_required(ROLE_ADMIN, ROLE_MANAGER)
def update_staff_status(username):
    status = request.form['status']
    db.users.update_one({'username': username}, {'$set': {'status': status}})
    return jsonify({'message': f'Staff status updated to {status}.'}), 200

@user_bp.route('/delete_staff/<username>', methods=['POST'])
@login_required
@role_required(ROLE_ADMIN, ROLE_MANAGER)
def delete_staff(username):
    db.users.delete_one({'username': username})
    return jsonify({'message': 'Staff deleted successfully.'}), 200
