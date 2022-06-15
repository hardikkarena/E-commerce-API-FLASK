import psycopg2
import psycopg2.extras
connection_pgsql = psycopg2.connect(
   database="product", user='postgres', password='admin', host='localhost', port= '5432'
)
cursor = connection_pgsql.cursor(cursor_factory=psycopg2.extras.DictCursor)


      

