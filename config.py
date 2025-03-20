import cx_Oracle
import os

# Oracle Instant Client 경로 명시적 지정 (네가 기존에 사용한 경로 유지)
cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_23_7\instantclient_23_7")

# 데이터베이스 연결 정보
DB_USER = "COMP214_W25_ers_72"
DB_PASSWORD = "password"  # 보안을 위해 환경 변수 사용 권장
DB_CONNECT_STRING = "199.212.26.208:1521/SQLD"

# SQLAlchemy Connection
SQLALCHEMY_DATABASE_URI = f"oracle+cx_oracle://{DB_USER}:{DB_PASSWORD}@{DB_CONNECT_STRING}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Oracle DB Connection testing
def test_db_connection():
    try:
        connection = cx_Oracle.connect(DB_USER, DB_PASSWORD, DB_CONNECT_STRING)
        cursor = connection.cursor()
        cursor.execute("SELECT SYSDATE FROM DUAL")
        result = cursor.fetchone()
        print(" Oracle DB Connected Successfully: Current Time ->", result[0])
        cursor.close()
        connection.close()
    except cx_Oracle.DatabaseError as e:
        print(" Oracle DB Connection Failed:", e)

# Main
if __name__ == "__main__":
    test_db_connection()
