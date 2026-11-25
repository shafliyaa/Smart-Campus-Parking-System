import mysql.connector
from database import connect_db

def record_violation():
    # 1.Define variables
    plate_number = "PAA1234"
    user_role = "Student"
    parking_zone = "Staff"
    violation_type = "Unauthorized parking"

    # 2.Connect to database
    db = connect_db()

    # 3.Create cursor
    cursor = db.cursor()

    # 4.Execute INSERT statement
    cursor.execute("INSERT INTO parking_violations (plate_number, user_role, parking_zone, violation_type) VALUES (%s, %s, %s, %s)", (plate_number, user_role, parking_zone, violation_type))

    # 5.Commit changes
    db.commit()

    # 6.Display success message
    print("Violation recorded successfully!")

    # 7.Close cursor and connection
    cursor.close()
    db.close()

record_violation()







