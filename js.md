<!-- TOC -->

# 目次

- [第1章 Javascript基本構文](#第1章-javascript基本構文)
  - [1.1 変数と定数](#11-変数と定数)
  - [1.2 データ型](#12-データ型)
  - [1.3 分割代入とスプレッド演算子](#13-分割代入とスプレッド演算子)
  - [1.4 演算子](#14-演算子)
  - [1.5 制御構文(if、switch、for、while)](#15-制御構文ifswitchforwhile)
  - [1.6 エラーハンドリング(try...catch)](#16-エラーハンドリングtrycatch)
  - [1.7 サンプルコード：簡単な計算機アプリ](#17-サンプルコード簡単な計算機アプリ)

<!-- /TOC -->

## 第1章 Javascript基本構文

### 1.1 変数と定数

#### 変数の宣言

```js
let message = "Hello, world!";
mesasge = "Hello, Javascript!";
console.log(message);
```

#### 定数の宣言

```js
const PI = 3.14159;
console.log(PI);
```

#### ブロックスコープ

```js
if (true) {
  let message = "Hello, World!";
  console.log(message); // "Hello, World!"と出力
}
console.log(message); // ReferenceError: message is not defined
```

### 1.2 データ型

- 数値(Number)：整数や浮動小数を表す。

```js
let age = 25;
console.log(`I am ${age} years old.`);
let temperature = 37.5;
console.log(`The current temperature is ${temperature} degrees Celsius.`);
```

- 文字列(String)：テキストデータを表す。シングルクォート(')またはダブルクォート(")で囲む。

```js
let fullname = "John Doe";
console.log(fullname);
let message = "Hello, world!";
console.log(message);
```

- 真偽値(Boolean)：trueまたはfalseのいずれかの値を持つ。

```js
let isStudent = true;
console.log(isStudent);
let hasChildren = false;
console.log(hasChildren);
```

- undefined：変数が宣言されているが、値が代入されていない状態を表す。

```js
let value;
console.log(value); // undefinedと出力されます
```

- null：変数が意図的に空の値を持つことを表す。

```js
let obj = null;
console.log(obj);
```

- オブジェクト(Object)：関連するデータや機能をグループ化したもの。

```js
let person = {
  name: "John",
  age: 30,
  occupation: "Developer",
};
console.log(person.name); // Output: John
console.log(person.age); // Output: 30
console.log(person.occupation); // Output: Developer
```

- 配列(Array)：複数の値を順序付けて格納するデータ構造。

```js
let numbers = [1, 2, 3, 4, 5];
console.log(numbers);
let fruits = ["apple", "banana", "cherry"];
console.log(fruits);
```

- 変数や定数のデータ型は代入された値によって決定される(動的型付け言語)

```js
let value = 42;
console.log(typeof value); // "number"と出力
value = "Hello";
console.log(typeof value); // "string"と出力
```

### 1.3 分割代入とスプレッド演算子

#### 分割代入

- 配列の分割代入

```js
const numbers = [1, 2, 3, 4, 5];
const [a, b, ...rest] = numbers;

console.log(a); // 1
console.log(b); // 2
console.log(rest); // [3, 4, 5]
```

- オブジェクトの分割代入

```js
const person = {
  name: "Alice",
  age: 30,
  occupation: "Engineer",
};

const { name, age } = person;

console.log(`Name: ${name}, Age: ${age}`); // Output: Name: Alice, Age: 30
```

#### スプレッド演算子

- 配列の結合と複製

```js
const arr1 = [1, 2, 3];
const arr2 = [4, 5, 6];
const combined = [...arr1, ...arr2];
console.log(combined); // Output: [1, 2, 3, 4, 5, 6]
const copiedArr = [...arr1];
console.log(copiedArr); // Output: [1, 2, 3]
```

- オブジェクトのプロパティの複製と結合

```js
const obj1 = { a: 1, b: 2 };
const obj2 = { c: 1, d: 2 };
const mergedObj = { ...obj1, ...obj2 };
console.log(mergedObj); // Output: {a: 1, b: 2, c: 1, d: 2}
const copiedObj = { ...obj1 };
console.log(copiedObj); // Output: {a: 1, b: 2}
```

### 1.4 演算子

- 算術演算子
  - 加算(+)
  - 減算(-)
  - 乗算(\*)
  - 除算(/)
  - 剰余(%)
  - インクリメント(++)
  - デクリメント(--)

```js
let x = 10;
let y = 3;
console.log(x + y); // 13
console.log(x - y); // 7
console.log(x * y); // 30
console.log(x / y); // 3.3333333333333335
console.log(x % y); // 1
```

- 代入演算子
  - 単純代入(-)
  - 加算代入(+=)
  - 減算代入(-=)
  - 乗算代入(\*=)
  - 除算代入(/=)
  - 剰余代入(%=)

```js
let x = 10;
x += 5; // x = x + 5
console.log(x); // Output: 15
```

- 比較演算子
  - 等価(==)
  - 不等価(!=)
  - 厳密等価(===)
  - 厳密不等価(!==)
  - 大なり(>)
  - 小なり(<)
  - 大なりイコール(>=)
  - 小なりイコール(<=)

```js
let x = 10;
let y = "10";

console.log(x == y); // true
console.log(x === y); // false
console.log(x != y); // false
console.log(x !== y); // true
```

- 論理演算子
  - 論理積AND(&&)
  - 論理和OR(||)
  - 論理否定NOT(!)

```js
let x = true;
let y = false;

console.log(x && y); // false
console.log(x || y); // true
console.log(!x); // false
```

### 1.5 制御構文(if、switch、for、while)

- if文

```js
let age = 20;
if (age < 18) {
  console.log("未成年です");
} else {
  console.log("成人です");
}
```

- switch文

```js
let fruit = "apple";

switch (fruit) {
  case "apple":
    console.log("これはリンゴです。");
    break;
  case "banana":
    console.log("これはバナナです。");
    break;
  case "orange":
    console.log("これはオレンジです。");
    break;
  default:
    console.log("これは未知の果物です。");
}
```

- for文

```js
for (let i = 0; i < 5; i++) {
  console.log(i);
}
```

- while文

```js
let i = 0;
while (i < 5) {
  console.log(i);
  i++;
}
```

- do...while文

```js
let i = 0;
do {
  console.log(i);
  i++;
} while (i < 5);
```

- break文

```js
for (let i = 0; i < 5; i++) {
  if (i === 3) {
    break;
  }
  console.log(i);
}
```

- continue文

```js
for (let i = 0; i < 5; i++) {
  if (i === 3) {
    continue;
  }
  console.log(i);
}
```

### 1.6 エラーハンドリング(try...catch)

```js
try {
  // エラーが発生する可能性のあるコード
  const result = riskyFunction();
  console.log("結果:", result);
} catch (error) {
  // エラーが発生した場合に実行されるコード
  console.error("エラーが発生しました:", error.message);
} finally {
  // エラーの有無に関係なく実行されるコード
  console.log("処理が完了しました。");
}
```

### 1.7 サンプルコード：簡単な計算機アプリ

```html
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <title>簡単な計算機アプリ</title>
  </head>
  <body>
    <h1>簡単な計算機アプリ</h1>
    <p>数値を入力して、演算子を選択し、計算ボタンを押してください。</p>
    <input type="number" id="num1" placeholder="数値1" />
    <select id="operation">
      <option value="add">+</option>
      <option value="subtract">-</option>
      <option value="multiply">×</option>
      <option value="divide">÷</option>
    </select>
    <input type="number" id="num2" placeholder="数値2" />
    <button onclick="calculate()">計算</button>
    <p id="result"></p>
    <script>
      function calculate() {
        try {
          // 入力値を取得
          const num1Input = document.getElementById("num1").value;
          const num2Input = document.getElementById("num2").value;

          // 未入力チェック
          if (num1Input === "" || num2Input === "") {
            throw new Error("数値を入力してください");
          }

          // 数値に変換
          const num1 = parseFloat(num1Input);
          const num2 = parseFloat(num2Input);

          // 数値チェック
          if (isNaN(num1) || isNaN(num2)) {
            throw new Error("正しい数値を入力してください");
          }

          const operation = document.getElementById("operation").value;
          let result;

          switch (operation) {
            case "add":
              result = num1 + num2;
              break;
            case "subtract":
              result = num1 - num2;
              break;
            case "multiply":
              result = num1 * num2;
              break;
            case "divide":
              if (num2 === 0) {
                throw new Error("0で割ることはできません");
              }
              result = num1 / num2;
              break;
            default:
              throw new Error("無効な演算子です");
          }

          document.getElementById("result").textContent = `結果: ${result}`;
        } catch (error) {
          // エラーが発生した場合ここに来る
          document.getElementById("result").textContent =
            `エラー: ${error.message}`;
        }
      }
    </script>
  </body>
</html>
```
