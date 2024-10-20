#データベースのテーブル定義するファイル


from sqlalchemy import Column, Integer, String, Float
from database import Base

# 商品テーブルのモデル定義
class Product(Base):
    __tablename__ = 'products'  # テーブル名を指定

    id = Column(Integer, primary_key=True, index=True)  # 主キー（商品ID）
    name = Column(String(100), nullable=False)  # 商品名
    price = Column(Float, nullable=False)  # 商品価格
