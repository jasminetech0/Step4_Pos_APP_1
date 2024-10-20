#空のテーブルにデータを入れるファイル


from database import SessionLocal
from models import Product

# データベースセッションを作成
db = SessionLocal()

# サンプル商品データ
products = [
    Product(id=1, name="コーヒー", price=300),
    Product(id=2, name="サンドイッチ", price=500),
    Product(id=3, name="サラダ", price=450),
    Product(id=4, name="ケーキ", price=400),
    Product(id=5, name="お茶", price=250),
]

# 商品データをデータベースに追加
db.add_all(products)  # サンプルデータを一括で挿入
db.commit()  # コミットして保存
db.close()  # セッションを閉じる

print("サンプルデータがデータベースに挿入されました")

