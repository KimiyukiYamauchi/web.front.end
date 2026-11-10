# ページ送り(ページネーション)ページの `<Suspense>` の処理

Next.js + microCMS のニュースサイトで、ページ送りを担当する次の2つのページに `<Suspense>` を書いた理由と、その中で何が起きているかをまとめます。

| ファイル | URL の例 | 内容 |
| --- | --- | --- |
| `app/news/p/[current]/page.tsx` | `/news/p/2` | ニュース一覧の 2 ページ目 |
| `app/news/category/[id]/p/[current]/page.tsx` | `/news/category/notice/p/2` | 特定カテゴリーのニュース一覧の 2 ページ目 |

**使用バージョン:** Next.js 16.4.2(`cacheComponents` と `partialPrefetching` を有効化)

> Next.js はバージョンによって動作が大きく変わります。別のバージョンを使う場合は、そのバージョンのドキュメントも確認してください。

`generateStaticParams` と `<Suspense>` の違いは [next.cache.components.md](next.cache.components.md) で詳しく扱っています。この記事は、その内容をページ送りのページに当てはめたものです。

## 目次

- [この記事で学べること](#この記事で学べること)
- [前提となる用語](#前提となる用語)
- [きっかけ:ビルドエラー](#きっかけビルドエラー)
- [修正の考え方:Page を2つに分ける](#修正の考え方page-を2つに分ける)
- [ニュース一覧のページ送り](#ニュース一覧のページ送り)
- [カテゴリー別のページ送り](#カテゴリー別のページ送り)
- [2つのページの比較](#2つのページの比較)
- [ビルド結果を読む](#ビルド結果を読む)
- [注意点](#注意点)
- [まとめ](#まとめ)
- [考えてみよう](#考えてみよう)

## この記事で学べること

- `await params` を `<Suspense>` の外に書くと、なぜビルドエラーになるのか
- `Page` を「外枠」と「データを取る部分」に分ける書き方
- `<Suspense>` の内側で `notFound()` を使うときの注意点

## 前提となる用語

| 用語 | 意味 |
| --- | --- |
| 動的ルート | `[current]` のように、URL の一部が変数になっているページ |
| `params` | URL の変数部分の値。`/news/p/2` なら `current` は `"2"`(文字列) |
| 事前生成(プリレンダリング) | ビルド時にページを作っておくこと |
| 静的シェル | ビルド時に作られる共通の外枠。ヘッダーや「読み込み中...」の表示が入る |
| ストリーミング | 外枠を先に送り、できあがった部分をあとから流し込むこと |
| `<Suspense>` | 「この中は待つ必要がある」という境界。待っている間は `fallback` を表示する |

## きっかけ:ビルドエラー

`next.config.ts` で `cacheComponents: true` を設定している状態で `npm run build` を実行すると、次のエラーでビルドが止まりました。

```text
Error: Route "/news/p/[current]": Next.js encountered uncached or runtime data during prerendering.

`fetch(...)`, `cookies()`, `headers()`, `params`, `searchParams`, or `connection()` accessed outside of `<Suspense>` prevents the route from being prerendered, blocking the page load and leading to a slower user experience.

Ways to fix this:
  - [stream] Provide a placeholder with `<Suspense fallback={...}>` around the data access
  - [cache] For uncached data (`fetch`, database calls): cache the access with `"use cache"` (does not apply to `connection()`)
  - [block] Set `export const instant = false` to allow a blocking route
```

修正前のコードは次のとおりです。

```tsx
// app/news/p/[current]/page.tsx(修正前)
export default async function Page({ params }: Props) {
  const { current } = await params; // ← ここが <Suspense> の外
  const currentNum = parseInt(current, 10);
  // ...
  const { contents: news } = await getNewsList({ /* ... */ });
  return <NewsList news={news} />;
}
```

`params` は「アクセスされるまで値が分からないデータ」です。`/news/p/2` なのか `/news/p/5` なのかは、ビルド時には分かりません。

`cacheComponents: true` のとき、Next.js はビルド時にできるだけ多くの部分を事前生成しようとします。ところが `Page` の先頭で `await params` すると、ページ全体が「値が分かるまで何も作れない」状態になります。Next.js はこれを「表示が遅くなる書き方」とみなし、エラーにします。

エラーメッセージには3つの直し方が書かれています。今回は1つ目の **[stream]**、つまり `<Suspense>` で囲む方法を使いました。

## 修正の考え方:Page を2つに分ける

`<Suspense>` を書いても、`Page` の中で `await params` したままでは意味がありません。`await` が `<Suspense>` より先に実行され、境界の外で待つことになるからです。

そこで、`Page` を次の2つに分けます。

| コンポーネント | `async` | 役割 |
| --- | --- | --- |
| `Page` | なし | `<Suspense>` を置くだけ。`params` は `await` せず、そのまま渡す |
| `PagedNews` | あり | `<Suspense>` の内側で `await params` し、データを取って描画する |

```text
Page(同期・すぐ返る)
└─ <Suspense fallback="読み込み中...">   ← ここまでが静的シェル(ビルド時に作れる)
   └─ PagedNews(async)                  ← アクセス時に実行され、あとから流し込まれる
      ├─ await params
      ├─ await getNewsList(...)
      └─ <NewsList /> を返す
```

`params` は `Promise` なので、`await` せずに子コンポーネントへ渡せます。値を取り出すタイミングを `<Suspense>` の内側まで遅らせるのがポイントです。

## ニュース一覧のページ送り

```tsx
// app/news/p/[current]/page.tsx(修正後)
import { Suspense } from "react";
import { notFound } from "next/navigation";
import { getNewsList } from "@/app/_libs/microcms";
import NewsList from "@/app/_components/NewsList";
import { NEWS_LIST_LIMIT } from "@/app/_constants";

type Props = {
  params: Promise<{
    current: string;
  }>;
};

export default function Page({ params }: Props) {
  return (
    <Suspense fallback={<p>読み込み中...</p>}>
      <PagedNews params={params} />
    </Suspense>
  );
}

async function PagedNews({ params }: Pick<Props, "params">) {
  const { current } = await params;
  const currentNum = parseInt(current, 10);

  if (Number.isNaN(currentNum) || currentNum < 1) {
    notFound();
  }

  const { contents: news } = await getNewsList({
    limit: NEWS_LIST_LIMIT,
    offset: NEWS_LIST_LIMIT * (currentNum - 1),
  });

  if (news.length === 0) {
    notFound();
  }

  return <NewsList news={news} />;
}
```

### 処理の流れ

**1. `export default function Page({ params }: Props)`**

`async` を付けていないので、`Page` は待たずにすぐ `<Suspense>` を返します。これが静的シェルになります。

**2. `<Suspense fallback={<p>読み込み中...</p>}>`**

内側の `PagedNews` の準備ができるまで、「読み込み中...」を表示します。

**3. `Pick<Props, "params">`**

`Props` 型から `params` だけを取り出した型です。`PagedNews` に必要なのは `params` だけなので、こう書いています。今は `Props` に `params` しかないので `Props` と書いても動きますが、あとで `Page` に別の値が増えても `PagedNews` 側に影響しません。

**4. `const { current } = await params;`**

ここで初めて URL の値を取り出します。`/news/p/2` なら `current` は `"2"` です。

**5. `parseInt(current, 10)` とページ番号のチェック**

URL の値は文字列なので、数値に変換します。`/news/p/abc` のような数値でない値(`NaN`)や、`0` 以下の値なら `notFound()` で 404 ページを表示します。

**6. `getNewsList({ limit, offset })`**

`NEWS_LIST_LIMIT` 件ずつ記事を取得します。`offset` は「何件飛ばすか」です。たとえば `NEWS_LIST_LIMIT` が 10 のとき、次のようになります。

| ページ | `offset` | 取得する記事 |
| --- | --- | --- |
| 1 | `10 × 0 = 0` | 1〜10 件目 |
| 2 | `10 × 1 = 10` | 11〜20 件目 |
| 3 | `10 × 2 = 20` | 21〜30 件目 |

**7. `news.length === 0` のチェック**

記事が 25 件しかないのに `/news/p/10` にアクセスされると、取得結果は 0 件です。存在しないページとして `notFound()` を呼びます。

**8. `return <NewsList news={news} />`**

取得した記事を描画します。この結果が、先に表示されていた「読み込み中...」と入れ替わります。

## カテゴリー別のページ送り

```tsx
// app/news/category/[id]/p/[current]/page.tsx
import { Suspense } from "react";
import { notFound } from "next/navigation";
import { getCategoryDetail, getNewsList } from "@/app/_libs/microcms";
import NewsList from "@/app/_components/NewsList";
import Pagination from "@/app/_components/Pagination";
import { NEWS_LIST_LIMIT } from "@/app/_constants";

type Props = {
  params: Promise<{
    id: string;
    current: string;
  }>;
};

export default function Page({ params }: Props) {
  return (
    <Suspense fallback={<p>読み込み中...</p>}>
      <PagedNews params={params} />
    </Suspense>
  );
}

async function PagedNews({ params }: Pick<Props, "params">) {
  const { current, id } = await params;
  const currentNum = parseInt(current, 10);

  if (Number.isNaN(currentNum) || currentNum < 1) {
    notFound();
  }

  const category = await getCategoryDetail(id).catch(notFound);

  const { contents: news, totalCount } = await getNewsList({
    filters: `category[equals]${category.id}`,
    limit: NEWS_LIST_LIMIT,
    offset: NEWS_LIST_LIMIT * (currentNum - 1),
  });

  if (news.length === 0) {
    notFound();
  }

  return (
    <>
      <NewsList news={news} />
      <Pagination
        totalCount={totalCount}
        current={currentNum}
        basePath={`/news/category/${id}`}
      />
    </>
  );
}
```

`Page` と `<Suspense>` の形はニュース一覧と同じです。違うのは `PagedNews` の中身です。

### ニュース一覧と違うところ

**1. URL の変数が2つある**

フォルダが `category/[id]/p/[current]` なので、`params` には `id` と `current` の2つが入ります。`/news/category/notice/p/2` なら `id` は `"notice"`、`current` は `"2"` です。

**2. ページ番号を先にチェックする**

`parseInt` のチェックを、microCMS への問い合わせより前に置いています。ページ番号が不正なら、API を呼ばずにすぐ 404 にできます。

**3. `getCategoryDetail(id).catch(notFound)`**

カテゴリーが存在するかを確認します。存在しない ID だと microCMS がエラーを返すので、`.catch(notFound)` で 404 ページに切り替えます。

**4. `filters: \`category[equals]${category.id}\``**

microCMS の絞り込み条件です。「`category` が指定した ID と等しい記事」だけを取得します。

**5. `totalCount` と `<Pagination>`**

`totalCount` は、絞り込み後の記事の総数です。`<Pagination>` はこれを使ってページ数を計算し、ページ番号のリンクを並べます。

`basePath` に `/news/category/${id}` を渡しているので、リンク先は `/news/category/notice/p/1`、`/news/category/notice/p/2` のようになります。`basePath` を省略すると `/news` になり、カテゴリーの絞り込みが外れたページに移動してしまいます。

`<Pagination>` も `<Suspense>` の内側にあるので、記事一覧と一緒に表示されます。`totalCount` はデータを取得するまで分からないので、外側に出すことはできません。

## 2つのページの比較

| | ニュース一覧 | カテゴリー別 |
| --- | --- | --- |
| ファイル | `app/news/p/[current]/page.tsx` | `app/news/category/[id]/p/[current]/page.tsx` |
| `params` | `current` | `id`、`current` |
| `<Suspense>` の位置 | `Page` 全体を囲む | `Page` 全体を囲む |
| `fallback` | `読み込み中...` | `読み込み中...` |
| microCMS への問い合わせ | `getNewsList` のみ | `getCategoryDetail` → `getNewsList` |
| `notFound()` の条件 | ページ番号が不正、記事が 0 件 | ページ番号が不正、カテゴリーがない、記事が 0 件 |
| `<Pagination>` | なし | あり |

同じ問題に同じ書き方を使っているので、片方を読めばもう片方も読めます。

## ビルド結果を読む

修正後に `npm run build` を実行すると、ビルドが最後まで通ります。

```text
├   /news/category/[id]
│ └ ◐ /news/category/[id]
└   /news/p/[current]
  └ ◐ /news/p/[current]
```

| 記号 | 名前 | 意味 |
| --- | --- | --- |
| `○` | Static | ページ全体が事前生成された |
| `◐` | Partial Prerender | 静的シェルだけ事前生成し、`<Suspense>` の内側はアクセス時にストリーミングする |

`◐` になっているのは、`<Suspense>` の外側(静的シェル)と内側(アクセス時に作る部分)に分かれたためです。

## 注意点

### 404 のはずが 200 になる場合がある

ストリーミングでは、静的シェルを送る時点で HTTP ステータス `200 OK` を返します。そのあと `<Suspense>` の内側で `notFound()` が呼ばれても、ステータスを `404` に変えることはできません。

| | 存在しないページ(例:`/news/p/999`)のステータス |
| --- | --- |
| `<Suspense>` の外で `notFound()` | `404` |
| `<Suspense>` の内側で `notFound()` | `200`(画面には 404 ページが表示される) |

どちらの場合も Next.js が `<meta name="robots" content="noindex">` を付けるので、検索結果には出ません。ただし、ステータスコードを厳密に `404` にしたい場合は設計を見直す必要があります。

> この節の内容は Next.js のドキュメントに基づいています。今回はビルドのみを確認しました。`npm run build` と `npm start` のあとに `curl -I http://localhost:3000/news/p/999` を実行して、実際のステータスを確かめてみましょう。

### 中身は事前生成されない

`<Suspense>` だけでは、記事一覧そのものはビルド時に作られません。アクセスのたびに、まず「読み込み中...」が表示されます。

ただし、microCMS からデータを取る関数には `"use cache"` を付けているので、アクセスのたびに API を呼ぶわけではありません。詳しくは [use-cache-getMembersList.md](use-cache-getMembersList.md) を参照してください。

## まとめ

- `cacheComponents: true` のとき、`<Suspense>` の外で `await params` するとビルドエラーになる
- `Page` は `async` にせず `<Suspense>` を返すだけにし、`await params` は内側のコンポーネントで行う
- `params` は `Promise` のまま子コンポーネントに渡せる
- 2つのページ送りのページは同じ形で書かれていて、違いは `PagedNews` の中身だけ
- ビルド結果の `◐` は、静的シェルとストリーミングに分かれたことを示す
- `<Suspense>` の内側の `notFound()` は、ステータスが `200` になる場合がある

## 考えてみよう

1. `Page` に `async` を付けて `const { current } = await params;` と書き、その下で `<Suspense>` を返すとどうなるでしょうか。実際にビルドして確かめてみましょう。
2. ページ数は記事の総数から計算できます。`generateStaticParams` で `[{ current: "1" }, { current: "2" }, ...]` を返すと、ビルド結果はどう変わるでしょうか。([next.cache.components.md](next.cache.components.md) を参考にしてください)
3. ニュース一覧のページ送り(`/news/p/[current]`)には `<Pagination>` がありません。追加するには、`getNewsList` の結果から何を取り出せばよいでしょうか。

## 参考

`node_modules/next/dist/docs/01-app/` にある次のドキュメントを参照しました。

- `02-guides/building.md`
- `02-guides/migrating-to-cache-components.md`
- `03-api-reference/04-functions/not-found.md`
