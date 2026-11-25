import mysql.connector

def connect_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jjkkth07$",
        database="scps"
    )

    return connection