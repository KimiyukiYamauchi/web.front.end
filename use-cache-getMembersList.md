# 「use cache」って何? なぜ必要になったの?

Next.js で microCMS からデータを取る関数に、`"use cache"` を書かないとエラーになった理由をまとめます。

## 何が起きた?

同じコードなのに、プロジェクトによって結果が違いました。

| プロジェクト | `getMembersList` | 結果 |
|---|---|---|
| my-next-project.yo | `"use cache"` なし | 動く |
| my-next-project | `"use cache"` なし | エラー |
| my-next-project | `"use cache"` あり | 動く |

コードは同じなので、原因は**設定**にあります。

## 原因は next.config.ts の 1 行

`my-next-project` の `next.config.ts` には、次の設定が入っています。

```ts
cacheComponents: true,
```

`my-next-project.yo` にはこの設定がありません。これが違いです。

## cacheComponents: true だとどうなる?

Next.js は、ページをあらかじめ作っておく(**事前レンダリング**)ことで、表示を速くします。

`cacheComponents: true` のときは、このあらかじめ作る段階で次のルールが厳しくなります。

> 「時間のように、呼ぶたびに変わる値」を、キャッシュなしで使ってはいけない

ところが、microCMS からデータを取る `client.getList` は、中で現在時刻(`new Date()`)を使っています。そのため、次のエラーが出ました。

```
Error: Route "/members": Next.js encountered the unstable value `new Date()` while prerendering.
```

日本語にすると「事前レンダリング中に、変わりやすい値 `new Date()` が見つかりました」という意味です。

## 直し方は 3 通り

### 1. `"use cache"` を書く(おすすめ)

取得した結果を「キャッシュ(保存)していい」と Next.js に伝えます。

```ts
import { cacheLife } from "next/cache";

export const getMembersList = async (queries?: MicroCMSQueries) => {
  "use cache";
  cacheLife("minutes"); // どのくらい保存するか
  const listData = await client.getList<Member>({
    endpoint: "members",
    queries,
  });
  return listData;
};
```

- `"use cache"`: この関数の結果を保存してよい、という宣言
- `cacheLife("minutes")`: 数分たったら古いデータとして取り直す、という期限

### 2. 毎回リクエストのたびに取得する

ページを開くたびに microCMS から取り直す方法です。呼び出し側を `<Suspense>` で囲み、取得の前に `await connection()` を呼びます。常に最新ですが、少し遅くなります。

### 3. 設定を外して `.yo` と同じにする

`next.config.ts` から `cacheComponents: true`(と `partialPrefetching: true`)を消します。この場合、`"use cache"` も消してください。残すとまた別のエラーになります。

## どれを選べばいい?

**`"use cache"` を使う方法(1)をおすすめします。**

- Next.js 16 の新しいやり方で、これからの標準になっていく
- ページの表示が速くなる
- 「何分保存するか」を自分で決められる

3 を選ぶのは、授業で `.yo` と同じ構成にそろえる必要があるときなど、キャッシュをまだ扱いたくない場合です。

## 気をつけること

`"use cache"` を使うと、保存している間は microCMS を更新しても画面にすぐ反映されません。反映が遅いと感じたら、`cacheLife` の期限を短くしてください。

## まとめ

- エラーの原因は、`next.config.ts` の `cacheComponents: true`
- `client.getList` の中の `new Date()` が、事前レンダリングで問題になった
- 関数に `"use cache"` を書いてキャッシュしてよいと伝えれば直る
