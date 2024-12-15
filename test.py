from fastapi import FastAPI
import mysql.connector
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()  # 環境変数を読み込む

app = FastAPI()

# CORSの設定を追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可（開発中のみ）
    allow_credentials=True,
    allow_methods=["*"],  # すべてのHTTPメソッドを許可
    allow_headers=["*"],  # すべてのヘッダーを許可
)

# Azure Database for MySQL接続設定
db_config = {
    "host": os.getenv("DB_HOST"),  # Azureのホスト名
    "user": os.getenv("DB_USER"),  # ユーザー名
    "password": os.getenv("DB_PASS"),  # パスワード
    "database": os.getenv("DB_NAME"),  # データベース名
}

@app.get("/api/possessions")
def read_possessions():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM possession_list")
        results = cursor.fetchall()
        return {"data": results}
    except Exception as e:
        return {"error": str(e)}
    finally:
        cursor.close()
        conn.close()
