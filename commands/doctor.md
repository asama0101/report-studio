---
description: report-studio が動く環境かを点検する（Playwright MCP・frontend-design・dataviz）
---

report-studio の動作に必要な環境を点検し、結果を箇条書きで報告する。点検だけを行い、インストールや設定の変更はしない。

判定は次のとおり。

1. Playwright MCP: `mcp__playwright__browser_navigate` などのブラウザツールが、利用可能なツールの一覧、または ToolSearch（遅延読み込みのツールを含む）で見つかれば「使える」。`mcp__claude-in-chrome__*` は対象外で、これがあっても「使える」としない。
2. `frontend-design`: 利用可能なスキルの一覧に `frontend-design:frontend-design` があれば「使える」。
3. `dataviz`（任意）: スキルの一覧にあれば「使える」。なければ「未導入でも動く」。

「使えない」項目には、README の「導入方法」の該当する番号を添える。
- Playwright MCP → 「導入方法」の 2
- `frontend-design` → 「導入方法」の 3

判定は推定であることを、最後に 1 行添える。
