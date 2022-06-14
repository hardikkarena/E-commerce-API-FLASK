from flask import request,jsonify
from library.validate import Validator
from library.s3 import S3
from library.authentication import Authentication
from models.product import Product_Model
from werkzeug.utils import secure_filename
import pandas as pd
import json

product_model = Product_Model()
validator = Validator()
authentication = Authentication()
s3 = S3()

class Product:
    def add_product(self):  
        name = request.form['name'],
        description = request.form['description'],
        price = request.form['price'],
        gst = request.form['gst'],
        category = request.form['category'],
        company_id = request.form['company_id'],
        img_list = request.files.getlist('product_image')
        if validator.validate_input([name,description,price,gst,category]):
            product_images=[]
            for i in img_list:
                product_images.append(secure_filename(i.filename))
            new_product = product_model.create_product(name,description,price,gst,category,product_images,company_id)
            for i in new_product["product images"]:
               
                image_url = s3.get_image("product/",i["image_name"])
                i["image_name"] = image_url

            return jsonify(new_product)
        else:
            return jsonify("Enter Valid Input")

    def update_product(self,id):
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        gst = request.form['gst']
        category = request.form['category']
        company_id = request.form['company_id']
        img_list=request.files['product_image']
        if validator.validate_input([name,description,price,gst,category,img_list,company_id]):
            # product_images=[]
            # for i in img_list:
            #     product_images.append(secure_filename(i.filename))
            if product_model.product_exist(id):
                updated_product=product_model.update_product_in_db(id,name,description,price,gst,category,company_id)
                return jsonify(updated_product)
            else:
                return jsonify("Product ID Not Exist")
        else:
            return jsonify("Enter Valid Input")

    def delete_product(self,id):
        if product_model.product_exist(id):
               product_model.delete_product_from_db(id)
               return jsonify("Product is Deleted")
        else:
                return jsonify("Product ID Not Exist")

    def get_one_product(self,id):
        if product_model.product_exist(id):
               product=product_model.get_one_product_from_db(id)
               return jsonify(product)
        else:
               return jsonify("Product ID Not Exist")

    def get_all_product(self):

        page=sort=order=filter_field=value=""
        if request.args.get('page'):
            page = request.args.get('page')
        if request.args.get('sort') and request.args.get('order'):
            sort = request.args.get('sort')
            order = request.args.get('order')
        if request.args.get('filter_field') and request.args.get('value'):
            filter_field = request.args.get('filter_field')
            value = request.args.get('value')
        data=product_model.paged_sorted_filerd(page=page,sort=sort,order=order,filter_field=filter_field,value=value)
        return jsonify(data)


    def get_file(self):
        file=request.files['file']
        file_name = secure_filename(request.files['file'].filename)
        
        s3.upload("files/",file)
        file_url = s3.get_image("files/",file_name)
        df=pd.read_csv(file_url,names=["C2Code","Br","Yr","Pfx","InvNo","InvDate","InvDay","InvMonth","InvYear","CustCode","CustC2id","OtherChg","InvFrght","shipcode","CrntPfx","CrntNo","CrntAmt","DbntPfx","DbntNo","DbntAmt","AdvPfx","AdvNo","AdvAmt","ReplPfx","ReplNo","ReplAmt","InvAmt","gstEnabled","fromGstNo","fromGstType","toGstNo","cgstTotal","sgstTotal","igstTotal","cessAmount","ItemCode","ItemC2id","ItemName","ItemName2","PackName","BatchNo","ExpDate","ExpDay","ExpMonth","ExpYear","InvQty","InvScQty","InvScDis","SchPer","InvDisc","SaleRate","VatPer","TSPer","LoclSale","CSTPer","CessPer","VatOnMrp","VatMrp","ItemMRP","TaxOnSch","DCNo","Repl","RefOrdNo","RefDate","MfgComp","MktgComp","ConvFact","CuItemId","CuItemCF","lostitem","Rack","MfCode","MrpIncl","CrDays","SmanCode","LRNo","LRDay","LRMonth","LRyear","itmTotal","hsnCode","cgstPer","cgstAmt","sgstPer","sgstAmt","igstPer","igstAmt","cessPer","cessAmt","MfacDate","BatchKey","Seller","Buyer","ItemPTR","TCSPer","TCSAmt"
    ])  
       
        main = {
            "status_code":"1",
    "status_message":"Data Fetched Successfully"
        }
        df['InvDate'] = pd.to_datetime(df['InvDate'])
        df['ExpDate'] = pd.to_datetime(df['ExpDate'])
        df['RefDate'] = pd.to_datetime(df['RefDate'])
        df['InvDate'] = df['InvDate'].dt.strftime('%d-%m-%Y')
        df['ExpDate'] = df['ExpDate'].dt.strftime('%d-%m-%Y')
        df['RefDate'] = df['RefDate'].dt.strftime('%d-%m-%Y')
        df2 = pd.DataFrame(columns=['amount','base_price','batch','chemist_medicine_name','discount_percentage','errors','expiry',"expiryLabel","expiryMonth","expiryYear","free","gst","gst_percentage","hsn_code","is_new","landing_price","margin_amount","margin_amount_single_item","margin_percentage","margin_percentage_on_mrp","medicine_id","medicine_name","mrp","old_medicine_id","pack_size","price_to_retailer","quantity","reference_code","scheme_amount","size","taxable","total_quantity"])
        df2[['batch']] = df[['BatchNo']] 
        df2[['chemist_medicine_name']] = df[['ItemName']] 
        df2[['discount_percentage']] = 5 
        df2[['expiry']] = df[['ExpDate']] 
        df2[['expiryLabel']] = df[['ExpDate']]
        df2['expiryLabel'] = pd.to_datetime(df2['expiryLabel'])
        df2['expiryLabel'] = df2['expiryLabel'].dt.strftime('%m-%y')
        df2[['expiryMonth']] = df[['ExpMonth']] 
        df2[['expiryYear']] = df[['ExpYear']] 
        df2[['free']] = 0
        df2[['gst_percentage']] = 18
        df2[['is_new']] = "yes"
        df2[['margin_percentage_on_mrp']] = 23.999596969696977
        df2[['medicine_name']] = df[['ItemName']] 
        df2[['mrp']] = df[['ItemMRP']] 
        df2[['pack_size']] = df[['PackName']] 
        df2[['price_to_retailer']] = df[['SaleRate']] 
        df2[['quantity']] = df[['InvQty']] 
        df2[['reference_code']] = df[['ItemCode']] 
        data = {
                "bill_date":"2022-05-31",
                "bill_no":"i22000730027622",
                "chemist_id":"116",
                "filename":"65a72f00-e0c0-11ec-82cb-001a7dda7112.csv",
                "payment_status":3
        }
        df2.fillna("",inplace=True)
        itemes = df2.to_dict(orient ='records')
        data["items"] = itemes
        main["data"] = data
        final_data = json.dumps(main)
        return jsonify(final_data)
