import os

import mysql.connector
from dbutils.pooled_db import PooledDB
from dotenv import load_dotenv
from flask import g

load_dotenv()

pool = PooledDB(
    creator=mysql.connector,
    maxconnections=10,
    mincached=2,
    maxcached=5,
    blocking=True,
    host=os.getenv("SQL_HOST"),
    user=os.getenv("SQL_USER"),
    password=os.getenv("SQL_PASSWORD"),
    database=os.getenv("SQL_DATABASE"),
    port=3306
)


def get_db():
    try:
        return pool.connection()
    except Exception as e:
        print("[ERROR] MySQL: " + str(e))


def init_db():
    if 'db' not in g:
        g.db = get_db()


def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()
