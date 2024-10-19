import os
from dotenv import load_dotenv  # dotenvのインポート
import mysql.connector
from mysql.connector import Error

# .envファイルを読み込む
load_dotenv()  # 追加

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),  # .envから環境変数を取得
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            ssl_ca="certs/BaltimoreCyberTrustRoot.crt.pem",  # SSL証明書
            ssl_verify_cert=True
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")  # エラー内容を表示
        return None


print(f"Host: {os.getenv('MYSQL_HOST')}")
print(f"User: {os.getenv('MYSQL_USER')}")
print(f"Password: {os.getenv('MYSQL_PASSWORD')}")
print(f"Database: {os.getenv('MYSQL_DATABASE')}")
