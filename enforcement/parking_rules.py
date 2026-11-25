def check_parking(role, zone):
    if (role == "Staff" and zone == "Staff"):
        result = "Allowed"
    elif (role == "Student" and zone == "Staff"):
        result = "Violation"
    else:
        result = "Allowed"

    return result

print(check_parking("Staff", "Staff"))
print(check_parking("Student", "Staff"))
print(check_parking("Student", "Open"))

