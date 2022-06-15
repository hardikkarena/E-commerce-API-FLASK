from flask import Blueprint
from controller.order import Order

order_obj = Order()
order = Blueprint('order', __name__,)
order_obj = Order()

order.route('/add_to_cart',methods=['POST'])(order_obj.add_to_cart)
order.route('/remove_from_cart',methods=['POST'])(order_obj.remove_from_cart)