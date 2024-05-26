from secrets import token_bytes

from flask import session

from src.database.database import get_db


def get_user_info(user_name):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    users = []

    try:
        cursor.execute(
            "SELECT * "
            "FROM Users "
            "WHERE user_name = %s ",
            (user_name,)
        )

        for user in cursor:
            users.append(user)
        return users

    except Exception as e:
        print(f"Error when getting users: {e}")


def is_user_authenticated():
    if 'user_name' in session and 'auth_token' in session:
        for user in get_user_info(session['user_name']):
            if user['user_name'] == session['user_name'] and user['auth_token'] == session['auth_token']:
                return True

    if 'user_name' in session:
        session.pop('user_name')
    if 'auth_token' in session:
        session.pop('auth_token')

    return False


def authenticate_user(user_name, password):
    db = get_db()
    try:
        cursor = db.cursor()
        cursor.execute(
            "SELECT auth_token "
            "FROM Users "
            "WHERE user_name = %s AND password = PASSWORD(%s)",
            (user_name, password)
        )
        result = cursor.fetchone()
        if result:
            session['user_name'] = user_name
            session['auth_token'] = result[0]
            session['graphs_days'] = 7
            return True

    except Exception as e:
        print(f"Error when checking passwords: {e}")

    return False


def create_user(user_name, password):
    db = get_db()
    cursor = db.cursor()
    try:
        auth_token = token_bytes(16).hex()
        cursor.execute(
            "INSERT INTO Users (user_name, password, auth_token) "
            "VALUES (%s, PASSWORD(%s), %s)",
            (user_name, password, auth_token)
        )
        db.commit()
        return auth_token

    except Exception as e:
        print(f"Error when creating user: {e}")
        return None


