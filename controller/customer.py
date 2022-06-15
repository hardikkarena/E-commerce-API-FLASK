from ast import Mod
from flask import request,jsonify
from library.validate import Validator
from library.s3 import S3
from library.authentication import Authentication,login_required
import hashlib
from werkzeug.utils import secure_filename
from models.customer import Model_Customer
import random

validator = Validator()
model_customer = Model_Customer()
authentication = Authentication()
s3 = S3()

class Customer:
    def singup(self):
        try:
            email = str(request.form['email'])
            first_name = str(request.form['first_name'])
            last_name = str(request.form['last_name'])
            profil_pic = request.files['profil_pic']
            password = str(request.form['password'])
        except:
            msg = "Invalid Fields"
            return jsonify(msg)

        if validator.validate_input([email,first_name,last_name,profil_pic,password]):
            if validator.validate_password(password):
                if model_customer.customer_exist(email):
                    msg = "customer already exist"
                    return jsonify(msg)
                else:
                    password = hashlib.md5(password.encode()).hexdigest()
                    profile_pic_name = secure_filename(profil_pic.filename)
                    new_user = model_customer.insert_customer(email,
                                                              password,
                                                              first_name,
                                                              last_name,
                                                              profile_pic_name
                    )

                    token = authentication.generate_token(new_user["id"])
                    new_user["access_token"] = token
                    path="customer/"
                    s3.upload(path,profil_pic)
                    profile_image = s3.get_image(path,profile_pic_name)
                    new_user["profile_image"] = profile_image
                    return jsonify(new_user)
            else:
                msg = "Invalid Password Format"
                return(msg)
        else:
            msg = "Blank Filed"
            return jsonify(msg)
    
    def sent_otp(self,id):
        if model_customer.is_user_exist_by_id(id):
            otp=str(random.randint(1000,9999))
            model_customer.update_otp(otp,id)
            msg = 'OTP SENT'
            return jsonify(msg)
        else:
            msg = 'User Dose Not Exist'
            return jsonify(msg)

    def verify_otp(self,id):
        otp = request.json['otp']
        if validator.validate_input([otp]):
            if model_customer.is_user_exist_by_id(id):
                if model_customer.is_otp_sent(id):
                    if model_customer.verify_otp_in_databse(otp,id):
                        model_customer.update_status(id)
                        return jsonify("Profile Verified")
                    else:
                        return jsonify("OTP Dose Not Matched")
                else:
                    return jsonify("OTP NOT SENT")  
            else:
                return jsonify('User Not Exist'),501
        else:
            return jsonify("Enter Valid Input")
    
    def login(self):
        email = request.json['email']
        password1 = request.json['password']

        if validator.validate_input([email,password1]):
            if model_customer.customer_exist(email):
                password = hashlib.md5(password1.encode()).hexdigest()
                user=model_customer.get_one_customer_by_email(email)
                if model_customer.is_customer_verified(user['email']):
                    if password == user["password"]:
                        user=model_customer.get_one_customer_no_pw(email)
                        authentication.generate_token(user["id"])
                        path = "customer/"
                        profile_image = s3.get_image(path,user["profile_image"])
                        user["profile_image"]=profile_image
                        return jsonify(user)
                    return jsonify("wrong passwoord")
                else:
                    return jsonify("Customer is Not Verified OTP")
            else:
                return jsonify('Invalide Email')
        else:
            return jsonify("Enter Valid Input")

    @login_required
    def get_profile(self,id):
        if model_customer.is_user_exist_by_id(id):
            customer = model_customer.get_one_customer_by_id(id)
            path = "customer/"
            profile_image = s3.get_image(path,customer["profile_image"])
            customer["profile_image"]=profile_image
            return jsonify(customer)
            
        else:
            return jsonify('User Dose Not Exist')
    
    def set_profile(self):
        email=str(request.form['email'])
        first_name=str(request.form['first_name'])
        last_name=str(request.form['last_name'])
        profile_pic=request.files['profile_pic']
        profile_pic_name=secure_filename(request.files['profile_pic'].filename)
        id = request.args.get("id")
        if validator.validate_input([email,first_name,last_name,profile_pic]):
            customer = model_customer.update_customer(id,
                                                      email,
                                                      first_name,
                                                      last_name,
                                                      profile_pic_name
            )
            path="customer/"
            s3.upload(path,profile_pic)
            profile_image = s3.get_image(path,profile_pic_name)
            customer["profile_image"] = profile_image
            return jsonify(customer)
        else:
            return jsonify("Enter Valid Input")
        
    def all_profile(self):
        page=sort=order=filter_field=value=""
        if request.args.get('page'):
            page = request.args.get('page')
        if request.args.get('sort') and request.args.get('order'):
            sort = request.args.get('sort')
            order = request.args.get('order')
        if request.args.get('filter_field') and request.args.get('value'):
            filter_field = request.args.get('filter_field')
            value = request.args.get('value')
        records=model_customer.paged_sorted_filerd(page=page,
                                                   sort=sort,
                                                   order=order,
                                                   filter_field=filter_field,
                                                   value=value
        )
        return jsonify(records)

    def forgot_password(self):
        id = request.headers['id']
        otp = request.json['otp']
        password = request.json['password']
        if validator.validate_input([otp,password]):
            if model_customer.is_user_exist_by_id(id):
                if model_customer.is_otp_sent(id):
                    if model_customer.verify_otp_in_databse(otp,id):
                        password = hashlib.md5(password.encode()).hexdigest()
                        model_customer.update_password(id,password)
                        return jsonify("Password Changed")
                    else:
                        return jsonify("OTP Dose Not Matched")
                else:
                    return jsonify("OTP NOT SENT")  
            else:
                return jsonify('User Not Exist'),501  
        else:
            return jsonify("Enter Valid Input")
        
    def change_password(self):
        id = request.headers['id']
        old_password = request.json['old_password']
        new_password = request.json['new_password']
        if validator.validate_input([old_password,new_password]):
            if model_customer.is_user_exist_by_id(id):
                    if model_customer.verify_password(old_password,id):
                        new_password = hashlib.md5(new_password.encode()).hexdigest()
                        model_customer.update_password(id,new_password)
                        return jsonify("Password Changed")
                    else:
                        return jsonify("Old Password Dose Not Matched") 
            else:
                return jsonify('User Not Exist'),501  
        else:
            return jsonify("Enter Valid Input")
    def add_address(self):
        id = request.headers['id']
        address = request.json['address']
        city = request.json['city']
        state = request.json['state']
        pin_code = request.json['pin_code']
        country = request.json['country']
        
        if validator.validate_input([address,city,state,pin_code,country]):
            address = Model_Customer.insert_address(self,
                                                    address,
                                                    city,
                                                    state,
                                                    pin_code,
                                                    country,
                                                    id
            ) 

            return jsonify(address)           
        else:
            return jsonify("Enter Valid Input")
        
        
        
        
        
        
