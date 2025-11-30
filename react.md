## React アプリの作成

### 1. プロジェクトを作成する

```bash
npx create-react-app (プロジェクト名)
```

(例)

```bash
npx create-react-app my-react
```

### 2. プロジェクトの内容を確認する

```lua
/                           # プロジェクトルート
├── /node_modules        # ライブラリ一式
├── public/
│   ├── favicon.ico     # ファビコン
│   ├── index.html      # トップページ
│   ├── logoXxx.png     # ロゴ画像
│   └── manifest.json   # アプリの構成情報
├── src/
│   ├── App.css         # Appコンポーネントのスタイル
│   ├── App.js          # Appコンポーネントの本体
│   ├── App.test.js     # Appコンポーネントのテストコード
│   ├── index.css       # アプリ共通のスタイル
│   ├── index.js        # 起動ファイル
│   ├── logo.svg        # ロゴ画像
│   ├── reportWebVitals.js # パフォーマンス監視のためのサービス
│   └── setupTests.js   # テストの初期設定
└── package.json
```

### 3. アプリを実行する

```
npm start
```
