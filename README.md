# web.front.end

授業「Web Front End」の教材・情報提供用リポジトリです。

JavaScript の基礎から React、Next.js（TypeScript）までを段階的に学び、最終的に **Next.js + ヘッドレスCMS + GitHub + Vercel** を使った Web アプリを自力で構築できるようになることを目標としています。

## 目次

- [授業の全体像](#授業の全体像)
- [使用技術](#使用技術)
- [教材一覧](#教材一覧)
  - [シラバス・課題](#シラバス課題)
  - [モジュールB：Vanilla JavaScript 基礎](#モジュールbvanilla-javascript-基礎)
  - [モジュールC：React 基礎](#モジュールcreact-基礎)
  - [環境構築](#環境構築)
  - [JavaScript リファレンス](#javascript-リファレンス)
  - [React / Next.js](#react--nextjs)
  - [Supabase 連携](#supabase-連携)
  - [サイト運用・パフォーマンス](#サイト運用パフォーマンス)
- [関連リポジトリ](#関連リポジトリ)
- [ツール](#ツール)
- [ディレクトリ構成](#ディレクトリ構成)

## 授業の全体像

| モジュール | 回数 | 内容 |
| --- | --- | --- |
| A. オリエンテーション・環境構築 | 第1〜2回 | 授業概要、開発環境構築、Git/GitHub 基礎 |
| B. Vanilla JavaScript 基礎 | 第3〜6回 | 基本文法〜DOM操作・非同期処理、メモアプリ実装 |
| C. React 基礎 | 第7〜9回 | コンポーネント、state、CSS Modules、メモアプリ（React版）実装 |
| D. 書籍ハンズオン（Next.js + ヘッドレスCMS） | 第10〜37回 | 書籍の章立てに沿って Next.js サイトを構築 |
| E. 期末課題（企画・開発） | 第38〜46回 | 個人での企画・設計・実装・デプロイ |
| F. 発表・まとめ | 第47〜48回 | アプリ説明会、総括 |

※ 48コマ版の構成です。38コマ版は [syllabus_38.md](syllabus_38.md) を参照してください。

## 使用技術

- **開発環境**：Node.js（LTS）、npm、Visual Studio Code
- **フロントエンド**：HTML / CSS / JavaScript、React、Next.js（TypeScript、ESLint、App Router）
- **スタイリング**：globals.css、CSS Modules
- **データ管理**：microCMS（一部教材では Supabase）
- **バージョン管理・デプロイ**：GitHub、Vercel
- **教科書**：『Next.js + ヘッドレスCMSではじめるかんたんモダンWebサイト制作入門』
- **補助教材**：[現代の JavaScript チュートリアル](https://ja.javascript.info/)

## 教材一覧

### シラバス・課題

| ファイル | 内容 |
| --- | --- |
| [syllabus.md](syllabus.md) | 授業シラバス（48コマ版）：到達目標・評価方法・授業計画・期末課題要件 |
| [syllabus_38.md](syllabus_38.md) | 授業シラバス（38コマ版）：48コマ版の短縮版 |
| [kadai.md](kadai.md) | 期末課題の要件・スケジュール・評価のポイント |

### モジュールB：Vanilla JavaScript 基礎

| ファイル | 内容 |
| --- | --- |
| [第3回 基本文法](02.B.Vanilla/03_基本文法.md) | 変数とデータ型、分割代入・スプレッド演算子、演算子、制御構文、計算機アプリ |
| [第4回 関数・スコープ・非同期処理](02.B.Vanilla/04_関数・スコープ・非同期処理.md) | 関数、スコープ、コールバック、Promise・async/await、ToDoリストアプリ |
| [第5回 オブジェクト指向とクラス](02.B.Vanilla/05_オブジェクト指向とクラス.md) | クラス構文、オブジェクト指向の3原則、プロトタイプ、図形描画アプリ |
| [第6回 配列・文字列・DOM操作／総合演習](02.B.Vanilla/06_配列・文字列・DOM操作_総合演習.md) | 配列メソッド、文字列・JSON、DOM操作、簡易メモアプリ（Vanilla JS版） |
| [第6回 総合演習 実装例](02.B.Vanilla/07_総合演習.実装例.md) | メモアプリ（Vanilla JS版）の実装例 |

### モジュールC：React 基礎

| ファイル | 内容 |
| --- | --- |
| [第7回 Reactの基礎](03.C.React/07_Reactの基礎.md) | 環境構築（CRA + TypeScript）、コンポーネントとJSX、props、state、自己紹介カード |
| [第8回 イベント処理・リスト表示・スタイリング](03.C.React/08_イベント処理・リスト表示・スタイリング.md) | イベントハンドリング、制御コンポーネント、`map()` によるリスト表示、CSS Modules、買い物リスト |
| [第9回 総合演習：メモアプリ（React版）](03.C.React/09_総合演習_メモアプリReact版.md) | Vanilla JS版との対応整理、メモアプリ（React版）、発展課題 |
| [第9回 総合演習 実装例](03.C.React/10_総合演習.実装例.md) | メモアプリ（React版）の `App.tsx` / `App.module.css` 実装例 |

### 環境構築

| ファイル | 内容 |
| --- | --- |
| [install.md](install.md) | Node.js / npm、Visual Studio Code のインストール手順 |
| [vite.md](vite.md) | React + TypeScript + Vite の環境構築と GitHub Pages での公開手順 |

### JavaScript リファレンス

| ファイル | 内容 |
| --- | --- |
| [js.md](js.md) | JavaScript 基本構文・関数とスコープ・クラス・配列と文字列操作などのまとめ |
| [js.tu.md](js.tu.md) | 「現代の JavaScript チュートリアル」の参照先リンク集 |

### React / Next.js

| ファイル | 内容 |
| --- | --- |
| [react.md](react.md) | Create React App（TypeScript）でのアプリ作成手順 |
| [next.md](next.md) | Next.js のバージョン確認方法 |
| [rendering.md](rendering.md) | レンダリング方式（SSR / SSG / CSR / ISR）の解説 |

### Supabase 連携

| ファイル | 内容 |
| --- | --- |
| [supabase.md](supabase.md) | Next.js + TypeScript + Supabase アプリを手動で作る手順 |
| [claude-code-guide.md](claude-code-guide.md) | Claude Code を使って Next.js + TypeScript + Supabase アプリを作る手順 |
| [contact.md](contact.md) | お問い合わせフォームの入力を Supabase のテーブルに保存する手順 |

### サイト運用・パフォーマンス

| ファイル | 内容 |
| --- | --- |
| [googleanalytics.md](googleanalytics.md) | Google Analytics の設定手順 |
| [corewebvitals.md](corewebvitals.md) | Lighthouse スコア改善（画像の優先読み込み・レスポンシブ画像）の対応前後比較 |

## 関連リポジトリ

| リポジトリ | 内容 |
| --- | --- |
| [memo.js.tl](https://github.com/KimiyukiYamauchi/memo.js.tl) | 第6回 メモアプリ（Vanilla JS版）のひな形 |
| [memo.react.tl](https://github.com/KimiyukiYamauchi/memo.react.tl) | 第9回 メモアプリ（React版）のひな形 |

## ツール

[add_toc.py](add_toc.py) は、Markdown の `##` / `###` 見出しから GitHub 用の目次を自動生成して挿入するスクリプトです。

```bash
# 別ファイルに出力
python add_toc.py input.md -o output.md

# 元ファイルを直接書き換え
python add_toc.py input.md --inplace
```

Markdown 内に以下のマーカーを置くと、その範囲が目次で置き換えられます（マーカーがなければ先頭に挿入）。

```markdown
<!-- TOC -->
<!-- /TOC -->
```

## ディレクトリ構成

```
web.front.end/
├── 02.B.Vanilla/        # モジュールB：Vanilla JavaScript 基礎（第3〜6回）
├── 03.C.React/          # モジュールC：React 基礎（第7〜9回）
├── img/                 # 教材内で使用する画像
├── syllabus.md          # シラバス（48コマ版）
├── syllabus_38.md       # シラバス（38コマ版）
├── kadai.md             # 期末課題
├── *.md                 # 各種手順書・リファレンス
└── add_toc.py           # 目次自動生成スクリプト
```
