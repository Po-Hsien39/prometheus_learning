import mysql.connector
from opentelemetry.instrumentation.mysql import MySQLInstrumentor

MySQLInstrumentor().instrument()

def initialize_database():
    print("initializing...")
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="1234"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS MySQL_Database")
    cursor.execute('USE MySQL_Database')
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS todo (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task VARCHAR(255) NOT NULL
    )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def get_db_connection():
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="1234"
    )
    return conn

def query_db(query, args=None, commit=False):
    conn = get_db_connection()
    cursor = conn.cursor(query)
    cursor.execute('USE MySQL_Database')
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def commit_db(query, args=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('USE MySQL_Database')
    result = conn.cursor(query, args)
    cursor.close()
    conn.close()
    return result
