from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from models import Product, Transaction, TransactionDetail
import datetime
from pydantic import BaseModel  # 追加部分
from fastapi.middleware.cors import CORSMiddleware  # 追加部分
from fastapi import FastAPI, File, UploadFile
from azure.storage.blob import BlobServiceClient
from uuid import uuid4
import os

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

# Azure Blob Storage 設定
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
CONTAINER_NAME = "jasmines"  # コンテナ名

# BlobServiceClient を初期化
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

# BLOB URL ベースを定義（blob_service_client 初期化後に配置）
BLOB_URL_BASE = f"https://{blob_service_client.account_name}.blob.core.windows.net/{CONTAINER_NAME}/"


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
    try:
        # ファイル名の一意性を確保
        unique_filename = f"{uuid4()}_{file.filename}"
        
        # Blob クライアントを取得
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=unique_filename)
        
        # ファイルをアップロード
        blob_client.upload_blob(file.file, overwrite=True)
        
        # アップロードしたファイルの URL を組み立て
        file_url = f"{BLOB_URL_BASE}{unique_filename}"
        
        return {"message": "ファイルが正常にアップロードされました", "file_url": file_url}
    except Exception as e:
        print(f"エラー: {str(e)}")
        return {"error": "ファイルアップロード中にエラーが発生しました"}