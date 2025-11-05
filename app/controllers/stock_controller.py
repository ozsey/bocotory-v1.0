from flask import Blueprint, render_template, request, jsonify
from app import db
from app.models.stock_model import login_required, role_required, ROLE_ADMIN, ROLE_MANAGER

stock_bp = Blueprint('stock', __name__)

@stock_bp.route('/manage_stock', methods=['GET'])
@login_required
@role_required(ROLE_ADMIN, ROLE_MANAGER)
def manage_stock():
    stocks = list(db.stock.find())
    return render_template('manage_stock.html', stocks=stocks)

@stock_bp.route('/add_stock', methods=['POST'])
@login_required
@role_required(ROLE_ADMIN, ROLE_MANAGER)
def add_stock():
    data = request.form
    item_name = data['item_name']
    quantity = data['quantity']
    storage = data['storage']
    supplier = data['supplier']
    
    db.stock.insert_one({
        'item_name': item_name,
        'quantity': quantity,
        'storage': storage,
        'supplier': supplier
    })
    return jsonify({'message': 'Stock added successfully.'}), 200

@stock_bp.route('/update_stock/<stock_id>', methods=['POST'])
@login_required
@role_required(ROLE_ADMIN, ROLE_MANAGER)
def update_stock(stock_id):
    data = request.form
    item_name = data['item_name']
    quantity = data['quantity']
    storage = data['storage']
    supplier = data['supplier']
    
    db.stock.update_one({'_id': stock_id}, {
        '$set': {
            'item_name': item_name,
            'quantity': quantity,
            'storage': storage,
            'supplier': supplier
        }
    })
    return jsonify({'message': 'Stock updated successfully.'}), 200

@stock_bp.route('/delete_stock/<stock_id>', methods=['POST'])
@login_required
@role_required(ROLE_ADMIN, ROLE_MANAGER)
def delete_stock(stock_id):
    db.stock.delete_one({'_id': stock_id})
    return jsonify({'message': 'Stock deleted successfully.'}), 200
