from fastapi import FastAPI
from database import get_db_connection  # database.py から接続関数をインポート

app = FastAPI()

# ルートエンドポイント
@app.get("/")
def read_root():
    return {"message": "POSアプリへようこそ！"}

# データベース接続確認用エンドポイント
@app.get("/test_connection")
def test_connection():
    connection = get_db_connection()
    if connection:
        return {"message": "データベースに接続できました"}
    else:
        return {"error": "データベース接続に失敗しました"}
