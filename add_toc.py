#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub用のMarkdownに「見出し2(##)と見出し3(###)」の目次を自動挿入するスクリプト。

- 入力Markdownを読み込み
- ## / ### 見出しからTOCを生成（GitHubアンカー相当のslugを生成）
- ファイル先頭（またはマーカー位置）に目次を挿入して書き戻し

使い方:
  python add_toc.py input.md -o output.md
  python add_toc.py input.md --inplace

任意（推奨）: 目次の挿入位置を固定したい場合、Markdown内に次のマーカーを置けます。
  <!-- TOC -->
  <!-- /TOC -->
この場合、その範囲を差し替えます（なければ先頭に挿入）。
"""

from __future__ import annotations

import argparse
import re
import unicodedata
from pathlib import Path
from typing import List, Tuple


TOC_START = "<!-- TOC -->"
TOC_END = "<!-- /TOC -->"


# 見出し行の検出（コードブロック ``` の中は無視）
# 重複した見出しのアンカー番号（-1, -2 ...）を正しく数えるため、# 〜 ###### をすべて拾う
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")


def strip_md_inline(text: str) -> str:
    """
    見出しテキストからインラインMarkdownっぽい装飾を軽く除去。
    GitHubのアンカー生成はもう少し複雑ですが、見出しが素直なら十分一致します。
    """
    t = text.strip()
    # 末尾の # を除去（Markdownの慣習: "## Title ##"）
    t = re.sub(r"\s+#+\s*$", "", t).strip()
    # インラインコード
    t = re.sub(r"`([^`]+)`", r"\1", t)
    # 強調
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
    t = re.sub(r"\*([^*]+)\*", r"\1", t)
    t = re.sub(r"__([^_]+)__", r"\1", t)
    t = re.sub(r"_([^_]+)_", r"\1", t)
    # リンク [text](url) → text
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    # 画像 ![alt](url) → alt
    t = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", t)
    return t.strip()


def github_slugify(heading_text: str) -> str:
    """
    GitHubの見出しアンカー（github-slugger と同じ規則）のslugを作ります。

    ルール:
    - 小文字化
    - 次の文字だけ残し、それ以外（記号・絵文字・①などの丸数字・全角スペース）は消す
      文字(L) / 結合文字(M) / 数字(Nd, Nl) / 連結記号(Pc: _ など) / '-' / 半角スペース
    - 半角スペースを1つずつ '-' に置き換える
      （連続した '-' や先頭・末尾の '-' もそのまま残す）

    例: "① Supabase でテーブルを作成" → "-supabase-でテーブルを作成"
    """
    s = strip_md_inline(heading_text).lower()

    out = []
    for ch in s:
        cat = unicodedata.category(ch)
        if ch in (" ", "-") or cat[0] in ("L", "M") or cat in ("Nd", "Nl", "Pc"):
            out.append(ch)

    return "".join(out).replace(" ", "-")


def extract_headings(md: str, toc_title: str = "目次") -> List[Tuple[int, str, str]]:
    """
    Markdownから見出し（##, ###）を抽出。
    戻り値: [(level, raw_title, anchor), ...]

    GitHubは同じアンカーが2回目以降に出ると "-1", "-2" ... を付けるので、
    すべての見出し（先頭に入る目次の見出しも含む）を数えて同じ番号を付ける。
    """
    headings: List[Tuple[int, str, str]] = []
    seen: dict[str, int] = {github_slugify(toc_title): 1}

    in_fenced = False
    in_toc = False
    fence_re = re.compile(r"^\s*```")  # ```で始まる行

    for line in md.splitlines():
        # 既存の目次（マーカー内）は数えない
        if line.strip() == TOC_START:
            in_toc = True
            continue
        if line.strip() == TOC_END:
            in_toc = False
            continue
        if in_toc:
            continue

        if fence_re.match(line):
            in_fenced = not in_fenced
            continue
        if in_fenced:
            continue

        m = HEADING_RE.match(line)
        if not m:
            continue

        hashes, title = m.group(1), m.group(2).strip()
        level = len(hashes)
        anchor = github_slugify(title)
        if anchor in seen:
            n = seen[anchor]
            seen[anchor] += 1
            anchor = f"{anchor}-{n}"
        else:
            seen[anchor] = 1

        if level in (2, 3) and anchor:  # 目次に載せるのは ## と ### だけ
            headings.append((level, title, anchor))

    return headings


def build_toc(headings: List[Tuple[int, str, str]], toc_title: str = "目次") -> str:
    """
    見出し2/3のTOCをMarkdownで生成。
    """
    lines: List[str] = []
    lines.append(f"## {toc_title}")
    lines.append("")

    for level, title, anchor in headings:
        indent = "" if level == 2 else "  "
        lines.append(f"{indent}- [{title}](#{anchor})")

    lines.append("")
    return "\n".join(lines)


def upsert_toc(md: str, toc_md: str) -> str:
    """
    TOCマーカーがあれば差し替え、なければ先頭に挿入。
    """
    if TOC_START in md and TOC_END in md:
        pattern = re.compile(
            re.escape(TOC_START) + r".*?" + re.escape(TOC_END),
            flags=re.DOTALL,
        )
        replacement = f"{TOC_START}\n\n{toc_md}\n{TOC_END}"
        return pattern.sub(replacement, md, count=1)

    # マーカーがない場合: 先頭にTOC + 区切りを追加
    return f"{toc_md}\n---\n\n{md.lstrip()}"


def main() -> None:
    ap = argparse.ArgumentParser(description="GitHub用MarkdownにTOC（##/###）を挿入します。")
    ap.add_argument("input", type=Path, help="入力Markdownファイル")
    ap.add_argument("-o", "--output", type=Path, help="出力先（省略時は標準出力）")
    ap.add_argument("--inplace", action="store_true", help="入力ファイルを上書きする")
    ap.add_argument("--title", default="目次", help="TOCの見出しタイトル（既定: 目次）")
    args = ap.parse_args()

    md = args.input.read_text(encoding="utf-8")

    headings = extract_headings(md, toc_title=args.title)
    toc = build_toc(headings, toc_title=args.title)
    new_md = upsert_toc(md, toc)

    if args.inplace:
        args.input.write_text(new_md, encoding="utf-8")
        return

    if args.output:
        args.output.write_text(new_md, encoding="utf-8")
        return

    print(new_md)


if __name__ == "__main__":
    main()
