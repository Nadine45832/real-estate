import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))
from config import get_db_connection


conn = get_db_connection()
if conn:
    print("✅ DB 연결 성공!")
    conn.close()  # 연결 닫기
else:
    print("❌ DB 연결 실패!")
