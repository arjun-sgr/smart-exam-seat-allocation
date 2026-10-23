# data.py
# Student data functions.

def get_sample_students():
    return [
        {"roll": "101", "name": "Aarav", "division": "IT-A"},
        {"roll": "102", "name": "Diya", "division": "IT-B"},
        {"roll": "103", "name": "Arjun", "division": "IT-A"},
        {"roll": "104", "name": "Riya", "division": "CE-A"},
        {"roll": "105", "name": "Krish", "division": "CE-B"},
        {"roll": "106", "name": "Mahi", "division": "IT-B"},
        {"roll": "107", "name": "Yash", "division": "IT-A"},
        {"roll": "108", "name": "Jiya", "division": "CE-A"},
        {"roll": "109", "name": "Dev", "division": "CE-B"},
        {"roll": "110", "name": "Nisha", "division": "IT-B"},
        {"roll": "111", "name": "Raj", "division": "IT-A"},
        {"roll": "112", "name": "Khushi", "division": "CE-A"},
    ]


def find_student(students, roll):
    for student in students:
        if student["roll"] == roll:
            return student
    return None
