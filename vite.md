# TypeScript + Vite

React + TypeScript + Vite 環境構築と GitHub Pages 運用手順

<!-- TOC -->

# 目次

- [1. 概要](#1-概要)
- [2. Node.jsの確認](#2-nodejsの確認)
- [3. React + TypeScript + Viteプロジェクトの作成](#3-react-typescript-viteプロジェクトの作成)
- [4. プロジェクト構成](#4-プロジェクト構成)
  - [index.html](#indexhtml)
- [5. 開発サーバーの起動](#5-開発サーバーの起動)
- [6. 開発](#6-開発)
- [7. TypeScriptの設定](#7-typescriptの設定)
  - [tsconfig.json](#tsconfigjson)
  - [tsconfig.app.json](#tsconfigappjson)
- [8. VS CodeでTypeScriptのエラーが出る場合](#8-vs-codeでtypescriptのエラーが出る場合)
- [9. 本番用ビルド](#9-本番用ビルド)
- [10. 本番ビルドの確認](#10-本番ビルドの確認)
- [11. GitHubリポジトリの作成](#11-githubリポジトリの作成)
- [12. GitHub Pages用パッケージのインストール](#12-github-pages用パッケージのインストール)
- [13. ViteをGitHub Pages用に設定](#13-viteをgithub-pages用に設定)
- [14. package.jsonの設定](#14-packagejsonの設定)
- [15. GitHub Pagesへデプロイ](#15-github-pagesへデプロイ)
- [16. GitHub Pagesの設定](#16-github-pagesの設定)
- [17. 開発後の更新手順](#17-開発後の更新手順)
- [18. デプロイ前の確認](#18-デプロイ前の確認)
- [19. 変更がGitHub Pagesに反映されない場合](#19-変更がgithub-pagesに反映されない場合)
- [20. gh-pagesブランチが更新されたか確認](#20-gh-pagesブランチが更新されたか確認)
- [21. gh-pagesは更新されているのに画面が古い場合](#21-gh-pagesは更新されているのに画面が古い場合)
  - [GitHub Pagesの設定](#github-pagesの設定)
  - [GitHub Actions](#github-actions)
  - [ブラウザキャッシュ](#ブラウザキャッシュ)
- [22. トラブル時の確認手順](#22-トラブル時の確認手順)
- [23. Create React Appとの主な違い](#23-create-react-appとの主な違い)
- [24. よく使用するコマンド](#24-よく使用するコマンド)
  - [開発](#開発)
  - [ビルド](#ビルド)
  - [本番ビルド確認](#本番ビルド確認)
  - [GitHubへpush](#githubへpush)
  - [GitHub Pagesへデプロイ](#github-pagesへデプロイ)
  - [デプロイキャッシュ削除](#デプロイキャッシュ削除)
  - [distを削除して再ビルド](#distを削除して再ビルド)
  - [gh-pagesの更新確認](#gh-pagesの更新確認)
- [25. 推奨する日常の運用](#25-推奨する日常の運用)
- [まとめ](#まとめ)

<!-- /TOC -->

## 1. 概要

React + TypeScript + Viteを使用してWebアプリケーションを開発し、GitHub Pagesへ公開するまでの手順をまとめます。

構成は以下を想定しています。

```text
React
  +
TypeScript
  +
Vite
  ↓
GitHub
  ↓
GitHub Pages
```

開発時はViteの開発サーバーを使用し、本番用にビルドした`dist`ディレクトリをGitHub Pagesへデプロイします。

---

## 2. Node.jsの確認

最初にNode.jsとnpmがインストールされていることを確認します。

```bash
node -v
npm -v
```

例：

```text
v24.12.0
11.6.2
```

---

## 3. React + TypeScript + Viteプロジェクトの作成

Viteを使用してReact + TypeScriptプロジェクトを作成します。

```bash
npm create vite@latest
```

対話形式で設定します。

例：

```text
Project name:
> quiz-app

Select a framework:
> React

Select a variant:
> TypeScript
```

プロジェクトへ移動します。

```bash
cd quiz-app
```

必要なパッケージをインストールします。

```bash
npm install
```

---

## 4. プロジェクト構成

基本的な構成は以下のようになります。

```text
quiz-app/
│
├── index.html
├── package.json
├── vite.config.ts
│
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.node.json
│
├── public/
│
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── App.css
    └── assets/
```

### index.html

Viteでは`index.html`をプロジェクトのルートディレクトリに配置します。

```text
quiz-app/
├── index.html
├── package.json
└── src/
```

Create React Appのような、

```text
public/index.html
```

ではない点に注意してください。

---

## 5. 開発サーバーの起動

以下を実行します。

```bash
npm run dev
```

正常に起動すると、例えば次のように表示されます。

```text
VITE ready

Local: http://localhost:5173/
```

ブラウザから、

```text
http://localhost:5173/
```

へアクセスします。

Viteでは標準で`5173`番ポートが使用されます。

---

## 6. 開発

主に`src`ディレクトリ内でReactアプリケーションを開発します。

```text
src/
├── main.tsx
├── App.tsx
├── App.css
│
├── components/
│   ├── Header.tsx
│   └── ...
│
├── data/
│   └── ...
│
└── types/
    └── ...
```

Reactでは画面をコンポーネントに分割して作成します。

例えば、

```text
App
├── Header
├── Main
└── Footer
```

のような構成にできます。

---

## 7. TypeScriptの設定

ViteのReact + TypeScriptプロジェクトでは、TypeScriptの設定が複数ファイルに分かれています。

```text
tsconfig.json
tsconfig.app.json
tsconfig.node.json
```

### tsconfig.json

プロジェクト全体のTypeScript設定をまとめます。

```json
{
  "files": [],
  "references": [
    {
      "path": "./tsconfig.app.json"
    },
    {
      "path": "./tsconfig.node.json"
    }
  ]
}
```

### tsconfig.app.json

Reactアプリケーション側のTypeScript設定です。

例えばJSONファイルを、

```ts
import data from "./data/data.json";
```

のように直接読み込む場合は、

```json
"resolveJsonModule": true
```

を設定します。

例：

```json
{
  "compilerOptions": {
    "target": "ES2023",
    "lib": ["ES2023", "DOM"],
    "module": "ESNext",
    "types": ["vite/client"],
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "verbatimModuleSyntax": true,
    "moduleDetection": "force",
    "resolveJsonModule": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true
  },
  "include": ["src"]
}
```

---

## 8. VS CodeでTypeScriptのエラーが出る場合

`tsconfig.json`などにエラーが表示されるにもかかわらず、

```bash
npm run build
```

ではエラーが出ない場合があります。

この場合、VS CodeがプロジェクトにインストールされたTypeScriptとは異なるバージョンを使用している可能性があります。

VS Codeで、

```text
Ctrl + Shift + P
```

を押して、

```text
TypeScript: Select TypeScript Version
```

を選択します。

続いて、

```text
Use Workspace Version
```

を選択します。

その後、

```text
TypeScript: Restart TS Server
```

を実行します。

必要であれば、

```text
Developer: Reload Window
```

も実行します。

プロジェクトで使用しているTypeScriptは、

```bash
npm list typescript
```

で確認できます。

---

## 9. 本番用ビルド

開発が完了したら、本番用ファイルを生成します。

```bash
npm run build
```

`package.json`が、

```json
"scripts": {
  "dev": "vite",
  "build": "tsc -b && vite build",
  "preview": "vite preview"
}
```

となっている場合、

```text
npm run build
      ↓
tsc -b
      ↓
TypeScriptのチェック
      ↓
vite build
      ↓
dist生成
```

という流れになります。

正常に終了すると、

```text
dist/
```

が作成されます。

例：

```text
dist/
├── index.html
└── assets/
    ├── index-xxxxx.css
    └── index-xxxxx.js
```

---

## 10. 本番ビルドの確認

本番用にビルドした内容をローカルで確認します。

```bash
npm run preview
```

例えば、

```text
http://localhost:4173/
```

で確認できます。

GitHub Pages用に`base`を設定している場合は、

```text
http://localhost:4173/リポジトリ名/
```

になることがあります。

例：

```text
http://localhost:4173/sec1.react/
```

---

## 11. GitHubリポジトリの作成

GitHubで新しいリポジトリを作成します。

例：

```text
quiz-app
```

ローカルプロジェクトをGit管理します。

```bash
git init
git add .
git commit -m "Initial commit"
```

リモートリポジトリを登録します。

```bash
git remote add origin git@github.com:<GitHubユーザー名>/<リポジトリ名>.git
```

mainブランチをpushします。

```bash
git branch -M main
git push -u origin main
```

---

## 12. GitHub Pages用パッケージのインストール

`gh-pages`をインストールします。

```bash
npm install --save-dev gh-pages
```

---

## 13. ViteをGitHub Pages用に設定

`vite.config.ts`を編集します。

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "/リポジトリ名/",
});
```

例えばGitHubリポジトリ名が、

```text
sec1.react
```

なら、

```ts
export default defineConfig({
  plugins: [react()],
  base: "/sec1.react/",
});
```

とします。

`base`はGitHubのリポジトリ名と一致させます。

---

## 14. package.jsonの設定

`package.json`の`scripts`へGitHub Pages用の設定を追加します。

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "preview": "vite preview",
    "predeploy": "npm run build",
    "deploy": "gh-pages -d dist"
  }
}
```

重要なのは、

```json
"predeploy": "npm run build",
"deploy": "gh-pages -d dist"
```

です。

Viteでは本番用ファイルが、

```text
dist/
```

へ生成されるため、

```text
gh-pages -d dist
```

とします。

---

## 15. GitHub Pagesへデプロイ

以下を実行します。

```bash
npm run deploy
```

処理の流れは、

```text
npm run deploy
      ↓
predeploy
      ↓
npm run build
      ↓
tsc -b
      ↓
vite build
      ↓
dist/
      ↓
gh-pages -d dist
      ↓
gh-pagesブランチへpush
```

となります。

正常にデプロイされると、

```text
Published
```

などと表示されます。

---

## 16. GitHub Pagesの設定

GitHubのリポジトリを開きます。

```text
Settings
  ↓
Pages
```

公開元を以下のように設定します。

```text
Source:
Deploy from a branch

Branch:
gh-pages

Folder:
/ (root)
```

保存します。

公開URLは通常、

```text
https://<GitHubユーザー名>.github.io/<リポジトリ名>/
```

となります。

例えば、

```text
GitHubユーザー名:
example

リポジトリ名:
quiz-app
```

なら、

```text
https://example.github.io/quiz-app/
```

です。

---

## 17. 開発後の更新手順

機能を追加・修正したら、まずローカル環境で確認します。

```bash
npm run dev
```

問題なければGitへコミットします。

```bash
git status
git add .
git commit -m "Update quiz app"
git push
```

続いてGitHub Pagesを更新します。

```bash
npm run deploy
```

基本的な運用は、

```text
ソース修正
   ↓
npm run dev
   ↓
動作確認
   ↓
git add .
   ↓
git commit
   ↓
git push
   ↓
npm run deploy
   ↓
GitHub Pages確認
```

となります。

---

## 18. デプロイ前の確認

GitHub Pagesへ公開する前に、本番ビルドでも正常に動作するか確認すると安全です。

```bash
npm run build
npm run preview
```

問題なければ、

```bash
npm run deploy
```

を実行します。

---

## 19. 変更がGitHub Pagesに反映されない場合

`npm run deploy`が成功しても、変更がGitHub Pagesに反映されない場合があります。

まず最新のビルドを作り直します。

```bash
rm -rf dist
npm run build
```

本番ビルドを確認します。

```bash
npm run preview
```

最新の内容になっていることを確認してから、`gh-pages`のキャッシュを削除します。

Git Bashの場合：

```bash
rm -rf node_modules/.cache/gh-pages
```

再度デプロイします。

```bash
npm run deploy
```

---

## 20. gh-pagesブランチが更新されたか確認

GitHub Pagesに反映されない場合は、`gh-pages`ブランチが実際に更新されたか確認します。

```bash
git fetch origin gh-pages
```

続いて、

```bash
git log origin/gh-pages --oneline -5
```

例えば、

```text
bc32a44 Updates
0399339 Updates
c277418 Updates
```

のように最新コミットが表示されれば、`gh-pages`ブランチへのpushは成功しています。

さらに確認する場合は、

```bash
git ls-remote --heads origin gh-pages
```

を実行します。

---

## 21. gh-pagesは更新されているのに画面が古い場合

`gh-pages`ブランチが最新なら、次を確認します。

### GitHub Pagesの設定

GitHubで、

```text
Settings
  ↓
Pages
```

を開き、

```text
Source: Deploy from a branch
Branch: gh-pages
Folder: / (root)
```

になっていることを確認します。

### GitHub Actions

GitHubの、

```text
Actions
```

を開き、GitHub Pagesのデプロイ処理が成功しているか確認します。

### ブラウザキャッシュ

ブラウザに古いファイルが残っている可能性があります。

Chromeなどでは、

```text
Ctrl + Shift + R
```

で強制再読み込みします。

---

## 22. トラブル時の確認手順

GitHub Pagesに変更が反映されない場合は、次の順番で確認すると原因を切り分けやすくなります。

```text
① npm run dev
      ↓
開発版は最新か？

② rm -rf dist
   npm run build
      ↓
ビルド成功？

③ npm run preview
      ↓
本番ビルドは最新か？

④ rm -rf node_modules/.cache/gh-pages
   npm run deploy
      ↓
デプロイ成功？

⑤ git fetch origin gh-pages
   git log origin/gh-pages --oneline -5
      ↓
gh-pagesは更新されたか？

⑥ GitHub
   Settings → Pages
      ↓
gh-pages / rootになっているか？

⑦ GitHub → Actions
      ↓
Pagesのデプロイは成功したか？

⑧ Ctrl + Shift + R
      ↓
ブラウザキャッシュを更新
```

この順番で確認すると、

```text
Reactのソース
    ↓
Viteのビルド
    ↓
gh-pagesへのpush
    ↓
GitHub Pages
    ↓
ブラウザ
```

のどこで問題が発生しているか切り分けることができます。

---

## 23. Create React Appとの主な違い

Create React AppからViteへ移行する場合、主に以下が変わります。

| 項目             | Create React App      | Vite               |
| ---------------- | --------------------- | ------------------ |
| 開発サーバー     | `npm start`           | `npm run dev`      |
| 標準ポート       | 3000                  | 5173               |
| ビルド           | `react-scripts build` | `vite build`       |
| ビルド出力       | `build/`              | `dist/`            |
| HTML             | `public/index.html`   | `index.html`       |
| 設定ファイル     | react-scripts中心     | `vite.config.ts`   |
| GitHub Pages公開 | `gh-pages -d build`   | `gh-pages -d dist` |

---

## 24. よく使用するコマンド

### 開発

```bash
npm run dev
```

### ビルド

```bash
npm run build
```

### 本番ビルド確認

```bash
npm run preview
```

### GitHubへpush

```bash
git add .
git commit -m "Update"
git push
```

### GitHub Pagesへデプロイ

```bash
npm run deploy
```

### デプロイキャッシュ削除

```bash
rm -rf node_modules/.cache/gh-pages
```

### distを削除して再ビルド

```bash
rm -rf dist
npm run build
```

### gh-pagesの更新確認

```bash
git fetch origin gh-pages
git log origin/gh-pages --oneline -5
```

---

## 25. 推奨する日常の運用

通常の開発では、毎回`dist`やキャッシュを削除する必要はありません。

基本的には以下で運用します。

```bash
# 開発
npm run dev

# GitHubへ保存
git add .
git commit -m "Update"
git push

# GitHub Pagesへ公開
npm run deploy
```

変更が反映されない場合だけ、

```bash
rm -rf dist
rm -rf node_modules/.cache/gh-pages
npm run deploy
```

を試します。

それでも反映されない場合は、

```bash
git fetch origin gh-pages
git log origin/gh-pages --oneline -5
```

で`gh-pages`ブランチの更新状況を確認します。

---

## まとめ

React + TypeScript + Viteを使用した開発からGitHub Pagesへの公開までの基本的な流れは以下です。

```text
React + TypeScript
        ↓
   npm run dev
        ↓
     開発・確認
        ↓
      Git commit
        ↓
      Git push
        ↓
   npm run build
        ↓
       dist/
        ↓
   npm run deploy
        ↓
   gh-pages branch
        ↓
    GitHub Pages
```

普段は、

```bash
npm run dev
npm run deploy
```

を中心に開発・公開を行い、問題が発生した場合に`dist`、`gh-pages`、GitHub Pages、ブラウザキャッシュの順に確認すると効率的です。
