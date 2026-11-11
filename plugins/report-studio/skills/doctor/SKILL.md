---
name: doctor
description: report-studio が動く環境かを点検し、足りないものと対処の手順を出す。Playwright MCP・frontend-design・dataviz の有無と、GitHub をマーケットプレイスに登録していれば最新版かどうかを、項目ごとに伝える。「環境を点検して」「doctor」「動かない原因を調べて」と頼まれたときに使う。何も変更しない。レポートの作成には使わない（create）。Windows 専用。
disable-model-invocation: true
---

report-studio の動作に必要な環境を点検し、結果を、共通の行形式で報告する。1 行 1 項目で、`[OK]`・`[NG]`（必須が足りない）・`[任意]`（なくても動く）・`[情報]`（版）のどれかを付け、対処は次の行に「→」で書く。点検だけを行い、インストールや設定の変更はしない。

判定は次のとおり。

1. Playwright MCP: `mcp__playwright__browser_navigate` などのブラウザツールが、利用可能なツールの一覧、または ToolSearch（遅延読み込みのツールを含む）で見つかれば `[OK]`、なければ `[NG]`。`mcp__claude-in-chrome__*` は対象外で、これがあっても `[OK]` としない。
2. `frontend-design`: 利用可能なスキルの一覧に `frontend-design:frontend-design` があれば `[OK]`、なければ `[NG]`。
3. `dataviz`（任意）: スキルの一覧にあれば `[OK]`、なければ `[任意]`（未導入でも動く）。

4. プラグインのバージョン（report-studio 本体）: 次の順に調べる。読み取りだけを行う。行の頭は `[情報] プラグインのバージョン: v<現在のバージョン>`。
   1. `${CLAUDE_PLUGIN_ROOT}/.claude-plugin/plugin.json` の `version` を、現在のバージョンとする。
   2. `~/.claude/plugins/known_marketplaces.json` の `report-studio` の `source` が `"source": "github"` でなければ（`--plugin-dir` で使っている場合など）、「（GitHub のマーケットプレイスに登録していないため、最新かは確認しません）」を続けて終わる。
   3. 手順 2 の `source.repo` を使い、Bash で `curl -fsS https://raw.githubusercontent.com/<repo>/HEAD/plugins/report-studio/.claude-plugin/plugin.json` を実行し、`version` を最新のバージョンとする。取得できないとき、または手順 2 のファイルを読めないときは、「（最新のバージョンを確認できませんでした: <理由>）」を続け、次の行に「  → ネットワークにつながっているか、github.com への通信を止めていないかを確認する」を書いて終わる。
   4. 現在と最新を、`MAJOR.MINOR.PATCH` の数値で比べる。現在が最新以上なら「（最新です）」。最新が大きければ「（GitHub に v<最新> があります）」を続け、次の 3 行を書く。
      - `  → /plugin marketplace update report-studio を実行する`
      - `  → /plugin update report-studio@report-studio を実行する`
      - `  → Claude Code を開き直す`

`[NG]` の項目には、README の「導入方法」の該当する番号を添える。
- Playwright MCP → 「導入方法」の 2
- `frontend-design` → 「導入方法」の 3

出力の例:

```
[OK] Playwright MCP: 使えます
[NG] frontend-design: 使えません
  → README の「導入方法」の 3 を行う
[任意] dataviz: 未導入（なくても動く）
[情報] プラグインのバージョン: v1.0.0（最新です）
```

出力は、項目の行と対処の行だけにする（前置きや結びの文は付けない）。
