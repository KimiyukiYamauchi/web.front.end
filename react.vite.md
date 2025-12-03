## React アプリの作成

### 1. Vite プロジェクトを作成

```bash
npm create vite@latest (プロジェクト名) --template react-ts

```

(例)

```bash
npm create vite@latest my-react-app --template react-ts

✔ Select a framework: › React
✔ Select a variant: › TypeScript

```

### 2. 作成したフォルダへ移動

```lua
cd my-react-app
```

### 3. 依存パッケージをインストール

```
npm install
```

### 4. 開発サーバーを起動

```
npm run dev
```

成功すると：

```arduino
  VITE v5.x.x  ready in 300 ms

  ➜  Local:   http://localhost:5173/

```

### 5. 開発サーバーを起動

```pgsql
my-react-app/
  ├─ src/
  │   ├─ App.tsx
  │   ├─ main.tsx
  │   └─ assets
  ├─ index.html
  ├─ tsconfig.json
  ├─ vite.config.ts
  └─ package.json

```

### 6. コードを編集してみよう

```tsx
function App() {
  return <h1>Hello React + TypeScript!</h1>;
}

export default App;
```
