import mysql.connector
import os

# Load database configuration from environment variables or use default values
db_config_user = {
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'jaipathak2005'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': 'user_auth'
}

db_config_heartattack = {
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', 'jaipathak2005'),
    'host': os.getenv('DB_HOST', 'localhost'),
    'database': 'heartattack'
}

def create_connection(config):
    try:
        return mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def create_connection_user():
    return create_connection(db_config_user)

def create_connection_heartattack():
    return create_connection(db_config_heartattack)

