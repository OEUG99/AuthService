import os
from abc import ABC
from FlaskRESTServiceLayer.AbstractDatabaseConnection import AbstractDatabaseConnection
import mysql.connector


class AuthDBConnection(AbstractDatabaseConnection, ABC):

    def __init__(self):
        # Connect to the "auth" database
        conn = mysql.connector.connect(
            host="auth-mysql",
            port=3306,
            user="root",
            password=str(os.getenv("MYSQL_ROOT_PASSWORD")),
        )

        # initializing the DB
        cursor = conn.cursor()
        # creating auth DB if it doesn't already exist mysql
        cursor.execute("CREATE DATABASE IF NOT EXISTS auth")
        cursor.execute("USE auth")
        self.conn = conn
        cursor.close()

    def connect(self):
        return self.conn

    def close(self):
        self.conn.close()

    def query(self, query, params=None):
        if self.conn is None:
            self.connect()

        cur = self.conn.cursor()
        cur.execute(query, params)
        result = cur.fetchall()
        self.conn.commit()
        cur.close()
        return result

