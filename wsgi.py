import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import (User, Admin, Staff, Attendance, Shifts)
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, delete_user, create_admin, create_staff,get_user_by_username )
from App.controllers.admin import (schedule_shifts, view_shift_report)
from App.controllers.attendance import (staff_in, staff_out)
from App.controllers.shifts import (view_combined_roster)




# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 
ad = AppGroup('admin', help='Admin object commands')
atnd= AppGroup('staff', help= 'Staff attendance object commands')

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

#----------------------------------- Added by Me
@user_cli.command("delete", help="deletes a user from the database")
@click.argument("id")
def delete_user_cmd(id):
    if id:
        delete_user(id)

@user_cli.command("createstaff", help="Creates a staff user")
@click.argument("username")
@click.argument("password")
def create_staff_command(username, password):
    create_staff(username, password)
    print(f'{username} created!')

#admin commands----------------
@ad.command("createsched", help="Creates a user schedule")
@click.argument("staff_id")
@click.argument("date")  
@click.argument("start_time") 
@click.argument("end_time")   
def create_schedule_cmd(staff_id, date, start_time, end_time):
    username = input("Enter your username: ").strip()
    user = User.query.filter_by(username=username).first()

    if not user:
        print("User not found.")
        return
    
    if user.position != "admin":
        print("Permission denied. Only admins can create schedules.")
        return


    shift = schedule_shifts(staff_id, date, start_time, end_time)
    if shift:
        print(f"Shift created for staff {staff_id} on {date} ({start_time} - {end_time})")
    else:
        print(f"Failed: staff {staff_id} not found")


@ad.command("getshifts", help="Get all scheduled shifts")
def get_shifts_cmd():
    username = input("Enter your username: ").strip()

    user = User.query.filter_by(username=username).first()
    if not user:
        print("User not found.")
        return
    
    if user.position != "admin":
        print("Permission denied. Only admins can view scheduled shifts.")
        return

    shifts = Shifts.query.all()
    if shifts:
        for s in shifts:
            print(s)
    else:
        print("No shifts scheduled yet.")

@ad.command("report", help="Admin generates shift report")
def report_cmd():
    username = input("Enter your username: ").strip()

    #refactor use the controller get_user_by_username from controllers/user.py
    user = get_user_by_username(username)
    user = User.query.filter_by(username=username).first()
    if not user:
        print("User not found.")
        return
    
    if user.position != "admin":
        print("Permission denied. Only admins can generate reports.")
        return
        
    report = view_shift_report()
    if report:
        for entry in report:
            print(entry)
    else:
        print("No attendance records yet.")

#staff attendance commands-------
@atnd.command("clock_in", help="Records staff start of shift")
@click.argument("username")
@click.argument("shift_id", type=int)
def clockin_cmd(username, shift_id):
    attn = staff_in(username, shift_id)
    print(attn)

@atnd.command("clock_out", help= "Records staff end of shift")
@click.argument("username")
@click.argument("shift_id", type=int)
def clockout_cmd(username, shift_id):
    attn= staff_out(username, shift_id)
    if attn:
        print(attn)
    else:
        print(f"Attendance record not found for '{username}") 

@atnd.command("roster", help= "Staff generates a combined report")
def combined_roster():
    roster = view_combined_roster()
    if roster:
        for shift in roster:
            print(shift)  # __repr__ output from Shifts
    else:
        print("No scheduled shifts yet.")
    #print(view_combined_roster())



app.cli.add_command(user_cli) # add the group to the cli
app.cli.add_command(ad)
app.cli.add_command(atnd)

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)