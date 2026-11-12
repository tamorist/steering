"""Collect the publishable documents into docs/ for the MkDocs site.

Run from this folder:  python3 build_content.py
It copies only the files listed in PAGES (English = master, Japanese = translation),
inserts figures in place of the [Figure ...] / ［図…］ placeholders, and removes
editing notes that are not meant for readers. Hand-written pages (home, about,
slides, stylesheets) live in src/ and are copied as they are.
"""
import glob, os, re, shutil, unicodedata, tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                     # 世界市民の民意集約システム/
DOCS = os.path.join(HERE, "docs")
SRC = os.path.join(HERE, "src")

OS_ = "分配型OSモデル"
PKG = "パッケージ提案"
GCW = "Global Citizen Will Platform"
YGC = "Youth GCC"
ESS = "システム変革の必要性"
GOV = "世界市民ガバナンス構想"

# slug: (English master, Japanese translation)
PAGES = {
    "start": (f"{PKG}/Plain_Guide_EN.md", f"{PKG}/やさしい解説_JP.md"),
    "why-now": (f"{PKG}/Why_Now_Article_EN.md", f"{PKG}/なぜ今か_記事_JP.md"),
    "overview": (f"{PKG}/One_Page_Overview_EN.md", f"{PKG}/1ページ概要_JP.md"),
    "pictures": (f"{PKG}/In_Pictures_EN.md", f"{PKG}/絵で見る提案_JP.md"),
    "package": (f"{PKG}/Package_Proposal_EN.md", f"{PKG}/パッケージ提案_JP.md"),
    "proposals/a-youth-gcc": (f"{YGC}/Proposal_A_EN.md", f"{YGC}/提案A_JP.md"),
    "proposals/b-platform": (f"{GCW}/Proposal_B_EN.md", f"{GCW}/提案B_JP.md"),
    "proposals/c-summary": (f"{OS_}/提案書/Proposal_C_Executive_Summary_EN.md", f"{OS_}/提案書/提案C_要約_JP.md"),
    "proposals/c-full": (f"{OS_}/提案書/Proposal_C_Full_EN.md", f"{OS_}/提案書/提案C_本編_JP.md"),
    "proposals/c-faq": (f"{OS_}/提案書/Proposal_C_FAQ_EN.md", f"{OS_}/提案書/提案C_FAQ_JP.md"),
    "essays/why-technology": (f"{ESS}/Essay1_Why_Technology_Does_Not_Make_Life_Easier_EN.md", f"{ESS}/論考1_なぜ技術が進んでも暮らしは楽にならないのか_JP.md"),
    "essays/next-layers": (f"{ESS}/Essay2_The_Next_Layers_of_Planetary_OS_EN.md", f"{ESS}/論考2_PlanetaryOSの次の層_JP.md"),
    "charter/charter": (f"{GOV}/Charter_EN.md", f"{GOV}/憲章_JP.md"),
    "charter/another-world-politics": (f"{GOV}/Another_World_Politics_EN.md", f"{GOV}/もう一つの世界政治_JP.md"),
    "join": (f"{GCW}/Co-Initiator_Page_EN.md", f"{GCW}/共同発起人の募集ページ_JP.md"),
}
for n in range(0, 9):
    en = glob.glob(os.path.join(ROOT, OS_, "series_EN", f"Part{n}_*.md"))[0]
    ja = glob.glob(os.path.join(ROOT, OS_, "note連載", f"第{n}回_*.md"))[0]
    PAGES[f"series/part-{n}"] = (os.path.relpath(en, ROOT), os.path.relpath(ja, ROOT))

FIG_EN = os.path.join(ROOT, OS_, "series_EN", "figures")
FIG_JA = os.path.join(ROOT, OS_, "note連載", "図")
FIG_W = os.path.join(ROOT, PKG, "図")
FIG_I = os.path.join(ROOT, PKG, "イラスト")   # illustrations for general readers (I-1 …)

# Lines that are editing notes, not content
DROP = [
    r"^\*\*Header image:.*", r"^\*\*見出し画像：.*", r"^\*\*Cover image:\*\*.*", r"^\*\*カバー画像\*\*.*",
    r"^> This English version is the master text.*", r"^> Master text\..*", r"^> 本書は、英語版.*",
    r"^> 英語版（.*を正本とする.*", r"^> 管理用の注記.*",
]


