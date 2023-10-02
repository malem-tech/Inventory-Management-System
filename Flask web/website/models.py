from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

#class Inventory(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    data = db.Column(db.String(10000))
#    date = db.Column(db.DateTime(timezone=True), default=func.now())
#    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(255))
    count = db.Column(db.Integer, default=0)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Adding department_id to Inventory
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    inventory = db.relationship('Inventory')
    department_id = db.Column(db.Integer)
    inventory_count = db.Column(db.Integer, default=0) 
    INVENTORY_THRESHOLD = 10  

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    items = db.relationship('Inventory', backref='department', lazy=True)
