import os
import oracledb
from dotenv import load_dotenv


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_CONNECT_STRING = os.getenv("DB_CONNECT_STRING")


# Oracle DB Connection testing
def get_db_connection():
    try:
        connection = oracledb.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            dsn=DB_CONNECT_STRING,
        )
        print(" Oracle DB Connection Successful")
        return connection
    except oracledb.DatabaseError as e:
        print(" Oracle DB Connection Failed:", e)
        return None


# Main
if __name__ == "__main__":
    get_db_connection()
