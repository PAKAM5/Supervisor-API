# from xml.sax.handler import DTDHandler
import os
import json
from unicodedata import name
from flask import Flask, jsonify, request, json
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, create_engine, func, select
from sqlalchemy.orm import relationship
import sqlalchemy
#Import foreignkeyconstraint 
from sqlalchemy import ForeignKeyConstraint, PrimaryKeyConstraint
import random
import secrets
import string
from datetime import datetime, timedelta


app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql://ops:ops2022@127.0.0.1/ops'
db = SQLAlchemy(app)

#Import models

#Define school table
class School(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_name = db.Column(db.String(255))
    user = db.relationship('User', backref='school', lazy=True)

#Define Manager table with school as foreign key
class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    supervisor_id = db.Column(db.Integer, primary_key=True)
    
    
#define User table
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    name = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    image_file = db.Column(db.String(255), nullable=False, default='default.jpg')
    survey = db.relationship('Survey', backref='author', lazy=True)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'))
    manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'))
    is_approved = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_superuser = db.Column(db.Boolean, default=False)
    is_manager = db.Column(db.Boolean, default=False)

    # def get_reset_token(self, expires_sec=1800):
    #     s = Serializer(app.config['SECRET_KEY'], expires_sec)
    #     return s.dumps({'user_id': self.id}).decode('utf-8')

    # @staticmethod
    # def verify_reset_token(token):
    #     s = Serializer(app.config['SECRET_KEY'])
    #     try:
    #         user_id = s.loads(token)['user_id']
    #     except:
    #         return None
    #     return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.image_file}')"


#Define Subsciption table
class Subscription(db.Model):
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False, primary_key = True)
    expiry_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    

# def create_app():CD 
#secure cookies data, and set up link to mysql database
app.config['SECRET_KEY'] = 'lolo'
# app.config ['SQLALCHEMY_DATABASE_URI'] = 'mysql://ops:ops2022@127.0.0.1/ops'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


# engine = create_engine('mysql://ops:ops2022@127.0.0.1/ops')
# insp = inspect(engine)
# table_names = insp.get_table_names()
# # if True == False:## FIXME: need condition to see if 'subscription' is an element of table_names
# if 'subscription' not in table_names:
#     db.create_all(app=app)
#     in_school = School(school_name = "UniOlly")
#     db.session.add(in_school)
#     db.session.commit()
#     print('Database created')


# SUPERVISOR_SECRET and woocommerce secret 
WOOCOMMERCE_SECRET = 'rUOE`&W$~/gaHj]{x{^l`=^ 7yLcn`L153Up=hiS<0;<7&_zA@'
SUPERVISOR_SECRET = "lolo"


SUPERVISOR_ENDPOINT = 'https://ops.irdo1.safecoms.net/webhook'

#Define error
class DataInputError(Exception):
    """There was an issue with the data input"""
    pass


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
    first_namew = request_json_dict['billing']['first_name']
    last_namew = request_json_dict['billing']['last_name']
    emailw = request_json_dict['billing']['email']
    phonew = request_json_dict['billing']['phone']
    product_idw= request_json_dict['line_items'][0]['product_id']
    quantityw = request_json_dict['line_items'][0]['quantity']
    school_namew = request_json_dict['meta_data'][0]['value']
    skuw= request_json_dict['line_items'][0]['sku']
    

    #Convert dictionary values to sql objects

    #print out examples of values needed 
    print('First Name: ' + first_namew)
    print('Last Name: ' + last_namew)
    print ('Email: ' + emailw)
    print('Phone : ' + phonew)
    print('Product_ID: ' + str(product_idw))
    print('Quantity: ' + str(quantityw))
    print('School Name: ' + str(school_namew))
    
    #
    

    
    # def transaction():
    #Send data to respective tables
    #add school data
    try:
         school_namew
         first_namew
         last_namew
         emailw
         phonew
         product_idw
         quantityw

    except:
        raise DataInputError 
    else: 
        #Count number of records in query where school name is equal to school name in webhook
        rec = School.query.filter_by(school_name = school_namew).count()
        if rec >1 :
            raise DataInputError
            #if number of tuples is 1
        elif rec== 1:
            #subscription renewal 
            #add subscription data - expiry date
            if skuw == 'one-month':
                subscription_data = Subscription(expiry_date = datetime.utcnow() + datetime.timedelta(days=30))
                db.session.add(subscription_data)
                db.session.commit()
            elif skuw == 'one-year':
                subscription_data = Subscription(expiry_date = datetime.utcnow() + datetime.timedelta(days=365))
                db.session.add(subscription_data)
                db.session.commit()
            #when data is sent to the database, convert user to is_superuser and is_approved
            user = User()
            user.is_superuser = True
            user.is_approved = True
            db.session.commit()
            return "Webhook received!"
            #if number of tuples is 0
        elif rec == 0: 
            #define random password generator function
            def random_password_generator(size=8, chars=string.ascii_letters + string.digits):
                return ''.join(random.choice(chars) for _ in range(size))
            #generate random password
            random_password = random_password_generator()
            school_data = School( school_name = school_namew)
            db.session.add(school_data)
            db.session.commit()
           #INSERT INTO table subscription (school_id, expiry_date) VALUES ($schoolid, CURRENT_DATE + INTERVAL 1 MONTH);
            #add subscription data
            if skuw =='one-month':
                subscription_data = Subscription(expiry_date = datetime.utcnow() + datetime.timedelta(days=30))
                db.session.add(subscription_data)
                db.session.commit()
            elif skuw =='one-year':
                subscription_data = Subscription(expiry_date = datetime.utcnow() + datetime.timedelta(days=365))
                db.session.add(subscription_data)
                db.session.commit()
           
            #add user data
            user_data = User(first_name = first_namew, last_name = last_namew, email = emailw, phone = phonew, name = 'Administrator', password = random_password)
            db.session.add(user_data)
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



