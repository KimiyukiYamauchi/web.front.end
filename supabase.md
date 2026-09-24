## 目次

- [Next.js + TypeScript + Supabase アプリ（手動で作る手順）](#nextjs--typescript--supabase-アプリ手動で作る手順)
  - [0️⃣ 事前準備](#0️⃣-事前準備)
  - [1️⃣ Next.js プロジェクトを作成する](#1️⃣-nextjs-プロジェクトを作成する)
  - [2️⃣ Supabase プロジェクトを作成する（ダッシュボード操作）](#2️⃣-supabase-プロジェクトを作成するダッシュボード操作)
  - [3️⃣ 「Connect」ダイアログから接続情報を取得し、.env.local を作成する](#3️⃣-connectダイアログから接続情報を取得しenvlocal-を作成する)
  - [4️⃣ Supabase クライアントを導入する](#4️⃣-supabase-クライアントを導入する)
  - [5️⃣ Supabase 側にテーブルを作成する](#5️⃣-supabase-側にテーブルを作成する)
  - [6️⃣ 一覧表示・追加・削除機能を実装する](#6️⃣-一覧表示追加削除機能を実装する)
  - [7️⃣ 動作確認](#7️⃣-動作確認)
  - [8️⃣ Git へのコミット](#8️⃣-git-へのコミット)
  - [フォルダ構成のイメージ](#フォルダ構成のイメージ)

---

## Next.js + TypeScript + Supabase アプリ（手動で作る手順）

Claude Code などのAIツールを使わず、自分の手でコマンドを実行し、コードを書きながら Next.js + TypeScript + Supabase の簡単な ToDo アプリを作成する手順です。

### 0️⃣ 事前準備

- Node.js（LTS版）がインストール済みであること（[install.md](./install.md) 参照）
- [Supabase](https://supabase.com/) のアカウントを作成しておく

```bash
node -v
npm -v
```

### 1️⃣ Next.js プロジェクトを作成する

作業用フォルダを作りたい場所で、以下のコマンドを実行します。

```bash
npx create-next-app@latest my-next-supabase-app --typescript --app --tailwind
cd my-next-supabase-app
```

作成後、開発サーバーが動くか確認します。

```bash
npm run dev
```

http://localhost:3000 を開いて初期画面が表示されればOKです。確認できたら `Ctrl + C` でサーバーを止めます。

### 2️⃣ Supabase プロジェクトを作成する（ダッシュボード操作）

1. [supabase.com](https://supabase.com/) にログイン
2. 「New project」からプロジェクト名・DBパスワード・リージョン（Tokyo等）を設定して作成
3. 作成完了を待つ

> **DBパスワードについて**: ここで設定するパスワードは、Supabase内部のPostgreSQLデータベースに直接接続する（`psql` や各種DBクライアント、Prisma等のORMから接続文字列で接続する）際に使用するものです。今回のアプリのように `@supabase/supabase-js` とURL・APIキー（publishable key）経由でアクセスする場合には使用しません。
>
> 直接DB接続を行う予定がなければ厳密にローカル保存する必要はありませんが、パスワードを忘れるとSupabaseダッシュボードから再設定が必要になるため、パスワードマネージャーなどに安全に控えておくことを推奨します。`.env.local` などGit管理下のファイルに書き込むことは避けてください。

### 3️⃣ 「Connect」ダイアログから接続情報を取得し、.env.local を作成する

1. プロジェクトダッシュボード上部の「Connect」ボタンをクリック
2. 表示されるダイアログの「App Frameworks」タブで「Next.js」を選択する
3. `.env.local` にそのまま貼り付けられる形式で、以下の内容が表示されるのでコピーする

```
NEXT_PUBLIC_SUPABASE_URL=あなたのProject URL
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=あなたのpublishable key
```

4. プロジェクト直下（`my-next-supabase-app` フォルダ内）に `.env.local` というファイルを作成し、コピーした内容をそのまま貼り付ける

> **Note**: 2024年以降、Supabase は従来の `anon key` / `service_role key`（JWT形式）を、新しい `publishable key`（`sb_publishable_...`）/ `secret key`（`sb_secret_...`）に置き換えています。旧キーは2026年末に廃止予定で、「Connect」ダイアログには基本的に新しい publishable key ベースの環境変数が表示されます。`secret key` はサーバー専用のキーなので、`NEXT_PUBLIC_` を付けず、ブラウザに絶対に渡さないでください（今回のアプリでは使いません）。旧プロジェクトで `anon key` しか表示されない場合は、`NEXT_PUBLIC_SUPABASE_ANON_KEY` という変数名に読み替えて同様に進めてください。

`.env.local` は秘密情報を含むため、`.gitignore` に含まれていることを必ず確認してください（`create-next-app` で作成した場合は標準で除外されています）。

### 4️⃣ Supabase クライアントを導入する

`@supabase/supabase-js` をインストールします。

```bash
npm install @supabase/supabase-js
```

`lib` フォルダを作成し、`lib/supabase.ts` に以下の内容を書きます。

```ts
// lib/supabase.ts
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabasePublishableKey = process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!;

export const supabase = createClient(supabaseUrl, supabasePublishableKey);
```

（旧プロジェクトで anon key しかない場合は、`NEXT_PUBLIC_SUPABASE_ANON_KEY` という変数名に読み替えて同様に実装してください）

### 5️⃣ Supabase 側にテーブルを作成する

Supabase ダッシュボードの「SQL Editor」で、簡単な todos テーブルを作成します。

```sql
create table todos (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  done boolean not null default false,
  created_at timestamp with time zone default now()
);

alter table todos enable row level security;

create policy "Allow public access"
on todos for all
using (true)
with check (true);
```

（学習用の簡易設定です。本番運用では適切な RLS ポリシーに変更してください）

### 6️⃣ 一覧表示・追加・削除機能を実装する

`app/page.tsx` を以下の内容に書き換えます。todosテーブルのデータを一覧表示し、入力欄から新規追加、各項目に削除ボタンを付けたページです。

```tsx
// app/page.tsx
"use client";

import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";

type Todo = {
  id: string;
  title: string;
  created_at: string;
};

export default function Home() {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTitle, setNewTitle] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTodos();
  }, []);

  async function fetchTodos() {
    setLoading(true);
    const { data, error } = await supabase
      .from("todos")
      .select("*")
      .order("created_at", { ascending: false });

    if (error) {
      setError(error.message);
    } else {
      setTodos(data ?? []);
      setError(null);
    }
    setLoading(false);
  }

  async function handleAdd(e: React.FormEvent) {
    e.preventDefault();
    const title = newTitle.trim();
    if (!title) return;

    const { data, error } = await supabase
      .from("todos")
      .insert({ title })
      .select()
      .single();

    if (error) {
      setError(error.message);
      return;
    }

    setTodos((prev) => [data, ...prev]);
    setNewTitle("");
    setError(null);
  }

  async function handleDelete(id: string) {
    const { error } = await supabase.from("todos").delete().eq("id", id);

    if (error) {
      setError(error.message);
      return;
    }

    setTodos((prev) => prev.filter((todo) => todo.id !== id));
  }

  return (
    <div className="flex flex-col flex-1 items-center bg-zinc-50 font-sans dark:bg-black">
      <main className="flex w-full max-w-xl flex-col gap-6 py-16 px-6">
        <h1 className="text-2xl font-semibold text-black dark:text-zinc-50">
          Todos
        </h1>

        <form onSubmit={handleAdd} className="flex gap-2">
          <input
            type="text"
            value={newTitle}
            onChange={(e) => setNewTitle(e.target.value)}
            placeholder="新しいTodoを入力"
            className="flex-1 rounded border border-black/[.1] bg-white px-3 py-2 text-black dark:border-white/[.145] dark:bg-black dark:text-zinc-50"
          />
          <button
            type="submit"
            className="rounded bg-foreground px-4 py-2 text-background transition-colors hover:bg-[#383838] dark:hover:bg-[#ccc]"
          >
            追加
          </button>
        </form>

        {error && <p className="text-sm text-red-600">{error}</p>}

        {loading ? (
          <p className="text-sm text-zinc-600 dark:text-zinc-400">
            読み込み中...
          </p>
        ) : (
          <ul className="flex flex-col gap-2">
            {todos.map((todo) => (
              <li
                key={todo.id}
                className="flex items-center justify-between rounded border border-black/[.1] bg-white px-3 py-2 dark:border-white/[.145] dark:bg-black"
              >
                <span className="text-black dark:text-zinc-50">
                  {todo.title}
                </span>
                <button
                  onClick={() => handleDelete(todo.id)}
                  className="rounded border border-red-600 px-2 py-1 text-sm text-red-600 transition-colors hover:bg-red-600 hover:text-white"
                >
                  削除
                </button>
              </li>
            ))}
            {todos.length === 0 && (
              <p className="text-sm text-zinc-600 dark:text-zinc-400">
                Todoがありません。
              </p>
            )}
          </ul>
        )}
      </main>
    </div>
  );
}
```

### 7️⃣ 動作確認

```bash
npm run dev
```

http://localhost:3000 を開き、以下を確認します。

- ページを開いた時に Supabase 上のデータが一覧表示される
- 入力欄からデータを追加できる
- 削除ボタンでデータが消える

うまく動かない場合は、ブラウザの開発者ツール（コンソール）やターミナルに表示されるエラーメッセージを確認し、コードや `.env.local` の設定を見直してください。

#### Supabase ダッシュボードでデータを確認する

アプリ画面で追加・削除したデータが、実際に Supabase 側にも反映されているかをダッシュボードから確認できます。

1. Supabase ダッシュボードの左メニューから「Table Editor」を開く
2. `todos` テーブルを選択する
3. 行の一覧が表示されるので、アプリで追加したデータが増えていること、削除したデータが消えていることを確認する

「SQL Editor」から直接SQLで確認することもできます。

```sql
select * from todos order by created_at desc;
```

テーブルエディタ上の表示は自動更新されない場合があるため、反映されていないように見えるときはページの再読み込み（ブラウザのリロードやテーブルエディタの更新ボタン）を試してください。

### 8️⃣ Git へのコミット

```bash
git init
git add .
git commit -m "Next.js + TypeScript + Supabase の簡単なアプリを作成"
```

`.env.local` がコミット対象に含まれていないことを `git status` で必ず確認してください。

### フォルダ構成のイメージ

```
my-next-supabase-app/
  ├─ app/
  │   ├─ page.tsx        ← ToDo一覧・追加・削除画面
  │   └─ layout.tsx
  ├─ lib/
  │   └─ supabase.ts     ← Supabaseクライアントの初期化
  ├─ .env.local           ← Supabaseの接続情報（Gitには含めない）
  ├─ package.json
  └─ tsconfig.json
```