def variant(text, target):
    """One source, two variants: <!-- package --> blocks appear only on the site,
    <!-- standalone --> blocks only in the note/Substack exports."""
    drop = "standalone" if target == "site" else "package"
    text = re.sub(rf"<!-- {drop} -->\n.*?<!-- /{drop} -->\n?", "", text, flags=re.S)
    text = re.sub(r"<!-- /?(?:package|standalone) -->\n?", "", text)
    return re.sub(r"\n{3,}", "\n\n", text)


def copy_fig(path, lang):
    base = unicodedata.normalize("NFC", os.path.basename(path))
    key = re.match(r"^(?:Fig|図)?([0-9WI]+-[0-9A-Z]+)", base).group(1)
    name = f"{key}.png"   # ASCII names avoid NFC/NFD mismatches on macOS
    dst = os.path.join(DOCS, "assets", "fig", lang, name)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(path, dst)
    return f"assets/fig/{lang}/{name}"


def find_fig(folder, prefix):
    hits = sorted(glob.glob(os.path.join(folder, prefix + "_*.png")))
    return hits[0] if hits else None


def find_illust(key, lang):
    """I-1 … : English files end in _EN, Japanese files do not."""
    hits = [h for h in sorted(glob.glob(os.path.join(FIG_I, key + "_*.png"))) if h.endswith("_EN.png") == (lang == "en")]
    return hits[0] if hits else None


def img(rel_from_page, src, caption):
    return f'<figure markdown="span">\n  ![{caption}]({rel_from_page}{src})\n  <figcaption>{caption}</figcaption>\n</figure>'


def episode_no(path):
    m = re.search(r"Part(\d)_", path) or re.search(r"第(\d)回_", path)
    return m.group(1) if m else None


def transform(text, lang, src_path, depth):
    up = "../" * depth
    lines = text.split("\n")
    # note versions start with a "---  title --- URL  ---" header; drop it
    if "note版" in src_path:
        i = next((k for k, l in enumerate(lines) if l.startswith("# ")), 0)
        lines = lines[i:]
    out, skip_quote = [], False
    ep = episode_no(src_path)
    for line in lines:
        if any(re.match(p, line) for p in DROP):
            continue
        if skip_quote:
            if line.startswith(">"):
                continue
            skip_quote = False
        # English placeholders
        m = re.match(r"^>?\s*\*\*\[Figure ([0-9WI]+-[0-9A-Z]+)(?::\s*([^\]]*))?\]\*\*\s*(.*)$", line)
        m2 = re.match(r"^\*\*\[Figure: ([^\]]*)\]\*\*$", line)
        if m or m2:
            if m2:
                key, cap = "2-B", m2.group(1)
            else:
                key, cap = m.group(1), (m.group(2) or m.group(3) or f"Figure {m.group(1)}").strip()
            if key.startswith("I"):
                f = find_illust(key, "en")
            else:
                f = find_fig(FIG_W, f"FigW-{key[2:]}") if key.startswith("W") else find_fig(FIG_EN, f"Fig{key}")
            if f:
                out.append(img(up, copy_fig(f, "en"), cap))
                skip_quote = line.startswith(">")
                continue
        # Japanese placeholders
        j = re.match(r"^>?\s*\*\*［図([^：］]*)(?:：([^］]*))?］(.*?)\*\*\s*(.*)$", line)
        if j:
            label, extra, tail = j.group(1), (j.group(2) or ""), (j.group(3) or j.group(4))
            if label.startswith("I"):
                f = find_illust(label, "ja")
            elif label.startswith("W"):
                f = find_fig(FIG_W, f"図{label}")
            elif label == "":
                f = find_fig(FIG_JA, "図2-B")
            elif "-" in label:
                f = find_fig(FIG_JA, f"図{label}")
            else:
                f = find_fig(FIG_JA, f"図{ep}-{label}")
            if f:
                cap = tail.strip(" *") or (extra if extra and "差し込み予定" not in extra else "") or unicodedata.normalize("NFC", os.path.basename(f))[:-4].split("_", 1)[1]
                out.append(img(up, copy_fig(f, "ja"), cap))
                skip_quote = line.startswith(">")
                continue
        out.append(line)
    return list_spacing("\n".join(out)).strip() + "\n"


