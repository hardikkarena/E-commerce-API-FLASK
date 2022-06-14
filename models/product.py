from dataclasses import field, fields

from certifi import where
from .models_utils import CRUD
from library.s3 import S3


crud = CRUD()
s3 = S3()

class Product_Model():
    table = " product as p "
    def create_product(self,name,description,price,gst,category,product_images,company_id):
        
        # record=crud.insert("product",
        #                   ("name","description","price","gst","category","company_id"),
        #                   (name,description,price,gst,category,company_id)
        # )
        
        fields = """ "name","description","price","gst","category","company_id" """
        data = [name,description,price,gst,category,company_id]
        record = crud.insert(self.table,
                             fields,
                             data
        )
        product_id=record['id']
        image_insert = []
        for i in product_images:
            image_insert.append((i,product_id))
        # sql = "INSERT INTO product_images(image_name,product_id)values(%s,%s)"
        # data=crud.insert_multiple_images(sql,image_insert)
        fields = """ "image_name","product_id" """
        data = image_insert
        crud.insert("product_images",
                    fields,
                    data,
                    many=True)
        fields = """ p.*,c.company_name """
        join = " LEFT join company c on p.company_id = c.id "
        where = " WHERE p.id='%s' "%product_id
        record = crud.select(self.table,
                           fields,
                           where,
                           join
        )
         # crud.insert("product_images",["image_name","product_id"],[image_insert],many=True)
        # sql = "select p.*,c.company_name from product p LEFT join company c on p.company_id = c.id WHERE p.id='%s'"
        # data=crud.get_all_record(sql,(product_id))
        # sql = "select image_name from  product_images where product_id=%s"
        # imgs=crud.get_all_record(sql,(product_id))
        fields = """ image_name """
        where = "WHERE product_id='%s'"%product_id
        imgs = crud.select("product_images ",
                           fields,
                           where,
                           many=True
        )
        # result = []
        # for i in data:
        #     result.append(dict(i))
        record = dict(record)
        product_images = []
        for i in imgs:
            product_images.append(dict(i))
        record["product images"] = product_images
        return dict(record)

    def product_exist(self,id):
        # record = crud.select("product",["*"],[id],"id")
        fields = "*"
        where = " WHERE id=%s"%id
        record = crud.select(self.table,
                             fields,
                             where,
        )
        if record!=None:
            return True
        else:
            return False
        
    def update_product_in_db(self,id,name,description,price,gst,category,company_id):
        # record = crud.update("product",
        #            ["name","description","price","gst","category","company_id"],
        #            [name,description,price,gst,category,company_id,id],
        #            "id"
        # )
        fields = """ name=%s,description=%s,price=%s,gst=%s,category=%s,company_id=%s  """
        data = [name,description,price,gst,category,company_id]
        where = "WHERE id = %s"%id
        record = crud.update(self.table,
                             fields,
                             data,
                             where
        )

        return dict(record)

    def delete_product_from_db(self,id):
        where = "WHERE id = '%s'"%id
        crud.delete(self.table,
                    where
        )

    def get_one_product_from_db(self,id):
        # sql = "select p.*,c.company_name from product p LEFT join company c on p.company_id = c.id WHERE p.id='%s'"
        # data=dict(crud.get_one_record(sql,(id)))
        fields = """ p.*,c.company_name """
        join = " LEFT join company c on p.company_id = c.id "
        where =" WHERE p.id='%s' "%id
        data = crud.select(self.table,
                           fields,
                           where,
                           join
        )
        product_id = data["id"]
        # sql = "select image_name from  product_images where product_id=%s"
        # imgs=crud.get_all_record(sql,(product_id))
        fields = """image_name """
        where = "WHERE product_id='%s'"%product_id
        imgs = crud.select("product_images ",
                           fields,
                           where,
                           many=True
        )
        
        product_images = []
        data = dict(data)
        
        for i in imgs:
            d1 = dict(i)
            url = s3.get_image("product/",i["image_name"])
            d1["image_name"] = url
            product_images.append(d1)
        data["product images"] = product_images
        return data
    
    def paged_sorted_filerd(self,page="",sort="",order="",filter_field="",value=""):
        fields = " p.*,c.company_name " 
        join = " left join company c on p.company_id = c.id "
        data = crud.select(self.table,
                           fields,
                           join=join,
                           page=page,sort=sort,order=order,filter_field=filter_field,value=value,
                           many=True
        )
        # sql="select p.*,c.company_name from product p left join company c on p.company_id = c.id"
        # if filter_field!="" and value!="":
        #     sql = sql+" where %s='%s'"%(filter_field,value)
        # if sort!="" and order!="":
        #     sql = sql+" ORDER BY %s %s"%(sort,order)
        # if page!="":
        #     limit=3
        #     offset=(limit * int(page)) - limit
        #     sql = sql+" limit %s offset %s"%(limit,offset)
        # data=crud.get_all_record(sql,())
        products = []
        for i in data:
            product = dict(i)
            product_id = product["id"]
            # sql = "select image_name from  product_images where product_id=%s"
            # imgs=crud.get_all_record(sql,(product_id))
            table = " product_images "
            fields = " image_name "
            where = " where product_id=%s"%product_id
            imgs = crud.select(table,
                              fields,
                              where,
                              many=True
            )
            product_images = []
            print(product_id)
            for i in imgs:
                d1 = dict(i)
                url = s3.get_image("product/",i["image_name"])
                d1["image_name"] = url
                product_images.append(d1)
            product["product images"] = product_images            
            products.append(product)
        return products

