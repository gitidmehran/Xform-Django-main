import json
import os
from django.conf import settings
import mysql.connector
from mysql.connector import Error

def load_database_settings():
    current_dir = os.getcwd()
    settings_filename = os.path.join(current_dir, 'myapi', 'record_files', 'database_settings.json')
    try:
        with open(settings_filename, 'r') as settings_file:
            database_settings = json.load(settings_file)
            return database_settings
    except FileNotFoundError:
        return False

def db_connection( db_type, Test = False ):
    database_settings = load_database_settings()
    if not database_settings or not database_settings[db_type].get("hostname", "root"):
        return False
    # db_config = settings.DATABASES['default']
    db_config = {
        "host": database_settings[db_type].get("hostname", "49.13.21.18"),
        "user": database_settings[db_type].get("username", "root"),
        "password": database_settings[db_type].get("password", "ZiaIqbal@123"),
        "database": database_settings[db_type].get("database", "mrph_testdb"),
        "port": database_settings[db_type].get("port", "33061")
    }
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("Connected to MySQL database")
            if Test:
                print("Test Connection", "Connected to MySQL database.")
            else:
                return connection
    except Error as e:
        if e.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist. You may need to create it.")
            print("Error", "Database does not exist. You may need to create it.")
        elif e.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Access denied. Check your username and password.")
            print("Error", "Access denied. Check your username and password.")
        else:
            print(f"Error: {e}")
            print("Error", e)
            exit()
    
    return None
