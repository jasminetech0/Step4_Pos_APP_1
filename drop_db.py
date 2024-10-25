from database import engine
from models import Base

# テーブルを削除する関数
def drop_tables():
    Base.metadata.drop_all(bind=engine)
    print("テーブルが削除されました")

if __name__ == "__main__":
    drop_tables()  # テーブルを削除
