# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app         import db
from flask_login import UserMixin
from sqlalchemy import *

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
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('order_item_id', db.Integer, db.ForeignKey('menu_item.id'), primary_key=True)
)

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
                
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer)
    #order_items = db.relationship('MenuItem', secondary='order_lines', lazy='subquery',backref=db.backref('orders', lazy=True))
    order_items = db.relationship("MenuItem", secondary=order_lines)
    
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
        return(str(total))






