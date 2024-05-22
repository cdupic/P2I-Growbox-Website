import os

import mysql.connector as mysql
from flask import g


# One database connection is established per request.
# This can slow down the website, but is still good for small projects.

def get_db():
    if 'db' not in g:
        try:
            g.db = mysql.connect(
                host=os.getenv("SQL_HOST"),
                port=3306,
                user=os.getenv("SQL_USER"),
                password=os.getenv("SQL_PASSWORD"),
                database=os.getenv("SQL_DATABASE")
            )
        except Exception as e:
            print("[ERROR] MySQL: " + str(e))
    return g.db


def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()
