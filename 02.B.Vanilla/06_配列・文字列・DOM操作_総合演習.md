# 第6回 配列・文字列・DOM操作／総合演習

<!-- TOC -->

## 目次

- [今回のゴール](#今回のゴール)
- [1. 配列の基本操作とメソッド](#1-配列の基本操作とメソッド)
  - [1.1 生成・アクセス・変更](#11-生成アクセス変更)
  - [1.2 スプレッド演算子・分割代入（第3回の復習）](#12-スプレッド演算子分割代入第3回の復習)
  - [1.3 `forEach` / `map` / `filter` / `reduce`（重要・頻出）](#13-foreach-map-filter-reduce重要頻出)
  - [1.4 その他のES6配列メソッド](#14-その他のes6配列メソッド)
- [2. 文字列操作／JSONの基本](#2-文字列操作jsonの基本)
  - [2.1 文字列の連結・部分取得・検索](#21-文字列の連結部分取得検索)
  - [2.2 split / join / replace](#22-split-join-replace)
  - [2.3 JSONの基本（parse / stringify）](#23-jsonの基本parse-stringify)
- [3. DOM操作の基本](#3-dom操作の基本)
  - [3.1 要素の取得](#31-要素の取得)
  - [3.2 要素の作成と追加](#32-要素の作成と追加)
  - [3.3 イベント処理](#33-イベント処理)
- [4. 総合演習：簡易メモアプリ（Vanilla JS版）](#4-総合演習簡易メモアプリvanilla-js版)
  - [4.1 要件](#41-要件)
  - [4.2 ひな形（`memo.js` リポジトリの構成）](#42-ひな形memojs-リポジトリの構成)
  - [4.3 手順（`memo.js` リポジトリの提出フロー）](#43-手順memojs-リポジトリの提出フロー)
  - [発展課題（時間が余ったら／持ち帰り課題）](#発展課題時間が余ったら持ち帰り課題)
- [モジュールB総復習（第3〜6回）](#モジュールb総復習第36回)
- [参考リンク](#参考リンク)

<!-- /TOC -->

## 今回のゴール

- 配列の基本操作と、`forEach` / `map` / `filter` / `reduce` を使い分けられるようになる
- 文字列の基本操作（連結・部分取得・検索・置換）ができるようになる
- DOM操作（要素の取得・作成・追加、イベント処理）の基本を理解する
- 総合演習として「簡易メモアプリ（Vanilla JS版）」を完成させ、GitHubに提出する（**このモジュールの最終課題**）

---

## 1. 配列の基本操作とメソッド

### 1.1 生成・アクセス・変更

```js
const fruits = ["apple", "banana", "cherry"];
console.log(fruits[0]); // apple
fruits[1] = "blueberry"; // 要素の変更
console.log(fruits.length); // 3

fruits.push("orange"); // 末尾に追加
fruits.pop(); // 末尾を削除
fruits.unshift("mango"); // 先頭に追加
fruits.shift(); // 先頭を削除
```

### 1.2 スプレッド演算子・分割代入（第3回の復習）

```js
const fruits1 = ["apple", "banana"];
const fruits2 = ["date", "elderberry"];
const combined = [...fruits1, ...fruits2];

const [first, second, ...restFruits] = combined;
```

### 1.3 `forEach` / `map` / `filter` / `reduce`（重要・頻出）

React（第7回〜）でリスト表示をするときに必ず使うメソッド群です。ここでしっかり手を動かしておきましょう。

```js
const numbers = [1, 2, 3, 4, 5];

// forEach：配列を「1つずつ処理する」だけ。戻り値は使わない
numbers.forEach((number, index) => {
  console.log(`Index: ${index}, Number: ${number}`);
});

// map：各要素を「変換」して、新しい配列を作る
const doubled = numbers.map((num) => num * 2);
console.log(doubled); // [2, 4, 6, 8, 10]

// filter：条件に合う要素だけを残して、新しい配列を作る
const evenNumbers = numbers.filter((num) => num % 2 === 0);
console.log(evenNumbers); // [2, 4]

// reduce：配列全体を「1つの値」にまとめる
const sum = numbers.reduce((accumulator, currentValue) => {
  return accumulator + currentValue;
}, 0);
console.log(sum); // 15
```

**ポイント**：「元の配列は変更されない（`numbers` はそのまま）」ことを必ず確認しておきましょう。`map` / `filter` は新しい配列を返す、という性質がReactのstate更新の基本ルールにそのままつながります。

### 1.4 その他のES6配列メソッド

```js
const numbers = [1, 2, 3, 4, 5];
console.log(numbers.find((n) => n > 3)); // 4（最初に条件に合う要素）
console.log(numbers.findIndex((n) => n > 3)); // 3（そのインデックス）
console.log(numbers.includes(3)); // true
```

---

## 2. 文字列操作／JSONの基本

### 2.1 文字列の連結・部分取得・検索

```js
const firstName = "John";
const lastName = "Doe";

// テンプレート文字列を使った連結（推奨）
const fullName = `${firstName} ${lastName}`;

const str = "Hello, World!";
console.log(str.slice(0, 5)); // "Hello"
console.log(str.slice(-6)); // "World!"
console.log(str.indexOf("World")); // 7
```

### 2.2 split / join / replace

```js
const csv = "apple,banana,cherry";
const fruitsArray = csv.split(","); // ["apple", "banana", "cherry"]
console.log(fruitsArray.join(" / ")); // "apple / banana / cherry"

const str = "Hello, world! Hello again!";
console.log(str.replace("Hello", "Hi")); // 最初の1つだけ置換
console.log(str.replace(/Hello/g, "Hi")); // gフラグで全て置換
```

### 2.3 JSONの基本（parse / stringify）

メモアプリでデータを保存する際に使う、非常に重要な仕組みです。

```js
const person = {
  name: "田中太郎",
  age: 30,
  skills: ["HTML", "CSS", "JavaScript"],
};

const jsonString = JSON.stringify(person); // オブジェクト→JSON文字列
console.log(jsonString);

const parsedPerson = JSON.parse(jsonString); // JSON文字列→オブジェクト
console.log(parsedPerson.name); // "田中太郎"

// localStorageへの保存例（ブラウザを閉じてもデータが残る）
function saveTask(task) {
  const tasks = JSON.parse(localStorage.getItem("tasks") || "[]");
  tasks.push(task);
  localStorage.setItem("tasks", JSON.stringify(tasks));
}
```

---

## 3. DOM操作の基本

### 3.1 要素の取得

```js
const element = document.getElementById("myElement");
const elements = document.getElementsByClassName("myClass");
const element2 = document.querySelector(".container > div");
const elements2 = document.querySelectorAll("ul li");
```

### 3.2 要素の作成と追加

```js
const newDiv = document.createElement("div");
newDiv.textContent = "新しい要素";
document.body.appendChild(newDiv);
```

### 3.3 イベント処理

```js
document.getElementById("myButton").addEventListener("click", (event) => {
  console.log("クリックされました！");
  event.preventDefault(); // デフォルトの動作を防ぐ
});

const inputValue = document.getElementById("myInput").value;
```

---

## 4. 総合演習：簡易メモアプリ（Vanilla JS版）

**これがモジュールBの最終課題です。** ここまでの配列操作・DOM操作・イベント処理をすべて使って、メモアプリを完成させます。

### 4.1 要件

- テキストフィールドにメモを入力できる
- 「追加」ボタンでメモ一覧に追加される（追加されたメモには「削除」ボタンを表示）
- 「削除」ボタンでそのメモが一覧から削除される

### 4.2 ひな形（`memo.js` リポジトリの構成）

`index.html`（配布済みのひな形）：

```html
<!doctype html>
<html lang="ja">
  <head>
    <title>簡単メモアプリ</title>
    <meta charset="UTF-8" />
    <link rel="stylesheet" href="css/styles.css" />
  </head>
  <body>
    <h1 id="title">簡単メモアプリ</h1>
    <input id="add-text" />
    <button id="add-button">追加</button>
    <div class="container">
      <p>メモ一覧</p>
      <ul id="memo-list"></ul>
    </div>
    <script src="js/index.js"></script>
  </body>
</html>
```

`js/index.js` の実装イメージ（配列＋DOM操作＋JSON保存の組み合わせ）：

```js
let memoList = [];

const addButton = document.getElementById("add-button");
const addText = document.getElementById("add-text");
const memoListEl = document.getElementById("memo-list");

addButton.addEventListener("click", () => {
  const text = addText.value.trim();
  if (text === "") return;

  memoList.push(text);
  addText.value = "";
  renderMemoList();
});

function renderMemoList() {
  memoListEl.innerHTML = "";

  memoList.forEach((memo, index) => {
    const li = document.createElement("li");
    const p = document.createElement("p");
    p.textContent = memo;

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "削除";
    deleteButton.addEventListener("click", () => {
      memoList = memoList.filter((_, i) => i !== index);
      renderMemoList();
    });

    li.appendChild(p);
    li.appendChild(deleteButton);
    memoListEl.appendChild(li);
  });
}
```

### 4.3 手順（`memo.js` リポジトリの提出フロー）

1. **リポジトリをクローンする**（`memo.js` リポジトリ）
2. **ブランチを作成して切り替える**（自分の学生番号を使用）

   ```bash
   git switch -c <学生番号>
   # 例： git switch -c t26001
   ```

3. 上記の要件（入力・追加・削除）を実装する
4. **GitHubにpushする**

   ```bash
   git push origin <学生番号>
   # 例： git push origin t26001
   ```

### 発展課題（時間が余ったら／持ち帰り課題）

- 追加日時を各メモに表示する
- メモを `localStorage` に保存し、ページを再読み込みしても消えないようにする（2.3の `JSON.stringify` / `JSON.parse` を活用）
- 空メモ追加時に入力欄を赤く光らせるなど、簡単なバリデーション演出を加える

---

## モジュールB総復習（第3〜6回）

| 回    | テーマ                     | 一言でいうと                               |
| ----- | -------------------------- | ------------------------------------------ |
| 第3回 | 基本文法                   | 値を入れる箱と、条件分岐・繰り返しのルール |
| 第4回 | 関数・スコープ・非同期処理 | 処理の部品化と、「待ってから実行する」処理 |
| 第5回 | オブジェクト指向とクラス   | データと処理をひとまとめにした設計図と実体 |
| 第6回 | 配列・文字列・DOM操作      | データの集合を操作し、画面に反映する       |

次回（第7回〜）からはReactに入ります。今日の `forEach` / `map` によるリスト表示や、`useState` の元になる「状態が変わったら画面を書き換える」という考え方は、そのままReactのstateにつながっていきます。

## 参考リンク

- 現代のJavaScriptチュートリアル：https://ja.javascript.info/array-methods
- 同：https://ja.javascript.info/document
- 同：https://ja.javascript.info/events
