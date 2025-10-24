import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Shifts, Attendance, Staff, Admin
from App.controllers import (
    create_user,
    create_admin,
    create_staff,
    get_all_users_json,
    get_user,
    update_user
)
from App.controllers.auth import login
from App.controllers.admin import schedule_shifts, view_shift_report
from App.controllers.attendance import staff_in, staff_out
from App.controllers.shifts import get_shift
from datetime import datetime

LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob", "position":"user"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password)
        user = User("bob", password)
        assert user.password != password

    def test_new_admin(self):
        newadmin = Admin("mary", "marypass")
        assert newadmin.username == "mary"

    def test_new_attendance(self):
        attendance = Attendance(1, 2, "09:00", "12:00")
        assert attendance.staff_id == 1
        assert attendance.shift_id == 2

    def test_new_shift(self):
        shift = Shifts(1, "07/04/2025", "09:00", "12:00")
        assert shift.staff_id == 1
        assert shift.date == "07/04/2025"
        assert shift.start_time == "09:00"

    def test_new_staff(self):
        newstaff = Staff("rob", "robpass")
        assert newstaff.username == "rob"

    def test_new_user(self):
        newuser = User("bob", "bobpass")
        assert newuser.username == "bob"


'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="class")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


class UserIntegrationTests(unittest.TestCase):

    def test_authenticate(self):
        user = create_user("bob", "bobpass")
        assert login("bob", "bobpass") != None
    
    def test_create_user(self):
        user = create_user("rick", "rickpass")
        assert user.username == "rick"
    
    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([
            {"id": 1, 
             "username":"bob", 
             "position":"user"}, 
             
             {"id": 2, 
              "username":"rick", 
              "position":"user"}
              ], users_json)
    
    def test_schedule_shift(self):
        newstaff = create_staff("mary", "marypass")
        newshift = schedule_shifts(newstaff.id, "07/04/2025", "09:00", "12:00")
        assert newshift.date == "07/04/2025"

    def test_staff_in(self):
        newshift = schedule_shifts(3, "07/04/2025", "10:00", "01:00")
        atnd = staff_in("mary", newshift.id)
        assert atnd.time_in == datetime.now().strftime("%H:%M")

    def test_staff_out(self):
        atnd = staff_out("mary", 2)
        assert atnd.time_out == datetime.now().strftime("%H:%M")


    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"


    def test_view_attendance_report(self):
        report_json = view_shift_report()
        self.assertListEqual([
            {"id": 1,  
             "staff_id": 3, 
             "staff_name": "mary", 
             "shift_id": 2, 
             "time_in": datetime.now().strftime("%H:%M"), 
             "time_out": datetime.now().strftime("%H:%M")}
             ], report_json)

    
    def test_view_combined_roster(self):
        roster_json = get_shift()
        self.assertListEqual([
            {"id": 1,
            "staff_id": 3,
            "staff_name": "mary",
            "date": "07/04/2025",
            "start_time": "09:00",
            "end_time": "12:00"},

            {"id": 2,
            "staff_id": 3,
            "staff_name": "mary",
            "date": "07/04/2025",
            "start_time": "10:00",
            "end_time": "01:00"}
            ], roster_json)