# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf          import FlaskForm
from flask_wtf.file     import FileField, FileRequired
from wtforms            import StringField, TextAreaField, SubmitField, PasswordField, IntegerField, FieldList, FormField, HiddenField
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
	endprice    = IntegerField  (u'EndPrice'  , validators=[DataRequired()])
	
#class MenuItemForm(FlaskForm):
#	name = HiddenField()
#	amount    = IntegerField  (u'StartPrice'  , validators=[DataRequired()])
	
#class OrderForm(FlaskForm):
#	"""A form for one or more menu items"""
#	items = FieldList(FormField(MenuItemForm), min_entries=1)
#	order_number = IntegerField  (u'Order Number'  , validators=[DataRequired()])

class BasicOrderForm(FlaskForm):
	order_number = IntegerField  (u'Order Number', validators=[DataRequired()])
	table_number = IntegerField  (u'Table Number')
	order_item_id = IntegerField  (u'Item ID Number', validators=[DataRequired()])
	item_amount = IntegerField (u'Amount', validators=[DataRequired()])
