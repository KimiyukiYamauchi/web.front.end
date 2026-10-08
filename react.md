## React アプリの作成

### 1️⃣ Vite でプロジェクトを作成

```bash
npm create vite@latest my-react-app -- --template react-ts
```

### 2️⃣ プロジェクトフォルダに移動して、パッケージをインストール

```bash
cd my-react-app
npm install
```

### 3️⃣ 開発サーバーを起動する

```bash
npm run dev
```

ターミナルに表示される `http://localhost:5173/` をブラウザで開きます。止めるときは `Ctrl + C` です。

### 4️⃣ フォルダ構成のイメージ

Vite + TypeScript（`react-ts` テンプレート）で作ると、だいたいこんな構成になります：

```
my-react-app/
  ├─ node_modules/      ← ライブラリ群（さわらない）
  ├─ public/            ← favicon などの静的ファイル
  ├─ src/               ← 自分が主に編集する場所
  │   ├─ assets/        ← 画像など
  │   ├─ App.tsx        ← メインのコンポーネント
  │   ├─ App.css
  │   ├─ main.tsx       ← React を画面に描画するエントリ
  │   └─ index.css
  ├─ index.html         ← アプリの入口となる HTML（プロジェクト直下にある）
  ├─ package.json       ← 使用ライブラリやスクリプト
  ├─ tsconfig.json      ← TypeScript の設定
  ├─ vite.config.ts     ← Vite の設定
  └─ README.md
```

最初は src/App.tsx と src/main.tsx だけ意識していれば OK です。

### 5️⃣ 実際に画面の文字を変えてみる

```tsx
function App() {
  return <h1>Hello React + TypeScript (Vite)!</h1>;
}

export default App;
```

### 6️⃣ よく使う npm スクリプト

package.json の scripts に定義されています。

- 開発サーバー起動：

```
npm run dev
```

- 本番用ビルド：

```
npm run build
```

dist/ フォルダに静的ファイルが生成されます。

- ビルド結果の確認：

```
npm run preview
```

- コードのチェック（ESLint）：

```
npm run lint
```
