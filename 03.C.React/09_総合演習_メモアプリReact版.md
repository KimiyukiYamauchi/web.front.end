# 第9回 総合演習：メモアプリ（React版）

<!-- TOC -->

## 目次

- [目次](#目次)
- [今回のゴール](#今回のゴール)
- [1. Vanilla JS版とReact版の対応整理](#1-vanilla-js版とreact版の対応整理)
- [2. 総合演習：簡易メモアプリ（React版）](#2-総合演習簡易メモアプリreact版)
  - [2.1 要件](#21-要件)
  - [2.2 ひな形（`memo.react.tl` リポジトリの構成）](#22-ひな形memoreacttl-リポジトリの構成)
  - [2.3 手順（`memo.react.tl` リポジトリの提出フロー）](#23-手順memoreacttl-リポジトリの提出フロー)
  - [2.4 追加機能の実装ヒント](#24-追加機能の実装ヒント)
  - [2.5 実装イメージ](#25-実装イメージ)
  - [2.6 実装のチェックポイント](#26-実装のチェックポイント)
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
| `memoList[i] = newText`（要素を書き換える） | `setMemoList(memoList.map(...))`（`map`で新しい配列を作る） |
| `input.classList.add("error")` | `className={hasError ? ... : ...}`（stateでクラスを切り替える） |
| `renderMemoList()`（手動で画面を再構築） | **不要**（stateが変わると自動的に再描画される） |

**この「手動で画面を作り直す関数が不要になる」という点こそが、ReactがVanilla JSと最も違うところです。** 実装に入る前に、この感覚をもう一度確認しておきましょう。

---

## 2. 総合演習：簡易メモアプリ（React版）

**これがモジュールCの最終課題です。** 第8回の買い物リストで作った「入力 → 追加 → 一覧 → 削除」の構造を土台に、**日時表示・入力チェック・件数表示・編集**の機能を加えたメモアプリを完成させます。

### 2.1 要件

**基本機能**（第6回のVanilla JS版・第8回の買い物リストと同じ）

- テキストフィールドにメモを入力できる（制御コンポーネント）
- 「追加」ボタンをクリックすると、入力した内容がメモ一覧に追加される
- 追加された各メモには「削除」ボタンを表示する
- 「削除」ボタンをクリックすると、対象のメモが一覧から削除される
- CSS Modulesでスタイリングする（第8回の内容）

**追加機能**（今回の課題のポイント）

1. **Enterキーで追加**：入力欄でEnterキーを押しても追加できる
2. **作成日時の表示**：各メモに、追加した日時を表示する
3. **入力チェック**：空のまま追加しようとしたら、入力欄を赤枠にし、「メモを入力してください」とエラーメッセージを表示する。入力を始めたらエラー表示を消す
4. **件数表示**：「メモ一覧（3件）」のようにメモの件数を表示する。0件のときは「メモはまだありません」と表示する
5. **編集機能**：各メモに「編集」ボタンを表示する。クリックするとそのメモが入力欄に切り替わり、「保存」で内容を更新、「キャンセル」で元に戻す

### 2.2 ひな形（`memo.react.tl` リポジトリの構成）

ひな形は [memo.react.tl](https://github.com/KimiyukiYamauchi/memo.react.tl) リポジトリの `main` ブランチです。第7回で作成したViteのプロジェクトと同じ構成になっています。

```text
memo.react.tl/
├── README.md
├── index.html
├── package.json
└── src/
    ├── main.tsx          ← 変更不要
    ├── index.css         ← 変更不要
    ├── App.tsx           ← ここに処理を書いていく
    └── App.module.css    ← スタイル（自由にアレンジしてかまいません）
```

`src/App.tsx`（配布済みのひな形）：

```tsx
import styles from "./App.module.css";

// ここに処理を記述する
// （下のJSXは完成イメージです。stateとmap()を使って書き換えていきましょう）

function App() {
  return (
    <div className={styles.container}>
      <h1 className={styles.title}>簡単メモアプリ</h1>

      <div className={styles.form}>
        <input className={styles.input} placeholder="メモを入力" />
        <button className={styles.addButton}>追加</button>
      </div>

      <p className={styles.subtitle}>メモ一覧（1件）</p>
      <ul className={styles.memoList}>
        <li className={styles.memoItem}>
          <div>
            <p className={styles.memoText}>買い物に行く</p>
            <p className={styles.date}>2026/10/8 10:00:00</p>
          </div>
          <div className={styles.buttons}>
            <button>編集</button>
            <button>削除</button>
          </div>
        </li>
      </ul>
    </div>
  );
}

export default App;
```

`<ul>` の中の `<li>` は、メモ1件分の表示イメージです。`map()` でメモを表示するときは、この `<li>` と同じ構造・クラス名にすると、`src/App.module.css` のスタイルがそのまま適用されます。`App.module.css` には、エラー表示用の `.error` や `.errorMessage`、0件表示用の `.empty` などのクラスもあらかじめ用意されています（中身は [10_総合演習.実装例.md](10_総合演習.実装例.md) の `App.module.css` と同じです）。

### 2.3 手順（`memo.react.tl` リポジトリの提出フロー）

1. **リポジトリをクローンする**（[memo.react.tl](https://github.com/KimiyukiYamauchi/memo.react.tl) リポジトリ）

   ```bash
   git clone https://github.com/KimiyukiYamauchi/memo.react.tl.git
   cd memo.react.tl
   ```

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
   npm run dev
   ```

   ブラウザで `http://localhost:5173` にアクセスして確認しながら実装します。

5. 上記の要件（基本機能 → 追加機能1〜5の順がおすすめ）を実装する
6. **GitHubにpushする**

   ```bash
   git push origin <学生番号>
   # 例： git push origin t26001
   ```

### 2.4 追加機能の実装ヒント

どの機能も、第7回・第8回で学んだ知識の組み合わせで作れます。

**1. Enterキーで追加**（第8回1.3のイベントオブジェクト）

```tsx
const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
  // isComposing：日本語の変換中に押したEnterでは追加しない
  if (e.key === "Enter" && !e.nativeEvent.isComposing) {
    handleAdd();
  }
};

<input onKeyDown={handleKeyDown} /* value・onChange も忘れずに */ />
```

**2. 作成日時の表示**（第8回3.3のオブジェクトの配列）

`Memo` 型にプロパティを増やし、追加するときに日時を文字列で保存します。

```tsx
type Memo = { id: number; text: string; createdAt: string };

setMemoList([
  ...memoList,
  { id: Date.now(), text, createdAt: new Date().toLocaleString() },
]);
```

**3. 入力チェック**（第7回の `&&`、第8回4.3のクラスの切り替え）

エラー中かどうかを `boolean` のstateで管理し、それに応じて表示を切り替えます。

```tsx
const [hasError, setHasError] = useState(false);

<input className={hasError ? `${styles.input} ${styles.error}` : styles.input} />
{hasError && <p className={styles.errorMessage}>メモを入力してください</p>}
```

**4. 件数表示**

配列の要素数は `memoList.length` で取得できます。0件のときの表示は `&&` で切り替えます。

**5. 編集機能**（第8回3.3の `map` による更新）

「どのメモを編集中か」と「編集中のテキスト」を、それぞれstateで管理します。

```tsx
const [editingId, setEditingId] = useState<number | null>(null); // null = 編集中のメモなし
const [editText, setEditText] = useState("");
```

- 「編集」ボタン：`setEditingId(memo.id)` と `setEditText(memo.text)` で編集モードにする
- 表示の切り替え：`editingId === memo.id` が `true` のメモだけ、`<input>` と「保存」「キャンセル」ボタンを表示する（三項演算子 `条件 ? A : B` を使う）
- 「保存」ボタン：`map` で対象のメモだけ `{ ...memo, text: editText }` に置き換えた新しい配列を作り、`setEditingId(null)` で編集モードを終える
- 「キャンセル」ボタン：`setEditingId(null)` だけでよい（`memoList` は変更しない）

### 2.5 実装イメージ

実装イメージ（`App.tsx` と `App.module.css`）は [10_総合演習.実装例.md](10_総合演習.実装例.md) にあります。

### 2.6 実装のチェックポイント

- `memoList.push(...)` のように配列を直接書き換えていないか（必ず `setMemoList([...memoList, ...])` の形にする）
- 編集の保存で `memo.text = editText` のようにオブジェクトを直接書き換えていないか（`map` とスプレッド構文で新しいオブジェクトを作る）
- `<input>` に `value` と `onChange` の両方が設定されているか（片方だけだと入力できない、またはstateと表示がズレる）。編集用の `<input>` も同様
- `<li>` に `key` を指定しているか（第8回3.2の復習）
- `useState` の型（`Memo[]`、`number | null` など）をTypeScriptで指定しているか
- 日本語入力の変換確定のEnterで、メモが追加されてしまわないか

---

## 3. 発展課題（時間が余ったら／持ち帰り課題）

- 検索欄をつけて、入力した文字を含むメモだけを表示する（`filter` と `includes` を組み合わせる。`memoList` 自体は書き換えず、表示用の配列を作る）
- 「削除」の前に確認ダイアログを出す（`window.confirm("削除しますか？")`）
- 「新しい順／古い順」の並び替えボタンをつける（`[...memoList].sort(...)` のように、コピーしてから並び替える）
- 重要なメモにチェックをつけ、背景色を変える（`Memo` 型に `important: boolean` を追加。第8回3.3のトグルの応用）
- 編集中にEnterキーで保存、Escキーでキャンセルできるようにする
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
