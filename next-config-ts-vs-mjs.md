# next.config.ts と next.config.mjs の違い(外部画像の設定はどこに書く?)

microCMS の画像など、外部サイトの画像を Next.js の `<Image>` で表示するには、`next.config` に許可の設定が必要です。このとき「どのファイルに書けばいいの?」で迷いやすいので、まとめます。

## 結論

`create-next-app` で作ったプロジェクトに `next.config.mjs` がなければ、**`next.config.ts` に同じ設定を書けば OK** です。`.mjs` を新しく作る必要はありません。

```ts
// next.config.ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "images.microcms-assets.io",
      },
    ],
  },
};

export default nextConfig;
```

## 拡張子 js / mjs / ts の違い

| 拡張子 | 意味 | 特徴 |
|---|---|---|
| `.js` | JavaScript | いちばん基本の形式。`import` を使えるか(ESM)、`require` を使うか(CommonJS)は、`package.json` の `"type"` の設定で決まる |
| `.mjs` | JavaScript(ESM 専用) | `m` は module(モジュール)の頭文字。`package.json` の設定に関係なく、必ず `import` / `export` を使う形式として扱われる |
| `.ts` | TypeScript | JavaScript に「型」を足したもの。入力補完やミスの検出が効く。実行前に JavaScript に変換される |

next.config では、それぞれ次のように書きます。

```js
// next.config.mjs(型なし。VSCode で補完を効かせたいときはコメントで型を指定する)
/** @type {import('next').NextConfig} */
const nextConfig = { /* ... */ };
export default nextConfig;
```

```ts
// next.config.ts(型あり。import type で型を読み込む)
import type { NextConfig } from "next";
const nextConfig: NextConfig = { /* ... */ };
export default nextConfig;
```

- `.mjs` は型を書けないので、`/** @type ... */` というコメントで型を伝える
- `.ts` は `: NextConfig` と直接書けるので、より分かりやすい
- どれも、書ける設定の中身(`images` など)は同じ

## なぜファイルが違うの?(経緯)

| 時期 | できごと |
|---|---|
| my-next-project.yo の作成時 | `create-next-app` が `next.config.ts` を作った(中身は `reactCompiler: true` だけ) |
| 講座の手順 | `next.config.mjs` に画像の許可を書く手順だったため、`.mjs` を新しく作って設定した |
| my-next-project の作成時 | 新しい `create-next-app` が `next.config.ts` だけを作った。`.mjs` は最初から無い |

講座の手順(`.mjs`)と、今の `create-next-app` の初期状態(`.ts`)がずれているだけです。

## 大事なルール: 読まれる設定ファイルは 1 つだけ

Next.js は、次の順番で設定ファイルを探し、**最初に見つかった 1 つだけ**を読みます。

1. `next.config.js`
2. `next.config.mjs`
3. `next.config.ts`

## .yo プロジェクトで起きていたこと

`my-next-project.yo` には、実は両方のファイルがあります。

| ファイル | 内容 | 読まれる? |
|---|---|---|
| next.config.mjs | 外部画像の許可 | 読まれる |
| next.config.ts | `reactCompiler: true` | **読まれない** |

つまり、`.yo` では `reactCompiler: true` が効いていません。画像の設定が効いているのは、`.mjs` が先に読まれるからです。

## 気をつけること

- `my-next-project` に `next.config.mjs` を**作らないでください**。`.mjs` が先に読まれて、`.ts` に書いた設定(`cacheComponents` など)が無視されます。
- `.ts` なら `NextConfig` の型で入力補完が効くので、`.ts` に一本化するのがおすすめです。
- 設定ファイルを変更したら、開発サーバー(`npm run dev`)を再起動してください。

## .yo を整理するには

`.mjs` の画像設定を `.ts` に移し、`.mjs` を削除します。すると `reactCompiler: true` も効くようになります。ただし、React Compiler が有効になるので、動作が変わらないか確認してください。

## まとめ

- 外部画像の許可は `next.config` の `images.remotePatterns` に書く
- `.mjs` が無いプロジェクトでは `next.config.ts` に書けばよい
- 設定ファイルは複数あっても、読まれるのは 1 つだけ(`.js` → `.mjs` → `.ts` の順)
- 拡張子の違い: `.js` は基本の JavaScript、`.mjs` は `import` 専用の JavaScript、`.ts` は型付きの TypeScript
