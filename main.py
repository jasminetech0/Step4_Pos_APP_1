from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from models import Product, Transaction, TransactionDetail
import datetime
from pydantic import BaseModel  # 追加部分
from fastapi.middleware.cors import CORSMiddleware  # 追加部分
import mysql.connector
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = FastAPI()

# CORSの設定を追加
origins = [
    "https://tech0-gen-7-step4-studentwebapp-pos-39-cnb9heehgfc0ajbm.eastus-01.azurewebsites.net",  # Next.js サーバーのURL
    "http://localhost:3000",  # ローカル開発環境のNext.js URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Azure Database for MySQL接続設定
db_config = {
    "host": os.getenv("DB_HOST"),  # Azureのホスト名
    "user": os.getenv("DB_USER"),  # ユーザー名
    "password": os.getenv("DB_PASS"),  # パスワード
    "database": os.getenv("DB_NAME"),  # データベース名
}


# Pydanticモデルで入力データを定義
class PossessionItem(BaseModel):
    product_name: str
    possession_count: int
    expire_date: str  # YYYY-MM-DD形式
    category: str

@app.post("/api/possessions")
def add_possession(item: PossessionItem):
    print("受信データ:", item)
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # SQLクエリ
        sql = """
        INSERT INTO possession_list (Customer_ID, Product_Name, Possession_count, Expire_Date, Category)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (1, item.product_name, item.possession_count, item.expire_date, item.category)  # Customer_IDは固定値1

        cursor.execute(sql, values)
        conn.commit()

        return {"message": "Item added successfully", "id": cursor.lastrowid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.get("/api/possessions")
def get_possessions():
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # データベースからデータを取得
        cursor.execute("SELECT * FROM possession_list")
        results = cursor.fetchall()

        return {"data": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@app.put("/api/possessions/{possession_id}")
def update_possession(possession_id: int, item: PossessionItem):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # SQLクエリ: データを更新
        sql = """
        UPDATE possession_list
        SET Product_Name=%s, Possession_count=%s, Expire_Date=%s, Category=%s
        WHERE Possession_List_ID=%s
        """
        values = (item.product_name, item.possession_count, item.expire_date, item.category, possession_id)

        cursor.execute(sql, values)
        conn.commit()

        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="対象の備蓄品が見つかりません")

        return {"message": "更新が成功しました"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conn.close()


# Yahoo APIの設定
YAHOO_API_URL = "https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch"
YAHOO_APP_ID = os.getenv("YAHOO_APP_ID")

# 商品検索エンドポイント
@app.get("/api/search-product")
def search_product(jan_code: str):
    params = {
        "appid": YAHOO_APP_ID,
        "query": jan_code,
        "hits": 1,  # 最初の1件のみ取得
    }

    try:
        response = requests.get(YAHOO_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # レスポンスデータの確認
        if "hits" not in data or not data["hits"]:
            raise HTTPException(status_code=404, detail="商品が見つかりません")

        # 商品名を抽出
        product_name = data["hits"][0]["name"]

        return {"product_name": product_name}

    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Yahoo API呼び出しエラー: {str(e)}")

# デバッグ用
@app.get("/api/debug-yahoo-api")
def debug_yahoo_api(jan_code: str):
    yahoo_api_url = "https://shopping.yahooapis.jp/ShoppingWebService/V3/itemSearch"
    appid = "YOUR_YAHOO_APP_ID"

    params = {
        "appid": appid,
        "query": jan_code,
        "hits": 1
    }

    try:
        response = requests.get(yahoo_api_url, params=params)
        response.raise_for_status()
        return response.json()  # Yahoo APIのレスポンスをそのまま返す
    except Exception as e:
        return {"error": str(e)}

# こっからジョーカーズ作成
# データモデル (必要に応じて拡張可能)
class StockpileInfo(BaseModel):
    jan_code: str
    name: str = None

# 4902181102480に対応する商品情報
dummy_data = {
    "4902181102480": "やわらかいかくんせい"
}

# ルートエンドポイント
@app.get("/")
def read_root():
    return {"message": "POSアプリへようこそ！"}

# データベース接続確認用エンドポイント
@app.get("/test_connection")
def test_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT DATABASE();"))
        db_name = result.fetchone()
        return {"message": f"データベース '{db_name[0]}' に接続できました"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"データベース接続に失敗しました: {str(e)}")

# 商品検索エンドポイント
@app.get("/products/{code}")
def search_product(code: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.CODE == code).first()
    if product is None:
        return None
    return {
        "PRD_ID": product.PRD_ID,
        "CODE": product.CODE,
        "NAME": product.NAME,
        "PRICE": product.PRICE
    }

# 購入処理API
@app.post("/purchase/")
def make_purchase(items: list[dict], cashier_code: str, db: Session = Depends(get_db)):
    total_amount = 0
    store_code = "30"
    pos_no = "90"

    if not cashier_code:
        cashier_code = "9999999999"

    transaction = Transaction(
        DATETIME=datetime.datetime.utcnow(),
        EMP_CD=cashier_code,
        STORE_CD=store_code,
        POS_NO=pos_no,
        TOTAL_AMT=0
    )
    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    for item in items:
        product = db.query(Product).filter(Product.PRD_ID == item["PRD_ID"]).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"商品ID {item['PRD_ID']} が見つかりません")
        total_amount += product.PRICE * item["quantity"]
        detail = TransactionDetail(
            TRD_ID=transaction.TRD_ID,
            PRD_ID=product.PRD_ID,
            PRD_CODE=product.CODE,
            PRD_NAME=product.NAME,
            PRD_PRICE=product.PRICE,
        )
        db.add(detail)

    transaction.TOTAL_AMT = total_amount
    db.commit()

    return {"success": True, "total_amount": total_amount}

# 備蓄品のエンドポイント (追加部分)
@app.get("/ReadStockpileInfo/")
async def read_stockpile_info(jan_code: str):
    if jan_code in dummy_data:
        return {"jan_code": jan_code, "name": dummy_data[jan_code]}
    else:
        raise HTTPException(status_code=404, detail="商品が見つかりません")

@app.post("/PostStockpileInfo/")
async def post_stockpile_info(info: StockpileInfo):
    print("OK")
    return {"message": "OK"}

@app.put("/PutStockpileInfo/")
async def put_stockpile_info(info: StockpileInfo):
    print("OK")
    return {"message": "OK"}

@app.get("/GetStockpilePoint/")
async def get_stockpile_point(user_id: int):
    print("OK")
    return {"message": "OK"}

@app.post("/PostStockpileImage/")
async def post_stockpile_image(file: UploadFile = File(...)):
    print(f"Received file: {file.filename}")
    return {"message": "OK"}
