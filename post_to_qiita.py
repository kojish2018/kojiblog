import os
import requests
import glob
import re

QIITA_ACCESS_TOKEN = os.getenv("QIITA_ACCESS_TOKEN")
if not QIITA_ACCESS_TOKEN:
    raise ValueError("Qiita access token is not set in environment variables.")

QIITA_API_URL = "https://qiita.com/api/v2/items"

def extract_title_and_body(file_path):
    """Markdownファイルからタイトルと本文を抽出"""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # YAMLフロントマターからタイトルを抽出
    match = re.search(r"^---\ntitle: (.+)\n---\n", content)
    if match:
        title = match.group(1)
        body = content[match.end():].strip()  # タイトル以外の部分を本文とする
    else:
        # タイトルが明示されていない場合は、ファイル名をタイトルにする
        title = os.path.basename(file_path).replace(".md", "")
        body = content

    return title, body

def post_to_qiita(file_path):
    """MarkdownファイルをQiitaに投稿する"""
    title, body = extract_title_and_body(file_path)

    # Qiita APIリクエストデータ
    headers = {"Authorization": f"Bearer {QIITA_ACCESS_TOKEN}"}
    data = {
        "title": title,
        "body": body,
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
