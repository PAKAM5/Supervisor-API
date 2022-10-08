# #import modules
# from flask_login import UserMixin, LoginManager
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import func
# from datetime import datetime
# from sqlalchemy import PrimaryKeyConstraint, ForeignKeyConstraint, Column, String, Integer
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# # from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# #import modules db
# from .__init__ import db, app
# #
# login_manager = LoginManager()
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


# #Define school table
# class School(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     school_name = db.Column(db.String(255), nullable=False)

# #define User table
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(255), unique=True)
#     password = db.Column(db.String(255))
#     phone = db.Column(db.String(255), nullable=False)
#     first_name = db.Column(db.String(255), nullable=False)
#     last_name = db.Column(db.String(255), nullable=False)
#     name = db.Column(db.String(255))
#     image_file = db.Column(db.String(255), nullable=False, default='default.jpg')
#     # document_file = db.Column(db.String(255), nullable=False)
#     reviews = db.relationship('Survey', backref='author', lazy=True)
#     school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
#     is_approved = db.Column(db.Boolean, default=False)
#     is_admin = db.Column(db.Boolean, default=False)
#     is_super = db.Column(db.Boolean, default=False)
#     is_manager = db.Column(db.Boolean, default=False)

#     # def get_reset_token(self, expires_sec=1800):
#     #     s = Serializer(app.config['SECRET_KEY'], expires_sec)
#     #     return s.dumps({'user_id': self.id}).decode('utf-8')

#     # @staticmethod
#     # def verify_reset_token(token):
#     #     s = Serializer(app.config['SECRET_KEY'])
#     #     try:
#     #         user_id = s.loads(token)['user_id']
#     #     except:
#     #         return None
#     #     return User.query.get(user_id)


#     def __repr__(self):
#         return f"User('{self.name}', '{self.email}', '{self.image_file}')"

   
# #Define Manager table
# class Manager(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    
   
# #Define Supervisor table with school and manager as foreign keys
# class Supervisor(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
#     manager_id = db.Column(db.Integer, db.ForeignKey('manager.id'), nullable=False)
    

# #Define Subsciption table
# class Subscription(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     product_id = db.Column(db.Integer, nullable=False)
#     quantity = db.Column(db.Integer, nullable=False)
#     school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    
   
# #define subscription by order table
# class SubscriptionByOrder(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     subscription_id = db.Column(db.Integer, db.ForeignKey('subscription.id'), nullable=False)
#     subscription_duration = db.Column(db.String(255), nullable=False)
    
    
    
    