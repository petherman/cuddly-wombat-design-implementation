# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from app         import db
from flask_login import UserMixin

class User(UserMixin, db.Model):

    id       = db.Column(db.Integer,     primary_key=True)
    user     = db.Column(db.String(64),  unique = True)
    email    = db.Column(db.String(120), unique = True)
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

class MenuItem(db.Model):
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
        
#class OrderLine(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    order_number = db.relationship('Order', backref='order_number', lazy='dynamic')
#    order_item = db.relationship('MenuItem', backref='order_item',lazy='dynamic')
    
#class Order(db.Model):
#    id = db.Column(db.Integer, primary_key=True)
#    table_number = db.Column(db.Integer)




