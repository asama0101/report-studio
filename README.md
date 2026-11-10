# report-studio

希望した内容を伝えるだけで、デザインされた HTML レポートを作る Claude Code プラグイン。

## 機能

- 依頼文と素材ファイル（CSV・Markdown・テキスト・画像）から、1 ファイルで完結する HTML レポートを作る。
- 足りない情報（目的・読み手・必須の内容・分量）だけを質問する。
- デザイン方向を 2〜3 案出し、選んだ案で `frontend-design` の指針に沿って設計する。
- 作った HTML を Playwright MCP で開き、画面幅 1280px と 375px、印刷表示の崩れを確かめて直す。
- 印刷・PDF 出力に耐える。外部 CDN・Web フォント・外部画像は使わない（画像は埋め込む）。

PDF・PowerPoint の生成、複数ページのサイト、フォーム送信などの双方向機能は対象外。

## 前提条件

- Windows 11（動作を確かめた OS）
- Claude Code
- Node.js 18 以上（Playwright MCP の起動に使う）
- Playwright MCP（必須）
- `frontend-design` プラグイン（必須）
- `dataviz` スキル（任意。グラフを描くときの指針になる）

## 導入方法

### 1. プラグインを読み込む

```
claude --plugin-dir D:\claude\local-repo\xxx
```

`/help` に `report-studio:create` と `report-studio:doctor` が出れば、読み込めている。

### 2. Playwright MCP を登録する

```
claude mcp add -s user playwright -- npx @playwright/mcp@latest --allow-unrestricted-file-access
```

`-s user` は、どのフォルダで使っても Playwright MCP が見えるようにする（付けないと、登録したフォルダだけで有効になる）。`--allow-unrestricted-file-access` は、ローカルの HTML を `file://` で開くために必要。登録後、Claude Code を再起動する。

### 3. frontend-design を入れる

```
/plugin install frontend-design@claude-plugins-official
```

### 4. 環境を点検する

```
/report-studio:doctor
```

## 使い方

```
/report-studio:create 先月の売上 CSV（C:\data\sales.csv）を、経営会議向けのレポートにして
```

1. 足りない点だけ質問される。
2. デザイン方向が 2〜3 案出るので、選ぶ。
3. 実行したフォルダ直下に `YYYY-MM-DD-題名.html` が保存される。完了報告に、保存先のパス、デザイン方針、検証の結果が出る。

修正は、同じ会話で「色を変えて」「章を足して」のように頼む。

素材の内容（機密情報を含む）は HTML にそのまま入る。共有する前に確かめる。

## 困ったとき

### 「Playwright MCP が使えません」と出て、HTML が作られない

Playwright MCP が登録されていない、または再起動していない。導入方法の 2 を行い、`/report-studio:doctor` で確かめる。

### 検証で `file://` が開けない

Playwright MCP が `--allow-unrestricted-file-access` なしで登録されている。導入方法の 2 のコマンドで登録し直す。

### 同じ名前のファイルがある

上書きしてよいか聞かれる。「いいえ」と答えると、末尾に `-2`, `-3` を付けた名前で保存される。
