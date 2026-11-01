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
