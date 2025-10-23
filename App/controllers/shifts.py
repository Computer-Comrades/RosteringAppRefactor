from App.models import User, Staff, Admin, Shifts, Attendance
from App.database import db
from datetime import datetime

def get_shift():
    return [a.get_json_shifts() for a in Shifts.query.all()]


