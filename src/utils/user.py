from flask import session, g
from src.database.database import get_db


def get_users():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    users = []

    try:
        cursor.execute(
            "SELECT * "
            "FROM Users")

        for user in cursor:
            users.append(user)
        return users

    except Exception as e:
        print(f"Error when getting users: {e}")


def is_user_authenticated():
    users = get_users()
    print(users)
    if 'user_name' not in session or 'auth_token' not in session:
        return False
    for user in users:
        if user['user_name'] == session['user_name'] and user['auth_token'] == session['auth_token']:
            return True
    return False


def authenticate_user(user_name, password):
    users = get_users()
    for user in users:
        if user['user_name'] == user_name and verify_password(user_name, password):
            print(True)
            session['user_name'] = user['user_name']
            session['auth_token'] = user['auth_token']
            return True
    return False


def verify_password(user_name, password):
    db = get_db()
    try :
        cursor = db.cursor()
        cursor.execute(
            "SELECT * "
            "FROM Users "
            "WHERE user_name = %s AND password = PASSWORD(%s)",
            (user_name, password)
        )
        user = cursor.fetchone()
        if user is None:
            return False
        return True

    except Exception as e:
        print(f"Error when checking passwords: {e}")




