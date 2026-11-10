# report-studio

希望した内容を伝えるだけで、デザインされた HTML レポートを作る Claude Code プラグイン。CSV やメモをもとに、読み手に合わせたレポートを作りたい人向け。

## 機能

- 依頼文と素材ファイル（CSV・Markdown・テキスト・画像）から、1 ファイルで完結する HTML レポートを作る。
- 足りない情報（目的・読み手・必須の内容・分量）だけを質問する。
- デザイン方向を 2〜3 案出し、選んだ案で `frontend-design` の指針に沿って設計する。
- 作った HTML を Playwright MCP で開き、画面幅 1280px と 375px、印刷表示の崩れを確かめて直す。
- `dataviz` スキルが使える環境では、グラフを描くときの指針にも使う（なくても動く）。
- 印刷（ブラウザの PDF 保存を含む）で崩れにくい。外部 CDN・Web フォント・外部画像は使わない（画像は埋め込む）。

PDF・PowerPoint の生成、複数ページのサイト、フォーム送信などの双方向機能は対象外。

## 前提条件

- Windows 11（動作を確かめた OS）
- Claude Code
- Git（B の clone に使う）
- Node.js 18 以上（Playwright MCP の起動に使う）
- Playwright MCP（必須）
- `frontend-design` プラグイン（必須）

## 導入方法

### 1. プラグインを入れる

次のどちらか 1 つを選ぶ。

**A. GitHub のマーケットプレイスから入れる**

Claude Code の中で、次の 2 つを実行する。

```
/plugin marketplace add asama0101/report-studio
/plugin install report-studio@report-studio
```

**B. clone して入れる**

リポジトリを取得し、取得したフォルダをマーケットプレイスとして登録する。

```
git clone https://github.com/asama0101/report-studio.git
```

Claude Code の中で、次の 2 つを実行する。`<clone したフォルダのパス>` は、clone したフォルダの絶対パス（例: `D:\tools\report-studio`）に置き換える。

```
/plugin marketplace add <clone したフォルダのパス>
/plugin install report-studio@report-studio
```

インストールしたあとは、clone したフォルダを移動・削除しない（インストールが、そのフォルダを直接読んでいる可能性がある。未検証）。

インストールせずに試すだけなら、シェルで次のように起動する。この指定は起動ごとに必要で、指定しない起動では読み込まれない。

```
claude --plugin-dir <clone したフォルダのパス>
```

**A と B を切り替えるとき**

A と B は、どちらも同じ名前（`report-studio`）のマーケットプレイスを登録する。切り替えるには、登録を消して入れ直す。登録を消すと、そのマーケットプレイスから入れた `report-studio` も外れる可能性がある（未検証）。

1. `/plugin marketplace remove report-studio` を実行する。
2. 切り替え先の `/plugin marketplace add ...` を実行する。
3. `/plugin install report-studio@report-studio` を実行する。

元に戻すときは、A と B を入れ替えて同じ手順を行う。

どちらの場合も、`/help` に `report-studio:create` と `report-studio:doctor` が出れば、読み込めている。

### 2. Playwright MCP を登録する

```
claude mcp add -s user playwright -- npx @playwright/mcp@latest --allow-unrestricted-file-access
```

すでに `playwright` を登録している場合は、先に `claude mcp remove playwright -s user` で消してから実行する（登録を消す操作なので、元の設定を控えておく）。

`-s user` は、どのフォルダで使っても Playwright MCP が見えるようにする（付けないと、登録したフォルダだけで有効になる）。`--allow-unrestricted-file-access` は、ローカルの HTML を `file://` で開くために必要。登録後、Claude Code を再起動する。

### 3. frontend-design を入れる

```
/plugin install frontend-design@claude-plugins-official
```

### 4. 環境を点検する

```
/report-studio:doctor
```

### 更新する

新しい版が出たら、Claude Code の中で次の 2 つを実行し、Claude Code を再起動する。B で入れた場合は、先に clone したフォルダで `git pull` を実行する。

```
/plugin marketplace update report-studio
/plugin update report-studio@report-studio
```

## 使い方

```
/report-studio:create 先月の売上 CSV（C:\data\sales.csv）を、経営会議向けのレポートにして
```

1. 足りない点だけ質問される。
2. デザイン方向が 2〜3 案出るので、選ぶ。
3. 実行したフォルダ直下に `YYYY-MM-DD-題名.html` が保存される。完了報告に、保存先のパス、デザイン方針、検証の結果が出る。

完了報告の例（内容は依頼ごとに変わる）:

```
保存先: C:\work\2026-11-10-先月の売上.html
デザイン方針: 落ち着いた紺と白を基調にした、経営会議向けの構成。
検証: 幅 1280px と 375px、印刷表示を確認。375px で表がはみ出したため、横スクロールに直した。
```

修正は、同じ会話で「色を変えて」「章を足して」のように頼む。

素材の内容（機密情報を含む）は HTML にそのまま入る。共有する前に確かめる。

### 素材の扱い

| 素材 | 扱い |
|---|---|
| CSV・Markdown・テキスト | そのまま読む。 |
| 画像（PNG・JPG） | HTML に埋め込む。大きい画像は縮小するか、確認される。 |
| Excel など | 読める関連スキルがあるときだけ読む。読めなければ、その旨が伝えられる。 |
| 1000 行を超える CSV | 全件は載せない。集計・要約した結果だけを載せる。 |

会話の内容は素材にならない。素材にしたい内容は、ファイルにして渡す。

## 困ったとき

### HTML が作られず、Playwright MCP が使えないと伝えられる

Playwright MCP が登録されていない、または再起動していない。導入方法の 2 を行い、`/report-studio:doctor` で確かめる。

### 検証で `file://` が開けない

Playwright MCP が `--allow-unrestricted-file-access` なしで登録されている。導入方法の 2 のコマンドで登録し直す。

### 同じ名前のファイルがある

上書きしてよいか聞かれる。「いいえ」と答えると、末尾に `-2`, `-3` を付けた名前で保存される。

## ライセンス

[MIT License](LICENSE)
