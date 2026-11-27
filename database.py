import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def connect_db():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", 4000)),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        ssl_verify_cert=False
    )

    return connection