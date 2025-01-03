import requests
import json

QIITA_ACCESS_TOKEN = '3801321e439a0a623a2e0dab1b4bd767e08f5987'
QIITA_API_URL = 'https://qiita.com/api/v2/items'

def check_article_exists(article_id):
    # QIITA_ACCESS_TOKEN = '3801321e439a0a623a2e0dab1b4bd767e08f5987'
    # QIITA_API_URL = 'https://qiita.com/api/v2/items'
    headers = {"Authorization": f"Bearer {QIITA_ACCESS_TOKEN}"}
    response = requests.get(f"{QIITA_API_URL}/{article_id}", headers=headers)
    if response.status_code == 200:
        print(f"Article with ID {article_id} exists: {response.json()}")
    else:
        print(f"Article with ID {article_id} does not exist. Status: {response.status_code}, Response: {response.text}")

def update_article(article_id, headers, data):
    response = requests.put(f"{QIITA_API_URL}/{article_id}", headers=headers, json=data)
    print("Request URL:", f"{QIITA_API_URL}/{article_id}")
    print("Request Headers:", headers)
    print("Request Data:", json.dumps(data, ensure_ascii=False, indent=4))
    print("Response Status Code:", response.status_code)
    print("Response Body:", response.text)
    return response


# check_article_exists('0c881395eecffd03bea3')


import os
import requests

QIITA_ACCESS_TOKEN = os.getenv("QIITA_ACCESS_TOKEN")
if not QIITA_ACCESS_TOKEN:
    raise ValueError("Qiita access token is not set in environment variables.")

QIITA_API_URL = "https://qiita.com/api/v2/items"

def get_authenticated_user():
    """トークン所有者を確認"""
    headers = {"Authorization": f"Bearer {QIITA_ACCESS_TOKEN}"}
    response = requests.get("https://qiita.com/api/v2/authenticated_user", headers=headers)
    if response.status_code == 200:
        print("Authenticated user:", response.json())
    else:
        print(f"Failed to authenticate: {response.status_code}, {response.text}")

def fetch_article(article_id):
    """記事が存在するか確認"""
    headers = {"Authorization": f"Bearer {QIITA_ACCESS_TOKEN}"}
    response = requests.get(f"{QIITA_API_URL}/{article_id}", headers=headers)
    if response.status_code == 200:
        print("記事取得成功:", response.json())
    else:
        print(f"記事取得失敗: {response.status_code}, {response.text}")

def update_article(article_id, title, body, tags):
    """記事を更新する"""
    headers = {"Authorization": f"Bearer {QIITA_ACCESS_TOKEN}"}
    data = {
        "title": title,
        "body": body,
        "tags": [{"name": tag} for tag in tags],
        "private": False,
    }
    response = requests.put(f"{QIITA_API_URL}/{article_id}", headers=headers, json=data)
    if response.status_code in [200, 201]:
        print("記事更新成功:", response.json())
    else:
        print(f"記事更新失敗: {response.status_code}, {response.text}")

# if __name__ == "__main__":
#     # 1. トークン所有者確認
#     print("\n=== トークン所有者確認 ===")
#     get_authenticated_user()

#     # 2. 記事存在確認
#     print("\n=== 記事存在確認 ===")
#     article_id = "b676e1196adbc1df5b48"  # 記事ID
#     fetch_article(article_id)

#     # 3. 記事更新
#     print("\n=== 記事更新 ===")
#     update_article(
#         article_id,
#         "testtitle",
#         "testdescription",
#         ["qiita", "github", "automation"]
#     )


def patch_article(article_id, title=None, body=None, tags=None):
    """PATCHメソッドを使って記事を更新"""
    headers = {"Authorization": f"Bearer {QIITA_ACCESS_TOKEN}"}
    data = {}
    if title:
        data["title"] = title
    if body:
        data["body"] = body
    if tags:
        data["tags"] = [{"name": tag} for tag in tags]

    response = requests.patch(f"{QIITA_API_URL}/{article_id}", headers=headers, json=data)
    print("\n=== PATCHリクエスト詳細 ===")
    print("リクエストURL:", f"{QIITA_API_URL}/{article_id}")
    print("リクエストデータ:", json.dumps(data, indent=4, ensure_ascii=False))
    if response.status_code in [200, 201]:
        print("記事更新成功:", response.json())
    else:
        print(f"記事更新失敗: {response.status_code}, {response.text}")


if __name__ == "__main__":
    article_id = "0c881395eecffd03bea3"  # 更新する記事ID
    patch_article(
        article_id,
        title="PATCHテスト用記事",
        body="この記事はPATCHメソッドを使って更新されました。",
        tags=["qiita", "patch", "test"]
    )