from flask import Blueprint
from controller.order import Order

order_obj = Order()
order = Blueprint('order', __name__,)
order_obj = Order()

order.route('/add_to_cart',methods=['POST'])(order_obj.add_to_cart)
order.route('/remove_from_cart',methods=['POST'])(order_obj.remove_from_cart)
order.route('/my_cart',methods=['POST'])(order_obj.my_cart)
order.route('/place_order',methods=['POST'])(order_obj.place_order)
order.route('/cancel_order',methods=['POST'])(order_obj.cancel_order)
order.route('/my_orders',methods=['POST'])(order_obj.my_orders)
order.route('/order/<int:id>',methods=['POST'])(order_obj.order)
order.route('/check_out_cart',methods=['POST'])(order_obj.check_out_cart)