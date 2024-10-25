#FastAPIのエンドポイントを定義するファイル

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Product, Transaction, TransactionDetail  # 追加部分
import datetime  # 追加部分
from fastapi.middleware.cors import CORSMiddleware  # 追加

app = FastAPI()

# CORSの設定を追加
origins = [
    "tech0-gen-7-step4-studentwebapp-pos-test-1-b0dkdqd4eygxfrdn.eastasia-01.azurewebsites.net",  # Next.js サーバーのURL
    "http://localhost:3000",  # ローカル開発環境のNext.js URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ルートエンドポイント
@app.get("/")
def read_root():
    return {"message": "POSアプリへようこそ！"}

# データベース接続確認用エンドポイント
@app.get("/test_connection")
def test_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute("SELECT DATABASE();")  # 生のSQLを実行
        db_name = result.fetchone()
        return {"message": f"データベース '{db_name[0]}' に接続できました"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="データベース接続に失敗しました")

# 商品検索エンドポイント
@app.get("/products/{code}")
def search_product(code: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.CODE == code).first()
    if product is None:
        return None  # 対象が見つからない場合は NULL を返す
    return {
        "PRD_ID": product.PRD_ID,
        "CODE": product.CODE,
        "NAME": product.NAME,
        "PRICE": product.PRICE
    }

# 購入処理API (追加部分)
@app.post("/purchase/")
def make_purchase(items: list[dict], cashier_code: str, db: Session = Depends(get_db)):
    # 合計金額の変数
    total_amount = 0

    # 店舗コードとPOS機IDは固定
    store_code = "30"
    pos_no = "90"

    # レジ担当者コードが空の場合、デフォルト値を設定
    if not cashier_code:
        cashier_code = "9999999999"

    # 取引を作成
    transaction = Transaction(
        DATETIME=datetime.datetime.utcnow(),
        EMP_CD=cashier_code,
        STORE_CD=store_code,
        POS_NO=pos_no,
        TOTAL_AMT=0  # 最初は0で保存し、後で更新
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)  # 取引IDを取得するためにリフレッシュ

    # 取引明細を追加
    for item in items:
        product = db.query(Product).filter(Product.PRD_ID == item["PRD_ID"]).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"商品ID {item['PRD_ID']} が見つかりません")

        # 合計金額を計算（数量に基づく計算）
        total_amount += product.PRICE * item["quantity"]  # 商品価格 × 購入数量

        # 取引明細を作成
        detail = TransactionDetail(
            TRD_ID=transaction.TRD_ID,
            PRD_ID=product.PRD_ID,
            PRD_CODE=product.CODE,
            PRD_NAME=product.NAME,
            PRD_PRICE=product.PRICE,
            # ここで quantity を保存する場合、別途カラムをテーブルに追加する必要があります
        )
        db.add(detail)

    # 合計金額を取引に更新
    transaction.TOTAL_AMT = total_amount
    db.commit()

    return {"success": True, "total_amount": total_amount}
