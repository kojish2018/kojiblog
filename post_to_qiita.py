import os
import requests
import glob

# 環境変数からアクセストークンを取得
QIITA_ACCESS_TOKEN = os.getenv("QIITA_ACCESS_TOKEN")
if not QIITA_ACCESS_TOKEN:
    raise ValueError("Qiita access token is not set in environment variables.")

QIITA_API_URL = "https://qiita.com/api/v2/items"

def post_to_qiita(file_path):
    """MarkdownファイルをQiitaに投稿する"""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    # 記事タイトルをファイル名から取得
    title = os.path.basename(file_path).replace(".md", "")
    
    # Qiita APIリクエストデータ
    headers = {"Authorization": f"Bearer {QIITA_ACCESS_TOKEN}"}
    data = {
        "title": title,
        "body": content,
        "tags": [{"name": "GitHub"}, {"name": "Qiita"}, {"name": "Automation"}],
        "private": False  # 公開記事
    }
    
    response = requests.post(QIITA_API_URL, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"Successfully posted: {title}")
        return True
    else:
        print(f"Failed to post {title}: {response.status_code} - {response.text}")
        return False

if __name__ == "__main__":
    # Markdownファイルを取得
    files = glob.glob("./articles/*.md")
    if not files:
        print("No Markdown files found in /articles.")
        exit(1)
    
    for file_path in files:
        post_to_qiita(file_path)
