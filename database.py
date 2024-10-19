import os
from dotenv import load_dotenv  # dotenvのインポート
import mysql.connector
from mysql.connector import Error
import logging

# ロギング設定
logging.basicConfig(level=logging.ERROR)

# .envファイルを読み込む
load_dotenv()

def get_db_connection():
    try:
        # MySQLサーバーにSSLで接続
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),  # .envから環境変数を取得
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE"),
            client_flags=[mysql.connector.ClientFlag.SSL],  # SSLを有効にする
            ssl_ca="C:/Users/jiebing/Desktop/Pos_APP_Backend/certs/DigiCertGlobalRootG2.crt.pem",
        )
        if connection.is_connected():
            print("MySQLにSSL接続しました")
        return connection
    except Error as e:
        logging.error(f"Error connecting to MySQL: {e}")  # エラー内容をロギング
        return None

# データベース接続のテスト
connection = get_db_connection()

if connection:
    # 接続に成功した場合の処理
    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE();")  # 現在のデータベースを確認
    db = cursor.fetchone()
    print(f"現在のデータベース: {db[0]}")

    # 接続を閉じる
    connection.close()
    print("MySQL接続を閉じました")

# デバッグ情報の表示
if os.getenv('DEBUG') == 'True':
    print(f"Host: {os.getenv('MYSQL_HOST')}")
    print(f"User: {os.getenv('MYSQL_USER')}")
    print(f"Password: {os.getenv('MYSQL_PASSWORD')}")
    print(f"Database: {os.getenv('MYSQL_DATABASE')}")
else:
    print("デバッグ情報は表示されません")
