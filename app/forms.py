# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from flask_wtf          import FlaskForm
from flask_wtf.file     import FileField, FileRequired
from wtforms            import StringField, TextAreaField, SubmitField, PasswordField, IntegerField
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