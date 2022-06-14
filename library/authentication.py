import jwt
from models.customer import Model_Customer
from flask import request,jsonify
from functools import wraps
from .validate import Validator

validator = Validator()
SECRET_KEY = 'abc'
model_customer = Model_Customer()

class Authentication:
    def generate_token(self,id):
        token = jwt.encode({
            'id': id,
        },SECRET_KEY)
        model_customer.save_token(token,id)
        return token

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = id = ""
        token = request.headers['access_token']
        id = request.headers['id']
        if validator.validate_input([token,id]):
            if model_customer.is_user_exist_by_id(id):
                if model_customer.check_token(token,id):
                    return f(*args, **kwargs)
                else:
                    return jsonify("invalid Token")
            else:
                return jsonify("Invlid Id")
        else:
            return jsonify("Enter Valid token and id")
    return decorated