LIST_ITEM = re.compile(r"^\s{0,3}(?:[-*+]|\d+\.)\s")


def list_spacing(text):
    """Python-Markdown needs a blank line before a list; add one where a list follows a paragraph line."""
    out, fence = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            fence = not fence
        prev = out[-1] if out else ""
        if (not fence and LIST_ITEM.match(line) and prev.strip()
                and not LIST_ITEM.match(prev) and not prev.startswith(("  ", "\t", ">", "|", "#"))):
            out.append("")
        # the same rule inside a blockquote: "> text" followed by "> - item"
        elif (not fence and line.startswith(">") and LIST_ITEM.match(line[1:].lstrip(" ") if line[1:2] == " " else line[1:])
              and prev.startswith(">") and prev[1:].strip() and not LIST_ITEM.match(prev[1:].lstrip(" "))):
            out.append(">")
        out.append(line)
    return "\n".join(out)


# ---------------- links (one register for every output) ----------------
LINKS = tomllib.load(open(os.path.join(ROOT, "links.toml"), "rb"))
BASE_URL = LINKS.get("site", {}).get("base_url", "").rstrip("/")
TOKEN = re.compile(r"\[link:([a-z0-9-]+)(?:@(en|ja))?\]|［リンク:([a-z0-9-]+)(?:@(en|ja))?］")
EXPORTS = os.path.join(ROOT, "_exports")


def entry(lid):
    e = LINKS.get(lid)
    if not e or lid == "site":
        raise SystemExit(f"links.toml has no entry '{lid}'")
    return e


def site_url_abs(e, lang):
    if not (BASE_URL and e.get("site")):
        return ""
    return f"{BASE_URL}/{'ja/' if lang == 'ja' else ''}{e['site']}/"


def resolve_site(text, lang, slug):
    def sub(m):
        lid, forced = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
        e = entry(lid)
        whole_line = m.group(0) == m.string[m.string.rfind("\n", 0, m.start()) + 1:].split("\n", 1)[0].strip()
        if e.get("site"):
            tl = forced or lang
            if tl == lang:
                href = os.path.relpath(e["site"] + ".md", os.path.dirname(slug) or ".")
            else:  # the other language: plain URL path
                here = ("ja/" if lang == "ja" else "") + slug + "/"
                there = ("ja/" if tl == "ja" else "") + e["site"] + "/"
                href = os.path.relpath(there, here) + "/"
            label = (e["title_ja"] if tl == "ja" else e["title_en"]) + " →" if whole_line else "→"
            return f"[{label}]({href})"
        ext = e.get("substack") or e.get("note") or e.get("url")
        return f"[↗]({ext})" if ext else ""
    return TOKEN.sub(sub, text)


def also_published(slug, lang):
    for lid, e in LINKS.items():
        if lid != "site" and e.get("site") == slug:
            items = []
            if e.get("note"):
                items.append(("note（日本語）" if lang == "ja" else "note (Japanese)", e["note"]))
            if e.get("substack"):
                items.append(("Substack（英語）" if lang == "ja" else "Substack (English)", e["substack"]))
            if items:
                head = "この文書は、次の場所でも公開しています：" if lang == "ja" else "This document is also published on:"
                return "\n\n---\n\n" + head + " " + " · ".join(f"[{n}]({u})" for n, u in items) + "\n"
    return ""


def resolve_export(text, lang):
    def sub(m):
        lid, forced = (m.group(1), m.group(2)) if m.group(1) else (m.group(3), m.group(4))
        e = entry(lid)
        tl = forced or lang
        order = ["note", "substack", "url"] if tl == "ja" else ["substack", "note", "url"]
        url = next((e.get(k) for k in order if e.get(k)), "") or site_url_abs(e, tl)
        if not url:
            return "（準備中）" if lang == "ja" else "(coming soon)"
        prev = m.string[m.start() - 1] if m.start() else " "
        return url if prev in " 　：:（(" else " " + url
    return TOKEN.sub(sub, text)


