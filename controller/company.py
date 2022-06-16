from flask import jsonify,request
from models.company import Model_Company

model_company = Model_Company()

class Company:
    def add_company():
        company_name = request.json['company_name']
        company=model_company.insert_company(company_name)
        return jsonify(company)

