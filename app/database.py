#tools for connecting with db
import psycopg2
from psycopg2.extras import RealDictCursor #needed to get column names
import time



def establish_connection():
    while True:
        try:
            conn = psycopg2.connect(host='localhost', database='db_name', user='postgres', password='*********', cursor_factory=RealDictCursor)
            cursor = conn.cursor()
            print("db connection was successful")
            return conn, cursor
        except Exception as error:
            print("Connection failed. Error:", error)
            time.sleep(3)