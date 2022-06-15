from numpy import record
from .crud import *



class Model_Company(CRUD):
    table = "company"
    def insert_company(self,company_name):
        fields = " company_name "
        data = [company_name]
        record = CRUD.insert(self,
                            self.table,
                            fields,
                            data
        )
        return dict(record)
    