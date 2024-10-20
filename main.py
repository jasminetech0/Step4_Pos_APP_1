#FastAPIのエンドポイントを定義するファイル

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db  # SQLAlchemyのセッションを取得
from models import Product  # Productモデルをインポート

app = FastAPI()

# ルートエンドポイント
@app.get("/")
def read_root():
    return {"message": "POSアプリへようこそ！"}

# データベース接続確認用エンドポイント
@app.get("/test_connection")
def test_connection(db: Session = Depends(get_db)):  # SQLAlchemyのセッションを使用
    try:
        result = db.execute("SELECT DATABASE();")  # 生のSQLを実行
        db_name = result.fetchone()
        return {"message": f"データベース '{db_name[0]}' に接続できました"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="データベース接続に失敗しました")

# 商品検索エンドポイント
@app.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="商品が見つかりません")
    return product
