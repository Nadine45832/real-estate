import oracledb
import os

DB_USER = "COMP214_W25_ers_72"
DB_PASSWORD = "password"
DB_CONNECT_STRING = "199.212.26.208:1521/SQLD"


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
