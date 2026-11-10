# report-studio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 利用者が希望した内容で、`frontend-design` の指針に沿った 1 ファイル完結の HTML レポートを生成する Claude Code プラグイン `report-studio` を作る。

**Architecture:** プラグインは Markdown 中心（スキル `create`・コマンド `doctor`・README）。生成ロジックはスキルの指示文で表し、コードは持たない。機械的に確かめられる受入条件（構成・HTML の外部参照・印刷 CSS）は、Python の検査スクリプト 2 本で確かめ、残りは手動シナリオで確かめる。

**Tech Stack:** Claude Code プラグイン（`.claude-plugin/plugin.json`、`skills/*/SKILL.md`、`commands/*.md`）、Python 3（標準ライブラリのみ、検査スクリプト用）、Playwright MCP（実行時の検証用）。

**Spec:** `D:\claude\local-repo\xxx\docs\grill-form\specs\2026-11-10-html-report-plugin-design.md`

## Global Constraints

- プラグインのルートは `D:\claude\local-repo\xxx\`。直下に `.claude-plugin\plugin.json`、`skills\create\SKILL.md`、`commands\doctor.md`、`README.md` を置く。
- プラグイン名 `report-studio`、スキル名 `create`（`/report-studio:create`）、コマンド名 `doctor`（`/report-studio:doctor`）。
- ローカルでの使い方は `claude --plugin-dir D:\claude\local-repo\xxx`。配布・マーケットプレイス・GitHub 公開はしない。
- git 管理は対象外（git 初期化も、コミットの手順も書かない）。
- 出力 HTML は 1 ファイル完結。外部 CDN・Web フォント・外部画像は不可。画像は base64 インライン。`@media print` を常に入れる。
- 保存名は `YYYY-MM-DD-題名.html`、保存先は利用者のカレントフォルダ直下。題名は最大 40 文字、`\ / : * ? " < > |` を除き、空なら `report`。同名なら確認し、「いいえ」は連番 `-2`, `-3`…。
- 検証は幅 1280px と 375px、印刷表示、修正は最大 3 回。
- 環境判定: Playwright MCP は `mcp__playwright__browser_*`（`mcp__claude-in-chrome__*` は対象外）、`frontend-design` は `frontend-design:frontend-design`、`dataviz` は任意。
- 不足補完の質問は 1 回に最大 4 問。デザイン案は毎回 2〜3 案を AskUserQuestion で出す。
- 言語は日本語で書く（README・SKILL.md・doctor.md）。

## Review Focus

- 題名が禁則文字だけのとき: 保存名が `YYYY-MM-DD-report.html` になる。
- 素材に `<script>` を含む CSV セルがあるとき: HTML にエスケープして埋め込まれ、実行されない。
- 同名ファイルがあり「いいえ」と答えたとき: 既存を壊さず `-2` で保存される。
- 素材が数千行の CSV のとき: 全件ではなく集計・要約が載り、コンテキストを使い切らない。
- Playwright MCP がない環境: HTML を作らず止まり、`doctor` と README を案内する。

---

### Task 1: プラグインの骨格と構成検査

**Files:**
- Create: `D:\claude\local-repo\xxx\tests\check_plugin.py`
- Create: `D:\claude\local-repo\xxx\.claude-plugin\plugin.json`

**Interfaces:**
- Produces: `python tests\check_plugin.py` は、成功で終了コード 0、失敗で 1 と不足項目を標準出力に出す。Task 2〜4 がファイルを置くたびにこれを再実行する。

- [ ] **Step 1: 失敗する検査を書く** `tests\check_plugin.py`。次を確かめる関数 `main() -> int`:
  - `.claude-plugin/plugin.json` が有効な JSON で `name == "report-studio"`、`description` が空でない。
  - `skills/create/SKILL.md` が存在し、frontmatter に `name: create` と空でない `description:` がある。
  - `commands/doctor.md` が存在し、frontmatter に `description:` がある。
  - `README.md` が存在し、`--plugin-dir`・`Playwright`・`frontend-design` の 3 語をすべて含む。
  - ルートはスクリプトの親の親フォルダ（`Path(__file__).resolve().parent.parent`）。
