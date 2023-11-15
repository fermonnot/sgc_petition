import psycopg2 


connection = psycopg2.connect(
    host= "localhost",
    user= "postgres",
    password= "Siste04*",
    port= "5432"
)

connection.autocommit = True

def deleteDb():
    cursor = connection.cursor()
    query = "DROP TABLE document_control"
    cursor.execute(query)
    cursor.close()

deleteDb()