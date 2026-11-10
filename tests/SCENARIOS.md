# 手動シナリオ

空の作業用フォルダ `D:\claude\local-repo\report-studio\tests\work` を作り、そこで `claude --plugin-dir D:\claude\local-repo\report-studio\plugins\report-studio` を起動して、上から順に実行する（保存先は起動時のカレントフォルダ直下になる）。

生成された HTML は、毎回 `D:\claude\local-repo\report-studio\.venv\Scripts\python D:\claude\local-repo\report-studio\tests\check_html.py <HTML のパス>` で検査する（外部読み込みと印刷 CSS）。`.venv` は、リポジトリ直下で `python -m venv .venv` を作り、`.venv\Scripts\pip install -r requirements-dev.txt` で整える。

サンプル素材: `D:\claude\local-repo\report-studio\tests\fixtures\sales.csv`（12 か月分。最終行の備考に `<script>alert(1)</script>` を含む）

大量データの素材（シナリオ 9）: `D:\claude\local-repo\report-studio\.venv\Scripts\python -c "import csv; w=csv.writer(open(r'D:\claude\local-repo\report-studio\tests\work\big.csv','w',newline='',encoding='utf-8')); w.writerow(['id','value']); [w.writerow([i,i*3]) for i in range(5000)]"`

Playwright MCP の無効化（シナリオ 10）: `claude --strict-mcp-config` で起動する（設定済みの MCP を読み込まない）。終わったら通常の起動に戻す。

※ 結果欄は、2026-11-10 の実施結果（構成変更前）に、2026-11-11 に新しい構成（plugins/report-studio/）で再実施した結果を足したもの。再実施は、非対話の `claude -p` を、git 管理外の作業フォルダで行った（リポジトリ内の `tests/work` では、git-flow のフックが main 上の作業を止める）。

| # | 受入条件 | 手順 | 期待結果 | 結果 |
|---|---|---|---|---|
| 1 | 1 | 起動後に `/help` を開く | `report-studio:create` と `report-studio:doctor` が出る | 一部: /help は未確認。--plugin-dir で create と doctor の両方が実行できた; 2026-11-11 再実施（plugins/report-studio/ の構成）: `/report-studio:doctor` が実行でき、create と doctor が解決された。/help の表示は未確認 |
| 2 | 9 | `/report-studio:doctor` を実行 | Playwright MCP・`frontend-design`・`dataviz` が、使える／使えない／未導入でも動く で箇条書きになる。使えない項目に README の節名が付く | 通過: 環境が揃った場合は 3 項目とも「使える」。`--strict-mcp-config` では Playwright MCP が「使えない」になり、README の「導入方法」の 2 を案内した; 2026-11-11 再実施（非対話の `claude -p`）: Playwright MCP・frontend-design・dataviz の 3 項目とも「使える」。版の確認は `known_marketplaces.json` などの読み取り権限がなく止まった（対話で承認すれば確認できる見込み・未確認） |
| 3 | 2, 4, 5, 10 | `/report-studio:create D:\claude\local-repo\report-studio\tests\fixtures\sales.csv を、経営会議向けの月次売上レポートにして。読み手は役員、A4 で 2 ページ程度、売上の推移と件数を中心に` | 質問なしでデザイン方向の選択に進む。選ぶと `YYYY-MM-DD-題名.html` が作業フォルダ直下にできる。CSV の月・売上が本文に入り、選んだ方向が見た目に出る。完了報告に保存先の絶対パス、デザイン方針、検証結果（画面幅と直した点）が入る | 通過（デザイン選択は依頼文に含めて代替）。質問なしで案を提示し、HTML 生成、1280px/375px/印刷表示とも崩れなし。SKILL.md 修正後に再実行し、本文の数値（7月以降の最小 148 万円、前月比 +7.1%、後半/前半 +15.9%・+17.9% ほか）を CSV から計算して一致を確認; 2026-11-11 再実施（非対話・デザイン選択は依頼文で代替）: 通過。HTML 生成、1280px/375px/印刷表示を確認し、375px で表の月が折り返す点を 1 回直した。完了報告に保存先・デザイン方針・検証結果あり。作業フォルダに生成用の `gen/gen.py` とスクリーンショット 2 枚が残った |
| 4 | 3, 6 | シナリオ 3 の HTML に `check_html.py` を実行。ブラウザで印刷表示にして横スクロールがないことを見る | `OK` が出る。横方向のはみ出しがない | 通過: check_html OK、印刷表示で scrollWidth=clientWidth=779、2 ページ; 2026-11-11 再実施: 通過。check_html OK。印刷表示で scrollWidth=clientWidth |
| 5 | Review Focus | シナリオ 3 の HTML を開く | `<script>alert(1)</script>` が文字として表示され、実行されない（アラートが出ない） | 通過: <script> は文字で表示、script 要素 0、アラートなし; 2026-11-11 再実施: 通過。script 要素 0、文字として表示、アラートなし |
| 6 | 2 | `/report-studio:create 週次報告のレポートを作って` | 目的・読み手・必須の内容・分量のうち分からないものだけが、1 回 4 問以内で聞かれる | 通過: 目的・読み手が分かる依頼（「来月の社内勉強会の案内、読み手は新入社員」）で、不足する必須の内容と分量だけを質問（任意の配色の希望も添えた）。全項目が不足する依頼（「週次報告のレポートを作って」）では 4 項目すべてを質問; 2026-11-11 再実施（非対話。質問ツールがなく、文章で質問）: 通過。素材・目的・読み手・必須の内容と分量の 4 点だけを聞き、推測で埋めなかった |
| 7 | 7 | シナリオ 3 と同じ依頼をもう一度実行し、同名の上書きを聞かれたら「いいえ」 | 既存のファイルが残り、末尾に `-2` が付いた別名で保存される | 通過: 既存を残し 2026-11-10-report-2.html で保存（「いいえ」は依頼文で代替）; 2026-11-11 再実施（「いいえ」は依頼文で代替）: 通過。既存を変えず `-2` の別名で保存。最終応答は `No messages returned from query` で取れなかった |
| 8 | Review Focus | `/report-studio:create ???:*? のレポートを作って`（題名が禁則文字だけになる依頼） | 保存名が `YYYY-MM-DD-report.html` になる | 通過: 2026-11-10-report.html で保存; 2026-11-11 再実施: 依頼文に「のレポート」が残る指示では `のレポート` になる（仕様どおり、題名が空でないため）。題名を「???:*?」だけにすると `YYYY-MM-DD-report.html` になり、通過 |
| 9 | Review Focus | 上の手順で作った `big.csv`（5000 行、`D:\claude\local-repo\report-studio\tests\work\big.csv`）を素材にして依頼する | 全件の羅列ではなく、集計・要約がレポートに載る | 通過: `python -I` のみ許可して再実行。5000 行を全件載せず、件数 5,000・合計 37,492,500・最大 14,997・最小 0・ヒストグラム（10 区間）を載せた。1280px/375px/印刷表示とも崩れなし; 2026-11-11 再実施: 通過。5000 行を全件載せず、件数・合計・最大・最小・分布（10 区間）を載せた。check_html OK |
| 10 | 8 | `claude --strict-mcp-config` で起動し、`/report-studio:create 簡単なレポートを作って` | HTML は作られず、使えないものと `/report-studio:doctor`、README の導入手順が案内される | 通過; 2026-11-11 再実施（`--strict-mcp-config`）: 通過。HTML は作られず、使えないものと `/report-studio:doctor`、README の導入手順を案内 |