- [ ] **Step 2: 失敗を確認する**
  Run: `python D:\claude\local-repo\xxx\tests\check_plugin.py`
  Expected: 終了コード 1、`plugin.json` が見つからない旨が出る。
- [ ] **Step 3: `plugin.json` を作る** `{"name":"report-studio","description":"希望した内容で、frontend-design の指針に沿った 1 ファイル完結の HTML レポートを生成する","version":"0.1.0"}`
- [ ] **Step 4: 再実行して進捗を確認する**
  Run: 同上
  Expected: `plugin.json` の項目は通り、SKILL.md・doctor.md・README.md の不足だけが残る。

### Task 2: `create` スキル

**Files:**
- Create: `D:\claude\local-repo\xxx\skills\create\SKILL.md`

**Interfaces:**
- Consumes: Task 1 の `check_plugin.py`。
- Produces: スキル本文が参照する「環境の判定方法」の節。Task 3 の `doctor.md` が同じ文言を使う。

- [ ] **Step 1: SKILL.md を書く。** frontmatter は `name: create` と、トリガーを含む `description`（「HTML のレポートを作って」「レポートを HTML で」などの依頼で使う。既存 HTML の編集には使わない）。本文は SPEC の「流れ」1〜8 と「HTML の仕様」を、手順 1〜8 の番号付きでそのまま指示文にする。次を省略しない:
  - 手順 1 の環境判定（Playwright MCP は `mcp__playwright__browser_navigate` が使えるか、`frontend-design` はスキル一覧に `frontend-design:frontend-design` があるか）と、使えないときの案内文（`/report-studio:doctor` と README）。
  - 手順 3 の質問項目（目的・読み手・必須の内容・分量）と 1 回最大 4 問。
  - 手順 4 のデザイン案 2〜3 案（トーン・配色・書体・レイアウト）と、「その他」での作り直し。
  - 手順 5 の `frontend-design` 呼び出し時に渡す 3 点（方向・素材・制約）と、制約優先、素材のエスケープ、大きい素材の集計・要約、数値の照合。
  - 手順 6 の保存名規則（Global Constraints のとおり）。
  - 手順 7 の検証（幅・印刷表示・修正 3 回、`file://` が開けないときは止まって設定を案内）。
  - 手順 8 の完了報告 3 点。
- [ ] **Step 2: 構成検査を実行する**
  Run: `python D:\claude\local-repo\xxx\tests\check_plugin.py`
  Expected: SKILL.md の項目が通る。
- [ ] **Step 3: SPEC との照合** SKILL.md の手順 1〜8 を SPEC の流れ 1〜8 と見比べ、Review Focus の 5 件それぞれに対応する指示文があることを確認する（なければ足す）。

### Task 3: `doctor` コマンド

**Files:**
- Create: `D:\claude\local-repo\xxx\commands\doctor.md`

**Interfaces:**
- Consumes: Task 2 の環境判定の文言。

- [ ] **Step 1: doctor.md を書く。** frontmatter は `description: report-studio が動く環境かを点検する`。本文は次を指示する: Playwright MCP のブラウザツール／`frontend-design` スキル／`dataviz` スキル（任意）を、Task 2 と同じ判定で調べ、各項目を「使える」「使えない」（任意項目は「未導入でも動く」）の箇条書きで示す。使えない項目には README の該当節名を添える。点検のみで、インストールや設定の変更はしない。
- [ ] **Step 2: 構成検査を実行する**
  Run: `python D:\claude\local-repo\xxx\tests\check_plugin.py`
  Expected: doctor.md の項目が通る。

### Task 4: README

**Files:**
- Create: `D:\claude\local-repo\xxx\README.md`

