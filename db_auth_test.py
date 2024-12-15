import os  # OSモジュールをインポート（環境変数の操作に使用）
import mysql.connector  # MySQLデータベース接続用モジュールをインポート
from mysql.connector import errorcode  # MySQLエラーコードをインポート
from dotenv import load_dotenv  # .envファイルから環境変数を読み込むためのモジュールをインポート

# .envファイルをロード
load_dotenv()

# データベース接続情報の設定
config = {
    'host': 'tech0-gen-7-step4-studentwebapp-test.mysql.database.azure.com',  # データベースのホスト名
    'user': 'tech0gen7student',  # データベースのユーザー名
    'password': os.getenv('DB_PASSWORD'),  # 環境変数からパスワードを取得
    'database': 'legotest',  # 使用するデータベース名
    'client_flags': [mysql.connector.ClientFlag.SSL],  # SSL接続を使用するためのフラグ
    'ssl_ca': 'DigiCertGlobalRootCA.crt.pem'  # SSL証明書ファイルのパス
}

# データベース接続を取得
try:
    conn = mysql.connector.connect(**config)  # configを使用してデータベースに接続
    print("Connection established")  # 接続成功メッセージを表示
    
    cursor = conn.cursor()  # カーソルオブジェクトを作成
    
    # データベース内のユーザー情報を取得するSQLクエリ
    query = "SELECT username, password FROM users;"  # usersテーブルからユーザー名とパスワードを選択
    cursor.execute(query)  # クエリを実行
    
    # データを取得し、ディクショナリ形式で保存
    users = {username: password for username, password in cursor.fetchall()}
    
    # テスト用の入力データ
    input_username = "lego"  # テスト用のユーザー名
    input_password = "password456"  # テスト用のパスワード
    
    # 認証チェック
    if input_username in users and users[input_username] == input_password:
        print(f"ようこそ！{input_username}さん")  # 認証成功メッセージ
    else:
        print("認証失敗")  # 認証失敗メッセージ

    # 接続を閉じる
    cursor.close()  # カーソルを閉じる
    conn.close()  # データベース接続を閉じる

except mysql.connector.Error as err:  # MySQLエラーが発生した場合の処理
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("ユーザー名またはパスワードに誤りがあります")  # アクセス拒否エラーの場合のメッセージ
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("データベースが存在しません")  # データベースが存在しない場合のメッセージ
    else:
        print(err)  # その他のエラーメッセージを表示
