#空のテーブルにデータを入れるファイル


from database import SessionLocal
from models import Product

# データベースセッションを作成
db = SessionLocal()

# サンプル商品データ
products = [
    Product(PRD_ID=1, CODE="P000000000001", NAME="コーヒー", PRICE=300),
    Product(PRD_ID=2, CODE="P000000000002", NAME="サンドイッチ", PRICE=500),
    Product(PRD_ID=3, CODE="P000000000003", NAME="サラダ", PRICE=450),
    Product(PRD_ID=4, CODE="P000000000004", NAME="ケーキ", PRICE=400),
    Product(PRD_ID=5, CODE="P000000000005", NAME="お茶", PRICE=250),
]

# 商品データをデータベースに挿入
db.add_all(products)  # 複数のデータを一括で追加
db.commit()  # コミットして保存
db.close()  # セッションを閉じる

print("サンプルデータがデータベースに挿入されました")
