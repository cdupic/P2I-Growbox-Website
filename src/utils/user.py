from flask import session
from src.database.test.sql_connexion_test import SQL_connection

# TODO: Modify to access database with g object

def get_users():
    sql_connection = SQL_connection()
    cursor = sql_connection.cursor

    users = []

    try:

        cursor.execute(
            "SELECT * "
            "FROM Users")

        for (user_name, password,_, token) in cursor:
            print(f"user_name: {user_name}, password: {password}, token: {token}")
            users.append({"user_name": user_name, "password": password, "auth_token": token})

        return users

    except Exception as e:
        print(f"Erreur lors de la récupération des users: {e}")



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


if __name__ == "__main__":
    # Example of use
    print(authenticate_user("test", "test"))
