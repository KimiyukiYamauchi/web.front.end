# Next.js の Cache Components と動的ルート：`generateStaticParams` と `<Suspense>` の使い分け

Next.js + microCMS のニュースサイトで、`await params` を書いた動的ルートのビルドエラーへの対応方法として `generateStaticParams` と `<Suspense>` の2種類が使われていることに気づき、違いを調べて統一した記録です。

**使用バージョン：** Next.js 16.4.2（`cacheComponents` と `partialPrefetching` を有効化）

> Next.js はバージョンによって動作が大きく変わります。別のバージョンを使う場合は、そのバージョンのドキュメントも確認してください。

## 目次

- [この記事で学べること](#この記事で学べること)
- [前提となる用語](#前提となる用語)
- [きっかけ：同じ問題なのに書き方が違う](#きっかけ同じ問題なのに書き方が違う)
- [2つの方法は何が違うのか](#2つの方法は何が違うのか)
- [実験：ビルドして確かめる](#実験ビルドして確かめる)
- [結論：両方使う](#結論両方使う)
- [注意点：404 が 200 になる場合がある](#注意点404-が-200-になる場合がある)
- [まとめ](#まとめ)
- [残っている課題](#残っている課題)

## この記事で学べること

- `generateStaticParams` と `<Suspense>` の役割の違い
- 「ビルドが通る」と「最適な書き方である」は別だということ
- ビルド結果の記号の読み方

## 前提となる用語

| 用語 | 意味 |
| --- | --- |
| 動的ルート | `app/news/[slug]/page.tsx` のように、URL の一部が変わるページ。`[slug]` の部分が変数になる |
| `params` | URL の変数部分の値。`/news/abc` なら `slug` は `abc` |
| 事前生成（プリレンダリング） | ビルド時にページを作っておくこと。アクセスされたら完成品をすぐ返せる |
| 静的シェル | ビルド時に作られる共通の「外枠」。ヘッダーや「読み込み中...」の表示などが含まれる |
| ストリーミング | まず外枠を送り、できあがった部分をあとから流し込むこと |
| `cacheComponents` | データをどこまでキャッシュするかを、コードで明示する Next.js の設定 |

## きっかけ：同じ問題なのに書き方が違う

`cacheComponents: true` の環境では、`await params` を書いた動的ルートをそのままにするとビルドエラーになることがあります。今回のプロジェクトでは、2つのページがそれぞれ別の方法でこれに対応していました。

**ニュース詳細ページ：`generateStaticParams` で対応**

```tsx
// app/news/[slug]/page.tsx
export async function generateStaticParams() {
  const { contents } = await getNewsList({ fields: "id", limit: 100 });
  return contents.map((news) => ({ slug: news.id }));
}

export default async function Page(props: Props) {
  const { slug } = await props.params;
  const data = await getNewsDetail(slug).catch(notFound);
  // 描画
}
```

**カテゴリー一覧ページ：`<Suspense>` で対応**

```tsx
// app/news/category/[id]/page.tsx
export default function Page({ params }: Props) {
  return (
    <Suspense fallback={<p>読み込み中...</p>}>
      <CategoryNews params={params} />
    </Suspense>
  );
}

async function CategoryNews({ params }: Pick<Props, "params">) {
  const { id } = await params;
  const { contents: news } = await getNewsList({
    filters: `category[equals]${id}`,
  });
  return <NewsList news={news} />;
}
```

どちらもビルドは通ります。では、どちらが正しいのでしょうか。

## 2つの方法は何が違うのか

この2つは、同じ問題を別の角度から解決しています。

- **`generateStaticParams`：** 「どの URL があるか」をビルド時に Next.js へ教える。値が分かるので、ページの中身まで事前生成できる
- **`<Suspense>`：** 「値が分からない間はここを待つ」という境界を示す。その外側だけを先に作り、内側の待ち時間にはフォールバックを表示できる

| | `generateStaticParams` のみ | `<Suspense>` のみ |
| --- | --- | --- |
| 中身の事前生成 | される | されない |
| 一覧にない URL の初回アクセス | 描画が終わるまで待つ | フォールバックをすぐ表示できる |
| 向いている場面 | URL を事前に列挙できる | URL を事前に列挙できない |

### `generateStaticParams` の処理を詳しく見る

ニュース詳細ページの `generateStaticParams` を、1行ずつ見ていきます。

```tsx
export async function generateStaticParams() {
  const { contents } = await getNewsList({ fields: "id", limit: 100 });
  return contents.map((news) => ({ slug: news.id }));
}
```

**1. `export async function generateStaticParams()`**

Next.js が決まった名前で認識する関数なので、自分で呼び出す必要はありません。`export` が必須で、microCMS からデータを取得するために `async` にしています。

**2. `await getNewsList({ fields: "id", limit: 100 })`**

microCMS からニュースの一覧を取得します。渡した条件は、そのまま microCMS の API に送られます。

- `fields: "id"`：取得する項目を `id` だけに絞ります。URL の生成に本文やタイトルは不要なので、通信量を抑えられます。
- `limit: 100`：最大100件まで取得します。

**3. `const { contents } = ...`**

分割代入で、レスポンスから記事の配列 `contents` だけを取り出しています。`fields: "id"` を指定しているため、中身は次のようになります。

```ts
[{ id: "n27h010yl" }, { id: "mcx_dv6ecrw1" }, ...]
```

**4. `contents.map((news) => ({ slug: news.id }))`**

記事の配列を、Next.js が求める形に変換します。

```ts
[{ slug: "n27h010yl" }, { slug: "mcx_dv6ecrw1" }, ...]
```

`slug` というキー名は、フォルダ名 `[slug]` と一致させる必要があります。また、`({ ... })` の丸括弧を外すと `{}` が関数本体と解釈されるので、オブジェクトを返すために必要です。

**ビルド時の流れ**

1. `npm run build` を実行すると、Next.js が `generateStaticParams` を呼び出します。
2. 返された配列から、`/news/n27h010yl` や `/news/mcx_dv6ecrw1` などの URL が決まります。
3. URL ごとに `Page` を実行します。`params` には `{ slug: "n27h010yl" }` のような値が入ります。
4. `await props.params` で `slug` を取り出し、`getNewsDetail(slug)` で記事の本文を取得して描画します。
5. 完成したページがビルド結果として保存されます。

**注意点**

- **対象は最大100件：** 101件目以降の記事はビルド時に事前生成されません。
- **ビルド後に追加された記事も対象外：** この関数はビルド時に実行されるので、新しい記事は次のビルドまで一覧に含まれません。これらの URL は、アクセス時に描画されます。

### `<Suspense>` のみの問題点

`<Suspense>` のみでもバグではありませんが、次の点で損をします。

1. **中身が事前生成されない：** ビルドで作られるのは外枠だけで、最初に「読み込み中...」が見える
2. **ページの描画結果がキャッシュされない：** Next.js のドキュメントでは、`generateStaticParams` がないルートは ISR の対象外になり、データに `"use cache"` を付けていても毎リクエスト描画されるとされている
3. **中身の問題にビルド時に気づけない：** 中身がビルド時に実行されないので、データ取得の不具合などは実際のアクセスで初めて表面化する

なお、データ取得関数に `"use cache"` を付けているため、描画が毎回でも microCMS の API を毎回呼ぶわけではありません。

## 実験：ビルドして確かめる

説明を読むだけでなく、ニュース詳細ページから `generateStaticParams` を外して `<Suspense>` のみにし、`npm run build` を実行しました。ビルドは成功しました。

```text
└   /news/[slug]
  └ ◐ /news/[slug]
```

次は `generateStaticParams` がある状態のビルド結果です。

```text
├   /news/[slug]
│ ├ ◐ /news/[slug]
│ ├ ○ /news/n27h010yl             15m      1y
│ ├ ○ /news/mcx_dv6ecrw1          15m      1y
│ └ ◐ [+18 more paths]
└   /news/category/[id]
  └ ◐ /news/category/[id]
```

記号の意味は次のとおりです。

| 記号 | 名前 | 意味 |
| --- | --- | --- |
| `○` | Static | 静的コンテンツとして事前生成された |
| `◐` | Partial Prerender | 静的な外枠を事前生成し、動的な部分はストリーミングする |

見比べると、違いがはっきり分かります。

- `generateStaticParams` なし：個別の記事 URL が1つも出てこない
- `generateStaticParams` あり：`/news/n27h010yl` のように個別の URL が出てくる
- カテゴリーページ：`generateStaticParams` がないので、個別の URL が出てこない

**「ビルドが通る」だけでは良し悪しは分かりません。ビルド結果の中身まで読むことが大切です。**

## 結論：両方使う

2つの方法は対立するものではなく、組み合わせることができます。`cacheComponents` と `partialPrefetching` を両方有効にしている場合、Next.js の ISR ガイドでもこの組み合わせが示されています。

```tsx
// app/news/[slug]/page.tsx（修正後）
import { Suspense } from "react";
import { notFound } from "next/navigation";
import { getNewsDetail, getNewsList } from "@/app/_libs/microcms";
import Article from "@/app/_components/Article";
import ButtonLink from "@/app/_components/ButtonLink";
import styles from "./page.module.css";

type Props = {
  params: Promise<{
    slug: string;
  }>;
};

// 既知の記事は、ビルド時に事前生成する
export async function generateStaticParams() {
  const { contents } = await getNewsList({ fields: "id", limit: 100 });
  return contents.map((news) => ({ slug: news.id }));
}

// Page 自身は await しない。params をそのまま渡す
export default function Page({ params }: Props) {
  return (
    <Suspense fallback={<p>読み込み中...</p>}>
      <NewsDetail params={params} />
    </Suspense>
  );
}

// await は Suspense の内側で行う
async function NewsDetail({ params }: Pick<Props, "params">) {
  const { slug } = await params;
  const data = await getNewsDetail(slug).catch(notFound);

  return (
    <>
      <Article data={data} />
      <div className={styles.footer}>
        <ButtonLink href="/news">ニュース一覧へ</ButtonLink>
      </div>
    </>
  );
}
```

**ポイント：** `await params` を `Page` に書かず、`<Suspense>` の内側のコンポーネントに移します。`Page` で `await` すると、`<Suspense>` を置いても境界の外で待つことになり、意味がありません。

この形にすると、URL ごとに次のように動きます。

| URL | 動作 |
| --- | --- |
| ビルド時に分かっていた記事 | 事前生成済みの完成ページをすぐ返す |
| ビルド後に追加された記事 | フォールバックをすぐ表示し、中身をあとから流し込む |

修正後も `npm run build` は成功し、個別の記事 URL が生成されることを確認しました。

## 注意点：404 が 200 になる場合がある

良いことばかりではありません。`<Suspense>` の内側で `notFound()` が動くと、HTTP ステータスが変わることがあります。

ストリーミングでは、外枠を送る時点で `200 OK` を返してしまいます。あとから `notFound()` が動いても、ステータスを `404` に変更することはできません。

| | 事前生成されない不正な URL のステータス |
| --- | --- |
| `<Suspense>` の外で `notFound()` | `404` |
| `<Suspense>` の内側で `notFound()` | `200` |

どちらの場合も Next.js が `<meta name="robots" content="noindex">` を付けるので、検索結果には出ません。ただし、ステータスコードを厳密に `404` にしたい場合は、この点を考慮して設計する必要があります。

> この節の内容は Next.js のドキュメントに基づいています。今回の作業ではビルドのみを確認し、サーバーを起動しての動作確認は行っていません。実際にどう動くか、`npm run build` と `npm start` のあとに `curl -I` で確かめてみましょう。

## まとめ

- `generateStaticParams` は「どの URL を事前に作るか」を教える
- `<Suspense>` は「値が分かるまで待つ範囲」を示す
- この2つは対立せず、組み合わせて使える
- `await params` は `<Suspense>` の内側で行う
- ビルドが通っても満足せず、`○` や `◐` などの結果を読む
- ストリーミングには、404 のステータスを返せない場合があるというトレードオフがある
- 同じ問題に同じ書き方を使うと、コードが読みやすくなる

## 残っている課題

カテゴリー一覧ページには、まだ `generateStaticParams` がありません。次のことを考えてみましょう。

1. カテゴリーの ID 一覧を取得するには、`microcms.ts` にどんな関数を追加すればよいでしょうか。
2. 記事からカテゴリーを集める方法と、カテゴリーの API から取得する方法では、何が違うでしょうか。
3. 存在しないカテゴリー ID にアクセスしたときは、どう表示するのがよいでしょうか。今のコードには `notFound()` の分岐がありません。

## 参考

`node_modules/next/dist/docs/01-app/` にある次のドキュメントを参照しました。

- `02-guides/incremental-static-regeneration-cache-components.md`
- `02-guides/migrating-to-cache-components.md`
- `03-api-reference/04-functions/generate-static-params.md`
- `03-api-reference/04-functions/not-found.md`