EXPORT_DROP = [r"^> This English version is the master text.*", r"^> Master text\..*", r"^> 本書は、英語版.*",
               r"^> 英語版（.*を正本とする.*", r"^> 管理用の注記.*"]


def export(rel, lang):
    """Write a copy for posting: links resolved to published URLs, editing notes removed, figure placeholders kept."""
    src = os.path.join(ROOT, rel)
    text = unicodedata.normalize("NFC", open(src, encoding="utf-8").read())
    lines = [l for l in variant(text, "export").split("\n") if not any(re.match(p, l) for p in EXPORT_DROP)]
    lines = [l for i, l in enumerate(lines) if l.strip() or i == 0 or lines[i - 1].strip()]   # no double blank lines
    out_dir = os.path.join(EXPORTS, "note" if lang == "ja" else "substack")
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, os.path.basename(rel)), "w", encoding="utf-8").write(resolve_vars(resolve_export("\n".join(lines), lang), lang, "export").strip() + "\n")


# ---------------- info register (contact details and other fill-in values) ----------------
INFO = tomllib.load(open(os.path.join(ROOT, "info.toml"), "rb"))
VAR = re.compile(r"\{\{([a-z_]+)\}\}")
PENDING = {"en": "(to be added)", "ja": "（準備中）"}
EXPORT_ONLY = [("Global Citizen Will Platform/Short_Pitch_EN.md", "en"), ("Global Citizen Will Platform/打診用ショートピッチ_JP.md", "ja"),
               # Background essay 3: published only on note/Substack, not on the site (decided 2026-11-12)
               ("既存ルート破綻/Essay3_The_Missing_Institution_EN.md", "en"), ("既存ルート破綻/論考3_足りないのは決めるための器_JP.md", "ja")]


def info_value(key, lang):
    p, c, f, l = INFO.get("person", {}), INFO.get("contact", {}), INFO.get("forms", {}), INFO.get("license", {})
    author = (p.get("author_ja") if lang == "ja" else "") or p.get("author_en", "")
    simple = {
        "author": author,
        "role": p.get(f"role_{lang}") or p.get("role_en", ""),
        "email": c.get("email", ""),
        "substack_url": c.get("substack", ""), "note_url": c.get("note", ""), "x_url": c.get("x", ""),
        "profile_url": c.get("x") or c.get("substack", ""),
        "interest_form_url": f.get("interest_form", ""),
        "contact_form_url": f.get("contact_form", ""),
        "license_holder": l.get("holder") or p.get("author_en", ""), "license_year": l.get("year", ""),
    }
    if key == "analytics_note":
        if not INFO.get("analytics", {}).get("goatcounter", "").strip():
            return ""
        return ("このサイトでは、Cookie を使わず個人を特定しないアクセス解析ツール GoatCounter で、ページごとの閲覧数だけを数えています。"
                if lang == "ja" else
                "This site counts page views with GoatCounter, a privacy-friendly analytics tool that uses no cookies and collects no personal data.")
    if key in simple:
        return simple[key]
    raise SystemExit(f"info.toml has no value for '{{{{{key}}}}}'")


def resolve_vars(text, lang, mode):
    def sub(m):
        key = m.group(1)
        if key == "contact":
            parts = []
            a = info_value("author", lang)
            if a: parts.append(a)
            e = info_value("email", lang)
            if e: parts.append(f"[{e}](mailto:{e})" if mode == "site" else e)
            for label, k in (("Substack", "substack_url"), ("note", "note_url"), ("X", "x_url")):
                u = info_value(k, lang)
                if u: parts.append(f"[{label}]({u})" if mode == "site" else u)
            u = info_value("contact_form_url", lang)
            if u:
                label = "お問い合わせフォーム" if lang == "ja" else "Contact form"
                parts.append(f"[{label}]({u})" if mode == "site" else f"{label}：{u}" if lang == "ja" else f"{label}: {u}")
            return " · ".join(parts) if parts else PENDING[lang]
        if key == "interest_form":
            u = info_value("interest_form_url", lang)
            label = "関心表明フォーム（約2分）" if lang == "ja" else "Co-Initiator interest form (about 2 minutes)"
            if not u: return label + " " + PENDING[lang]
            return f"[{label}]({u})" if mode == "site" else f"{label}: {u}"
        if key == "contact_form":
            u = info_value("contact_form_url", lang)
            label = "お問い合わせフォーム" if lang == "ja" else "contact form"
            if not u: return label + " " + PENDING[lang]
            return f"[{label}]({u})" if mode == "site" else f"{label}（{u}）" if lang == "ja" else f"{label} ({u})"
        v = info_value(key, lang)
        return v if (v or key == "analytics_note") else PENDING[lang]
    return VAR.sub(sub, text)


