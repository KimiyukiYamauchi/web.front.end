# Next.js をアップグレードする手順

Next.js は数週間おきに新しいバージョンが出ます。不具合やセキュリティの修正も入るので、ときどき最新の**安定版**に上げておきましょう。ここでは、作成中のプロジェクト(例: `my-next-project`)の Next.js を安全に上げる手順をまとめます。

## 全体の流れ

1. 作業中の変更をコミットしておく
2. 今のバージョンと最新のバージョンを確認する
3. `next` と `eslint-config-next` を最新版に上げる
4. lint・ビルド・画面で動作を確認する
5. アップグレードをコミットして push する

## 1. 作業中の変更をコミットしておく

アップグレードで問題が起きたとき、すぐ元に戻せるようにするためです。まず変更が残っていないか確認します。

```bash
cd ~/next/my-next-project
git status
```

変更が残っていれば、先にコミットしておきます。

```bash
git add -A
git commit -m "作業中の変更をコミット"
```

`git status` で `nothing to commit, working tree clean` と出れば準備完了です。

## 2. バージョンを確認する

今プロジェクトで使っているバージョンを確認します。

```bash
npx next --version
```

```
Next.js v16.4.2
```

次に、公開されている最新の安定版を確認します。

```bash
npm view next version
npm view eslint-config-next version
```

```
16.4.6
16.4.6
```

> `package.json` の `"next": "16.4.2"` の部分を見ても、今のバージョンが分かります。

### バージョン番号の読み方

`16.4.6` は「メジャー.マイナー.パッチ」の順に並んでいます。

| 上がる場所 | 例 | 意味 | 注意 |
| --- | --- | --- | --- |
| パッチ | 16.4.2 → 16.4.6 | 不具合の修正 | そのまま上げて問題ないことがほとんど |
| マイナー | 16.4 → 16.5 | 機能の追加 | 基本はそのまま動く。念のためリリースノートを確認 |
| メジャー | 16 → 17 | 大きな変更 | 書き方が変わることがある。[アップグレードガイド](https://nextjs.org/docs/app/guides/upgrading)を必ず読む |

> `16.5.0-canary.53` のように `canary` が付いたものは試験版です。授業のプロジェクトでは使わず、安定版を使ってください。

## 3. 最新版に上げる

`next` と `eslint-config-next` は**必ず同じバージョン**にそろえます。

```bash
npm install next@latest eslint-config-next@latest
```

バージョンを指定したいときは、`@latest` の代わりに番号を書きます。

```bash
npm install next@16.4.6 eslint-config-next@16.4.6
```

インストールが終わったら、バージョンが上がったか確認します。

```bash
npx next --version
```

```
Next.js v16.4.6
```

`package.json` と `package-lock.json` の2つのファイルが書き換わります。

```diff
-    "next": "16.4.2",
+    "next": "16.4.6",
...
-    "eslint-config-next": "16.4.2",
+    "eslint-config-next": "16.4.6",
```

### メジャーバージョンを上げるとき

メジャーバージョンを上げるときは、公式の自動変換ツール(codemod)を使うと、必要な書き換えの多くを自動で行ってくれます。

```bash
npx @next/codemod@latest upgrade latest
```

実行すると質問がいくつか出るので、内容を読んで答えてください。終わったら、`git diff` で何が書き換わったかを必ず確認します。

## 4. 動作を確認する

### lint

```bash
npm run lint
```

`0 errors` であれば OK です。`warning`(警告)は、使っていない変数などのお知らせなので、動作には影響しません。

### ビルド

Vercel でも同じビルドが行われるので、**ここが通ることが一番大事**です。

```bash
npm run build
```

最後にページの一覧(`Route (app)` の表)が表示されれば成功です。

```
✓ Compiled successfully
✓ Generating static pages using 11 workers (30/30)

Route (app)
┌ ○ /
├ ○ /contact
├ ○ /members
├ ○ /news
...
```

### 画面の確認

```bash
npm run dev
```

ブラウザで http://localhost:3000 を開き、トップ・ニュース一覧・ニュース詳細・お問い合わせなど、主なページが今までどおり表示されるか確認します。

## 5. コミットして push する

確認ができたら、アップグレードだけを1つのコミットにまとめます。

```bash
git add package.json package-lock.json
git commit -m "Next.js を 16.4.6 にアップグレード"
git push
```

> `package-lock.json` も必ずコミットしてください。これがないと、Vercel で別のバージョンがインストールされることがあります。

push すると Vercel で自動的にデプロイされます。Vercel のダッシュボードでデプロイが成功したか、公開中のサイトが正しく表示されるかも確認しましょう。

## うまくいかないとき

### ビルドでエラーが出た

まずエラーメッセージを読み、どのファイルの何行目で起きているかを確認します。パッチやマイナーで直せないときは、いったん元に戻してから調べ直します。

```bash
git restore package.json package-lock.json
npm install
```

コミットした後なら、そのコミットを取り消します。

```bash
git revert HEAD
npm install
```

### `install-scripts` の警告が出た

```
npm warn install-scripts 1 package had install scripts blocked ...
npm warn install-scripts   unrs-resolver@1.12.2 (postinstall: node postinstall.js)
```

npm の設定で、一部のパッケージがインストール時のスクリプトを実行しなかったというお知らせです。lint とビルドが通っていれば、そのままで問題ありません。

### `npm install` で `ERESOLVE` エラーが出た

`next` と `eslint-config-next` のバージョンがそろっていないことが多いです。2つを同じバージョンで指定して、もう一度インストールしてください。

## 参考

- [Next.js 公式: Upgrading](https://nextjs.org/docs/app/guides/upgrading)
- [Next.js のリリース一覧(GitHub)](https://github.com/vercel/next.js/releases)
- [next.md](next.md): Next.js のバージョン確認方法
