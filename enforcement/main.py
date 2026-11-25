import mysql.connector
from database import connect_db

try: 
    db = connect_db()

    if db.is_connected():
        print("Successfully connected to Smart Campus Parking System")

    db.close()

except mysql.connector.Error as error:
    print("Database connection failed:", error)