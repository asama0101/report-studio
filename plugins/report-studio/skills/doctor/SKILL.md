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

4. プラグインのバージョン（report-studio 本体。項目名は「プラグインのバージョン」）: 次の順に調べる。読み取りだけを行う。
   1. `~/.claude/plugins/known_marketplaces.json` の `report-studio` の `source` が `"source": "github"` でなければ、「GitHub のマーケットプレイスから入れていないので、確認しない」と`[情報]` で報告して終わる（`--plugin-dir` で使っている場合など）。
   2. `~/.claude/plugins/installed_plugins.json` の `report-studio@report-studio` の `version` を、現在の版とする。見つからなければ「マーケットプレイス経由で入っていない」と`[情報]` で報告して終わる。
   3. 手順 1 の `source.repo` を使い、Bash で `curl -fsS https://raw.githubusercontent.com/<repo>/HEAD/plugins/report-studio/.claude-plugin/plugin.json` を実行し、`version` を最新の版とする。取得できなければ「最新版を確認できなかった」と `[情報]` で報告して終わる。
   4. 現在の版と最新の版を、`MAJOR.MINOR.PATCH` の数値で比べる。同じなら「最新です」。最新の版が大きければ「GitHub に vX.Y.Z があります」と `[情報]` で報告し、次の行に「→」で README の「更新する」の 2 つのコマンドを案内する。現在の版が大きければ、その旨だけを報告する。

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
