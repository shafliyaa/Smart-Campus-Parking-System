from database import connect_db
from enforcement.parking_rules import check_parking
from enforcement.violations import record_violation, view_violations, update_violations, delete_violation
from datetime import datetime, timedelta
import time 
import threading

grace_periods = {}

print("========== SMART CAMPUS PARKING SYSTEM ==========\n")
print("1. Check parking eligibility")
print("2. View violations")
print("3. Update violations status")
print("4. Delete violation status")
print("5. Exit")

def main_menu():
    while True: 
        choice = input("Enter your choice: ")

        if choice == "1":
            plate_number = input("Enter plate number: ")
            role = input("Enter role: ")
            zone = input("Enter zone: ")
            enforce_parking(plate_number, role, zone)
            
        elif choice == "2":
            view_violations()

        elif choice == "3":
            violation_id = int(input("Enter violation_id: "))
            new_status = input("Enter new status: ")
            update_violations(violation_id,new_status)

        elif choice == "4":
            violation_id = int(input("Enter violation_id: "))
            delete_violation(violation_id)

        elif choice == "5":
            print("Exiting system...")
            break

        else:
            print("Invalid choice. Please try again.")
            

def start_grace_period(plate_number, role, zone):
    curr_time = datetime.now()

    db = connect_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT * FROM grace_periods WHERE plate_number = %s",
        (plate_number,)
    )

    existing_record = cursor.fetchone()

    if existing_record:
        # Index [2] represents parking_zone
        existing_zone = existing_record[2]

        if existing_zone == zone:
            print("Vehicle already has an active grace period in this zone.")

        else:
            cursor.execute(
                """UPDATE grace_periods
                   SET start_time = %s,
                       user_role = %s,
                       parking_zone = %s,
                       final_warning_sent = %s
                   WHERE plate_number = %s""",
                (curr_time, role, zone, False, plate_number)
            )

            db.commit()

            grace_periods[plate_number] = {
                "start_time": curr_time,
                "role": role,
                "zone": zone,
                "final_warning_sent": False
            }

            print(
                f"WARNING: Vehicle {plate_number} has entered "
                "a different restricted zone. "
                "New 10-minute grace period started."
            )

    else:
        cursor.execute(
            """INSERT INTO grace_periods
               (plate_number, start_time, user_role,
                parking_zone, final_warning_sent)
               VALUES (%s, %s, %s, %s, %s)""",
            (plate_number, curr_time, role, zone, False)
        )

        db.commit()

        grace_periods[plate_number] = {
            "start_time": curr_time,
            "role": role,
            "zone": zone,
            "final_warning_sent": False
        }

        print(
            f"WARNING: Unauthorised parking detected! "
            f"Vehicle {plate_number} has 10 minutes to move."
        )

    cursor.close()
    db.close()


def check_grace_period(plate_number):
    grace_period = timedelta(minutes=10)
    start_time = grace_periods[plate_number]["start_time"]

    elapsed_time = datetime.now() - start_time

    if elapsed_time >= timedelta(minutes=8) and grace_periods[plate_number]["final_warning_sent"] == False :
        grace_periods[plate_number]["final_warning_sent"] = True

        db = connect_db()
        cursor = db.cursor()

        cursor.execute(
            """UPDATE grace_periods
            SET final_warning_sent = TRUE
            WHERE plate_number = %s""",
            (plate_number,)
        )

        db.commit()
        cursor.close()
        db.close()
        print(f"WARNING: Unauthorised parking detected! Vehicle {plate_number} has 2 minutes remain to move.")
        

    if elapsed_time < grace_period :
        return "Active"
    else:
        return "Expired"

def cancel_grace_period(plate_number):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM grace_periods WHERE plate_number = %s", 
        (plate_number,))
    if cursor.rowcount > 0:
        print("Grace period record deleted from database.")
    else:
        print("No grace period record found in database.")
    db.commit()
    cursor.close()
    db.close()

    if plate_number in grace_periods:
        grace_periods.pop(plate_number)
        print("Grace period cancelled. Vehicle has left.")
    else:
        print("No active grace period found.")

def enforce_parking(plate_number, role, zone):
    result = check_parking(role, zone)

    if result == "Allowed":
        print("Parking Allowed")
    elif role == "Visitor":
        record_violation(plate_number, role, zone, "Unauthorized parking - Immediate clamping")
        print("Visitor parking violation detected. JK will clamp the vehicle immediately.")
    else:
        start_grace_period(plate_number, role, zone)

#Check expired grace period
def enforce_grace_parking(plate_number):
    result = check_grace_period(plate_number)

    if result == "Expired":
        details = grace_periods[plate_number] #to retrieve details
        record_violation(plate_number, details["role"], details["zone"], "Unauthorized parking")

        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM grace_periods WHERE plate_number = %s", (plate_number,))
        db.commit()
        cursor.close()
        db.close()

        grace_periods.pop(plate_number)
    

def check_all_grace_periods():
    for plate_number in list(grace_periods):
        result = check_grace_period(plate_number)
        if result == "Expired":
            enforce_grace_parking(plate_number)
        '''else:
            print("Vehicle still have time to move the car.")'''

def automatic_grace_monitor():
    while True:
        check_all_grace_periods()
        time.sleep(5) #tell python to pause for 5 sec

def load_grace_periods():
    db = connect_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT plate_number, start_time, user_role, parking_zone, final_warning_sent FROM grace_periods"
    )

    records = cursor.fetchall()

    for row in records: 
        plate_number = row[0]

        grace_periods[plate_number] = {
            "start_time": row[1],
            "role": row[2],
            "zone": row[3],
            "final_warning_sent": bool(row[4])
        }

    cursor.close()
    db.close()

    print(f"{len(grace_periods)} active grace period(s) loaded from database.")

load_grace_periods()

monitor_thread = threading.Thread(
    target=automatic_grace_monitor,
    daemon=True
)
monitor_thread.start()

main_menu()
