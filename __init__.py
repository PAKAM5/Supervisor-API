# from xml.sax.handler import DTDHandler
import os
import json
import requests
from flask import Flask, jsonify, request, json
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, create_engine
from sqlalchemy.orm import relationship
import sqlalchemy


app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql://ops:ops2022@127.0.0.1/ops'
db = SQLAlchemy(app)


#import models
#Define school table
class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(255), nullable=False)

#define User table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(255))
    image_file = db.Column(db.String(255), nullable=False, default='default.jpg')
    # reviews = db.relationship('Survey', backref='author', lazy=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=False)
    is_manager = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.image_file}')"
    
#Define Subsciption table
class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    

#define subscription by order table
class SubscriptionByOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=False)
    subscription_duration = db.Column(db.Integer, nullable=False)



# def create_app():
#secure cookies data, and set up link to mysql database
app.config['SECRET_KEY'] = 'lolo'
# app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql://ops:ops2022@127.0.0.1/ops'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


engine = create_engine('mysql://ops:ops2022@127.0.0.1/ops')
insp = inspect(engine)
table_names = insp.get_table_names()
# if True == False:## FIXME: need condition to see if 'subscription' is an element of table_names
if 'subscription' not in table_names:
    db.create_all(app=app)
    in_school = School(school_name = "UniOlly")
    db.session.add(in_school)
    db.session.commit()
    print('Database created')


# SUPERVISOR_SECRET and woocommerce secret 
WOOCOMMERCE_SECRET = 'rUOE`&W$~/gaHj]{x{^l`=^ 7yLcn`L153Up=hiS<0;<7&_zA@'
SUPERVISOR_SECRET = "lolo"


SUPERVISOR_ENDPOINT = 'https://ops.irdo1.safecoms.net/webhook'


@app.route('/', methods=['GET', "POST"])
def index():
    return "Hello World!"


@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method != 'POST':
        return 405
    if request.headers['Content-Type'] != 'application/json':
        return 400
    #Get Json
    request_json     = request.get_json()

    #turn the json into a string
    request_json_str = json.dumps(request_json)
    #turn the string into a dictionary
    request_json_dict = json.loads(request_json_str)
    # print the dictionary
    print(request_json_dict)

    #retrieve the value of the keys
    first_name = request_json_dict['billing']['first_name']
    last_name = request_json_dict['billing']['last_name']
    email = request_json_dict['billing']['email']
    phone = request_json_dict['billing']['phone']
    product_id = request_json_dict['line_items'][0]['product_id']
    quantity = request_json_dict['line_items'][0]['quantity']
    school_name = request_json_dict['meta_data'][0]['value']
    

    #Convert dictionary values to sql objects

    #print out examples of values needed 
    print('First Name: ' + first_name)
    print('Last Name: ' + last_name)
    print ('Email: ' + email)
    print('Phone : ' + phone)
    print('Product_ID: ' + str(product_id))
    print('Quantity: ' + str(quantity))
    print('School Name: ' + str(school_name))
    

    #Send data to respective tables
    #add school data     
    school_data = School( school_name = school_name)
    db.session.add(school_data)
    db.session.commit()
    #add user data
    user_data = User(first_name = first_name, last_name = last_name, email = email, phone = phone, name = 'Administrator')
    db.session.add(user_data)
    db.session.commit()
    #add subscription data
    subscription_data = Subscription(product_id = product_id, quantity = quantity)
    db.session.add(subscription_data)
    db.session.commit()
    #when data is sent to the database, convert user to is_superuser and is_approved
    user = User()
    user.is_superuser = True
    user.is_approved = True
    db.session.commit()
    return "Webhook received!"

    
# #  #Create product subscription function for subscription by order table
#     def subscription_duration():
#         #monthly subscription
#         if product_id == "a":
#             sub = SubscriptionByOrder()
#             sub.subscription_duration = func.now() + func.interval(1, 'month')
#             # new_subscription
#         #yearly subscription
#         elif product_id == "b":
#             sub = SubscriptionByOrder()
#             sub.subscription_duration = func.now() + func.interval(1, 'year')
#         db.session.add(new_subscription)
#         db.session.commit()



    # return app
#run app
if __name__ == '__main__':
    app.run(debug=True)



