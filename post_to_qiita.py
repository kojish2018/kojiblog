import os
import requests
import glob
import re

QIITA_ACCESS_TOKEN = os.getenv("QIITA_ACCESS_TOKEN")
if not QIITA_ACCESS_TOKEN:
    raise ValueError("Qiita access token is not set in environment variables.")

QIITA_API_URL = "https://qiita.com/api/v2/items"

def extract_metadata(content, key):
    """Markdownコンテンツから特定のメタデータを抽出"""
    match = re.search(rf"<!--\s*{key}:\s*(.+?)\s*-->", content)
    return match.group(1) if match else None

def update_metadata(file_path, key, value):
    """Markdownファイルにメタデータを埋め込む"""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.readlines()
    
    # メタデータが既存の場合は更新
    updated = False
    for i, line in enumerate(content):
        if line.strip().startswith(f"<!-- {key}:"):
            content[i] = f"<!-- {key}: {value} -->\n"
            updated = True
            break

    # 存在しない場合は先頭に追加
    if not updated:
        content.insert(0, f"<!-- {key}: {value} -->\n")

    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(content)

def post_or_update_qiita(file_path):
    """Qiita記事を投稿または更新"""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    
    # メタデータの取得
    article_id = extract_metadata(content, "id")
    title = extract_metadata(content, "title")
    if not title:
        title = os.path.basename(file_path).replace(".md", "")

    # リクエスト共通部分
    headers = {"Authorization": f"Bearer {QIITA_ACCESS_TOKEN}"}
    data = {
        "title": title,
        "body": content,
        "tags": [{"name": "GitHub"}, {"name": "Qiita"}, {"name": "Automation"}],
        "private": False  # 公開記事
    }

    # 投稿または更新
    if article_id:
        # 更新
        response = requests.put(f"{QIITA_API_URL}/{article_id}", headers=headers, json=data)
    else:
        # 投稿
        response = requests.post(QIITA_API_URL, headers=headers, json=data)
    
    # 結果を確認
    if response.status_code in [200, 201]:
        result = response.json()
        print(f"Successfully processed: {title}")
        # 記事IDを保存
        if not article_id:
            update_metadata(file_path, "id", result["id"])
    else:
        print(f"Failed to process {title}: {response.status_code} - {response.text}")

if __name__ == "__main__":
    # Markdownファイルを取得
    files = glob.glob("./articles/*.md")
    if not files:
        print("No Markdown files found in /articles.")
        exit(1)
    
    for file_path in files:
        post_or_update_qiita(file_path)
