from xml.sax.handler import DTDHandler
from flask import Flask, jsonify, request, json
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
# import socketserver
# import http.server
# import cgi


app = Flask(__name__)
# api = Api(app)
# 


@app.route('/', methods=['GET', "POST"])
def index():
    return "Hello World!"

#Loop Back interface


@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    # if request.method == 'POST':
    if request.headers['Content-Type'] == 'application/json':
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
        

       #Convert dictionary values to sql objects

       #print out examples
        print(firstname)
        print(lastname)


        #another way of retrieving the value of the key 'first_name'
        firstname2 = request_json_dict.get('_links').get('billing').get('first_name')
        lastname2 = request_json_dict['billing']['last_name']
        
        
       
        # firstname           = request_json.get(['Body']['first_name'])
        # lastname           = request_json.get(['Body']['last_name'])
        # email           = request_json.get(['Body']['email'])
        # phone           = request_json.get(['Body']['phone'])
        # address_1       = request_json.get(['Body']['address_1'])
        #print (result)
       # return result
        #print('JSON Message: ' + json.dumps(request.json))
        print('First Name: ' + firstname)    
    return "Webhook received!"


###convert json to sql object
#run app
if __name__ == '__main__':
    app.run(debug=True)

