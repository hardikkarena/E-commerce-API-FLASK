
from dataclasses import fields
from importlib.metadata import files
from tkinter import W

from library.extra import Extra
from .crud import CRUD
from library.dbconection import *
from library.s3 import S3
from datetime import date
class Model_Order(S3,CRUD):
    product_table = "product"
    customer_table = "customer"
    cart_table = "cart"
    address_table = "address"
    order_table = "customer_order"
    order_detail_table = "order_detail"
    def is_product_exist(self,id):
        fields = " * "
        where = " WHERE id=%s"%id
        record = CRUD.select(self,
                             self.product_table,
                             fields,
                             where
        )
        if record != None:
            return True
        else:
            return False
    
    def insert_in_cart(self,id,product_id,quantity):
        fields = " * "
        where = " WHERE id=%s"%product_id
        product = CRUD.select(self,
                             self.product_table,
                             fields,
                             where
        )
        total_price = product["price"] * int(quantity)
        
        fields = """customer_id,product_id,quantity,total_price"""
        data=[id,product_id,quantity,total_price]
        record=CRUD.insert(self,
                    self.cart_table,
                    fields,
                    data
        )
        return dict(record)
    
    def is_product_exist_in_cart(self,product_id):
        fields = " * "
        where = " WHERE product_id=%s"%product_id
        product = CRUD.select(self,
                             self.cart_table,
                             fields,
                             where
        )
        if product != None:
            return True
        else:
            return False
        
    def update_in_cart(self,product_id,quantity):
        fields = " * "
        where = " WHERE product_id=%s"%product_id
        cart = CRUD.select(self,
                             self.cart_table,
                             fields,
                             where
        )
        fields = " * "
        where = " WHERE id=%s"%product_id
        product = CRUD.select(self,
                             self.product_table,
                             fields,
                             where
        )
        quantity = int(quantity) + cart["quantity"]
        total_price = product["price"] * int(quantity)
        fields = """ quantity=%s,total_price=%s """
        data=[quantity,total_price]
        where = " WHERE product_id=%s"%product_id
        cart = CRUD.update(self,
                           self.cart_table,
                           fields,
                           data,
                           where,
        )
        return dict(cart)

        
    def delete_product_from_cart(self,product_id):
        where = " WHERE product_id=%s"%product_id
        CRUD.delete(self,
                    self.cart_table,
                    where
        )
        
    def get_cart(self,customer_id):
        fields = "*"
        where = "WHERE customer_id=%s"%customer_id
        record = CRUD.select(self,
                           self.cart_table,
                           fields,
                           where,
                           many=True
                           )
        cart = Extra.get_list_of_dict(self,record)
        return cart
    
    def is_address_exist(self,address_id):
        fields = " * "
        where = " WHERE id=%s"%address_id
        record = CRUD.select(self,
                             self.address_table,
                             fields,
                             where
        )
        if record != None:
            return True
        else:
            return False
        
    def insert_order(self,customer_id,payment_mode,payment_satatus,address_id,product_id,quantity):
        fields = " * "
        where = " WHERE id=%s"%product_id
        product = CRUD.select(self,
                             self.product_table,
                             fields,
                             where
        )
        
        
        data_of_order = date.today()
        order_status = "pending"
        delivery_charges = product["delivery_charges"]
        total_price = product["price"] * int(quantity) 
        total_amount = total_price + delivery_charges
        fields =  """customer_id,total_amount,payment_mode,payment_satatus,data_of_order,address_id,order_status,delivery_charges"""
        data = [customer_id,total_amount,payment_mode,payment_satatus,data_of_order,address_id,order_status,delivery_charges]
        order = CRUD.insert(self,
                            self.order_table,
                            fields,
                            data
        )
        
        order_id  = order["id"]
        
        fields = """ order_id,product_id,quantity,total_price"""
        data = [order_id,product_id,quantity,total_price]
        order_detail = CRUD.insert(self,
                                   self.order_detail_table,
                                   fields,
                                   data,
        )
        order["order_detail"] = order_detail
        final_order = {}
        final_order ["order"] =order
        return final_order
        
    def is_order_exist(self,order_id):
        fields = " * "
        where = " WHERE id=%s"%order_id
        record = CRUD.select(self,
                             self.order_table,
                             fields,
                             where
        )
        if record != None:
            return True
        else:
            return False
    def update_order(self,order_id):
        order_status = "canceled"
        fields = "order_status=%s"
        data = [order_status]
        where = " WHERE id = %s"%order_id
        order = CRUD.update(self,
                            self.order_table,
                            fields,
                            data,
                            where
        )
        return dict(order)
    
    def get_orders(self,customer_id):
        fields = """ * """
        where = " WHERE customer_id=%s"%customer_id
        records = CRUD.select(self,
                              self.order_table,
                              fields,
                              where,
                              many=True
        )
        orders = []
        for i in records:
            order =dict(i)
            order_id = order["id"]
            fields = "*"
            where = " WHERE order_id=%s"%order_id
            records2 = CRUD.select(self,
                                        self.order_detail_table,
                                        fields,
                                        where,
                                        many=True
            )

            order_details = Extra.get_list_of_dict(self,records2)
            order["order_details"] = order_details
            orders.append(order)
        return orders
    
    def get_order(self,customer_id,id):
        fields = "*"
        where = "WHERE id=%s AND customer_id=%s"%(id,customer_id)
        order = CRUD.select(self,
                            self.order_table,
                            fields,
                            where
        )
        order = dict(order)
        order_id = order["id"]
         
        fields = "*"
        where = "WHERE order_id=%s"%order_id
        records = CRUD.select(
                              self,
                              self.order_detail_table,
                              fields,
                              where,
                              many=True
        )
        order_details = Extra.get_list_of_dict(self,records)
            
        order["order_details"] = order_details
        return order
    
    def is_cart_empty(self,id):
        fields = "*"
        where = "WHERE customer_id=%s"%id
        cart = CRUD.select(self,
                           self.cart_table,
                           fields,
                           where,
                           many=True
        )
        if cart!=[]:
            return True
        else:
            return False
        
    def insert_cart_order(self,customer_id,payment_mode,payment_satatus,address_id,):
        fields = "*"
        where = "WHERE customer_id=%s"%customer_id
        cart = CRUD.select(self,
                           self.cart_table,
                           fields,
                           where,
                           many=True
        )
        
        total_amount = 0
        delivery_charges = 0
        data_of_order = date.today()
        order_status = "pending"
        for i in cart:
            one_cart = dict(i)
            product_id = one_cart["product_id"]
            fields = " * "
            where = " WHERE id=%s"%product_id
            product = CRUD.select(self,
                                self.product_table,
                                fields,
                                where
            )
            total_amount = total_amount + product["price"]*one_cart["quantity"]
            delivery_charges = delivery_charges + product["delivery_charges"]

        fields = """ customer_id,total_amount,payment_mode,payment_satatus,data_of_order,address_id,order_status,delivery_charges """
        data = [customer_id,total_amount,payment_mode,payment_satatus,data_of_order,address_id,order_status,delivery_charges]
        order = CRUD.insert(self,
                            self.order_table,
                            fields,
                            data
        )
        order = dict(order)
        order_id = order["id"]
        product_details = []
        
        for i in cart:
            one_cart = dict(i)
            product_id = one_cart["product_id"]
            fields = " * "
            where = " WHERE id=%s"%product_id
            product = CRUD.select(self,
                                self.product_table,
                                fields,
                                where
            )
            quantity = one_cart["quantity"]
            total_price = product["price"] * quantity
            product_details.append((order_id,product_id,quantity,total_price))
            
        fields = """ order_id,product_id,quantity,total_price """
        data = product_details
        CRUD.insert(self,
                    self.order_detail_table,
                    fields,
                    data,
                    many=True
        )
        
        where = " WHERE customer_id=%s"%customer_id
        CRUD.delete(self,
                    self.cart_table,
                    where)
        
        fields = "*"
        where = "WHERE order_id=%s"%order_id
        records = CRUD.select(self,
                                    self.order_detail_table,
                                    fields,
                                    where,
                                    many=True
        )
        
        order_details = Extra.get_list_of_dict(self,records)
        order["order_details"] = order_details
        
        return order
        
        
        
                    
        
            
        
        
        
        
        
        
        
        

    