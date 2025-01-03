import os
import requests
import json
import glob

# Qiita APIの設定
QIITA_ACCESS_TOKEN = os.getenv("QIITA_ACCESS_TOKEN")
if not QIITA_ACCESS_TOKEN:
    raise ValueError("Qiita access token is not set in environment variables.")
QIITA_API_URL = "https://qiita.com/api/v2/items"

# Configファイルのパス
CONFIG_FILE = "config.json"


def load_config():
    """config.jsonを読み込む"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}


def save_config(config):
    """config.jsonに保存する"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=4)


def post_or_update_qiita(file_path, config):
    """Qiita記事を投稿または更新"""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # 記事タイトルをファイル名から取得
    title = os.path.basename(file_path).replace(".md", "")

    # config.jsonから記事IDを取得
    article_id = config.get(file_path)

    # リクエスト共通部分
    headers = {"Authorization": f"Bearer {QIITA_ACCESS_TOKEN}"}
    data = {
        "title": title,
        "body": content,
        "tags": [{"name": "GitHub"}, {"name": "Qiita"}, {"name": "Automation"}],
        "private": False,  # 公開記事
    }

    if article_id:
        # 更新リクエストをPATCHに変更
        print(f"Attempting to update article: {title} with ID: {article_id}")
        response = requests.patch(f"{QIITA_API_URL}/{article_id}", headers=headers, json=data)

        if response.status_code in [200, 201]:
            print(f"Successfully updated article: {title}")
            return
        elif response.status_code == 404:
            print(f"Article with ID {article_id} not found. Switching to new post.")
            article_id = None  # 新規投稿に切り替え
        else:
            print(f"Failed to update article: {response.status_code} - {response.text}")
            return

    # 新規投稿リクエスト（記事IDがない場合）
    if not article_id:
        print(f"Attempting to create a new article: {title}")
        response = requests.post(QIITA_API_URL, headers=headers, json=data)

        if response.status_code == 201:
            result = response.json()
            new_id = result["id"]
            print(f"Successfully created a new article: {title} with ID: {new_id}")
            # 新しいIDをconfigに保存
            config[file_path] = new_id
            save_config(config)
        else:
            print(f"Failed to create a new article: {response.status_code} - {response.text}")


if __name__ == "__main__":
    # Configファイルを読み込み
    config = load_config()

    # Markdownファイルを取得
    files = glob.glob("./articles/*.md")
    if not files:
        print("No Markdown files found in /articles.")
        exit(1)

    # 各Markdownファイルについて投稿または更新
    for file_path in files:
        post_or_update_qiita(file_path, config)
