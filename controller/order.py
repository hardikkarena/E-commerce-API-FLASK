from ast import Return
from library.validate import Validator
from library.s3 import S3
from library.authentication import Authentication
from library.extra import Extra
from models.crud import CRUD
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
        
    def my_cart(self):
        customer_id = request.headers['id']
        cart = Model_Order.get_cart(self,customer_id)
        if cart!=[]:
            return jsonify(cart)
        else:
            return jsonify("no items in cart")
        
    def place_order(self):  
        customer_id = request.headers['id']
        payment_mode = request.json["payment_mode"]
        payment_satatus = request.json["payment_satatus"]
        address_id = request.json["address_id"]
        product_id = request.json['product_id']
        quantity = request.json['quantity']
        if Validator.validate_input(self,[payment_mode,payment_satatus,address_id,product_id,quantity]):
            if Model_Order.is_product_exist(self,product_id):
                if Model_Order.is_address_exist(self,address_id):
                    order = Model_Order.insert_order(self,
                                                     customer_id,
                                                     payment_mode,
                                                     payment_satatus,
                                                     address_id,
                                                     product_id,
                                                     quantity
                    )
                    return jsonify(order)
                else:
                    return jsonify("invlid Address Id")
            else:
                return jsonify("invalid Product id")
        else:
            return jsonify("invalid input")
    
    def cancel_order(self):
        order_id = request.json["order_id"]
        if Validator.validate_input(self,[order_id]):
            if Model_Order.is_order_exist(self,order_id):
                order=Model_Order.update_order(self,order_id)
                return jsonify(order)
            else:
                return jsonify("invlid order id")
        else:
            return jsonify("invalid input")
        
    def my_orders(self):
        customer_id = request.headers['id']
        orders = Model_Order.get_orders(self,customer_id)
        if orders!=[]:
            return jsonify(orders)
        else:
            return jsonify("no orders")
        
    def order(self,id):
        customer_id = request.headers['id']
        order = Model_Order.get_order(self,customer_id,id)
        return jsonify(order)
    
    def check_out_cart(self):
        customer_id = request.headers['id']
        if Model_Order.is_cart_empty(self,customer_id):
            
            payment_mode = request.json["payment_mode"]
            payment_satatus = request.json["payment_satatus"]
            address_id = request.json["address_id"]
            if Validator.validate_input(self,[payment_mode,payment_satatus,address_id]):
                if Model_Order.is_address_exist(self,address_id):
                    order = Model_Order.insert_cart_order(self,
                                                        customer_id,
                                                        payment_mode,
                                                        payment_satatus,
                                                        address_id,
                    )
                    return jsonify(order)
                else:
                    return jsonify("invlid Address Id")
                
            else:
                return jsonify("invalid input")
        else:
            return jsonify("cart is empty")
 
        
        
        
        
        
        
        
