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


def view_violations():
    db = connect_db()

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * from parking_violations")

    records = cursor.fetchall()

    print("========== PARKING VIOLATIONS ==========")

    for row in records:

        print("Plate Number: ",row["plate_number"])
        print("Role: ", row["user_role"])
        print("Zone: ", row["parking_zone"])
        print("Violation: ", row["violation_type"])
        print("========================================")

    cursor.close()
    db.close()

def update_violations(violation_id, new_status):
    db = connect_db()
    cursor = db.cursor()

    cursor.execute("UPDATE parking_violations SET violation_status = %s WHERE violation_id = %s",(new_status, violation_id))

    db.commit()

    print("Violation status updated successfully!")

    cursor.close()
    db.close()

update_violations(1, "Resolved")