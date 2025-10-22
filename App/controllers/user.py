from App.models import User, Staff, Admin, Shifts
from App.database import db

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def create_admin(username, password):
    new_admin = Admin(username=username, password=password)
    db.session.add(new_admin)
    db.session.commit()
    return new_admin

def create_staff(username, password):
    new_staff = Staff(username=username, password=password)
    db.session.add(new_staff)
    db.session.commit()
    return new_staff

def delete_user(user_id):
    todel= User.query.get(user_id)
    if not todel:
        return print(f'User not found')

    db.session.delete(todel)
    db.session.commit()
    return print(f'User deleted')



def get_user_by_username(username):
    result = db.session.execute(db.select(User).filter_by(username=username))
    return result.scalar_one_or_none()

def get_user(id):
    return db.session.get(User, id)

def get_all_users():
    return db.session.scalars(db.select(User)).all()

def get_all_users_json():
    users = get_all_users()
    if not users:
        return []
    users = [user.get_json() for user in users]
    return users

def update_user(id, username):
    user = get_user(id)
    if user:
        user.username = username
        # user is already in the session; no need to re-add
        db.session.commit()
        return True
    return None

#Refactor: Combine shift and attendance reports
def view_combined_roster():
    return Shifts.query.all() 
