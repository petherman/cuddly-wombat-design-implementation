# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf          import FlaskForm
from flask_wtf.file     import FileField, FileRequired
from wtforms            import StringField, TextAreaField, SubmitField, PasswordField, IntegerField, FieldList, FormField, HiddenField, DateField
from wtforms.fields.html5 import TimeField
from wtforms.validators import InputRequired, Email, DataRequired

class LoginForm(FlaskForm):
	username    = StringField  (u'Username'        , validators=[DataRequired()])
	password    = PasswordField(u'Password'        , validators=[DataRequired()])
	
class RegisterForm(FlaskForm):
	username    = StringField  (u'Username'  , validators=[DataRequired()])
	password    = PasswordField(u'Password'  , validators=[DataRequired()])
	email       = StringField  (u'Email'     , validators=[DataRequired(), Email()])
	
class AddMenuItemForm(FlaskForm):
	name    = StringField  (u'Name'  , validators=[DataRequired()])
	description    = StringField  (u'Description'  , validators=[DataRequired()])
	startprice    = IntegerField  (u'StartPrice'  , validators=[DataRequired()])
	endprice    = IntegerField  (u'EndPrice')
	
class HiddenOrderID(FlaskForm):
	order_id = HiddenField()

class BasicOrderForm(FlaskForm):
	order_number = IntegerField  (u'Order Number', validators=[DataRequired()])
	table_number = IntegerField  (u'Table Number')
	order_item_id = IntegerField  (u'Item ID Number', validators=[DataRequired()])
	item_amount = IntegerField (u'Amount', validators=[DataRequired()])

class ReservationForm(FlaskForm):
	reservation_name = StringField  (u'Reservation Name'  , validators=[DataRequired()])
	reservation_contact_number = StringField  (u'Mobile Number'  , validators=[DataRequired()])
	reservation_party_size = IntegerField  (u'Party Size'  , validators=[DataRequired()])
	reservation_date = DateField(u'Date', validators=[DataRequired()])
	reservation_time = TimeField(u'Time', validators=[DataRequired()])
	