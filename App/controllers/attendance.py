from App.models import Attendance, Shifts, Staff
from App.database import db
from datetime import datetime

#refactor attendance controllers to remove time_in. 
def staff_in(username, shift_id):
    staff = Staff.query.filter_by(username=username).first()
    if not staff:
        return None  # Staff not found
  
    time_in = datetime.now().strftime("%H:%M")
    atd = Attendance(staff_id=staff.id, shift_id=shift_id, time_in=time_in)
    db.session.add(atd)
    db.session.commit()
    return atd

#refactor attendance controllers to remove time_out = None
# 
def staff_out(username, shift_id):
    staff = Staff.query.filter_by(username=username).first()
    if not staff:
        return None  

    atd = Attendance.query.filter_by(staff_id=staff.id, shift_id=shift_id, time_out=None).first()
    if not atd:
        return None 

    
    time_out = datetime.now().strftime("%H:%M")
    
    atd.time_out = time_out
    db.session.commit()
    return atd


