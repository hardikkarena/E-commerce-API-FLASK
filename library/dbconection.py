import psycopg2
import psycopg2.extras
connection_pgsql = psycopg2.connect(
   database="product", user='postgres', password='admin', host='localhost', port= '5432'
)
cursor = connection_pgsql.cursor(cursor_factory=psycopg2.extras.DictCursor)

def exicute_query(sql,peram,many=False):
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

      

