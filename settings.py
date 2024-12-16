import os
from dotenv import load_dotenv

# .envファイルの内容を環境変数として読み込む
load_dotenv()

# 環境変数の取得
API_BASE_URL = os.getenv("API_BASE_URL")
API_APP_ID = os.getenv("API_APP_ID")

# デバッグ確認
print(f"API_BASE_URL: {API_BASE_URL}")
print(f"API_APP_ID: {API_APP_ID}")
