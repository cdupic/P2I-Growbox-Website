from flask import session

# TODO: Replace this with a real user management system using the database
users = [{
    "user_name": "test",
    "password": "test",  # Can be replaced by a hash (md5, sha256, bcrypt or other)
    "auth_token": "7713d075cae2f40323802bb73b355114"  # Random 16 bytes hex value
}]


def is_user_authenticated():
    if 'user_name' not in session or 'auth_token' not in session:
        return False
    for user in users:
        if user['user_name'] == session['user_name'] and user['auth_token'] == session['auth_token']:
            return True
    return False


def authenticate_user(user_name, password):
    for user in users:
        if user['user_name'] == user_name and user['password'] == password:
            session['user_name'] = user['user_name']
            session['auth_token'] = user['auth_token']
            return True
    return False
