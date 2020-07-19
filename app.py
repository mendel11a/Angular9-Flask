# from flask import Flask, jsonify, request, json
# from bson.objectid import ObjectId
# from datetime import datetime
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import datetime
import os
from functools import wraps
from flask_bcrypt import Bcrypt
from flask import Flask, request, render_template, flash, redirect, url_for, session,jsonify
from passlib.hash import sha256_crypt
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)
from pymongo import MongoClient
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)  # Configure the connection to the database
db = client.FirstApp  # Select the database
users = db.Users  # Select the collection
arts = db.Articles  # Select the collection

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'secret'
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)


# User register
@app.route('/users/register', methods=['POST'])
def register():
    name = request.get_json()['name']
    user_name = request.get_json()['user_name']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')    
    created = datetime.datetime.utcnow()
    user_id=users.insert({"name": name, "email": email, "user_name": user_name, "password": password,'created' : created })
    new_user = users.find_one({'_id' : user_id})
    result = {'email' : new_user['email'] + ' registered'}
    return jsonify({'result' : result})


@app.route('/users/login', methods=['POST'])
def login():
    email = request.get_json()['email']
    password_candidate = request.get_json()['password']
    result = ""
    response = users.find_one({'email' : email})
    if response:	
        if bcrypt.check_password_hash(response['password'], password_candidate):
            access_token = create_access_token(identity = {
			    'name': response['name'],
				'user_name': response['user_name'],
				'email': response['email']}
				)
            result = jsonify({"token":access_token})
        else:
            result = jsonify({"error":"Invalid PASSWORD"})            
    else:
        result = jsonify({"result":"Username not found"})
    return result
	
	
if __name__ == '__main__':
    app.run(debug=True)