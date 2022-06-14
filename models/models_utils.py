from dataclasses import field, fields
from library.dbconection import *

class CRUD:
    def insert(self,table,fields,data,many=False): 
        print(type(data))
        print(data)
        sql = "INSERT INTO " + table + "(" + fields + ") values("
        for i in data:
            sql =sql+"%s,"
        sql = sql.rstrip(sql[-1])
        
        sql = sql + ") RETURNING *"
        # sql = sql + table + "("

        # for i in field:
        #     f = str(i)
        #     sql = sql + f + ","

        # sql = sql.rstrip(sql[-1])
        # sql = sql + ") values("
        
        # for i in field:
        #     sql =sql+"%s,"
        # sql = sql.rstrip(sql[-1])
        # sql = sql+") RETURNING *"
        
        record = exicute_query(sql,data,many)
        return record

    def update(self,table,fields,data,where):
        sql = "UPDATE" + table +" SET "+fields+where+" RETURNING *"
        # sql = sql + table+" SET "
       
        # if condition_field!="":
        #     sql = sql+" WHERE "+condition_field+"=%s"
        # sql = sql+" RETURNING *"
        record = exicute_query(sql,data)
        
        return record

    def delete(self,table,where=""):
        sql = "DELETE FROM " + table + where
        exicute_query(sql,())

    def select(self,table,fields,where="",join="",page="",sort="",order="",filter_field="",value="",many=False):
        sql = "SELECT "+ fields + "FROM " + table 
        # for i in field:
        #     sql = sql + i +","
        # sql = sql.rstrip(sql[-1])
        # sql = sql + " FROM "+table
        # if condition_field!="":
        #     sql = sql+" WHERE "+condition_field+"=%s"
        if join != "":
            sql = sql + join
            
        if filter_field!="" and value!="":
            sql = sql+" where %s='%s'"%(filter_field,value)

        if sort!="" and order!="":
            sql = sql+" ORDER BY %s %s"%(sort,order)
            
        if page!="":
            limit=3
            offset=(limit * int(page)) - limit
            sql = sql+" limit %s offset %s"%(limit,offset)
        sql = sql + where
        record = exicute_query(sql,(),many)
        return record


       
    
    
    
        
        
    

    


