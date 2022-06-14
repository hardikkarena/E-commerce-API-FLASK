from flask import Blueprint
from controller.product import Product


productt = Blueprint('product', __name__,url_prefix='/product')
product_obj = Product()
productt.route('/add_product',methods=['POST'])(product_obj.add_product)
productt.route('/update_product/<int:id>',methods=['POST'])(product_obj.update_product)
productt.route('/delete_product/<int:id>',methods=['POST'])(product_obj.delete_product)
productt.route('/get_one_product/<int:id>',methods=['POST'])(product_obj.get_one_product)
productt.route('/get_all_product',methods=['POST'])(product_obj.get_all_product)    
productt.route('/get_file',methods=['POST'])(product_obj.get_file)