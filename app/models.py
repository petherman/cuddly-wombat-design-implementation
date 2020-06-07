# -*- encoding: utf-8 -*-

# This is the collection of data access object (DAO) classes

"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""



from app         import db
from flask_login import UserMixin
from sqlalchemy import *
from datetime import datetime, timedelta

class User(UserMixin, db.Model):

    id = db.Column(db.Integer,     primary_key=True)
    user = db.Column(db.String(64),  unique = True)
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(500))

    def __init__(self, user, email, password):
        self.user       = user
        self.password   = password
        self.email      = email

    def __repr__(self):
        return '<User %r - %s>' % (self.id) % (self.email)

    def save(self):
        # inject self into db session    
        db.session.add ( self )
        # commit change and save the object
        db.session.commit( )
        return self 


# This table is a helper table to facilitate many to many relationship
order_lines = db.Table('order_lines',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
    db.Column('order_item_id', db.Integer, db.ForeignKey('ordered_item.id'))
)

# This is the menu item DAO
class MenuItem(db.Model):
    __tablename__ = 'menu_item'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(250))
    category = db.Column(db.String(64))
    price = db.Column(db.String(5))

    def __init__(self,name,description,category,price):
        self.name = name
        self.description = description
        self.category = category
        self.price = price
    
    def save(self):
        db.session.add ( self )
        # commit change and save the object
        db.session.commit( )
        return self 

# This is the order DAO                
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer)
    order_status= db.Column(db.Boolean)
    order_items = db.relationship("OrderedItem", secondary=order_lines)
    last_update_time = db.Column(db.DateTime)
    due_time = db.Column(db.DateTime)
    total = db.Column(db.Integer)
    
    def __init__(self,table_number):
        self.table_number = table_number
        
    def add_item(self,item):
        self.order_items.append(item)
        # commit change and save the object
        db.session.commit()
    
    def calc_total(self):
        total=float(0.00)
        for item in self.order_items:
            total+=float(item.price)
        total=round(total,2)
        total=format(total,'.2f')
        self.total=total
        return(str(total))

    def save(self):
        db.session.add ( self )
        self.update()
        return self 

    def update(self):
        self.last_update_time = datetime.now()
        self.due_time = self.last_update_time + timedelta(minutes=30)
        # commit change and save the object
        db.session.commit( )
        return self 
    
    def close_order(self):
        self.order_status = 0
        self.update()

    def reopen_order(self):
        self.order_status = 1
        self.update()


class OrderedItem(db.Model):
# This is the menu item DAO
    __tablename__ = 'ordered_item'
    id = db.Column(db.Integer, primary_key=True)
    ordered_item_id = db.Column(db.Integer)     
    name = db.Column(db.String(64))
    description = db.Column(db.String(250))
    category = db.Column(db.String(64))
    price = db.Column(db.String(5))

    def __init__(self,ordered_item_id,name,description,category,price):
        self.ordered_item_id = ordered_item_id
        self.name = name
        self.description = description
        self.category = category
        self.price = price
    
    def save(self):
        db.session.add ( self )
        # commit change and save the object
        db.session.commit( )
        return self 

class Reservation(db.Model):
    reservation_name = db.Column(db.String(64), primary_key=True)
    contact_number = db.Column(db.String(64), primary_key=True)
    party_size = db.Column(db.Integer, primary_key=True)
    reservation_time = db.Column(db.DateTime, primary_key=True)
    
    def __init__(self, reservation_name, contact_number, party_size, reservation_time):
        self.reservation_name = reservation_name
        self.contact_number = contact_number
        self.party_size = party_size
        self.reservation_time = reservation_time

    def save(self):
        db.session.add ( self )
        # commit change and save the object
        db.session.commit( )
        return self         
    



