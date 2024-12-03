from pymysql import connect
from app.utils.config import Config

def get_db_connection():
    return connect(
        host=Config.DB_HOST,
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME,
    )

def execute_query(conn, query, args=None):
    with conn.cursor() as cursor:
        cursor.execute(query, args)
        conn.commit()
