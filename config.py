import cx_Oracle
import os

cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_23_7\instantclient_23_7")

DB_USER = "COMP214_W25_ers_72"
DB_PASSWORD = "password"
DB_CONNECT_STRING = "199.212.26.208:1521/SQLD"



# Oracle DB Connection testing
def get_db_connection():
    try:
        connection = cx_Oracle.connect(DB_USER, DB_PASSWORD, DB_CONNECT_STRING)
        print(" Oracle DB Connection Successful")
        return connection
    except cx_Oracle.DatabaseError as e:
        print(" Oracle DB Connection Failed:", e)
        return None  # 연결 실패 시 None 반환

# Main
if __name__ == "__main__":
    get_db_connection()
