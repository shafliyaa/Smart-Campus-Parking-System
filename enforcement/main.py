import mysql.connector
from database import connect_db
from parking_rules import check_parking

def record_violation(plate_number, user_role, parking_zone, violation_type):
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


def process_parking(plate_number, role, zone):
    result = check_parking(role, zone)
    if result == "Violation":
        record_violation(plate_number, role, zone, result)
    else:
        print("Parking Allowed")

process_parking("ABC1234", "Student", "Open")
process_parking("ABC1234", "Student", "Open")
process_parking("PAA1234", "Student", "Staff")






