
from dataclasses import field

from certifi import where
from numpy import product
from sqlalchemy import true
from .crud import CRUD
from library.dbconection import *
from library.s3 import S3

class Model_Order(S3,CRUD):
    product_table = "product"
    customer_table = "customer"
    cart_table = "cart"
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

    