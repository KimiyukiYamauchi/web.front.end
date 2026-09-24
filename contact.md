## 目次

- [✅ お問い合わせフォームの入力を Supabase のテーブルに保存する手順](#-お問い合わせフォームの入力を-supabase-のテーブルに保存する手順)
  - [① Supabase でテーブルを作成](#-supabase-でテーブルを作成)
  - [② API の URL とキーを確認](#-api-の-url-とキーを確認)
  - [③ 環境変数を設定](#-環境変数を設定)
  - [④ Supabase のライブラリをインストール](#-supabase-のライブラリをインストール)
  - [⑤ Supabase クライアントを作成](#-supabase-クライアントを作成)
  - [⑥ Server Action を書き換える](#-server-action-を書き換える)
  - [⑦ フォーム側の不要な import を削除](#-フォーム側の不要な-import-を削除)
  - [⑧ 動作確認](#-動作確認)
  - [⑨ うまくいかないとき](#-うまくいかないとき)
  - [📝 Vercel などにデプロイする場合](#-vercel-などにデプロイする場合)

---

## ✅ お問い合わせフォームの入力を Supabase のテーブルに保存する手順

対象：Next.js のプロジェクトディレクトリ（`package.json` があるフォルダ。以下「プロジェクトディレクトリ」と書きます）

- フォーム：`app/_components/ContactForm/index.tsx`
- Server Action：`app/_actions/contact.tsx`

いまのフォームは、送信すると Server Action の `createContactData` が動き、入力チェックのあとに **HubSpot** へデータを送っています。
この送信先を **Supabase のテーブル** に置き換えます。

```
[ContactForm] --送信--> [createContactData（サーバーで実行）] --insert--> [Supabase: contacts テーブル]
```

> 💡 Supabase への書き込みを Server Action（サーバー側）で行うので、ブラウザから直接 Supabase にアクセスするコードは書きません。

---

### ① Supabase でテーブルを作成

1. 👉 https://supabase.com/dashboard を開き、使うプロジェクトを選択
2. 左メニュー「**SQL Editor**」→「**New query**」
3. 以下の SQL を貼り付けて「**Run**」

```sql
-- お問い合わせを保存するテーブル
create table public.contacts (
  id         bigint generated always as identity primary key,
  lastname   text not null,
  firstname  text not null,
  company    text not null,
  email      text not null,
  message    text not null,
  created_at timestamptz not null default now()
);

-- RLS（行レベルセキュリティ）を有効にする
alter table public.contacts enable row level security;

-- 誰でも「追加（insert）」だけはできるようにする
grant insert on public.contacts to anon;

create policy "anyone can insert contacts"
  on public.contacts
  for insert
  to anon
  with check (true);
```

**ポイント**

- 列名はフォームの `name` 属性（`lastname` / `firstname` / `company` / `email` / `message`）と同じにしています。
- **insert のポリシーだけ**を作り、select（読み取り）のポリシーは作りません。
  → フォームからの送信はできますが、他人のお問い合わせ内容を公開キーで読み出すことはできません。
- 保存されたデータは、ダッシュボードの「**Table Editor**」→ `contacts` で確認できます。

---

### ② API の URL とキーを確認

1. ダッシュボード左下の「**Project Settings**」（歯車）
2. 「**Data API**」→ **Project URL** をコピー（例：`https://xxxxxxxx.supabase.co`）
3. 「**API Keys**」→ **Publishable key** をコピー（例：`sb_publishable_xxxxxxxx`）

> ⚠️ **Secret key（`sb_secret_...` / 旧 `service_role`）は使いません。** RLS を無視して何でもできてしまうキーです。

---

### ③ 環境変数を設定

プロジェクトディレクトリの直下にある `.env.local`（なければ作成）に 2 行追加します。

```env
SUPABASE_URL=https://xxxxxxxx.supabase.co
SUPABASE_PUBLISHABLE_KEY=sb_publishable_xxxxxxxx
```

- 今回は Supabase を **サーバー（Server Action）からしか使わない**ので、`NEXT_PUBLIC_` は付けていません。
  `NEXT_PUBLIC_` を付けないと、値がブラウザに送られるコードに含まれません。
- `.env.local` は Git にコミットしないでください（`.gitignore` に含まれているか確認）。
- 環境変数を変更したら、`npm run dev` を **いったん止めてから起動し直してください**。

---

### ④ Supabase のライブラリをインストール

```bash
cd プロジェクトディレクトリ
npm install @supabase/supabase-js
```

---

### ⑤ Supabase クライアントを作成

`プロジェクトディレクトリ/app/_libs/supabase.ts` を新しく作ります（`microcms.ts` と同じフォルダです）。

```ts
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_PUBLISHABLE_KEY;

if (!supabaseUrl || !supabaseKey) {
  throw new Error(
    "Missing SUPABASE_URL or SUPABASE_PUBLISHABLE_KEY environment variable."
  );
}

export const supabase = createClient(supabaseUrl, supabaseKey);
```

> `tsconfig.json` で `"@/*": ["./*"]` と設定されているので、`@/app/_libs/supabase` で読み込めます。

---

### ⑥ Server Action を書き換える

`app/_actions/contact.tsx` を修正します。

**1. ファイルの先頭に import を追加**

```ts
"use server";

import { supabase } from "@/app/_libs/supabase";
```

**2. HubSpot に送っている部分を置き換える**

入力チェック（`if (!rawFormData.message) { ... }` まで）は**そのまま残し**、その下の

```ts
  const result = await fetch(
    `https://api.hsforms.com/submissions/v3/integration/submit/...`,
    ...
  );

  try {
    await result.json();
  } catch (e) {
    ...
  }

  return { status: "success", message: "OK" };
```

を、次のコードに置き換えます。

```ts
  // contacts テーブルに 1 行追加する
  const { error } = await supabase.from("contacts").insert(rawFormData);

  if (error) {
    console.log(error);
    return {
      status: "error",
      message: "お問い合わせに失敗しました",
    };
  }

  return { status: "success", message: "OK" };
```

- `rawFormData` のキー名とテーブルの列名が同じなので、そのまま `insert` に渡せます。
- `.select()` を付けていないのは、①で select のポリシーを作っていないためです（付けると権限エラーになります）。

---

### ⑦ フォーム側の不要な import を削除

`app/_components/ContactForm/index.tsx` の 7 行目にある次の行は使われていないので削除します。

```ts
import { send } from "process";
```

> `process` は Node.js のモジュールなので、`"use client"` のファイルで読み込むとエラーや警告の原因になります。

フォーム本体（`useActionState(createContactData, initialState)`）は変更不要です。

---

### ⑧ 動作確認

1. 開発サーバーを起動

   ```bash
   npm run dev
   ```

2. ブラウザでお問い合わせページを開き、すべての項目を入力して「送信する」
3. 「お問い合わせいただき、ありがとうございます。」が表示されれば成功
4. Supabase ダッシュボード「**Table Editor**」→ `contacts` に 1 行増えていることを確認

---

### ⑨ うまくいかないとき

| 症状（ターミナルの `console.log(error)` など） | 原因と対処 |
| --- | --- |
| `Missing SUPABASE_URL or SUPABASE_PUBLISHABLE_KEY ...` | `.env.local` の変数名のつづりを確認し、`npm run dev` を再起動 |
| `new row violates row-level security policy` | ①の `create policy ...` が実行されていない。SQL Editor で再実行 |
| `permission denied for table contacts` | ①の `grant insert ...` が実行されていない |
| `Could not find the table 'public.contacts'` | テーブル名のつづり、または別のプロジェクトの URL を使っていないか確認 |
| `Could not find the 'xxx' column` | テーブルの列名とフォームの `name` 属性が一致しているか確認 |
| `Invalid API key` | Publishable key をコピーし直す（前後の空白に注意） |

---

### 📝 Vercel などにデプロイする場合

`.env.local` はデプロイ先にアップロードされません。
Vercel の「**Settings**」→「**Environment Variables**」に、`SUPABASE_URL` と `SUPABASE_PUBLISHABLE_KEY` を同じ値で登録してから再デプロイしてください。
