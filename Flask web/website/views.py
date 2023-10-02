from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import  login_required, current_user
from .models import Inventory, User
from . import db
import json


import csv
from flask import Response

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        inventory_item_name = request.form.get('inventory_name')
        inventory_count_change = int(request.form.get('inventory_count_change', 0))

        existing_item = Inventory.query.filter_by(item_name=inventory_item_name, user_id=current_user.id).first()
        
        if existing_item:
            existing_item.count += inventory_count_change
            
            # Check if the count is below threshold after decreasing
            if existing_item.count < User.INVENTORY_THRESHOLD:
                flash(f'Warning: {inventory_item_name} count is below the threshold!', category='error')
        else:
            new_inventory = Inventory(item_name=inventory_item_name, count=inventory_count_change, user_id=current_user.id)
            db.session.add(new_inventory)
        
        db.session.commit()
        flash('Inventory updated!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-inventory', methods=['POST'])
def delete_inventory():  
    inventory_data = json.loads(request.data) 
    inventoryId = inventory_data['inventoryId']
    inventory_item = Inventory.query.get(inventoryId)

    if inventory_item and inventory_item.user_id == current_user.id:
        inventory_item.count -= 1
        
        if inventory_item.count <= 0:
            db.session.delete(inventory_item)
        
        # Check if the count is below threshold after decreasing
        if inventory_item.count < User.INVENTORY_THRESHOLD:
            flash(f'Warning: {inventory_item.item_name} count is below the threshold!', category='error')
            
        db.session.commit()

    return jsonify({})



@views.route('/generate-report')
@login_required
def generate_report():
    department_id = current_user.department_id
    items = Inventory.query.filter_by(department_id=department_id).all()

    def generate():
        data = [["Item Name", "Current Count"]]
        for item in items:
            data.append([item.item_name, item.count])  
    
        for row in data:
            yield ','.join(map(str, row)) + '\n'

    headers = {
        "Content-Disposition": "attachment; filename=report.csv",
        "Content-type": "text/csv",
    }

    return Response(generate(), headers=headers)