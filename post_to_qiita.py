import os
import requests
import json
import glob
import re
import boto3

# Qiita APIの設定
QIITA_ACCESS_TOKEN = os.getenv("QIITA_ACCESS_TOKEN")
if not QIITA_ACCESS_TOKEN:
    raise ValueError("Qiita access token is not set in environment variables.")
QIITA_API_URL = "https://qiita.com/api/v2/items"

def load_config_from_s3(bucket_name, object_key):
    """S3からconfig.jsonを読み込む"""
    print('s3読み込み')
    s3 = boto3.client('s3')
    try:
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        content = response['Body'].read().decode('utf-8')
        return json.loads(content)
    except Exception as e:
        print(f"Error loading config from S3: {e}")
        return {}

def save_config_to_s3(config, bucket_name, object_key):
    """S3にconfig.jsonを保存する"""
    print('s3書き込み')
    s3 = boto3.client('s3')
    try:
        content = json.dumps(config, ensure_ascii=False, indent=4)
        s3.put_object(Bucket=bucket_name, Key=object_key, Body=content.encode('utf-8'))
    except Exception as e:
        print(f"Error saving config to S3: {e}")

def load_config():
    """S3からconfig.jsonを読み込む"""
    bucket_name = 'kojiblog'
    object_key = 'config.json'
    return load_config_from_s3(bucket_name, object_key)

def save_config(config):
    """S3にconfig.jsonを保存する"""
    bucket_name = 'kojiblog'
    object_key = 'config.json'
    save_config_to_s3(config, bucket_name, object_key)

def extract_title_from_content(content):
    """Markdownファイルの内容からタイトルを抽出"""
    match = re.search(r"<!--\s*title:\s*(.+?)\s*-->", content)
    if match:
        return match.group(1).strip()
    else:
        raise ValueError("Markdownファイル内に<!-- title: タイトル名 -->が見つかりません。")

def extract_tags_from_content(content):
    """Markdownファイルの内容からタグを抽出"""
    match = re.search(r"<!--\s*tags:\s*(.+?)\s*-->", content)
    if match:
        tags = [tag.strip() for tag in match.group(1).split(",")]
        return [{"name": tag} for tag in tags if tag]
    return []

def post_or_update_qiita(file_path, config):
    """Qiita記事を投稿または更新"""
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Markdownファイル内のタイトルとタグを抽出
    try:
        title = extract_title_from_content(content)
        tags = extract_tags_from_content(content)
    except ValueError as e:
        print(f"Error in file {file_path}: {e}")
        return

    # デフォルトタグ（タグがなかった場合の対策）
    if not tags:
        tags = [{"name": "botter"}, {"name": "仮想通貨"}, {"name": "機械学習"}]

    # config.jsonから記事IDを取得
    article_id = config.get(file_path)

    # リクエスト共通部分
    headers = {"Authorization": f"Bearer {QIITA_ACCESS_TOKEN}"}
    data = {
        "title": title,
        "body": content,
        "tags": tags,
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
