import os  # OSモジュールをインポート（環境変数の操作に使用）
import mysql.connector  # MySQLデータベース接続用モジュールをインポート
from mysql.connector import errorcode  # MySQLエラーコードをインポート
from dotenv import load_dotenv  # .envファイルから環境変数を読み込むためのモジュールをインポート

# .envファイルをロード
load_dotenv()

# ポータルから接続文字列情報を取得
config = {
  'host': 'tech0-gen-7-step4-studentrdb-20.mysql.database.azure.com',  # データベースのホスト名
  'user': 'tech0gen7student',  # データベースのユーザー名
  'password': os.getenv('DB_PASSWORD'),  # 環境変数からパスワードを取得
  'database': 'legotest',  # 使用するデータベース名
  'client_flags': [mysql.connector.ClientFlag.SSL],  # SSL接続を使用するためのフラグ
  'ssl_ca': 'C:/Users/yuya.hosokawa/Downloads/DigiCertGlobalRootCA.crt.pem'  # SSL証明書ファイルのパス
}

# 接続文字列を構築
try:
   conn = mysql.connector.connect(**config)  # configを使用してデータベースに接続
   print("Connection established")  # 接続成功メッセージを表示
except mysql.connector.Error as err:  # 接続エラーが発生した場合の処理
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with the user name or password")  # ユーザー名またはパスワードが間違っている場合のメッセージ
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")  # データベースが存在しない場合のメッセージ
  else:
    print(err)  # その他のエラーメッセージを表示
else:
  cursor = conn.cursor()  # カーソルオブジェクトを作成

  # 既存のusersテーブルがあれば削除
  cursor.execute("DROP TABLE IF EXISTS users;")
  print("Finished dropping table (if existed).")

  # usernameとpasswordカラムを持つusersテーブルを作成
  cursor.execute("""
  CREATE TABLE users (
      id SERIAL PRIMARY KEY,
      username VARCHAR(50) NOT NULL,
      password VARCHAR(50) NOT NULL
  );
  """)
  print("Finished creating users table.")

  # usersディクショナリからデータを挿入
  users = {
      'yagimasa': 'password123',
      'lego': 'password456'
  }

  for username, password in users.items():  # usersディクショナリをループ処理
      cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s);", (username, password))  # ユーザーデータを挿入
      print(f"Inserted user: {username}")  # 挿入したユーザー名を表示

  # トランザクションをコミット
  conn.commit()

  # クリーンアップ
  cursor.close()  # カーソルを閉じる
  conn.close()  # データベース接続を閉じる
  print("Done.")  # 処理完了メッセージを表示
