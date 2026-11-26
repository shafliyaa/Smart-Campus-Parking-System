from database import connect_db

def record_violation(plate_number, user_role, parking_zone, violation_type):
    #Connect to database
    db = connect_db()

    #Create cursor
    cursor = db.cursor()

    #Execute INSERT statement
    cursor.execute("INSERT INTO parking_violations (plate_number, user_role, parking_zone, violation_type) VALUES (%s, %s, %s, %s)", (plate_number, user_role, parking_zone, violation_type))

    #Commit changes
    db.commit()

    #Display success message
    print("Violation recorded successfully!")

    #Close cursor and connection
    cursor.close()
    db.close()

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

def delete_violation(violation_id,):
    db = connect_db()

    cursor = db.cursor()

    cursor.execute("DELETE FROM parking_violations WHERE violation_id = %s", (violation_id,))
    print("The records deleted successfully")
    db.commit()
    cursor.close()
    db.close()