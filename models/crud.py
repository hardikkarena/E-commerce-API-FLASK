from dataclasses import field, fields
from library.dbconection import *

class CRUD:
    
    def exicute_query(self,sql,peram,many=False):
        query = sql.split()
        if query[0]=="INSERT":
            if many:
                cursor.executemany(sql,peram)
                connection_pgsql.commit()
            else:
                cursor.execute(sql,peram)
                connection_pgsql.commit()
                return cursor.fetchone()
        if query[0]=="UPDATE":
            cursor.execute(sql,peram)
            connection_pgsql.commit()
            return cursor.fetchone()
        if query[0]=="DELETE":
            cursor.execute(sql,peram)
            connection_pgsql.commit()
        if query[0]=="SELECT":
            if many:    
                cursor.execute(sql,peram)
                return cursor.fetchall()
            else:
                cursor.execute(sql,peram)
                return cursor.fetchone()

    def insert(self,table,fields,data,many=False): 
        sql = "INSERT INTO " + table + "(" + fields + ") values("
        for i in data:
            sql =sql+"%s,"
        sql = sql.rstrip(sql[-1])
        sql = sql + ") RETURNING *"
        record = self.exicute_query(sql,data,many)
        return record

    def update(self,table,fields,data,where):
        sql = "UPDATE " + table +" SET "+fields+where+" RETURNING *"
        record = self.exicute_query(sql,data)
        return record

    def delete(self,table,where=""):
        sql = "DELETE FROM " + table + where
        self.exicute_query(sql,())

    def select(self,table,fields,where="",join="",page="",sort="",order="",filter_field="",value="",many=False):
        sql = "SELECT "+ fields + " FROM " + table 
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
        record = self.exicute_query(sql,(),many)
        return record


       
    
    
    
        
        
    

    


