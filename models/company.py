from .models_utils import *
crud = CRUD()


class Model_Company:
    def insert_company(self,company_name):
        record = crud.insert("company",
                            ["company_name"],
                            [company_name]
        )
        return dict(record)
    