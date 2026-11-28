def check_parking(role, zone):
    if (role == "Staff" and zone == "Staff"):
        result = "Allowed"
    elif (role == "Staff" and zone == "Student"):
        result = "Allowed"
    elif (role == "Staff" and zone == "Visitor"):
        result = "Allowed"
    elif (role == "Student" and zone == "Student"):
        result = "Allowed"
    elif (role == "Student" and zone == "Staff"):
        result = "Violation"
    elif (role == "Student" and zone == "Visitor"):
        result = "Allowed"
    elif (role == "Visitor" and zone == "Visitor"):
        result = "Allowed"
    elif (role == "Visitor" and zone == "Staff"):
        result = "Violation"
    elif (role == "Visitor" and zone == "Student"):
        result = "Allowed"
    else:
        result = "Violation"

    return result



'''def check_parking(role, zone):
    allowed_parking = [
        ("Staff", "Staff"),
        ("Staff", "Student"),
        ("Staff", "Visitor"),
        ("Student", "Student"),
        ("Visitor", "Visitor"),
        ("Visitor", "Student")
    ]

    if (role, zone) in allowed_parking:
        return "Allowed"
    else:
        return "Violation"'''