REPORT = os.path.join(ROOT, "管理レポート（自動生成）.md")


def goatcounter_snippet():
    code = INFO.get("analytics", {}).get("goatcounter", "").strip()
    if not code:
        return ""
    return (f'<script data-goatcounter="https://{code}.goatcounter.com/count" '
            'async src="https://gc.zgo.at/count.js"></script>')


def write_analytics():
    """GoatCounter (cookie-free analytics), only when a site code is set in info.toml."""
    snip = goatcounter_snippet()
    od = os.path.join(HERE, "overrides")
    os.makedirs(od, exist_ok=True)
    open(os.path.join(od, "main.html"), "w", encoding="utf-8").write(
        '{% extends "base.html" %}\n{% block analytics %}\n' + snip + '\n{% endblock %}\n')
    if snip:  # standalone pages (simulator, slides) do not use the theme, so add the snippet there too
        for p in glob.glob(os.path.join(DOCS, "simulator", "*.html")) + glob.glob(os.path.join(DOCS, "slides", "*.html")):
            t = open(p, encoding="utf-8").read()
            if "goatcounter" not in t:
                open(p, "w", encoding="utf-8").write(t.replace("</body>", snip + "\n</body>", 1))


def write_report():
    """One page that shows where every link and every fill-in value ends up, and what is still missing."""
    sources = [(rel, lang) for en, ja in PAGES.values() for rel, lang in ((en, "en"), (ja, "ja"))] + EXPORT_ONLY
    sources += [(os.path.relpath(p, ROOT), "ja" if p.endswith(".ja.md") else "en") for p in glob.glob(os.path.join(SRC, "**", "*.md"), recursive=True)]
    sources += [("_website/LICENSE.template.md", "en")]
    seen, link_uses, var_uses = set(), {}, {}
    for rel, lang in sources:
        if rel in seen: continue
        seen.add(rel)
        for i, line in enumerate(open(os.path.join(ROOT, rel), encoding="utf-8").read().split("\n"), 1):
            for m in TOKEN.finditer(line):
                lid = m.group(1) or m.group(3)
                link_uses.setdefault(lid, []).append(f"{rel}:{i}")
            for m in VAR.finditer(line):
                var_uses.setdefault(m.group(1), []).append(f"{rel}:{i}")
    out = ["# 管理レポート（自動生成）", "",
           "`_website/build_content.py` を実行するたびに作り直されます。手で直さないでください。",
           "リンクは `links.toml`、連絡先などは `info.toml` で管理しています。", ""]
    # 1. missing
    out += ["## 1. 未設定の項目（確認と書き込みが必要なもの）", "", "### 基本情報（info.toml）", "", "| キー | 使われている箇所の数 | 使われている文書 |", "|---|---|---|"]
    missing_vars = []
    for key, uses in sorted(var_uses.items()):
        empty = (key == "contact" and not any(info_value(k, "en") for k in ("author", "email", "substack_url", "note_url", "x_url"))) or \
                (key == "interest_form" and not info_value("interest_form_url", "en")) or \
                (key == "contact_form" and not info_value("contact_form_url", "en")) or \
                (key not in ("contact", "interest_form", "contact_form") and not info_value(key, "en"))
        if key == "contact" and not info_value("author", "en"): empty = True
        if empty:
            missing_vars.append(key)
            out.append(f"| `{{{{{key}}}}}` | {len(uses)} | " + "<br>".join(sorted({u.rsplit(':', 1)[0] for u in uses})) + " |")
    if not missing_vars: out.append("| （なし） | | |")
    out += ["", "※ `{{contact}}` は、名前（author）が空のときもここに出します。", "", "### リンク（links.toml）：公開先の URL がまだないもの", "",
            "| ID | 文書 | サイト | note | Substack | 使われている箇所の数 |", "|---|---|---|---|---|---|"]
    for lid, uses in sorted(link_uses.items()):
        e = LINKS[lid]
        if not (e.get("note") or e.get("substack") or e.get("url")):
            out.append(f"| `{lid}` | {e['title_ja']} | {'○' if e.get('site') else '—（サイトにもない）'} | 未 | 未 | {len(uses)} |")
    # 2. link map
    out += ["", "## 2. リンクの反映先", "",
            "各 ID が、サイト・note 用・Substack 用の書き出しで、どこにつながるか。", "",
            "| ID | 文書 | サイト | note 用（日本語） | Substack 用（英語） | 使われている箇所 |", "|---|---|---|---|---|---|"]
    for lid, e in LINKS.items():
        if lid == "site": continue
        uses = link_uses.get(lid, [])
        site = f"`/{e['site']}/`" if e.get("site") else ("外部 ↗" if (e.get("substack") or e.get("note") or e.get("url")) else "（リンクなし）")
        note = next((e.get(k) for k in ("note", "substack", "url") if e.get(k)), "") or site_url_abs(e, "ja") or "（準備中）"
        sub = next((e.get(k) for k in ("substack", "note", "url") if e.get(k)), "") or site_url_abs(e, "en") or "(coming soon)"
        where = "<br>".join(uses) if uses else "（未使用）"
        out.append(f"| `{lid}` | {e['title_ja']} | {site} | {note} | {sub} | {where} |")
    # 3. info map
    out += ["", "## 3. 基本情報の反映先", "", "| キー | 今の値（英語／日本語） | 使われている箇所 |", "|---|---|---|"]
    for key, uses in sorted(var_uses.items()):
        en = resolve_vars("{{" + key + "}}", "en", "export"); ja = resolve_vars("{{" + key + "}}", "ja", "export")
        val = en if en == ja else f"{en}／{ja}"
        out.append(f"| `{{{{{key}}}}}` | {val} | " + "<br>".join(uses) + " |")
    # 4. key figures
    out += ["", "## 4. 主な数値の出現箇所", "",
            "数値（すべて一例）を見直すときに、直す場所の一覧として使います。図は生成スクリプトに数値を直接書いているので、スクリプトも対象にしています。", "",
            "| 数値 | 出てくる文書と行 |", "|---|---|"]
    fig_sources = [os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, "**", "_*生成スクリプト.py"), recursive=True) if "_旧版" not in p]
    fig_sources += [os.path.relpath(p, ROOT) for p in glob.glob(os.path.join(ROOT, OS_, "simulator", "*.html"))]
    for label, pat in KEY_FIGURES:
        hits = []
        for rel in sorted(seen) + sorted(fig_sources):
            if not rel.endswith((".md", ".py", ".html")) or rel.startswith("_website/src/slides"): continue
            lines = open(os.path.join(ROOT, rel), encoding="utf-8").read().split("\n")
            nums = [str(i) for i, l in enumerate(lines, 1) if re.search(pat, l)]
            if nums: hits.append(f"{rel}:{','.join(nums)}")
        out.append(f"| {label} | " + ("<br>".join(hits) or "（なし）") + " |")
    open(REPORT, "w", encoding="utf-8").write("\n".join(out) + "\n")


