import bcrypt
from flask import session, g


def get_users():
    cursor = g.db.cursor
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
        if user['user_name'] == user_name and user['password'] == password:
            print(True)
            session['user_name'] = user['user_name']
            session['auth_token'] = user['auth_token']
            return True
    return False


def hash_password(user_name, password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)


def test_password(password, hash):
    bcrypt.checkpw(password, hash)
