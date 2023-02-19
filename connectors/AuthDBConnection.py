from abc import ABC
from libraries.FlaskRESTServiceLayer.connections import AbstractDatabaseConnection as db
import mysql.connector


class AuthDBConnection(db.AbstractDatabaseConnection, ABC):


    def __init__(self):
        # Connect to the "auth" database
        conn = mysql.connector.connect(
            host="host.docker.internal",
            user="root",
            password="101Quark101!"
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

