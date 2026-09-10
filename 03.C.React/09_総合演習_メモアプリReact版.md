# 第9回 総合演習：メモアプリ（React版）

<!-- TOC -->

## 目次

- [目次](#目次)
- [今回のゴール](#今回のゴール)
- [1. Vanilla JS版とReact版の対応整理](#1-vanilla-js版とreact版の対応整理)
- [2. 総合演習：簡易メモアプリ（React版）](#2-総合演習簡易メモアプリreact版)
  - [2.1 要件（第6回のVanilla JS版と同じ機能要件）](#21-要件第6回のvanilla-js版と同じ機能要件)
  - [2.2 手順（`memo.react` リポジトリの提出フロー）](#22-手順memoreact-リポジトリの提出フロー)
  - [2.3 実装イメージ](#23-実装イメージ)
  - [2.4 実装のチェックポイント](#24-実装のチェックポイント)
- [3. 発展課題（時間が余ったら／持ち帰り課題）](#3-発展課題時間が余ったら持ち帰り課題)
- [モジュールC 総復習（第7〜9回）](#モジュールc-総復習第79回)
- [次回予告](#次回予告)
- [参考リンク](#参考リンク)

<!-- /TOC -->

## 今回のゴール

- Vanilla JS版（第6回）とReact版の書き方の対応関係を整理する
- モジュールC最終課題「簡易メモアプリ（React版）」を完成させ、GitHubへ提出する

---

## 1. Vanilla JS版とReact版の対応整理

第6回で作ったメモアプリ（Vanilla JS版）を思い出しながら、React版でどう書き換わるかを整理します。

| Vanilla JS（第6回） | React |
|---|---|
| `let memoList = [];` | `const [memoList, setMemoList] = useState<string[]>([]);` |
| `document.getElementById()` | 基本的に使用しない（JSXとstateで完結する） |
| `input.value` | `value={inputText}`（制御コンポーネント） |
| `addButton.addEventListener("click", ...)` | `<button onClick={handleAdd}>` |
| `innerHTML` で組み立てる | JSXで宣言的に書く |
| `memoList.push(text)` | `setMemoList([...memoList, text])` |
| `memoList.filter((_, i) => i !== index)` | 同じ（`filter`はReactでも同様に使う） |
| `renderMemoList()`（手動で画面を再構築） | **不要**（stateが変わると自動的に再描画される） |

**この「手動で画面を作り直す関数が不要になる」という点こそが、ReactがVanilla JSと最も違うところです。** 第9回の実装に入る前に、この感覚をもう一度確認しておきましょう。

---

## 2. 総合演習：簡易メモアプリ（React版）

**これがモジュールCの最終課題です。** 第8回で作った買い物リストコンポーネントとほぼ同じ構造で、メモアプリを完成させます。

### 2.1 要件（第6回のVanilla JS版と同じ機能要件）

- テキストフィールドにメモを入力できる（制御コンポーネント）
- 「追加」ボタンをクリックすると、入力した内容がメモ一覧に追加される
- 追加された各メモには「削除」ボタンを表示する
- 「削除」ボタンをクリックすると、対象のメモが一覧から削除される
- CSS Modulesでスタイリングする（第8回の内容）

### 2.2 手順（`memo.react` リポジトリの提出フロー）

1. **リポジトリをクローンする**（`memo.react` リポジトリ）
2. **ブランチを作成して切り替える**（自分の学生番号を使用）

   ```bash
   git switch -c <学生番号>
   # 例： git switch -c t26001
   ```

3. **必要なパッケージをインストールする**

   ```bash
   npm install
   ```

4. **開発サーバーを起動する**

   ```bash
   npm start
   ```

   ブラウザで `http://localhost:3000` にアクセスして確認しながら実装します。

5. 上記の要件（入力・追加・削除）を実装する
6. **GitHubにpushする**

   ```bash
   git push origin <学生番号>
   # 例： git push origin t26001
   ```

### 2.3 実装イメージ

`App.tsx`：

```tsx
import { useState } from "react";
import styles from "./App.module.css";

type Memo = { id: number; text: string };

function App() {
  const [memoList, setMemoList] = useState<Memo[]>([]);
  const [inputText, setInputText] = useState("");

  const handleAdd = () => {
    const text = inputText.trim();
    if (text === "") return;

    setMemoList([...memoList, { id: Date.now(), text }]);
    setInputText("");
  };

  const handleDelete = (id: number) => {
    setMemoList(memoList.filter((memo) => memo.id !== id));
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>簡単メモアプリ</h1>

      <div className={styles.form}>
        <input
          className={styles.input}
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="メモを入力"
        />
        <button className={styles.addButton} onClick={handleAdd}>
          追加
        </button>
      </div>

      <p className={styles.subtitle}>メモ一覧</p>
      <ul className={styles.memoList}>
        {memoList.map((memo) => (
          <li key={memo.id} className={styles.memoItem}>
            <p>{memo.text}</p>
            <button onClick={() => handleDelete(memo.id)}>削除</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
```

`App.module.css`（例。第8回の内容を活かして自由にアレンジしてよい）：

```css
.container {
  max-width: 480px;
  margin: 40px auto;
  font-family: sans-serif;
}

.title {
  font-size: 24px;
}

.form {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
}

.input {
  flex: 1;
  padding: 8px;
}

.addButton {
  padding: 8px 16px;
}

.subtitle {
  font-weight: bold;
  margin-top: 24px;
}

.memoList {
  list-style: none;
  padding: 0;
}

.memoItem {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px;
  border-bottom: 1px solid #eee;
}
```

### 2.4 実装のチェックポイント

- `memoList.push(...)` のように配列を直接書き換えていないか（必ず `setMemoList([...memoList, ...])` の形にする）
- `<input>` に `value` と `onChange` の両方が設定されているか（片方だけだと入力できない、またはstateと表示がズレる）
- `<li>` に `key` を指定しているか（第8回3.2の復習）
- `useState` の型（`Memo[]` など）をTypeScriptで指定しているか

---

## 3. 発展課題（時間が余ったら／持ち帰り課題）

- メモの追加日時を各メモに表示する（`new Date().toLocaleString()`）
- 空メモを追加しようとしたら、入力欄を赤く光らせる（CSS Modulesで `.error` クラスを条件付きで適用）
- メモの編集機能をつける（クリックで編集モードに切り替え、`useState` で編集中のIDを管理する）
- メモを `localStorage` に保存し、ページを再読み込みしても消えないようにする（第6回2.3のJSON.stringify/JSON.parseの考え方をReactの `useEffect` と組み合わせる。`useEffect` は今後の書籍ハンズオンで登場します）

---

## モジュールC 総復習（第7〜9回）

| 回 | テーマ | 一言でいうと |
|---|---|---|
| 第7回 | Reactの基礎 | コンポーネント・JSX・props・useStateという部品の作り方 |
| 第8回 | イベント処理・リスト表示・スタイリング | ユーザー操作への反応と、配列データの表示・見た目の整え方 |
| 第9回 | 総合演習：メモアプリ（React版） | ここまでの知識を組み合わせて、1つのアプリを完成させる |

Vanilla JS（モジュールB）と比べると、Reactは「DOMを直接操作する」代わりに「**stateを更新すれば、画面は勝手についてくる**」という考え方に大きく変わりました。この考え方は、第10回以降のNext.jsハンズオンでも一貫して使われます。

## 次回予告

第10回からは、書籍『Next.js + ヘッドレスCMSではじめるかんたんモダンＷｅｂサイト制作入門』の目次に沿ったハンズオンが始まります。Next.jsのプロジェクト構成、ディレクトリ構成、そして今日学んだコンポーネント・props・stateの考え方が、そのままNext.jsの中でも活かされていきます。

## 参考リンク

- React公式ドキュメント（日本語）：https://ja.react.dev/learn/state-a-components-memory
- 同：https://ja.react.dev/learn/updating-arrays-in-state
