from App.models import User, Staff, Admin, Shifts, Attendance
from App.database import db
from datetime import datetime

def get_shift():
    shift= get_json_shifts()

