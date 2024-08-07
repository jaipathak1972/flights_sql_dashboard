import bcrypt
from db_connection import create_connection_user
import mysql.connector

class UserRegister:
    def __init__(self):
        pass

    def register_user(self, username, password):
        conn = create_connection_user()
        if conn is None:
            return
        cursor = conn.cursor()

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        try:
            # Insert the user into the database
            cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password.decode('utf-8')))
            conn.commit()
            print("User registered successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            conn.close()

    def login_user(self, username, password):
        conn = create_connection_user()
        if conn is None:
            return
        cursor = conn.cursor()

        try:
            # Retrieve the user from the database
            cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()

            if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
                return True
            else:
                return False
        finally:
            cursor.close()
            conn.close()
