import mysql.connector
from database import connect_db
from parking_rules import check_parking
from violations import record_violation, view_violations, update_violations, delete_violation
from datetime import datetime, timedelta

grace_periods = {}

def process_parking(plate_number, role, zone):
    result = check_parking(role, zone)
    if result == "Violation":
        record_violation(plate_number, role, zone, result)
    else:
        print("Parking Allowed")


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
            process_parking(plate_number, role, zone)
            
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
    grace_periods[plate_number] = {
        "start_time": curr_time,
        "role": role,
        "zone": zone
    }

    print("You have 10 minutes to move your vehicles before your car being clamp")

def check_grace_period(plate_number):
    grace_period = timedelta(minutes=10)
    start_time = grace_periods[plate_number]["start_time"]

    elapsed_time = datetime.now() - start_time

    if elapsed_time < grace_period :
        return "Active"
    else:
        return "Expired"

def cancel_grace_period(plate_number):
    if plate_number in grace_periods:
        grace_periods.pop(plate_number)
        print("Grace period cancelled. Vehicle has left.")
    else:
        print("No active grace period found.")

def enforce_parking(plate_number, role, zone):
    result = check_parking(role, zone)

    if result == "Allowed":
        print("Parking Allowed")
    else:
        start_grace_period(plate_number, role, zone)

def enforce_grace_parking(plate_number, role, zone):
    result = check_grace_period(plate_number)

    if result == "Expired":
        record_violation(plate_number, role, zone, "Unauthorized parking")
        grace_periods.pop(plate_number)
    else:
        print("You still have time to move your car.")

grace_periods["ABC1234"] = datetime.now() - timedelta(minutes=11)

enforce_grace_parking("ABC1234", "Student", "Staff")