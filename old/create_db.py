#空のテーブルを作成するファイル

from database import engine
from models import Base

# テーブル作成関数
def create_tables():
    Base.metadata.create_all(bind=engine)
    print("テーブルが作成されました")

if __name__ == "__main__":
    create_tables()  # テーブルを作成
