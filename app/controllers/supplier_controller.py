from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models.supplier_model import login_required, role_required, ROLE_ADMIN, ROLE_MANAGER

supplier_bp = Blueprint('supplier', __name__)

@supplier_bp.route('/manage_supplier', methods=['GET'])
@login_required
@role_required(ROLE_ADMIN, ROLE_MANAGER)
def manage_supplier():
    suppliers = list(db.supplier.find())
    return render_template('manage_supplier.html', suppliers=suppliers)

@supplier_bp.route('/add_supplier', methods=['POST'])
@login_required
@role_required(ROLE_ADMIN, ROLE_MANAGER)
def add_supplier():
    data = request.form
    supplier_name = data['supplier_name']
    contact_info = data['contact_info']
    
    db.supplier.insert_one({
        'supplier_name': supplier_name,
        'contact_info': contact_info
    })
    return jsonify({'message': 'Supplier added successfully.'}), 200

@supplier_bp.route('/update_supplier/<supplier_id>', methods=['POST'])
@login_required
@role_required(ROLE_ADMIN, ROLE_MANAGER)
def update_supplier(supplier_id):
    data = request.form
    supplier_name = data['supplier_name']
    contact_info = data['contact_info']
    
    db.supplier.update_one({'_id': supplier_id}, {
        '$set': {
            'supplier_name': supplier_name,
            'contact_info': contact_info
        }
    })
    return jsonify({'message': 'Supplier updated successfully.'}), 200

@supplier_bp.route('/delete_supplier/<supplier_id>', methods=['POST'])
@login_required
@role_required(ROLE_ADMIN, ROLE_MANAGER)
def delete_supplier(supplier_id):
    db.supplier.delete_one({'_id': supplier_id})
    return jsonify({'message': 'Supplier deleted successfully.'}), 200
