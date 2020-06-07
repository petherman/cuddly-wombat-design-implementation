# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

# Python modules
import os, logging
from datetime import datetime
# Flask modules
from flask               import render_template, request, url_for, redirect, send_from_directory
from flask_login         import login_user, logout_user, current_user, login_required
from werkzeug.exceptions import HTTPException, NotFound, abort

# App modules
from app        import app, lm, db, bc
from app.models import User, MenuItem, Order, OrderedItem, Reservation
from app.forms  import LoginForm, RegisterForm, AddMenuItemForm, BasicOrderForm, HiddenOrderID, ReservationForm
from app.report import *

# Sqlalchemy
from sqlalchemy import desc, exc

# provide login manager with load_user callback
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Logout user
@app.route('/logout.html')
def logout():
    logout_user()
    return redirect(url_for('index'))

# Register a new user
@app.route('/register.html', methods=['GET', 'POST'])
def register():
    
    # declare the Registration Form
    form = RegisterForm(request.form)

    msg = None

    if request.method == 'GET': 

        return render_template('layouts/auth-default.html',
                                content=render_template( 'pages/register.html', form=form, msg=msg ) )

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 
        email    = request.form.get('email'   , '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        # filter User out of database through username
        user_by_email = User.query.filter_by(email=email).first()

        if user or user_by_email:
            msg = 'Error: User exists!'
        
        else:         

            pw_hash = password #bc.generate_password_hash(password)

            user = User(username, email, pw_hash)

            user.save()

            msg = 'User created, please <a href="' + url_for('login') + '">login</a>'     

    else:
        msg = 'Input error'     

    return render_template('layouts/auth-default.html',
                            content=render_template( 'pages/register.html', form=form, msg=msg ) )

# Authenticate user
@app.route('/login.html', methods=['GET', 'POST'])
def login():
    
    # Declare the login form
    form = LoginForm(request.form)

    # Flask message injected into the page, in case of any errors
    msg = None

    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():

        # assign form data to variables
        username = request.form.get('username', '', type=str)
        password = request.form.get('password', '', type=str) 

        # filter User out of database through username
        user = User.query.filter_by(user=username).first()

        if user:
            
            #if bc.check_password_hash(user.password, password):
            if user.password == password:
                login_user(user)
                return redirect(url_for('index'))
            else:
                msg = "Wrong password. Please try again."
        else:
            msg = "Unkkown user"

    return render_template('layouts/auth-default.html',
                            content=render_template( 'pages/login.html', form=form, msg=msg ) )


# View Menu
@app.route('/menu.html')
def show_menu():
    
    menu = MenuItem.query.all()
    return render_template('layouts/default.html',
                            content=render_template( 'pages/menu.html', menu=menu) )

# View Current Orders
@app.route('/current_orders.html', methods=['GET', 'POST'])
def current_orders():
    
    orders = Order.query.filter_by(order_status=1)
    
    msg = None
    
    current_datetime = datetime.now()

    form = HiddenOrderID(request.form)

    
    
    if request.method == 'GET':
        return render_template('layouts/default.html',
                                content=render_template( 'pages/current_orders.html', orders=orders, msg=msg, form=form, current_datetime=current_datetime) )
    if form.validate_on_submit():
        order_id = request.form.get('order_id', '', type=int)
        closed_order = Order.query.filter_by(id=order_id).first()
        closed_order.close_order()
        msg = 'Order #' + str(order_id) + ' closed'
    else:
        msg = 'Input error' 
           
    return render_template('layouts/default.html',
                            content=render_template( 'pages/current_orders.html', orders=orders, msg=msg, form=form, current_datetime=current_datetime) )

# View Previous Orders
@app.route('/previous_orders.html', methods=['GET', 'POST'])
def previous_orders():
    
    orders = Order.query.filter_by(order_status=0)
    
    msg = None
    
    form = HiddenOrderID(request.form)
    
    if request.method == 'GET':
        return render_template('layouts/default.html',
                                content=render_template( 'pages/previous_orders.html', orders=orders, msg=msg, form=form) )
    if form.validate_on_submit():
        order_id = request.form.get('order_id', '', type=int)
        reopened_order = Order.query.filter_by(id=order_id).first()
        reopened_order.reopen_order()
        msg = 'Order #' + str(order_id) + ' reopened'
    else:
        msg = 'Input error' 
           
    return render_template('layouts/default.html',
                            content=render_template( 'pages/previous_orders.html', orders=orders, msg=msg, form=form) )



# Add items to menu
@app.route('/add_menu_item.html', methods=['GET', 'POST'])
def add_menu_item():
    # declare the menu item Form
    form = AddMenuItemForm(request.form)

    msg = None

    if request.method == 'GET':
        return render_template('layouts/default.html',
                                content=render_template( 'pages/add_menu_item.html', form=form, msg=msg) )
    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():
        # assign form data to variables
        name = request.form.get('name', '', type=str)
        description = request.form.get('description', '', type=str)
        price_string = request.form.get('startprice', '', type=str) + '.' + request.form.get('endprice', '', type=str)[:2]
        # filter User out of database through username
                
        checkItemName = MenuItem.query.filter_by(name=name).first()

        if checkItemName:
            msg = 'Error: Item ' + name + ' exists!'
        else:
            newItem = MenuItem(name=name,description=description,price=price_string,category='placeholder')
            newItem.save()
            msg = 'Item added: '+ name + ' with price of $' + price_string
    else:
        msg = 'Input error'

    return render_template('layouts/default.html',
                            content=render_template( 'pages/add_menu_item.html', form=form, msg=msg) )
                            
# Create orders
@app.route('/create_order.html', methods=['GET', 'POST'])
def create_order():
    
    # import menu items
    menu_items = MenuItem.query.all()
    # declare the menu item Form
    form = BasicOrderForm(request.form)

    msg = None

    if request.method == 'GET':
        return render_template('layouts/default.html',
                                content=render_template( 'pages/create_order.html', form=form, msg=msg, menu=menu_items) )
    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():
        # assign form data to variables
        order_number = request.form.get('order_number', '', type=int)
        table_number = request.form.get('table_number', '', type=int)
        order_item_id = request.form.get('order_item_id', '', type=int)
        item_amount = request.form.get('item_amount', '', type=int)
        # filter User out of database through username
        item = MenuItem.query.filter_by(id=order_item_id).first()
        
        # checks whether the menu item exists
        if item:
            # checks whether there is an existing order
            checkOrderNumberExists = Order.query.filter_by(id=order_number).first()
            if checkOrderNumberExists:
                # stores the test object into variable
                currentOrder = checkOrderNumberExists
                if currentOrder.order_status:
                    # Adds item to order
                    for x in range(item_amount):
                        newItem = OrderedItem(item.id, item.name, item.description, item.category, item.price)
                        newItem.save()
                        currentOrder.order_items.append(newItem)
                    currentOrder.calc_total()
                    currentOrder.update()
                    
                    # True for order_status signals order is still open
                    msg = 'Added '+ str(item_amount) + 'x ' + item.name + ' to order #' + str(order_number)                    
                                
                else:
                    # If false the order is completed and cannot be updated
                    msg = 'Order #' + str(order_number)+ ' has already been completed and the item cannot be added to the order.'
            else:
                newOrder = Order(table_number)
                newOrder.order_status = True
                for x in range(item_amount):
                    # Adds item to order
                    newItem = OrderedItem(item.id, item.name, item.description, item.category, item.price)
                    newItem.save()
                    newOrder.order_items.append(newItem)
                newOrder.calc_total()    
                newOrder.save()

                tempOrder = Order.query.order_by(desc(Order.id)).first()
                app.logger.info('%s newId', tempOrder.id)


                msg = 'Order #' + str(order_number) + " doesn't exist but order #" + str(tempOrder.id) + ' created'
        else:
            msg = "item with id #" + str(order_item_id) + " doesn't exist"
            
    else:
        msg = 'Input error'

    return render_template('layouts/default.html',
                            content=render_template( 'pages/create_order.html', form=form, msg=msg, menu=menu_items) )
        

# Create reservations
@app.route('/create_reservation.html', methods=['GET', 'POST'])
def create_reservation():
    
    # declare the menu item Form
    form = ReservationForm(request.form)

    msg = None

    if request.method == 'GET':
        return render_template('layouts/default.html',
                                content=render_template( 'pages/create_reservation.html', form=form, msg=msg) )
                                
    # check if both http method is POST and form is valid on submit
    if form.validate_on_submit():
        
        reservation_name = request.form.get('reservation_name', '', type=str)
        reservation_contact_number = request.form.get('reservation_contact_number', '', type=str)
        reservation_party_size = request.form.get('reservation_party_size', '', type=int)
        reservation_date = request.form.get('reservation_date', '')
        reservation_time = request.form.get('reservation_time', '')

        mytime = datetime.strptime(reservation_time,'%H:%M').time()
        mydate = datetime.strptime(reservation_date,'%Y-%m-%d').date()
        mydatetime = datetime.combine(mydate, mytime)
        
        print(mydatetime)
        
    
        reservation = Reservation(reservation_name, reservation_contact_number, reservation_party_size, mydatetime)
        try:
            reservation.save()
            msg = 'Reservation created'
        except exc.SQLAlchemyError:
            msg = 'Reservation has already been created'
    else:
        msg = 'Input error'
        app.logger.debug(form.errors)


    return render_template('layouts/default.html',
                            content=render_template( 'pages/create_reservation.html', form=form, msg=msg) )
                            

# View Menu
@app.route('/reservations.html')
def view_reservations():
    
    reservations = Reservation.query.all()
    return render_template('layouts/default.html',
                            content=render_template( 'pages/reservations.html', reservations=reservations) )                

# Reporting
@app.route('/reporting.html')
def view_reports():
    
    orders = Order.query.all()
    reservations = Reservation.query.all()
    
    report = Report(orders, reservations)
    
    return render_template('layouts/default.html',
                            content=render_template( 'pages/reporting.html', report=report) )    

# App main route + generic routing
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path>')
def index(path):

    if not current_user.is_authenticated:
        return redirect(url_for('login'))

    content = None

    try:

        # try to match the pages defined in -> pages/<input file>
        return render_template('layouts/default.html',
                                content=render_template( 'pages/'+path) )
    except:
        
        return render_template('layouts/auth-default.html',
                                content=render_template( 'pages/404.html' ) )

# Return sitemap 
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'sitemap.xml')
