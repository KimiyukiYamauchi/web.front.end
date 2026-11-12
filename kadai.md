# 期末課題作成

## 1. 課題要件

以下の要件をすべて満たす Web アプリを作成してください。

### 使用技術

- Next.js（フレームワーク）
  - プロジェクト作成時の設定
    - TypeScript
    - ESLint
    - App Router
  - スタイル設定
    - globals.css
    - CSS Modules（Scoped CSS）
  - ルーティング（トップページ、下層ページ）
- microCMS（データ保存）
  - API キーは `.env.local` に記載し、GitHub には push しない（`.gitignore` の対象になっていることを確認する）
  - Vercel では、プロジェクトの設定画面（Settings → Environment Variables）で環境変数として登録する
- GitHub（ソース管理）
  - README.md ファイルに、作成する Web アプリの**機能仕様**を記載する
- Vercel（デプロイ・公開サーバ）

## 2. スケジュール

### 1. 公開内容の提出 — 11/18（水）まで

11/18（水）までに、GitHub へのリポジトリ作成と Vercel への初回デプロイまで済ませてください。

そのうえで、Slack に以下の情報を投稿してください。

- 作成するアプリの機能
- プロジェクト名
- GitHub の URL
- Vercel の URL

投稿例：

```
- 検定の問題サイト（ITF+、SEA/J）
- quizsite
- https://github.com/KimiyukiYamauchi/quizsite
- https://quizsite-beta.vercel.app/
```

### 2. 開発期間 — 11/18（水）〜 11/26（木）11:00

- 日次で成果物を GitHub に push すること  
  → この更新状況を**授業態度の評価**に反映します
- 最終の push 期限は **11/26（木）11:00** です。期限後の push は評価の対象外とします

### 3. アプリ説明会 — 11/26（木）

発表時間：**一人 7 分**

発表内容（説明のポイント）：

- 機能の説明
- ページ構成の説明
- ディレクトリ構成の説明
- microCMS にアクセスする処理の説明
- 工夫した点
- 苦労した点

## 3. 評価のポイント

- アプリが「1. 課題要件」をすべて満たしているか
- アプリ説明会で、上記の説明ポイントが明確に説明されているか
