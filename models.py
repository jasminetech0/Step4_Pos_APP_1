#データベースのテーブル定義するファイル  仕様書p7　DBイメージ


from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import datetime

# 商品マスタのモデル
class Product(Base):
    __tablename__ = 'products'

    PRD_ID = Column(Integer, primary_key=True, index=True)  # 商品ID (主キー)
    CODE = Column(String(13), unique=True, nullable=False)  # 商品コード (char 13)
    NAME = Column(String(50), nullable=False)  # 商品名 (varchar 50)
    PRICE = Column(Integer, nullable=False)  # 商品単価

# 取引テーブルのモデル
class Transaction(Base):
    __tablename__ = 'transactions'

    TRD_ID = Column(Integer, primary_key=True, index=True)  # 取引ID (主キー)
    DATETIME = Column(DateTime, default=datetime.datetime.utcnow)  # 取引日時 (timestamp)
    EMP_CD = Column(String(10), nullable=False)  # レジ担当者コード (char 10)
    STORE_CD = Column(String(5), nullable=False)  # 店舗コード (char 5)
    POS_NO = Column(String(3), nullable=False)  # POS機ID (char 3)
    TOTAL_AMT = Column(Integer, nullable=False)  # 合計金額

    details = relationship("TransactionDetail", back_populates="transaction")  # 取引明細とのリレーション

# 取引明細テーブルのモデル
class TransactionDetail(Base):
    __tablename__ = 'transaction_details'

    DTL_ID = Column(Integer, primary_key=True, index=True)  # 取引明細ID (主キー)
    TRD_ID = Column(Integer, ForeignKey('transactions.TRD_ID'), primary_key=True)  # 取引ID（外部キー & 主キー）
    PRD_ID = Column(Integer, ForeignKey('products.PRD_ID'))  # 商品ID（外部キー）
    PRD_CODE = Column(String(13), nullable=False)  # 商品コード (char 13)
    PRD_NAME = Column(String(50), nullable=False)  # 商品名 (varchar 50)
    PRD_PRICE = Column(Integer, nullable=False)  # 商品単価

    transaction = relationship("Transaction", back_populates="details")  # 取引テーブルとのリレーション
    product = relationship("Product")  # 商品テーブルとのリレーション
