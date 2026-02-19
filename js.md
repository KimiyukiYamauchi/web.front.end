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
- [第2章 関数とスコープ](#第2章-関数とスコープ)
  - [2.1 関数の定義と呼び出し](#21-関数の定義と呼び出し)
  - [2.2 引数と返り値](#22-引数と返り値)
  - [2.3 関数の引数としてのスプレッド演算子](#23-関数の引数としてのスプレッド演算子)
  - [2.4 スコープ](#24-スコープ)
  - [2.5 コールバック変数](#25-コールバック変数)
  - [2.6 アロー関数](#26-アロー関数)
  - [2.7 サンプルコード：ToDo リストアプリ](#27-サンプルコードtodo-リストアプリ)
- [第3章 オブジェクト指向とクラス](#第3章-オブジェクト指向とクラス)
  - [3.1 クラス構文](#31-クラス構文)
  - [3.2 クラスからのインスタンス(オブジェクト)の生成](#32-クラスからのインスタンスオブジェクトの生成)
  - [3.3 オブジェクト指向プログラミングの原則](#33-オブジェクト指向プログラミングの原則)
  - [3.4 プロトタイプとインスタンス](#34-プロトタイプとインスタンス)
  - [3.5 クラス構文以前のオブジェクト作成方法](#35-クラス構文以前のオブジェクト作成方法)
  - [3.6 サンプルコード：図形病がアプリケーション](#36-サンプルコード図形病がアプリケーション)

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

## 第2章 関数とスコープ

### 2.1 関数の定義と呼び出し

#### 関数の定義

```js
function greet(name) {
  console.log(`Hello, ${name}!`);
}
```

#### 関数の呼び出し

```js
greet("Alice"); // Output: Hello, Alice!
```

#### アロー関数

```js
const multiply = function (a, b) {
  return a * b;
};
console.log(multiply(2, 3)); // Output: 6
```

```js
const multiply = (a, b) => a * b;
console.log(multiply(2, 3)); // Output: 6
```

#### 関数の返り値

```js
function add(a, b) {
  return a + b;
}

const result = add(2, 3);
console.log(result); // 5と出力されます
```

#### 関数式

```js
const multiply = function (a, b) {
  return a * b;
};

console.log(multiply(2, 3)); // 6と出力されます
```

### 2.2 引数と返り値

#### 引数

```js
function greet(name) {
  return `Hello, ${name}!`;
}

console.log(greet("Alice")); // "Hello, Alice!"
console.log(greet("Bob")); // "Hello, Bob!"
```

#### デフォルト引数

```js
function greet(name = "Guest") {
  return `Hello, ${name}!`;
}

console.log(greet()); // "Hello, Guest!"
console.log(greet("Bob")); // "Hello, Bob!"
```

#### レストパラメータ

```js
function sum(...numbers) {
  return numbers.reduce((acc, curr) => acc + curr, 0);
}

console.log(sum(1, 2, 3)); // Output: 6
console.log(sum(4, 5, 6, 7)); // Output: 22
```

#### 返り値

```js
function multiply(a, b) {
  return a * b;
}

const result = multiply(5, 3);
console.log(result); // Output: 15
```

### 2.3 関数の引数としてのスプレッド演算子

#### スプレッド演算子を使った配列の展開

```js
function sum(a, b, c) {
  return a + b + c;
}

const numbers = [1, 2, 3];
console.log(sum(...numbers)); // Output: 6
// console.log(sum(numbers[0], numbers[1], numbers[2])); と同様
```

#### レストパラメータとの違い

- スプレッド演算子は、関数の実行時や配列・オブジェクトの展開時に使用
- レストパラメータは、関数の宣言時に使用

```js
function myFunction(...args) {
  console.log(args);
}

myFunction(1, 2, 3); // Output: [1, 2, 3]
```

#### スプレッド演算子による可読性の向上

```js
const numbers = [1, 2, 3, 4, 5];
console.log(Math.max(...numbers)); // Output: 5
```

### 2.4 スコープ

#### グローバルスコープ

```js
const globalVal = "グローバル変数";
function printGlobal() {
  console.log(globalVal);
}

printGlobal(); // "グローバル変数"
console.log(globalVal); // "グローバル変数"
```

#### ローカルスコープ(関数スコープ)

```js
function printLocal() {
  const localVar = "ローカル変数";
  console.log(localVar);
}
printLocal(); // "ローカル変数"
console.log(localVar); // ReferenceError: localVar is not defined
```

#### ローカルスコープ(関数スコープ)

```js
function printLocal() {
  const localVar = "ローカル変数";
  console.log(localVar);
}
printLocal(); // "ローカル変数"
console.log(localVar); // ReferenceError: localVar is not defined
```

#### ブロックスコープ

```js
if (true) {
  let blockVar = "ブロック変数";
  console.log(blockVar); // "ブロック変数"
}
console.log(blockVar); // ReferenceError: blockVar is not defined
```

### 2.5 コールバック変数

#### コールバック関数の例

```js
function fetchData(callback) {
  // データの取得処理(ここでは簡単のため、疑似的な処理を行っています)
  const data = "取得したデータ";
  callback(data);
}

function processData(data) {
  console.log("取得したデータ: " + data);
}

// データを取得して処理する
fetchData(processData); // "取得したデータ: 取得したデータ"
```

#### コールバック関数を使った非同期処理の例

```js
function fetchData(callback) {
  setTimeout(() => {
    const data = "取得したデータ";
    callback(data);
  }, 1000); // 1秒後にデータを取得してコールバック関数を呼び出す
}

function processData(data) {
  console.log("取得したデータ: " + data);
}

console.log("データの取得を開始...");
fetchData(processData); // "取得したデータ: 取得したデータ"
console.log("データの取得を待っています...");
```

#### コールバック関数のエラーハンドリング

```js
function fetchData(callback) {
  setTimeout(() => {
    const data = "取得したデータ";
    const error = null; // エラーが発生した場合はここにエラーオブジェクトを設定する
    callback(error, data);
  }, 1000); // 1秒後にデータを取得してコールバック関数を呼び出す
}

function processData(error, data) {
  if (error) {
    console.log("エラーが発生しました: " + error);
    return;
  }
  console.log("取得したデータ: " + data);
}

console.log("データの取得を開始...");
fetchData(processData); // "取得したデータ: 取得したデータ"
console.log("データの取得を待っています...");
```

#### コールバック関数の代替手法

- Promise: 非同期処理の状態(成功または失敗)を表すオブジェクトで、コールバック関数の代替として使用される

```js
function fetchData() {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const data = "取得したデータ";
      const error = null; // エラーがある場合は値を入れる

      if (error) {
        reject(error); // 失敗
      } else {
        resolve(data); // 成功
      }
    }, 1000);
  });
}

console.log("データの取得を開始...");

fetchData()
  .then((data) => {
    console.log("取得したデータ: " + data);
  })
  .catch((error) => {
    console.log("エラーが発生しました: " + error);
  });

console.log("データの取得を待っています...");
```

- Async/Await: Promiseをさらに簡潔に書くための構文で、非同期処理を同期処理のように書くことができる

```js
function fetchData() {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const data = "取得したデータ";
      const error = null; // エラーにしたい場合は文字を入れる

      if (error) {
        reject(error);
      } else {
        resolve(data);
      }
    }, 1000);
  });
}

// asyncをつける
async function main() {
  try {
    console.log("データの取得を開始...");

    // awaitでPromiseの完了を待つ
    const data = await fetchData();

    console.log("取得したデータ: " + data);
  } catch (error) {
    console.log("エラーが発生しました: " + error);
  }

  console.log("データの取得が終了しました");
}

main();
```

### 2.6 アロー関数

```js
const 関数名 = (引数1, 引数2,...) => 式;
```

#### アロー関数の基本構文

```js
const 関数名 = (引数1, 引数2,...) => {
  // 関数の本体
}
```

```js
const add = (a, b) => {
  return a + b;
};

console.log(add(2, 3)); // Output: 5
```

#### 簡略化されたアロー関数

```js
const 関数名 = (引数1, 引数2,...) => 式;
```

```js
const add = (a, b) => a + b;

console.log(add(2, 3)); // Output: 5
```

#### アロー関数の注意点

- 従来の関数式と同様に引数を使用できるが、argumentsオブジェクトは使用できない。代わりにレストパラメータ(...args)を使用して可変長引数を扱う
- newキーワードを呼び出すことができないため、コンストラクタ関数として使用できない
- prototypeプロパティを持たない

### 2.7 サンプルコード：ToDo リストアプリ

```html
<!doctype html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <title>ToDo リスト</title>
  </head>
  <body>
    <h1>ToDo リスト</h1>
    <input type="text" id="new-task" placeholder="新しいタスクを入力" />
    <button onclick="addTodo()">タスクを追加</button>
    <ul id="task-list"></ul>
    <script>
      let todoList = [];

      // タスクを追加する関数
      function addTodo() {
        const input = document.getElementById("new-task");
        const taskList = document.getElementById("task-list");

        if (input.value.trim() === "") {
          alert("タスクを入力してください");
          return;
        }

        todoList.push({ text: input.value, completed: false });
        input.value = "";

        renderTodoList();
      }

      // タスクを表示する関数
      function renderTodoList() {
        const taskList = document.getElementById("task-list");
        taskList.innerHTML = "";

        todoList.forEach((todo, index) => {
          const li = document.createElement("li");
          li.innerHTML = `<input type="checkbox" ${todo.completed ? "checked" : ""} onclick="toggleComplete(${index})"> ${todo.text} <button onclick="deleteTodo(${index})">削除</button>`;
          taskList.appendChild(li);
        });
      }

      // タスクの完了状態を切り替える関数
      const toggleComplete = (index) => {
        todoList[index].completed = !todoList[index].completed;
        renderTodoList();
      };

      // タスクを削除する関数
      const deleteTodo = (index) => {
        todoList.splice(index, 1);
        renderTodoList();
      };
    </script>
  </body>
</html>
```

## 第3章 オブジェクト指向とクラス

### 3.1 クラス構文

#### クラスの定義

```js
class Person {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }

  greet() {
    console.log(`Hello, my name is ${this.name}`);
  }

  sayAge() {
    console.log(`I am ${this.age} years old`);
  }
}
```

#### クラスからのインスタンスの生成

```js
const person1 = new Person("Alice", 30);
const person2 = new Person("Bob", 25);
```

#### メソッドの呼び出し

```js
person1.greet(); // Output: Hello, my name is Alice
person1.sayAge(); // Output: I am 30 years old

person2.greet(); // Output: Hello, my name is Bob
person2.sayAge(); // Output: I am 25 years old
```

#### 静的メソッド

```js
class MathUtils {
  static square(x) {
    return x * x;
  }
}

console.log(MathUtils.square(5)); // 25と出力されます
```

### 3.2 クラスからのインスタンス(オブジェクト)の生成

#### コンストラクタメソッド

```js
class Person {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }
}
```

#### インスタンスの生成

```js
const person1 = new Person("Alice", 30);
const person2 = new Person("Bob", 25);
```

#### インスタンスメソッドの呼び出し

```js
class Person {
  constructor(name, age) {
    this.name = name;
    this.age = age;
  }

  greet() {
    console.log(`Hello, my name is ${this.name}`);
  }
}
const person1 = new Person("Alice", 30);
person1.greet(); // Output: Hello, my name is Alice
```

### 3.3 オブジェクト指向プログラミングの原則

#### カプセル化

カプセル化は、オブジェクトの内部状態を隠蔽し、外部からのアクセスを制限する原則

```js
class BankAccounrt {
  #balance = 0; // プライベートフィールド

  constructor(initialBalance) {
    this.#balance = initialBalance;
  }

  deposit(amount) {
    if (amount > 0) {
      this.#balance += amount;
      console.log(`Deposited: ${amount}. New balance: ${this.#balance}`);
    } else {
      console.log("Deposit amount must be positive.");
    }
  }

  withdraw(amount) {
    if (amount > 0 && amount <= this.#balance) {
      this.#balance -= amount;
      console.log(`Withdrew: ${amount}. New balance: ${this.#balance}`);
    } else {
      console.log(
        "Withdrawal amount must be positive and less than or equal to the current balance.",
      );
    }
  }

  getBalance() {
    return this.#balance;
  }
}
```

#### 継承

継承は、既存のクラスを拡張して新しいクラスを作成する原則。継承を使うことで、コードの再利用性が向上し、階層構造を作ることができる。

```js
class Animal {
  constructor(name) {
    this.name = name;
  }

  speak() {
    console.log(`${this.name} makes a noise.`);
  }
}

class Dog extends Animal {
  bark() {
    console.log("わんわん");
  }
}

const dog = new Dog("ぽち");
dog.speak(); // ぽち makes a noise.(継承したメソッド)
dog.bark(); // わんわん (独自のメソッド)
```

#### ポリモーフィズム

ポリモーフィズム(多態性)は、同じインタフェースを持つオブジェクトが、それぞれ異なる動作を行うことができる原則

```js
class Animal {
  constructor(name) {
    this.name = name;
  }

  speak() {
    console.log(`${this.name} makes a noise.`);
  }

  bark() {
    console.log("Animal can't bark.");
  }
}

class Dog extends Animal {
  bark() {
    // オーバーライド
    console.log("わんわん");
  }
}

class Cat extends Animal {
  bark() {
    // オーバーライド
    console.log("にゃー");
  }
}

const dog = new Dog("ぽち");
dog.speak(); // ぽち makes a noise.(継承したメソッド)
dog.bark(); // わんわん (オーバライドしたメソッド)

const cat = new Cat("たま");
cat.speak(); // たま makes a noise.(継承したメソッド)
cat.bark(); // にゃー (オーバライドしたメソッド)
```

### 3.4 プロトタイプとインスタンス

#### プロトタイプオブジェクト

```js
function Person(name, age) {
  this.name = name;
  this.age = age;
}

// Personのプロトタイプオブジェクトにgreetメソッドを追加
Person.prototype.greet = function () {
  console.log(`Hello, my name is ${this.name} and I am ${this.age} years old.`);
};
```

#### インスタンスの作成とプロトタイプチェーン

```js
function Person(name, age) {
  this.name = name;
  this.age = age;
}

// Personのプロトタイプオブジェクトにgreetメソッドを追加
Person.prototype.greet = function () {
  console.log(`Hello, my name is ${this.name} and I am ${this.age} years old.`);
};

const alice = new Person("Alice", 30);
alice.greet(); // Hello, my name is Alice and I am 30 years old.(プロトタイプチェーン経由で実行)

console.log(alice instanceof Person); // true
console.log(alice instanceof Object); // true(すべてのオブジェクトはObjectのインスタンスであるため)
```

#### プロトタイプを使った継承

```js
function Person(name, age) {
  this.name = name;
  this.age = age;
}

// Personのプロトタイプオブジェクトにgreetメソッドを追加
Person.prototype.greet = function () {
  console.log(`Hello, my name is ${this.name} and I am ${this.age} years old.`);
};

function Student(name, age, grade) {
  Person.call(this, name, age); // Personコンストラクタを呼び出して、nameとageを初期化
  this.grade = grade;
}

// StudentのプロトタイプオブジェクトをPersonのプロトタイプオブジェクトに設定
Student.prototype = Object.create(Person.prototype);
Student.prototype.constructor = Student; // constructorプロパティを修正

// Studentのプロトタイプに独自のメソッドを追加
Student.prototype.study = function () {
  console.log(`${this.name} is studying in grade ${this.grade}.`);
};

const bob = new Student("Bob", 20, "A");
bob.greet(); // Hello, my name is Bob and I am 20 years old.(Personのgreetメソッドが呼び出される)
bob.study(); // Bob is studying in grade A.  (Studentのstudyメソッドが呼び出される)
```

### 3.5 クラス構文以前のオブジェクト作成方法

#### オブジェクトリテラルを使ったオブジェクトの作成

```js
const person = {
  name: "John",
  age: 30,
  sayHello: function () {
    console.log(
      `Hello, my name is ${this.name} and I am ${this.age} years old.`,
    );
  },
};

person.sayHello(); // Output: Hello, my name is John and I am 30 years old.
```

#### コンストラクタ関数を使ったオブジェクトの作成

```js
function Person(name, age) {
  // コンストラクタ関数(慣習的に関数名は大文字で始める)
  this.name = name; // インスタンスのプロパティ
  this.age = age;
  this.greet = function () {
    // インスタンスのメソッド
    console.log(
      `Hello, my name is ${this.name} and I am ${this.age} years old.`,
    );
  };
}

// インスタンスの作成
const person1 = new Person("Alice", 30);
const person2 = new Person("Bob", 25);

// メソッドの呼び出し
person1.greet(); // Hello, my name is Alice and I am 30 years old.
person2.greet(); // Hello, my name is Bob and I am 25 years old.
```

```js
function Person(name, age) {
  // コンストラクタ関数(慣習的に関数名は大文字で始める)
  this.name = name; // インスタンスのプロパティ
  this.age = age;
}

// メソッドをプロトタイプに追加
Person.prototype.greet = function () {
  console.log(`Hello, my name is ${this.name} and I am ${this.age} years old.`);
};

// インスタンスの作成
const person1 = new Person("Alice", 30);
const person2 = new Person("Bob", 25);

// メソッドの呼び出し
person1.greet(); // Hello, my name is Alice and I am 30 years old.
person2.greet(); // Hello, my name is Bob and I am 25 years old.

// greetメソッドはプロトタイプに定義されているため、
// person1とperson2は同じgreetメソッドを共有しています。
console.log(person1.greet === person2.greet); // true
```

### 3.6 サンプルコード：図形描画アプリケーション

```js
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>図形描画アプリケーション</title>
  </head>
  <body>
    <h1>図形描画アプリケーション</h1>
    <p>
      このアプリケーションは、ユーザーが図形を描画できるようにするものです。
    </p>
    <canvas
      id="canvas"
      width="500"
      height="500"
      style="border: 1px solid #000000"
    ></canvas>
    <script>
      // 図形の基本クラス
      class Shape {
        constructor(x, y, color) {
          this.x = x;
          this.y = y;
          this.color = color;
        }

        // 図形を描画するためのメソッド(サブクラスでオーバーライドされる)
        draw(ctx) {
          // サブクラスで実装される
        }
      }

      // 円のクラス
      class Circle extends Shape {
        constructor(x, y, radius, color) {
          super(x, y, color); // 親クラスのコンストラクタを呼び出す
          this.radius = radius;
        }
        // 円を描画するためのメソッド
        draw(ctx) {
          ctx.beginPath();
          ctx.arc(this.x, this.y, this.radius, 0, 2 * Math.PI);
          ctx.fillStyle = this.color;
          ctx.fill();
        }
      }

      // 四角形のクラス
      class Rectangle extends Shape {
        constructor(x, y, width, height, color) {
          super(x, y, color); // 親クラスのコンストラクタを呼び出す
          this.width = width;
          this.height = height;
        }
        // 四角形を描画するためのメソッド
        draw(ctx) {
          ctx.fillStyle = this.color;
          ctx.fillRect(this.x, this.y, this.width, this.height);
        }
      }

      // 三角形のクラス
      class Triangle extends Shape {
        constructor(x, y, base, height, color) {
          super(x, y, color); // 親クラスのコンストラクタを呼び出す
          this.base = base;
          this.height = height;
        }
        // 三角形を描画するためのメソッド
        draw(ctx) {
          ctx.beginPath();
          ctx.moveTo(this.x, this.y);
          ctx.lineTo(this.x + this.base / 2, this.y + this.height);
          ctx.lineTo(this.x - this.base / 2, this.y + this.height);
          ctx.closePath();
          ctx.fillStyle = this.color;
          ctx.fill();
        }
      }

      // キャンバスのコンテキストを取得
      const canvas = document.getElementById("canvas");
      const ctx = canvas.getContext("2d");

      // 図形のインスタンスを作成
      const shapes = [
        new Circle(100, 100, 50, "red"),
        new Rectangle(200, 200, 100, 50, "blue"),
        new Triangle(300, 300, 80, 60, "green"),
      ];

      // 図形を描画
      shapes.forEach((shape) => shape.draw(ctx));
    </script>
  </body>
</html>

```
