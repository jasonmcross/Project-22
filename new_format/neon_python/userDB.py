#updated
import os
import psycopg2
from dotenv import load_dotenv

class DatabaseOperations:
    def __init__(self):
        load_dotenv()
        self.connection_string = "postgresql://PhilopateerAz:CF3q1wNWbOle@ep-lively-hat-a5tacpqp.us-east-2.aws.neon.tech/Project22?sslmode=require"
        print("url:", self.connection_string)
        self.conn = psycopg2.connect(self.connection_string)

    def __del__(self):
     if hasattr(self, 'conn') and self.conn is not None:
        self.conn.close()


    def add_user(self, email, name, password):
        cur = self.conn.cursor()
        sql = "INSERT INTO users (email, name, password) VALUES (%s, %s, %s)"
        cur.execute(sql, (email, name, password))
        self.conn.commit()
        cur.close()

    def remove_user(self, email):
        cur = self.conn.cursor()
        sql = "DELETE FROM users WHERE email = %s"
        cur.execute(sql, (email,))
        self.conn.commit()
        cur.close()

    def edit_user_password(self, email, new_password):
        cur = self.conn.cursor()
        sql = "UPDATE users SET password = %s WHERE email = %s"
        cur.execute(sql, (new_password, email))
        self.conn.commit()
        cur.close()

    def lookup_user(self, email):
        cur = self.conn.cursor()
        sql = "SELECT password FROM users WHERE email = %s"
        cur.execute(sql, (email,))
        result = cur.fetchone()
        cur.close()
        return result
