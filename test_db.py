# MYSQLサーバーからデータを取ってくるテストをするファイル

from sqlalchemy.orm import Session
from database import get_db  # Database.pyからget_db関数をインポート
from models import Product, Transaction, TransactionDetail  # models.pyからモデルをインポート

# 商品データを取得する関数
def get_products(db: Session):
    return db.query(Product).all()

# 取引データとその明細を取得する関数
def get_transactions_with_details(db: Session):
    return db.query(Transaction).all()

if __name__ == "__main__":
    # データベースセッションを取得
    db = next(get_db())

    # 商品マスタから全ての商品を取得
    print("== 商品一覧 ==")
    products = get_products(db)
    for product in products:
        print(f"商品ID: {product.PRD_ID}, 商品名: {product.NAME}, 価格: {product.PRICE}")

    # 取引と取引明細を取得
    print("\n== 取引と取引明細一覧 ==")
    transactions = get_transactions_with_details(db)
    for transaction in transactions:
        print(f"取引ID: {transaction.TRD_ID}, 日時: {transaction.DATETIME}, 合計金額: {transaction.TOTAL_AMT}")
        for detail in transaction.details:
            print(f"  明細ID: {detail.DTL_ID}, 商品コード: {detail.PRD_CODE}, 商品名: {detail.PRD_NAME}, 価格: {detail.PRD_PRICE}")
