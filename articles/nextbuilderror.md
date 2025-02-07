<!-- title: NextでbuildするとUnexpected end of JSON inputのエラーが出た -->
<!-- tags: Next, Typescript, Node -->

# Next.js プロジェクト開発備忘録

## エラー内容

`Unexpected end of JSON input` のエラー発生

### 状況

- **Local 環境:** 表示問題なし
- **API データ:** 確認済み、異常なし
- **ビルド時:** エラー発生

## 原因

どうやら **Node.js 23 系** で `build` すると発生するエラーの模様

## 解決策

Node.js のバージョンを **20.10.0** に変更

```
nvm install v20.10.0
nvm use v20.10.0
```

これでエラーは消えた