# Key illustrative figures that appear in many documents (label, regex over EN and JP text).
KEY_FIGURES = [
    ("競売収入の配分：市民への還元90％・公正な移行10％", r"90 ?%|90％|9割"),
    ("還元の内訳：一律60％・縮小に連動40％", r"一律.{0,12}(?:60|6割)|(?:universal|equal)[^|.]{0,15}60 ?%|60/40|60％／40％|60 ?% is paid equally|60％は、全員に同じ額"),
    ("上限の引き下げ：年8％前後", r"8 ?% (?:a|per) year|年8％|年8パーセント"),
    ("クラブの削減率：年3％・5％・7％（規模20・40・60％）", r"年[357]％|[357] ?% a year"),
    ("手取りがプラスになる人：目安約7割（6割前後〜7割台前半）、多数派保証で少なくとも7割", r"約7割の人|約70％の人|6割前後|少なくとも7割|70% of (?:people|households)|at least 70%|about 60% to the low 70s|net-positive share"),
    ("BEI の規模：年約1兆ドル規模（0.8〜1.3兆ドル）", r"0\.8[–〜-]1\.3|1兆ドル規模|order of USD 1 trillion|around USD 1 trillion|1(?:–|-| to )1\.5 trillion|1〜1\.5兆ドル"),
    ("所得の上位10％：富の76％・排出の48％", r"76 ?%|76％|48 ?%|48％"),
    ("二重の鍵：くじ引きの会議の4分の3", r"three-quarters|3/4|4分の3"),
    ("第1段階：約18か月", r"18 months|18-month|18か月|18ヶ月"),
    ("世界市民会議：常設500〜2,000人", r"500[–-]2,000|500〜2,?000"),
    ("若者評議会：15〜35歳程度", r"15[–-]35|15〜35"),
]

