# Steering Within Limits — website

Source for the website of **Steering Within Limits** (限界の内側で、舵を取る), a package of three proposals for a civilizational transition:

- **A. Youth GCC** — a youth-led Global Citizens' Congress for future generations (who acts)
- **B. Global Citizen Will Platform** — an alliance that connects civic will to decisions (how)
- **C. Planetary OS** — operating rules for a world where reducing pays (what)

**Read the site: https://tamorist.github.io/steering/** (English / 日本語)

All names, ratios, and figures in the proposals are illustrative. Everything here is a working draft, meant to be tested, criticized, and rewritten.

## How this site is built

- Built with [MkDocs](https://www.mkdocs.org/) and the [Material](https://squidfunk.github.io/mkdocs-material/) theme, with English and Japanese versions.
- The pages in `docs/` are generated from the source documents by `build_content.py`, which is run before each commit. The source documents themselves are kept outside this repository, so please do not edit `docs/` by hand.
- On every push to `main`, GitHub Actions builds the site and publishes it to GitHub Pages.

## Contact

Questions, corrections, and suggestions are welcome through the [contact form](https://docs.google.com/forms/d/e/1FAIpQLSexBpD4BcRWIV--FuhMC9BxbP4I9fXl6pi9nxQPmX2bjivjqw/viewform). To join or collaborate, see [Join as a Co-Initiator](https://tamorist.github.io/steering/join/).

## License

- Text and figures: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- Code (the Citizen Dividend Simulator, the slides, and the build scripts): MIT

See [LICENSE.md](LICENSE.md).

---

## 日本語

文明の転換に向けた3つの提案（Youth GCC、Global Citizen Will Platform、Planetary OS）をまとめたパッケージ提案「**限界の内側で、舵を取る**」のウェブサイトの元データです。

- **サイト**：https://tamorist.github.io/steering/ja/
- 名前・比率・数値は、すべて一例です。すべて草案で、検証と批判を通じて書き直していくことを前提としています。
- `docs/` のページは、元の原稿から `build_content.py` で自動で作っています（手で直さないでください）。
- ご質問・誤りの指摘・ご意見は、[お問い合わせフォーム](https://docs.google.com/forms/d/e/1FAIpQLSexBpD4BcRWIV--FuhMC9BxbP4I9fXl6pi9nxQPmX2bjivjqw/viewform)からお願いします。
- ライセンス：文章と図は CC BY 4.0、コード（還元シミュレーター、スライド、ビルドのスクリプト）は MIT です。