- [ ] **Step 1: README を書く。** 節: 概要／必要な環境（Playwright MCP、`frontend-design`、任意の `dataviz`）／導入（`claude --plugin-dir D:\claude\local-repo\xxx`、Playwright MCP の登録方法、`frontend-design` の導入方法）／使い方（`/report-studio:create 〇〇のレポートを作って`、`/report-studio:doctor`）／制約（SPEC の非目標を要約）。Playwright MCP の登録コマンドは、実行前に `claude mcp add --help` で確認し、確認した書式を載せる（推測で書かない）。
- [ ] **Step 2: 構成検査を実行する**
  Run: `python D:\claude\local-repo\xxx\tests\check_plugin.py`
  Expected: 終了コード 0、全項目が通る。

### Task 5: 生成 HTML の検査スクリプトと手動シナリオ

**Files:**
- Create: `D:\claude\local-repo\xxx\tests\check_html.py`
- Create: `D:\claude\local-repo\xxx\tests\test_check_html.py`
- Create: `D:\claude\local-repo\xxx\tests\fixtures\sales.csv`
- Create: `D:\claude\local-repo\xxx\tests\SCENARIOS.md`

**Interfaces:**
- Produces: `check_html.find_problems(html: str) -> list[str]`。問題がなければ空リスト。CLI は `python tests\check_html.py <html のパス>` で、問題を 1 行ずつ出し、なければ終了コード 0。

- [ ] **Step 1: 失敗するテストを書く** `test_check_html.py`（unittest）。ケース:
  - 外部の `<script src="https://x/y.js">` を含む HTML → 問題に「外部読み込み」が含まれる。
  - `<link href="https://...">`、`@import url(https://...)`、`url(http://...)` も同様に検出される。
  - `<svg xmlns="http://www.w3.org/2000/svg">` と `<a href="https://example.com">` は検出されない。
  - `@media print` がない HTML → 問題に「印刷 CSS」が含まれる。
  - 外部参照がなく `@media print` がある HTML → 空リスト。
- [ ] **Step 2: 失敗を確認する**
  Run: `python -m unittest D:\claude\local-repo\xxx\tests\test_check_html.py -v`
  Expected: FAIL（`check_html` がない）。
- [ ] **Step 3: `check_html.py` を実装する。** 外部読み込みは、`src=`・`<link ... href=`・`@import`・`url(` の引数が `http://` または `https://` で始まるものだけを正規表現で見る。
- [ ] **Step 4: 通過を確認する**
  Run: 同上
  Expected: 全ケース PASS。
- [ ] **Step 5: フィクスチャと手動シナリオを書く。** `sales.csv` は月・売上・件数の 12 行に、`<script>alert(1)</script>` を含むセルを 1 行混ぜる。`SCENARIOS.md` は受入条件 1・2・4・5・6・7・8・9・10 と Review Focus の 5 件を、「手順」「期待結果」の表で書く（受入条件 8 は Playwright MCP を無効にして起動する手順を含む）。各シナリオで生成された HTML には `check_html.py` を実行する旨を書く。

### Task 6: 通しの確認

- [ ] **Step 1: 構成検査と単体テストを実行する**
  Run: `python D:\claude\local-repo\xxx\tests\check_plugin.py` と `python -m unittest D:\claude\local-repo\xxx\tests\test_check_html.py`
  Expected: どちらも成功。
- [ ] **Step 2: 手動シナリオを実行する。** `claude --plugin-dir D:\claude\local-repo\xxx` で起動し、`SCENARIOS.md` を上から順に実行して結果を表に記録する。失敗した項目は該当タスクに戻って直す。
- [ ] **Step 3: 完了報告** 通ったシナリオ・通らなかったシナリオを、証拠（保存された HTML のパスと `check_html.py` の出力）つきで報告する。

---

## Self-Review

- **Spec coverage:** 受入条件 1→Task 1・6、2・4・5→Task 2・5（手動）、3・6→Task 5、7→Task 2・5、8→Task 2・4、9→Task 3、10→Task 2。非目標は README（Task 4）に反映。
- **Step scan:** コードの本体は書かず、署名・テストケース・値を指定した。
- **Type consistency:** `find_problems(html: str) -> list[str]` を Task 5 の中だけで使う。
- **Review Focus:** 5 件とも Task 2 の指示文と Task 5 のシナリオで押さえた。
- **Proportion:** SPEC より短い。
