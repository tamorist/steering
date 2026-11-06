# Steering Within Limits — website

Source for the website of the package proposal *Steering Within Limits* (Youth GCC, Global Citizen Will Platform, Planetary OS). Built with MkDocs (Material theme) and published with GitHub Pages.

## サイトの更新のしかた（日本語）

1. 元の文書（このフォルダの外、`世界市民の民意集約システム/` の各フォルダ）を直す。英語版が正本。
2. `python3 build_content.py` を実行する。公開する文書だけが `docs/` にコピーされ、図が差し込まれる。
   - 公開する文書の一覧は `build_content.py` の `PAGES`。アーカイブ、メモ、事実確認リスト、修正プランなどは含めない。
   - スライドを直したときは、先に `python3 src/slides/_make_slides.py` を実行する。
3. `mkdocs serve` で確認する（http://127.0.0.1:8000）。
4. コミットして `main` に push すると、GitHub Actions がサイトを作り、GitHub Pages に公開する。

## リンクの管理

- 文書の中のリンク先は、リンク台帳 `../links.toml` の ID で書きます（`[link:package]`、`［リンク:package］`、別の言語を指すときは `[link:series@ja]`）。
- `build_content.py` が、出力先ごとに自動で解決します。
  - **サイト**：サイト内のページへのリンク（`→`）。サイトにない資料は外部の URL（`↗`）。どこにもなければリンクを省く。
  - **ページの末尾**：台帳に note・Substack の URL があるページには、「この文書は、次の場所でも公開しています」を自動で加える。
  - **書き出し**（`../_exports/note/`、`../_exports/substack/`）：note は note → Substack → サイトの順、Substack は Substack → note → サイトの順で、最初にある URL。なければ「（準備中）」「(coming soon)」。
- 記事を公開したら、台帳の `note` か `substack` に URL を書き、`build_content.py` を実行し直します。サイトを公開したら、台帳の `[site] base_url` も書きます。
- 台帳にない ID を書くと、ビルドが止まって知らせます。

## サイトと note で中身を出し分ける

1本の原稿の中で、`<!-- package -->` … `<!-- /package -->` で囲んだ部分はサイトにだけ、`<!-- standalone -->` … `<!-- /standalone -->` で囲んだ部分は note・Substack の書き出し（`_exports/`）にだけ出ます。今は世界市民ガバナンスの2本と、入口の4本（はじめての方へ・1ページ概要・なぜ今か・パッケージ提案書）の冒頭にある「このページについて」（誰向けか、読む時間の目安）で使っています。

## 基本情報（連絡先など）の管理

- 名前、メール、フォームの URL など、あとから書き込んだり変えたりする情報は `../info.toml` に書きます。
- 文書の中では `{{contact}}`（名前・メール・Substack・note をまとめた連絡先）、`{{interest_form}}`（関心表明フォームへのリンク）、`{{author}}`、`{{role}}`、`{{profile_url}}` などのキーで書きます。
- 空の項目は、サイトと書き出しで「（準備中）」「(to be added)」と表示します。
- `LICENSE.md` は `LICENSE.template.md` から作られます（著作権者の表記は `info.toml` の `[license]`）。

## 画像の拡大表示

本文の図は、タップ（クリック）すると画面いっぱいに拡大表示されます（プラグイン `mkdocs-glightbox`。設定は `mkdocs.yml` の `plugins`）。拡大した図をもう一度タップすると、さらに拡大して動かせます。

## アクセス解析（GoatCounter）

- `../info.toml` の `[analytics] goatcounter` に、GoatCounter のサイトコードを書くと、すべてのページ（シミュレーターとスライドを含む）に計測用のスクリプトが入ります。空なら何も入りません。
- GoatCounter は Cookie を使わず、個人を特定しない解析ツールです。設定すると、About ページの「プライバシー」に、その旨の説明が自動で入ります。

## 管理レポート

`build_content.py` を実行するたびに、`../管理レポート（自動生成）.md` が作り直されます。

1. 未設定の項目（info.toml の空の項目と、公開先の URL がまだないリンク）
2. リンクの反映先（ID ごとに、サイト・note 用・Substack 用でどこにつながるか、どの文書のどの行で使われているか）
3. 基本情報の反映先（キーごとに、今の値と使われている箇所）
4. 主な数値の出現箇所（還元の割合、クラブの削減率など、一例の数値がどの文書・図の生成スクリプトの何行目に出てくるか。数値を見直すときの直し漏れを防ぐため。対象の数値は `build_content.py` の `KEY_FIGURES`）

## フォルダ

| 場所 | 内容 |
|---|---|
| `src/` | 手書きのページ（ホーム、About、ツール、スライド、スタイル） |
| `docs/` | `build_content.py` が作る公開用の文書（手で直さない） |
| `mkdocs.yml` | サイトの設定（メニュー、言語の切り替え） |
| `.github/workflows/pages.yml` | 公開の自動化 |
| `site/` | 作られたサイト（コミットしない） |

## First-time publishing (GitHub)

1. Create an empty public repository on GitHub.
2. In this folder: `git init`, `git add .`, `git commit`, add the remote, and push to `main`.
3. In the repository settings, under **Pages**, set the source to **GitHub Actions**.
4. Set `site_url` in `mkdocs.yml` to the published address.
