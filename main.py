from flask import Flask, jsonify, request, json
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import socketserver
import http.server
import cgi


app = Flask(__name__)
api = Api(app)
# 


@app.route('/', methods=['GET', "POST"])
def index():
    return "Hello World!"


# @app.route('/webhook', methods=['POST', 'GET'])
# def webhook():
#     # if request.method == 'POST':
#     if request.headers['Content-Type'] == 'application/json':
#         request_json     = request.get_json()
#         #turn the json into a string
#         request_json_str = json.dumps(request_json)
#         #turn the string into a dictionary
#         request_json_dict = json.loads(request_json_str)
#        # print the dictionary
#         print(request_json_dict)
#         #retrieve the value of the key 'name'
#         firstname = request_json_dict['first_name']
#         print (firstname)
#         # firstname           = request_json.get(['Body']['first_name'])
#         # lastname           = request_json.get(['Body']['last_name'])
#         # email           = request_json.get(['Body']['email'])
#         # phone           = request_json.get(['Body']['phone'])
#         # address_1       = request_json.get(['Body']['address_1'])
#         #print (result)
#        # return result
#         #print('JSON Message: ' + json.dumps(request.json))
#         print('First Name: ' + firstname)    
#     return "Webhook received!"


###convert json to sql object
#run app
if __name__ == '__main__':
    app.run(debug=True)

