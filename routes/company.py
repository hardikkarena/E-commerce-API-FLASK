from flask import Blueprint
from controller.company import Company

company_obj = Company
company = Blueprint('company', __name__,url_prefix='/company')

company.route('/add_company',methods=['POST'])(company_obj.add_company)