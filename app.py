# from xml.sax.handler import DTDHandler
import os
import json
import hmac
import hashlib
import requests
from flask import Flask, jsonify, request, json
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# api = Api(app)

# SUPERVISOR_SECRET= SUPERVISOR APP SECRET
# WOOCOMMERCE_SECRET= WOOCOMMERCE webhook secret>
WOOCOMMERCE_SECRET = 'rUOE`&W$~/gaHj]{x{^l`=^ 7yLcn`L153Up=hiS<0;<7&_zA@'
SUPERVISOR_SECRET = "lolo"


SUPERVISOR_ENDPOINT = 'https://ops.irdo1.safecoms.net/webhook'


@app.route('/', methods=['GET', "POST"])
def index():
    return "Hello World!"

#Loop Back interface----


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
    firstname = request_json_dict['billing']['first_name']
    lastname = request_json_dict['billing']['last_name']
    email = request_json_dict['billing']['email']
    phone = request_json_dict['billing']['phone']
    product_id = request_json_dict['line_items'][0]['product_id']
    quantity = request_json_dict['line_items'][0]['quantity']
    school_name = request_json_dict['meta_data'][0]['value']
    
    #tData to send to Application
        
    send_data = (firstname, lastname, email, phone, product_id, quantity, school_name)

    #Convert dictionary values to sql objects

    #print out examples
    print('First Name: ' + firstname)
    print('Last Name: ' + lastname)
    print ('Email: ' + email)
    print('Phone : ' + phone)
    print('Product_ID: ' + str(product_id))
    print('Quantity: ' + str(quantity))
    print('School Name: ' + str(school_name))

    print('First Name: ' + firstname)    

    #if sending via json
    header = {'content-type': 'application/json'}

    #Send to supervisor app
    Supervisor_response = requests.post(SUPERVISOR_ENDPOINT, 
        send_data)

        
    
    return "Webhook received!"

###convert json to sql object
#run app
if __name__ == '__main__':
    app.run(debug=True)

