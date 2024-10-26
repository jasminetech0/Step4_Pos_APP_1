#DATABASEと接続するファイル

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# .envから環境変数を読み込む
load_dotenv()

# 環境を判定（local または azure）
env = os.getenv("ENVIRONMENT", "local")

# SSL証明書のパスを取得（Azure環境でのみ使用）
ssl_ca_path = os.getenv("SSL_CA_PATH") if env == "azure" else None

# データベース接続URLを生成
if ssl_ca_path:
    # Azure環境（SSL証明書が必要）
    DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}?ssl_ca={ssl_ca_path}"
else:
    # ローカル環境
    DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}"

# SQLAlchemyのエンジンを作成
engine = create_engine(DATABASE_URL)

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラスの作成（モデル定義に使用）
Base = declarative_base()

# データベースセッションを取得するための依存関係
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
