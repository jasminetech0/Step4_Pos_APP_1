import os
from fastapi import FastAPI
import mysql.connector
from mysql.connector import Error

app = FastAPI()

# 環境変数からMySQL接続情報を取得
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),  # ホスト名
            user=os.getenv("MYSQL_USER"),  # ユーザー名
            password=os.getenv("MYSQL_PASSWORD"),  # パスワード
            database=os.getenv("MYSQL_DATABASE")  # データベース名
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# ルートエンドポイント
@app.get("/")
def read_root():
    return {"message": "POSアプリへようこそ！"}

# データベースから製品情報を取得するエンドポイント（/products）
@app.get("/products")
def get_products_from_db():
    # MySQLデータベースに接続
    connection = get_db_connection()
    if connection is None:
        return {"error": "データベースに接続できませんでした"}

    try:
        # クエリを実行して製品情報を取得
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM products")  # ここで実際のテーブル名を使用してください
        products = cursor.fetchall()

        # 結果を返す
        return {"products": products}

    except Error as e:
        return {"error": str(e)}

    finally:
        # カーソルと接続を閉じる
        if cursor:
            cursor.close()
        if connection:
            connection.close()
