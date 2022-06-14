
from numpy import record
from sqlalchemy import table
from .models_utils import *
from library.dbconection import *
from library.s3 import S3

crud = CRUD()
s3 = S3()

class Model_Customer(S3):
    table = " customer "
    
    def insert_customer(self,email,password,first_name,last_name,profil_pic):
        fields = """ "email","password","first_name","last_name","profile_image" """
        data=[email,password,first_name,last_name,profil_pic]
        print(type(self.table))
        record=dict(crud.insert(self.table,
                    fields,
                    data   
        ))
        record.pop("otp")
        record.pop("password")
        return dict(record)
    
    def customer_exist(self,email):
        # record=crud.select("customer",
        #             ["*"],
        #             [email],
        #             "email",
        # )
        fields = " * "
        where = "where email = '%s'"%email
        record = crud.select(self.table,
                             fields,
                             where
        )
        if record!=None:
            return True
        else:
            return False

    def save_token(self,token,id):
        fields = """ access_token = %s """
        data  = [token] 
        where =  " where id = %s"%id
        
        crud.update(self.table,
                    fields,
                    data,
                    where    
        )
    
    def is_user_exist_by_id(self,id):
        # record = crud.select("customer",
        #                     ["*"],
        #                     [id],
        #                     "id"
        # )
        fields = "* "
        where = " where id=%s"%id
        record = crud.select(self.table,
                             fields,where
        )
        print(record)
        if record!=None:
            return True
        else:
            return False

    def update_otp(self,otp,id):
        fields = ' otp = %s'
        data = [otp]
        where = " where id = %s"%id
        crud.update(self.table,
                    fields,
                    data,
                    where
        )
        # crud.update("customer",
        #             ['otp'],
        #             [otp,id],
        #             "id"
        # )

    def is_otp_sent(self,id):
        # record = crud.select("customer","*",[id],"id")
        fields = "* "
        where = "where id =%s"%id
        record = crud.select(self.table,
                             fields,where
        )
        # print(type(record))
        if record["otp"] != None:
            return True
        else:
            return False

    def verify_otp_in_databse(self,otp,id):
        # record = crud.select("customer",["otp"],[id],"id")
        fields = "* "
        where = "where id =%s"%id
        record = crud.select(self.table,
                             fields,where
        )
        if int(otp) == record["otp"]:
            return True
        else:
            return False

    def update_status(self,id):
        fields = "verified =%s "
        data = [True]
        where = "where id =%s"%id 
        crud.update(self.table,
             fields,
             data,
             where
        )
        # crud.update("customer",
        #             ["verified"],
        #             [True,id],
        #             "id"
        # )

    def is_customer_verified(self,email):
        # record = crud.select("customer",
        #                     ["verified"],
        #                     [email],
        #                     "email"
        # )
        fields = "* "
        where = "where email ='%s'"%email
        record = crud.select(self.table,
                             fields,where
        )
        if record["verified"] == True:
            return True
        else:
            return False
        
    def get_one_customer_by_email(self,email):
        # record = crud.select("customer",
        #                     ["id","email","first_name","last_name","profile_image","verified,password"],
        #                     [email],
        #                     "email"
        # )
        fields = "* "
        where = "where email ='%s'"%email
        record = dict(crud.select(self.table,
                             fields,where
        ))
        
        
        return record
    
    def get_one_customer_no_pw(self,email):
        # record = crud.select("customer",
        #                     ["id","email","first_name","last_name","profile_image","verified","access_token"],
        #                     [email],
        #                     "email"
        #         )
        fields = """ id,email,first_name,last_name,profile_image,verified,access_token """
        where = "where email ='%s'"%email
        record = crud.select(self.table,
                             fields,where
        )
        return dict(record)

    def get_one_customer_by_id(self,id):
        # record = crud.select("customer",
        #                     ["id","email","first_name","last_name","profile_image","verified,password"],
        #                     [id],
        #                     "id"
        # )
        fields = "* "
        where = "where id =%s"%id
        record = crud.select(self.table,
                             fields,where
        )
        
        return dict(record)

    def update_customer(self,id,email,first_name,last_name,profil_pic):
        fields = ''' email=%s,first_name=%s,last_name=%s,profile_image=%s  '''
        data =  [email,first_name,last_name,profil_pic,id]
        where = " where id = %s "
        crud.update(self.table,
                    fields,
                    data,
                    where
        )   
        
        # crud.update("customer",
        #             [],
        #             [email,first_name,last_name,profil_pic,id],
        #             "id"
        # )
        fields = """ id,email,first_name,last_name,profile_image,verified,access_token """
        where = "where id ='%s'"%id
        record = crud.select(self.table,
                             fields,where
        )
        # record = crud.select("customer",
        #                     ["id","email","first_name","last_name","profile_image","verified"],
        #                     [id],
        #                     "id"
        # )
        
        return dict(record)

    def paged_sorted_filerd(self,page="",sort="",order="",filter_field="",value=""):
        # record = crud.select("customer",
        #                     field=["id","email","first_name","last_name","profile_image","verified"],
        #                     page=page,sort=sort,order=order,filter_field=filter_field,value=value
        # )
        fields = """ id,email,first_name,last_name,profile_image,verified """
        record = crud.select(self.table,
                    fields,
                    page=page,sort=sort,order=order,filter_field=filter_field,value=value
                    ,many=True)
        print(record)
        data=[]
        for i in record:
            path="customer/"    
            profile_image = s3.get_image(path,i["profile_image"])
            i["profile_image"] = profile_image
            data.append(dict(i))
        return data

    def  check_token(self,token,id):
        user =  crud.select("customer",
                            ["access_token"],
                            [id],
                            "id"
        )
        if token == user["access_token"]:
            return True
        else:
            return False
    