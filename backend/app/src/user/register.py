from eve import Eve
from flask import request, abort, make_response, jsonify
import sys, os
from .utility import *
from werkzeug.security import generate_password_hash

def register(app):
    try:
        return process_request()
    except KeyError as e:
        abort(make_response(jsonify(missingKey=str(e)), 500))
    except:
        import sys
        error = sys.exc_info()[0]
        print("Unexpected error in register: %s!" % error)
        raise

def process_request():
    json = request.get_json(force=True)
        username = getKey("username", json)
        password = getKey("password", json)
        displayName = getKey("displayName", json)
        users = app.data.driver.db['users']
        token = get_unique_token(app)
        validate_unique("username", username)
        validate_unique("displayName", displayName)
        result = users.insert([{
                    "username": username
                    , "password": generate_password_hash(password)
                    , "displayName": displayName
                    , "token": token
                }])
        if result:
            return jsonify(authToken=token)

def validate_unique(key, value):
    if(users.find_one({key: value})):
            abort(make_response(jsonify(takenKey=key), 500))
