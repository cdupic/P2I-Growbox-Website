import os
from dotenv import load_dotenv

import mysql.connector as mysql
from flask import g

# One database connection is established per request.
# This can slow down the website, but is still good for small projects.
load_dotenv()

def get_db():

    try:
        db = mysql.connect(
        host = os.getenv("SQL_HOST"),
        port = 3306,
        user = os.getenv("SQL_USER"),
        password = os.getenv("SQL_PASSWORD"),
        database = os.getenv("SQL_DATABASE")
        )
        return db

    except Exception as e:
        print("[ERROR] MySQL: " + str(e))




def init_db():
    if 'db' not in g:
        g.db = get_db()


def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()
