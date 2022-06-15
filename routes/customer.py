from flask import Blueprint
from controller.customer import *

customer = Blueprint('customer', __name__,url_prefix='/customer')
customer_obj = Customer()
customer.route('/sign_up',methods=['POST'])(customer_obj.singup)
customer.route('/sent_otp/<int:id>',methods=['POST'])(customer_obj.sent_otp)
customer.route('/verify_otp/<int:id>',methods=['POST'])(customer_obj.verify_otp)
customer.route("/login",methods=['POST'])(customer_obj.login)
customer.route('/get_profile/<int:id>',methods=['POST'])(customer_obj.get_profile)
customer.route('/set_profile',methods=['POST'])(customer_obj.set_profile)
customer.route('/all_profile',methods=['POST'])(customer_obj.all_profile)
customer.route('/forgot_password',methods=['POST'])(customer_obj.forgot_password)
customer.route('/change_password',methods=['POST'])(customer_obj.change_password)
customer.route('/add_address',methods=['POST'])(customer_obj.add_address)










