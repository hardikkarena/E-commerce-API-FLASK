from ast import Return
from library.validate import Validator
from library.s3 import S3
from library.authentication import Authentication
from models.order import Model_Order
from models.customer import Model_Customer
from werkzeug.utils import secure_filename
from flask import request,jsonify

class Order(Validator,Authentication,Model_Order,Model_Customer,S3):
    def add_to_cart(self):
        id = request.headers['id']
        product_id = request.json['product_id']
        quantity = request.json['quantity']
        if Validator.validate_input(self,[product_id,quantity]):
            if Model_Order.is_product_exist(self,product_id):
                if Model_Order.is_product_exist_in_cart(self,product_id):
                    cart=Model_Order.update_in_cart(self,
                                                    product_id,
                                                    quantity
                    )
                    return jsonify(cart)
                else:    
                    cart = Model_Order.insert_in_cart(self,
                                                      id,
                                                      product_id,
                                                      quantity
                    )
                    return jsonify(cart)
            else:
                return jsonify("invalid Product id")
        else:
            return jsonify("invalid input")
        
    def remove_from_cart(self):
        product_id = request.json['product_id']
        if Validator.validate_input(self,[product_id]):
            if Model_Order.is_product_exist(self,product_id):
                if Model_Order.is_product_exist_in_cart(self,product_id):
                    Model_Order.delete_product_from_cart(self,product_id)
                    return jsonify("product removed from cart")
                else:
                    return jsonify("Product is not in cart")
            else:
                return jsonify("invalid Product id")
        else:
            return jsonify("invalid input")
        
