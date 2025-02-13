<!-- title: SSR、SSG、ISR、CSRの記法 -->
<!-- tags: Next, React, Rendering -->

個人で SSG を、社内システムで SSR を使ったが、備忘録としてそれぞれ 4 つの記法とメリット・デメリットを記しておきます。

# Next.js のレンダリング手法の比較と実装方法

Next.js では、ページのレンダリング手法として **SSR（Server-Side Rendering）**、**SSG（Static Site Generation）**、**ISR（Incremental Static Regeneration）**、**CSR（Client-Side Rendering）** の 4 つが提供されています。これらの手法は、データ取得のタイミングやレンダリングの場所が異なり、アプリケーションのパフォーマンスやユーザー体験に大きく影響します。

## 1. SSR（Server-Side Rendering）

**特徴**:

- **データ取得タイミング**: ユーザーからのリクエストごとにサーバー側でデータを取得し、HTML を生成します。
- **レンダリング場所**: サーバー側。

**メリット**:

- 常に最新のデータを表示できます。
- サーバーでレンダリングされた HTML を返すため、SEO に適しています。

**デメリット**:

- リクエストごとにサーバーで HTML を生成するため、サーバー負荷が高くなります。
- ユーザーのリクエストに対してサーバーで処理を行うため、応答速度がネットワーク状況やサーバー性能に依存します。

**適したアプリケーション要件**:

- ユーザーごとに異なるデータを表示する必要があるダッシュボードやユーザープロフィールページ。
- 頻繁に更新されるデータを表示するニュースサイトやブログ。

**実装方法**:

`getServerSideProps` 関数を使用して、リクエストごとにデータを取得します。

**コード例**:

```javascript
// pages/ssr-example.js
export async function getServerSideProps() {
  const res = await fetch("https://api.example.com/data");
  const data = await res.json();
  return { props: { data } };
}

function SSRExample({ data }) {
  return (
    <div>
      <h1>SSR Example</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

export default SSRExample;
```

このコードでは、ユーザーのリクエストごとに `getServerSideProps` が実行され、最新のデータが取得されます。

## 2. SSG（Static Site Generation）

**特徴**:

- **データ取得タイミング**: ビルド時にデータを取得し、静的な HTML を生成します。
- **レンダリング場所**: ビルド時のサーバー側。

**メリット**:

- 静的な HTML を配信するため、ページの読み込み速度が速く、サーバー負荷も低いです。
- SEO に適しています。

**デメリット**:

- データの更新には再ビルドが必要なため、リアルタイム性が求められるアプリケーションには不向きです。

**適したアプリケーション要件**:

- コンテンツの更新頻度が低い企業のコーポレートサイトや製品カタログ。
- 事前に生成されたコンテンツを提供するブログやドキュメンテーションサイト。

**実装方法**:

`getStaticProps` 関数を使用して、ビルド時にデータを取得します。

**コード例**:

```javascript
// pages/ssg-example.js
export async function getStaticProps() {
  const res = await fetch("https://api.example.com/data");
  const data = await res.json();
  return { props: { data } };
}

function SSGExample({ data }) {
  return (
    <div>
      <h1>SSG Example</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

export default SSGExample;
```

このコードでは、ビルド時に `getStaticProps` が実行され、静的な HTML が生成されます。

## 3. ISR（Incremental Static Regeneration）

**特徴**:

- **データ取得タイミング**: ビルド時に静的な HTML を生成し、指定した間隔でバックグラウンドで再生成します。
- **レンダリング場所**: ビルド時のサーバー側およびバックグラウンドプロセス。

**メリット**:

- SSG の高速性を維持しつつ、定期的なデータ更新が可能です。
- SEO に適しています。

**デメリット**:

- 再生成の間隔内でのデータ更新は反映されないため、リアルタイム性には限界があります。

**適したアプリケーション要件**:

- 定期的に更新されるブログやニュースサイト。
- 頻繁に更新されるが、リアルタイム性がそれほど重要でないコンテンツ。

**実装方法**:

`getStaticProps` 関数内で `revalidate` プロパティを設定します。

**コード例**:

```javascript
// pages/isr-example.js
export async function getStaticProps() {
  const res = await fetch("https://api.example.com/data");
  const data = await res.json();
  return {
    props: { data },
    revalidate: 60, // 60 秒ごとにページを再生成
  };
}

function ISRExample({ data }) {
  return (
    <div>
      <h1>ISR Example</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

export default ISRExample;
```

このコードでは、ビルド時に `getStaticProps` が実行され、初回の静的 HTML が生成されます。その後、`revalidate` で指定した秒数（この例では 60 秒）ごとに、バックグラウンドでページが再生成され、最新のデータが反映されます。

## 4. CSR（Client-Side Rendering）

**特徴**:

- **データ取得タイミング**: クライアント側でコンポーネントのマウント時やユーザーの操作時にデータを取得します。
- **レンダリング場所**: クライアント（ブラウザ）側。

**メリット**:

- ユーザーの操作に応じて、リアルタイムでデータを更新できます。
- 初期ロード後のページ遷移が高速で、スムーズなユーザー体験を提供できます。

**デメリット**:

- 初回ロード時に JavaScript やデータの取得が必要なため、表示までに時間がかかることがあります。
- SEO 対策が難しい場合があります。

**適したアプリケーション要件**:

- ユーザーの操作に応じて頻繁にデータが変わるダッシュボードやチャットアプリ。
- リアルタイム性が求められるアプリケーション。

**実装方法**:

React の `useEffect` フックを使用して、クライアントサイドでデータを取得します。

**コード例**:

```javascript
// pages/csr-example.js
import { useEffect, useState } from "react";

function CSRExample() {
  const [data, setData] = useState(null);

  useEffect(() => {
    async function fetchData() {
      const res = await fetch("https://api.example.com/data");
      const data = await res.json();
      setData(data);
    }
    fetchData();
  }, []);

  if (!data) {
    return <div>Loading...</div>;
  }

  return (
    <div>
      <h1>CSR Example</h1>
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

export default CSRExample;
```

このコードでは、コンポーネントのマウント時に `useEffect` フック内でデータを取得し、取得したデータをコンポーネントの状態に保存します。データが取得されるまで「Loading...」と表示し、データ取得後に内容を表示します。
