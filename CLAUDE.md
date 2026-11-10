# CLAUDE.md

Claude Code 用プラグイン `report-studio`（`plugins/report-studio/`）。依頼と素材から、1 ファイル完結の HTML レポートを作る。Windows 11 で動作を確かめている。利用者向けの説明は `README.md`。

## コマンド

開発用の依存は `requirements-dev.txt`。`.venv/` は Git 管理外（リポジトリ直下で `python -m venv .venv` を作る）。

```bash
.venv/Scripts/python -m pytest        # 全テスト（形式の検査 test_plugin.py と、HTML の検査 test_check_html.py）
.venv/Scripts/python -m ruff check .  # lint（ルールは pyproject.toml）
```

`test_claude_plugin_validateが通る` は `claude plugin validate --strict` を実行する（`claude` がなければ skip）。

## 構成

- `plugins/report-studio/skills/create/SKILL.md`: レポートを作る手順そのもの。コードはない。
- `plugins/report-studio/skills/doctor/SKILL.md`: 環境の点検。Claude が利用可能なツールとスキルを見て判定するので、スクリプトはない（plugin-rules A4 の例外）。
- `tests/check_html.py`: 作った HTML の検査（外部読み込み・印刷 CSS）。`tests/SCENARIOS.md` は手動の受入シナリオ。

## 守ること

- 版は `plugins/report-studio/.claude-plugin/plugin.json` の `version` だけにある。
- SKILL.md の環境の判定方法は、create と doctor で同じ文面にそろえる。
- 規則は `~/.claude/reference/plugin-rules.md`。SKILL.md や README を直したら、テストを先に流す。
- `docs/superpowers/`・`docs/grill-form/` は `.gitignore` の対象（作業メモの置き場）。
