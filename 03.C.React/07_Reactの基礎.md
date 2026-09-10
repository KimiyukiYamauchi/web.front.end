# 第7回 Reactの基礎

<!-- TOC -->

## 目次

- [目次](#目次)
- [今回のゴール](#今回のゴール)
- [モジュールCの位置づけ](#モジュールcの位置づけ)
- [1. 環境構築（CRA + TypeScriptテンプレート）](#1-環境構築cra-typescriptテンプレート)
  - [1.1 プロジェクトの作成](#11-プロジェクトの作成)
  - [1.2 フォルダ構成](#12-フォルダ構成)
  - [1.3 画面の文字を変えてみる](#13-画面の文字を変えてみる)
  - [1.4 よく使うnpmスクリプト](#14-よく使うnpmスクリプト)
- [2. コンポーネントとJSX](#2-コンポーネントとjsx)
  - [2.1 コンポーネントとは](#21-コンポーネントとは)
  - [2.2 JSXの基本ルール](#22-jsxの基本ルール)
  - [2.3 コンポーネントは1つの要素を返す](#23-コンポーネントは1つの要素を返す)
- [3. props](#3-props)
  - [3.1 propsとは](#31-propsとは)
  - [3.2 複数のpropsを渡す](#32-複数のpropsを渡す)
- [4. state（useState）](#4-stateusestate)
  - [4.1 なぜstateが必要か](#41-なぜstateが必要か)
  - [4.2 useStateの基本](#42-usestateの基本)
  - [4.3 文字列のstate（入力欄と組み合わせる）](#43-文字列のstate入力欄と組み合わせる)
- [5. 総合演習：自己紹介カードコンポーネント](#5-総合演習自己紹介カードコンポーネント)
  - [完成イメージ](#完成イメージ)
  - [発展課題（時間が余ったら）](#発展課題時間が余ったら)
- [まとめ・次回予告](#まとめ次回予告)
- [参考リンク](#参考リンク)

<!-- /TOC -->

## 今回のゴール

- Create React App（TypeScriptテンプレート）でReactプロジェクトを作成し、開発サーバーを起動できる
- コンポーネントとJSXの基本ルールを理解する
- props（親から子へのデータの受け渡し）を理解する
- state（`useState`）で「変化する値」を扱えるようになる
- 総合演習として、props・stateを使った自己紹介カードコンポーネントを作成する

## モジュールCの位置づけ

第3〜6回（モジュールB）でVanilla JavaScriptの基礎を身につけました。ここからの3回（第7〜9回）では、Vanilla JSで書いていた処理をReactでどう書き直すかを学びます。第6回で作ったメモアプリ（Vanilla JS版）を、第9回でReact版として作り直すのが最終ゴールです。

---

## 1. 環境構築（CRA + TypeScriptテンプレート）

### 1.1 プロジェクトの作成

```bash
npx create-react-app my-react-app --template typescript
cd my-react-app
npm start
```

`npm start` で開発サーバーが起動し、`http://localhost:3000` に自動でブラウザが開きます。ファイルを保存すると自動で画面がリロードされます（ホットリロード）。

### 1.2 フォルダ構成

Create React App + TypeScript で作ると、だいたい次のような構成になります。

```text
my-react-app/
  ├─ node_modules/      ← ライブラリ群（さわらない）
  ├─ public/            ← 画像や index.html など
  ├─ src/                ← 自分が主に編集する場所
  │   ├─ App.tsx        ← メインのコンポーネント
  │   ├─ index.tsx      ← Reactを画面に描画するエントリ
  │   ├─ react-app-env.d.ts
  │   ├─ reportWebVitals.ts
  │   └─ setupTests.ts  など
  ├─ package.json       ← 使用ライブラリやスクリプト
  ├─ tsconfig.json      ← TypeScriptの設定
  └─ README.md
```

**最初は `src/App.tsx` と `src/index.tsx` だけ意識していればOK**です。

### 1.3 画面の文字を変えてみる

```tsx
import React from "react";

function App() {
  return <h1>Hello React + TypeScript (CRA)!</h1>;
}

export default App;
```

`src/App.tsx` を保存すると、ブラウザの表示が自動で切り替わることを確認しましょう。

### 1.4 よく使うnpmスクリプト

| コマンド | 内容 |
|---|---|
| `npm start` | 開発サーバー起動（`http://localhost:3000`） |
| `npm run build` | 本番用ビルド（`build/` フォルダに静的ファイルを生成） |
| `npm test` | テスト実行 |

---

## 2. コンポーネントとJSX

### 2.1 コンポーネントとは

Reactでは、画面をコンポーネント（部品）に分割して作ります。コンポーネントは「UIを返す関数」です。

```tsx
function Hello() {
  return <h1>こんにちは、React！</h1>;
}

export default Hello;
```

- コンポーネント名は **パスカルケース**（`Hello`, `UserCard` のように先頭大文字）にする
- 関数の中で **JSX**（HTMLのように見える構文）を `return` する

### 2.2 JSXの基本ルール

JSXはHTMLに似ていますが、いくつか異なるルールがあります。

```tsx
function Profile() {
  const name = "田中太郎";
  const age = 20;

  return (
    <div className="profile">
      {/* {} の中にJavaScriptの式を埋め込める */}
      <h2>{name}さんのプロフィール</h2>
      <p>年齢: {age}歳</p>
      <p>来年は{age + 1}歳になります</p>
    </div>
  );
}
```

主な違い：

| HTML | JSX | 理由 |
|---|---|---|
| `class="..."` | `className="..."` | `class` はJavaScriptの予約語のため |
| `<input>`（閉じタグ省略可） | `<input />`（自己終了タグ必須） | JSXはすべてのタグを閉じる必要がある |
| `onclick="..."` | `onClick={...}` | イベント名はキャメルケース（第8回で詳しく扱う） |
| 値埋め込みなし | `{式}` | `{}` の中にJavaScriptの式を書ける |

### 2.3 コンポーネントは1つの要素を返す

JSXは **1つのルート要素** しか返せません。複数の要素を返したい場合は `<div>` で囲むか、`<>...</>`（Fragment）を使います。

```tsx
// NG：2つの要素を並べて返すことはできない
// return (
//   <h1>タイトル</h1>
//   <p>本文</p>
// );

// OK：Fragmentで囲む（余計なdivを増やしたくないときに便利）
function Article() {
  return (
    <>
      <h1>タイトル</h1>
      <p>本文</p>
    </>
  );
}
```

**やってみよう**：`Profile` コンポーネントを参考に、自分の名前・出身地・好きなものを表示する `MyProfile` コンポーネントを作ってみましょう。

---

## 3. props

### 3.1 propsとは

props（プロパティ）は、**親コンポーネントから子コンポーネントへデータを渡す仕組み**です。関数の引数のようなイメージです。

```tsx
// 子コンポーネント：propsを受け取って表示するだけ
type GreetingProps = {
  name: string;
};

function Greeting({ name }: GreetingProps) {
  return <p>こんにちは、{name}さん！</p>;
}

// 親コンポーネント：Greetingにpropsを渡す
function App() {
  return (
    <div>
      <Greeting name="佐藤" />
      <Greeting name="鈴木" />
    </div>
  );
}
```

- `<Greeting name="佐藤" />` のように、HTML属性のような形でpropsを渡す
- 子コンポーネントは `{ name }` のように**分割代入**で受け取るのが一般的（第3回で学んだ分割代入がここで使われる）
- propsは **読み取り専用**。子コンポーネントの中でpropsの値を直接書き換えることはできない

### 3.2 複数のpropsを渡す

```tsx
type UserCardProps = {
  name: string;
  age: number;
  isStudent: boolean;
};

function UserCard({ name, age, isStudent }: UserCardProps) {
  return (
    <div className="user-card">
      <h3>{name}</h3>
      <p>{age}歳</p>
      {isStudent && <p>学生です</p>}
      {/* isStudentがtrueのときだけ<p>を表示する、よく使う書き方 */}
    </div>
  );
}

function App() {
  return <UserCard name="田中太郎" age={20} isStudent={true} />;
}
```

**ポイント**：`{isStudent && <p>学生です</p>}` は「isStudentがtrueなら右側を表示、falseなら何も表示しない」という頻出パターンです。第3回で学んだ論理演算子（`&&`）の応用だと考えると理解しやすいです。

---

## 4. state（useState）

### 4.1 なぜstateが必要か

propsは親から渡される「読み取り専用」のデータでした。一方、**コンポーネント自身が持つ、変化する値**を扱うには `useState` というReactの機能（Hook）を使います。

Vanilla JS（第6回まで）では、値が変わるたびに `document.getElementById()` で画面を書き換える必要がありました。Reactでは、**stateが変わると画面が自動的に再描画される**のが最大の違いです。

### 4.2 useStateの基本

```tsx
import { useState } from "react";

function Counter() {
  // useState(初期値) は [現在の値, 値を更新する関数] の配列を返す
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>カウント: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
      <button onClick={() => setCount(count - 1)}>-1</button>
    </div>
  );
}
```

- `const [count, setCount] = useState(0);` ← 配列の分割代入（第3回の復習）
- `count` は現在の値、`setCount` はその値を更新するための関数
- `setCount(...)` を呼ぶと、Reactが自動的にコンポーネントを再描画し、画面上の `{count}` の表示が更新される
- **`count = count + 1` のように直接書き換えてはいけない**。必ず `setCount(...)` を使う

### 4.3 文字列のstate（入力欄と組み合わせる）

```tsx
import { useState } from "react";

function NameInput() {
  const [name, setName] = useState("");

  return (
    <div>
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <p>入力中の名前: {name}</p>
    </div>
  );
}
```

この「`value` と `onChange` をセットでstateにつなげる」書き方は、第8回で「制御コンポーネント」として詳しく扱います。ここでは「入力欄の中身もstateで管理できる」ということだけ押さえておきましょう。

---

## 5. 総合演習：自己紹介カードコンポーネント

props（名前・自己紹介文）とstate（「いいね」カウント）を組み合わせて、自己紹介カードを作ります。

### 完成イメージ

- 名前と自己紹介文をpropsで受け取り、カード状に表示する
- 「いいね」ボタンを押すと、カウントが増える（useState）

```tsx
import { useState } from "react";

type ProfileCardProps = {
  name: string;
  bio: string;
};

function ProfileCard({ name, bio }: ProfileCardProps) {
  const [likeCount, setLikeCount] = useState(0);

  return (
    <div className="profile-card">
      <h3>{name}</h3>
      <p>{bio}</p>
      <button onClick={() => setLikeCount(likeCount + 1)}>
        いいね！ {likeCount}
      </button>
    </div>
  );
}

function App() {
  return (
    <div>
      <ProfileCard name="田中太郎" bio="Webフロントエンドを勉強中です。" />
      <ProfileCard name="佐藤花子" bio="Reactが好きです。" />
    </div>
  );
}

export default App;
```

### 発展課題（時間が余ったら）

- 「いいね」を10回押したら「ありがとう！」のメッセージを表示する（`{likeCount >= 10 && <p>...</p>}`）
- カードの色をpropsで受け取り、`style={{ backgroundColor: color }}` で切り替える
- 自己紹介カードを3人分、配列＋`map()`で表示してみる（第8回の予告）

---

## まとめ・次回予告

- CRA + TypeScriptでReactプロジェクトを作成し、`npm start` で開発サーバーを起動できるようになった
- コンポーネントは「UIを返す関数」であり、JSXにはHTMLとは異なるルール（className、自己終了タグ、`{}`埋め込み）があることを学んだ
- props（親→子への読み取り専用データ）とstate（コンポーネント自身が持つ、変化する値）の違いを理解した
- 自己紹介カードで、props・useStateを組み合わせて実装した

次回（第8回）は、イベント処理・制御コンポーネント・`map()`によるリスト表示・CSS Modulesを学びます。今日軽く触れた `onClick` や `value`/`onChange` を、本格的に扱っていきます。

## 参考リンク

- React公式ドキュメント（日本語）：https://ja.react.dev/learn
- 同：https://ja.react.dev/learn/your-first-component
- 同：https://ja.react.dev/learn/passing-props-to-a-component
- 同：https://ja.react.dev/learn/state-a-components-memory
