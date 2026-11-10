---
description: report-studio が動く環境かを点検する（Playwright MCP・frontend-design・dataviz・最新版かどうか）
---

report-studio の動作に必要な環境を点検し、結果を箇条書きで報告する。点検だけを行い、インストールや設定の変更はしない。

判定は次のとおり。

1. Playwright MCP: `mcp__playwright__browser_navigate` などのブラウザツールが、利用可能なツールの一覧、または ToolSearch（遅延読み込みのツールを含む）で見つかれば「使える」。`mcp__claude-in-chrome__*` は対象外で、これがあっても「使える」としない。
2. `frontend-design`: 利用可能なスキルの一覧に `frontend-design:frontend-design` があれば「使える」。
3. `dataviz`（任意）: スキルの一覧にあれば「使える」。なければ「未導入でも動く」。

4. 版（report-studio 本体）: 次の順に調べる。読み取りだけを行う。
   1. `~/.claude/plugins/known_marketplaces.json` の `report-studio` の `source` が `"source": "github"` でなければ、「GitHub のマーケットプレイスから入れていないので、確認しない」と報告して終わる（`--plugin-dir` で使っている場合など）。
   2. `~/.claude/plugins/installed_plugins.json` の `report-studio@report-studio` の `version` を、現在の版とする。見つからなければ「マーケットプレイス経由で入っていない」と報告して終わる。
   3. 手順 1 の `source.repo` を使い、Bash で `curl -fsS https://raw.githubusercontent.com/<repo>/HEAD/.claude-plugin/plugin.json` を実行し、`version` を最新の版とする。取得できなければ「最新版を確認できなかった」と報告して終わる。
   4. 現在の版と最新の版を、`MAJOR.MINOR.PATCH` の数値で比べる。同じなら「最新」。最新の版が大きければ「更新がある」と報告し、README の「更新する」の 2 つのコマンドを案内する。現在の版が大きければ、その旨だけを報告する。

「使えない」項目には、README の「導入方法」の該当する番号を添える。
- Playwright MCP → 「導入方法」の 2
- `frontend-design` → 「導入方法」の 3

判定は推定であることを、最後に 1 行添える。
