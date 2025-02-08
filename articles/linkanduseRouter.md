<!-- title: Next.jsでページ遷移を実装する際、LinkコンポーネントとuseRouterフックのどちらを使うべきか -->
<!-- tags: Next, React, Typescript -->

# Next.js のページ遷移：`<Link>` vs `useRouter`

Next.js でのページ遷移には、`<Link>`コンポーネントと`useRouter`フックの 2 つの方法がある。それぞれの特徴や使い方を理解し、適切に使い分けることで、効率的なナビゲーションを実現できる。

## `<Link>`コンポーネントとは？

`<Link>`は、Next.js が提供する組み込みのコンポーネントで、HTML の`<a>`タグを拡張し、クライアントサイドのナビゲーションやプリフェッチ（事前読み込み）などの機能を提供する。主に静的なリンクを作成する際に使用される。

### 使用例

```jsx
import Link from "next/link";

export default function Home() {
  return (
    <div>
      <Link href="/about">About Us</Link>
    </div>
  );
}
```

このコードでは、`/about`ページへのリンクが作成され、クリックするとクライアントサイドでのページ遷移が行われる。また、`<Link>`はデフォルトでリンク先のページを事前に読み込む（プリフェッチ）ため、ユーザー体験の向上が期待できる。

## `useRouter`フックとは？

`useRouter`は、Next.js のルーター機能にアクセスするための React フックで、プログラム的にルートを変更したり、現在のルート情報を取得したりするのに使用される。主に動的なナビゲーションやユーザーのアクションに応じたページ遷移を実現する際に便利。

### 使用例

```jsx
"use client";

import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter();

  const goToAbout = () => {
    router.push("/about");
  };

  return (
    <div>
      <button onClick={goToAbout}>Go to About Us</button>
    </div>
  );
}
```

このコードでは、ボタンをクリックすると`/about`ページに遷移する。`useRouter`を使うことで、ユーザーのアクションに応じて動的にルートを変更できる。

## どちらを使うべきか？

### `<Link>`を使うべき場合

- **静的なリンク**：ナビゲーションメニューや記事一覧など、固定のリンクを表示する場合。
- **SEO 対策**：`<Link>`は内部的に`<a>`タグを生成するため、検索エンジンがリンクを正しく認識する。

### `useRouter`を使うべき場合

- **動的なナビゲーション**：フォーム送信後や特定の条件に応じてページ遷移させたい場合。
- **プログラム的な制御**：ユーザーのアクションやイベントに応じてルートを変更したい場合。

基本的には、**静的なリンクには`<Link>`、動的なナビゲーションには`useRouter`**を使うのが良い。状況に応じて使い分けることで、コードの可読性やメンテナンス性が向上する。

## まとめ

Next.js でのページ遷移には、`<Link>`コンポーネントと`useRouter`フックの 2 つの方法がある。それぞれの特徴を理解し、適切に使い分けることで、より効率的でユーザーフレンドリーなアプリケーションを構築できる。
