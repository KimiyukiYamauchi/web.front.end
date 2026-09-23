## 目次

- [Claude Code で作る Next.js + TypeScript + Supabase アプリ](#claude-code-で作る-nextjs-typescript-supabase-アプリ)
  - [0️⃣ 事前準備](#0️-事前準備)
  - [1️⃣ Claude Code のインストールと起動](#1️-claude-code-のインストールと起動)
  - [2️⃣ Next.js プロジェクトの作成を依頼する](#2️-nextjs-プロジェクトの作成を依頼する)
  - [3️⃣ Supabase プロジェクトを作成する（ダッシュボード操作）](#3️-supabase-プロジェクトを作成するダッシュボード操作)
  - [4️⃣ 「Connect」ダイアログから接続情報を取得し、.env.local を作成する](#4️-connectダイアログから接続情報を取得しenvlocal-を作成する)
  - [5️⃣ Supabase クライアントの導入を依頼する](#5️-supabase-クライアントの導入を依頼する)
  - [6️⃣ Supabase 側にテーブルを作成する](#6️-supabase-側にテーブルを作成する)
  - [7️⃣ 一覧表示・追加・削除機能の実装を依頼する](#7️-一覧表示追加削除機能の実装を依頼する)
  - [8️⃣ 動作確認](#8️-動作確認)
  - [9️⃣ Git へのコミット](#9️-git-へのコミット)
  - [フォルダ構成のイメージ](#フォルダ構成のイメージ)

---

## Claude Code で作る Next.js + TypeScript + Supabase アプリ

Claude Code（AIコーディングアシスタントのCLI）を使って、Next.js + TypeScript + Supabase の簡単な ToDo アプリを作成する手順です。

### 0️⃣ 事前準備

- Node.js（LTS版）がインストール済みであること（[install.md](./install.md) 参照）
- [Supabase](https://supabase.com/) のアカウントを作成しておく

```bash
node -v
npm -v
```

### 1️⃣ Claude Code のインストールと起動

```bash
npm install -g @anthropic-ai/claude-code
```

作業用フォルダを作って移動し、Claude Code を起動します。

```bash
mkdir my-next-supabase-app
cd my-next-supabase-app
claude
```

以降は Claude Code のチャットにプロンプト（指示文）を入力しながら進めます。

### 2️⃣ Next.js プロジェクトの作成を依頼する

Claude Code に次のように指示します。

```
TypeScript版のNext.jsプロジェクトをこのフォルダに作成してください。
App Router、Tailwind CSSを使う設定でお願いします。
```

Claude Code が内部で `create-next-app` 等のコマンドを実行し、雛形を作成します。
（自分の手で作る場合は以下のコマンドでも同じことができます）

```bash
npx create-next-app@latest . --typescript --app --tailwind
```

作成後、開発サーバーが動くか確認します。

```bash
npm run dev
```

http://localhost:3000 を開いて初期画面が表示されればOKです。

### 3️⃣ Supabase プロジェクトを作成する（ダッシュボード操作）

1. [supabase.com](https://supabase.com/) にログイン
2. 「New project」からプロジェクト名・DBパスワード・リージョン（Tokyo等）を設定して作成
3. 作成完了を待つ

### 4️⃣ 「Connect」ダイアログから接続情報を取得し、.env.local を作成する

1. プロジェクトダッシュボード上部の「Connect」ボタンをクリック
2. 表示されるダイアログの「App Frameworks」タブで「Next.js」を選択する
3. `.env.local` にそのまま貼り付けられる形式で、以下の内容が表示されるのでコピーする

```
NEXT_PUBLIC_SUPABASE_URL=あなたのProject URL
NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY=あなたのpublishable key
```

4. プロジェクト直下に `.env.local` を作成し、コピーした内容をそのまま貼り付ける

> **Note**: 2024年以降、Supabase は従来の `anon key` / `service_role key`（JWT形式）を、新しい `publishable key`（`sb_publishable_...`）/ `secret key`（`sb_secret_...`）に置き換えています。旧キーは2026年末に廃止予定で、「Connect」ダイアログには基本的に新しい publishable key ベースの環境変数が表示されます。`secret key` はサーバー専用のキーなので、`NEXT_PUBLIC_` を付けず、ブラウザに絶対に渡さないでください（今回のアプリでは使いません）。旧プロジェクトで `anon key` しか表示されない場合は、`NEXT_PUBLIC_SUPABASE_ANON_KEY` という変数名に読み替えて同様に進めてください。

`.env.local` は秘密情報を含むため、`.gitignore` に含まれていることを必ず確認してください（`create-next-app` で作成した場合は標準で除外されています）。

### 5️⃣ Supabase クライアントの導入を依頼する

```
@supabase/supabase-js をインストールして、
lib/supabase.ts にSupabaseクライアントを初期化するコードを作成してください。
環境変数 NEXT_PUBLIC_SUPABASE_URL と NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY を使ってください。
```

Claude Code が以下のようなインストールとファイル作成を行います。

```bash
npm install @supabase/supabase-js
```

```ts
// lib/supabase.ts
import { createClient } from "@supabase/supabase-js";

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabasePublishableKey = process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY!;

export const supabase = createClient(supabaseUrl, supabasePublishableKey);
```

（旧プロジェクトで anon key しかない場合は、`NEXT_PUBLIC_SUPABASE_ANON_KEY` という変数名に読み替えて同様に実装してください）

### 6️⃣ Supabase 側にテーブルを作成する

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

### 7️⃣ 一覧表示・追加・削除機能の実装を依頼する

```
todosテーブルのデータを一覧表示し、
入力欄から新規追加、各項目に削除ボタンを付けたページを
app/page.tsx に実装してください。Supabaseクライアントはlib/supabase.tsを使ってください。
```

Claude Code が `app/page.tsx` を編集し、`useEffect` でのデータ取得、`insert`・`delete` の処理などを実装します。

### 8️⃣ 動作確認

```bash
npm run dev
```

http://localhost:3000 を開き、以下を確認します。

- ページを開いた時に Supabase 上のデータが一覧表示される
- 入力欄からデータを追加できる
- 削除ボタンでデータが消える

うまく動かない場合は、エラーメッセージをそのまま Claude Code に貼り付けて「このエラーを直してください」と依頼すると修正してくれます。

### 9️⃣ Git へのコミット

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
