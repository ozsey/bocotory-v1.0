from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models.storage_model import login_required, role_required, ROLE_ADMIN, ROLE_MANAGER

storage_bp = Blueprint('storage', __name__)

@storage_bp.route('/manage_storage', methods=['GET'])
@login_required
@role_required(ROLE_ADMIN, ROLE_MANAGER)
def manage_storage():
    storages = list(db.storage.find())
    return render_template('manage_storage.html', storages=storages)

@storage_bp.route('/add_storage', methods=['POST'])
@login_required
@role_required(ROLE_ADMIN, ROLE_MANAGER)
def add_storage():
    data = request.form
    storage_name = data['storage_name']
    location = data['location']
    manager = data['manager']
    
    db.storage.insert_one({
        'storage_name': storage_name,
        'location': location,
        'manager': manager
    })
    return jsonify({'message': 'Storage added successfully.'}), 200

@storage_bp.route('/update_storage/<storage_id>', methods=['POST'])
@login_required
@role_required(ROLE_ADMIN, ROLE_MANAGER)
def update_storage(storage_id):
    data = request.form
    storage_name = data['storage_name']
    location = data['location']
    manager = data['manager']
    
    db.storage.update_one({'_id': storage_id}, {
        '$set': {
            'storage_name': storage_name,
            'location': location,
            'manager': manager
        }
    })
    return jsonify({'message': 'Storage updated successfully.'}), 200

@storage_bp.route('/delete_storage/<storage_id>', methods=['POST'])
@login_required
@role_required(ROLE_ADMIN, ROLE_MANAGER)
def delete_storage(storage_id):
    db.storage.delete_one({'_id': storage_id})
    return jsonify({'message': 'Storage deleted successfully.'}), 200
