import mysql.connector
from mysql.connector import Error
import os

# データベース接続の共通関数
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),  # AzureのMySQLホスト名
            user=os.getenv("MYSQL_USER"),  # AzureのMySQLユーザー名
            password=os.getenv("MYSQL_PASSWORD"),  # AzureのMySQLパスワード
            database=os.getenv("MYSQL_DATABASE")  # データベース名
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None
