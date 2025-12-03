## React アプリの作成

### 1️⃣ Create React App でプロジェクトを作成

```bash
npx create-react-app my-react-app --template typescript

```

### 2️⃣ プロジェクトフォルダに移動

```lua
cd my-react-app
```

### 3️⃣ 開発サーバーを起動する

```
npm start

```

### 4️⃣ フォルダ構成のイメージ

Create React App + TypeScript で作ると、だいたいこんな構成になります：

```
my-react-app/
  ├─ node_modules/      ← ライブラリ群（さわらない）
  ├─ public/            ← 画像や index.html など
  ├─ src/               ← 自分が主に編集する場所
  │   ├─ App.tsx        ← メインのコンポーネント
  │   ├─ index.tsx      ← React を画面に描画するエントリ
  │   ├─ react-app-env.d.ts
  │   ├─ reportWebVitals.ts
  │   └─ setupTests.ts  など
  ├─ package.json       ← 使用ライブラリやスクリプト
  ├─ tsconfig.json      ← TypeScript の設定
  └─ README.md

```

最初は src/App.tsx と src/index.tsx だけ意識していれば OK です。

### 5️⃣ 実際に画面の文字を変えてみる

```tsx
import React from "react";

function App() {
  return <h1>Hello React + TypeScript (CRA)!</h1>;
}

export default App;
```

### 6️⃣ よく使う npm スクリプト

package.json の scripts に定義されています。

- 開発サーバー起動：

```
npm start
```

- 本番用ビルド：

```
npm run build
```

build/ フォルダに静的ファイルが生成されます。

- テスト実行：

```
npm test
```