def build():
    if os.path.exists(DOCS):
        shutil.rmtree(DOCS)
    shutil.copytree(SRC, DOCS)
    for old in glob.glob(os.path.join(EXPORTS, "*", "*.md")):   # exports are regenerated; drop stale copies
        os.remove(old)
    for path in glob.glob(os.path.join(DOCS, "**", "*.md"), recursive=True):
        lang = "ja" if path.endswith(".ja.md") else "en"
        slug = os.path.relpath(path, DOCS)[:-6]
        t = open(path, encoding="utf-8").read()
        open(path, "w", encoding="utf-8").write(resolve_vars(resolve_site(t, lang, slug), lang, "site"))
    for rel, lang in EXPORT_ONLY:
        export(rel, lang)
    lic = open(os.path.join(HERE, "LICENSE.template.md"), encoding="utf-8").read()
    open(os.path.join(HERE, "LICENSE.md"), "w", encoding="utf-8").write(resolve_vars(lic, "en", "export"))
    for slug, (en, ja) in PAGES.items():
        depth = slug.count("/")
        for lang, rel in (("en", en), ("ja", ja)):
            src = os.path.join(ROOT, rel)
            text = unicodedata.normalize("NFC", open(src, encoding="utf-8").read())
            dst = os.path.join(DOCS, f"{slug}.{lang}.md")
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            page = resolve_vars(resolve_site(transform(variant(text, "site"), lang, rel, depth), lang, slug), lang, "site") + also_published(slug, lang)
            open(dst, "w", encoding="utf-8").write(page)
            export(rel, lang)
    # simulator: wrap the fragment as a standalone page
    sim = open(os.path.join(ROOT, OS_, "simulator", "citizen_dividend_simulator.html"), encoding="utf-8").read()
    # allow ?lang=ja / ?lang=en so each language of the site opens the simulator in that language
    marker = "/* storage unavailable */ }"
    assert marker in sim
    sim = sim.replace(marker, marker + ' { const q = new URLSearchParams(location.search).get("lang"); if (q === "ja") { state.lang = "ja"; state.cur = "JPY"; } else if (q === "en") { state.lang = "en"; } }', 1)
    head, body = sim.split("</style>", 1)
    back = ('<p style="margin:12px 16px;font:14px system-ui,sans-serif">'
            '<a href="../">← Steering Within Limits</a></p>')
    page = ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
            + head + "</style>\n</head>\n<body>\n" + back + body + "\n</body>\n</html>\n")
    os.makedirs(os.path.join(DOCS, "simulator"), exist_ok=True)
    open(os.path.join(DOCS, "simulator", "index.html"), "w", encoding="utf-8").write(page)
    # cover images for the home page
    for p in [f"{PKG}/カバー画像/cover_Package_Proposal_EN.png", f"{PKG}/カバー画像/カバー_パッケージ提案_JP.png"]:
        shutil.copy2(os.path.join(ROOT, p), os.path.join(DOCS, "assets", os.path.basename(p)))
    write_analytics()
    write_report()
    print("built", len(PAGES) * 2, "pages; exports in", EXPORTS, "; report:", REPORT)


if __name__ == "__main__":
    build()
