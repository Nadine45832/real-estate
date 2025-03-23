from backend.config import get_db_connection


conn = get_db_connection()
if conn:
    print("✅ DB 연결 성공!")
    conn.close()  # 연결 닫기
else:
    print("❌ DB 연결 실패!")
