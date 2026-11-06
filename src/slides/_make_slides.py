# Generates index.html (English) and ja.html (Japanese) from the slide lists below.
import os
HERE = os.path.dirname(os.path.abspath(__file__))
CSS = """
*{box-sizing:border-box}html,body{margin:0;height:100%;background:#16212E;font-family:"Helvetica Neue",Helvetica,Arial,"Hiragino Kaku Gothic ProN","Noto Sans JP",sans-serif;color:#1F2A37}
.deck{position:relative;width:100vw;height:100vh;overflow:hidden}
.slide{position:absolute;inset:0;margin:auto;width:min(100vw,177.78vh);height:min(56.25vw,100vh);background:#fff;padding:5% 6%;display:none;flex-direction:column;justify-content:center}
.slide.on{display:flex}
.slide.dark{background:linear-gradient(135deg,#16212E,#1F3A5F);color:#fff}
.k{color:#E0662C;font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:clamp(12px,1.6vw,22px);margin:0 0 .6em}
h1{font-size:clamp(28px,5.2vw,76px);margin:0 0 .3em;line-height:1.1}
h2{font-size:clamp(22px,3.4vw,50px);margin:0 0 .5em;line-height:1.15}
p,li{font-size:clamp(14px,1.9vw,28px);line-height:1.45;margin:.25em 0}
ul{margin:.3em 0 0;padding-left:1.1em}
.dark p,.dark li{color:#C9D6E6}
img{max-width:100%;max-height:62%;object-fit:contain;align-self:center;margin-top:.6em}
.cols{display:grid;grid-template-columns:repeat(3,1fr);gap:2.5%;margin-top:.6em}
.col{border-top:6px solid #E0662C;background:#F4F6F8;border-radius:10px;padding:4% 6%}
.col b{display:block;font-size:clamp(16px,2.2vw,32px);margin-bottom:.3em}
.col p{font-size:clamp(12px,1.5vw,22px)}
.big{font-size:clamp(22px,3.6vw,54px);font-weight:800;color:#fff}
.bar{position:fixed;left:0;bottom:0;height:4px;background:#E0662C;transition:width .2s}
.num{position:fixed;right:14px;bottom:10px;color:#9DB8D9;font-size:13px}
.hint{position:fixed;left:14px;bottom:10px;color:#9DB8D9;font-size:13px}
a{color:#E0662C}
"""
JS = """
const s=[...document.querySelectorAll('.slide')];let i=0;const bar=document.querySelector('.bar'),num=document.querySelector('.num');
function go(n){i=Math.max(0,Math.min(s.length-1,n));s.forEach((e,k)=>e.classList.toggle('on',k===i));bar.style.width=((i+1)/s.length*100)+'%';num.textContent=(i+1)+' / '+s.length;history.replaceState(null,'','#'+(i+1))}
document.addEventListener('keydown',e=>{if(['ArrowRight','PageDown',' '].includes(e.key))go(i+1);if(['ArrowLeft','PageUp'].includes(e.key))go(i-1);if(e.key==='Home')go(0);if(e.key==='End')go(s.length-1);if(e.key==='f'||e.key==='F'){document.fullscreenElement?document.exitFullscreen():document.documentElement.requestFullscreen()}});
document.addEventListener('click',e=>{if(e.target.closest('a'))return;go(e.clientX>innerWidth/3?i+1:i-1)});
go((parseInt(location.hash.slice(1))||1)-1);
"""
def page(lang, title, hint, slides):
    body = "\n".join(slides)
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><style>{CSS}</style></head><body><div class="deck">
{body}
</div><div class="bar"></div><div class="num"></div><div class="hint">{hint}</div><script>{JS}</script></body></html>
"""
F = "../assets/fig/"
EN = [
 '<section class="slide dark"><p class="k">Package proposal · working draft</p><h1>Steering Within Limits</h1><p>Three proposals for a civilizational transition: Youth GCC, the Global Citizen Will Platform, and Planetary OS</p></section>',
 f'<section class="slide"><p class="k">Why now</p><h2>In 50 years, the world changed more than our rules did</h2><img src="{F}en/W-3.png" alt=""></section>',
 '<section class="slide"><p class="k">The diagnosis</p><h2>Not a shortage, but a runaway</h2><ul><li>Efficiency gains are swallowed by overcompetition</li><li>Benefits flow into asset prices, while daily life gets harder</li><li>Everyone acting rationally produces a collective failure, like a theater audience all standing on tiptoe</li></ul></section>',
 f'<section class="slide"><p class="k">The diagnosis</p><h2>Wealth and emissions are concentrated in the same hands</h2><img src="{F}en/2-B.png" alt=""></section>',
 '<section class="slide"><p class="k">The transition</p><h2>From a civilization that grew without steering, to one that steers within limits</h2><ul><li>Planetary limits defined strictly, as guardrails</li><li>Freedom for life and business within them</li><li>Continual correction by data and pre-agreed rules</li><li>Goals set democratically, including for future generations</li></ul></section>',
 '<section class="slide"><p class="k">Three gaps, three proposals</p><h2>Who, how, and what</h2><div class="cols"><div class="col"><b>A · Youth GCC</b><p>A youth-led global citizens\' congress. A World Citizens\' Assembly selected by lot, a World Policy Institute, a World Policy Laboratory</p></div><div class="col"><b>B · Platform</b><p>A federation of existing movements that makes support visible and connects it to decisions</p></div><div class="col"><b>C · Planetary OS</b><p>Operating rules under which reducing pays</p></div></div></section>',
 '<section class="slide"><p class="k">A · Youth GCC</p><h2>A second political circuit, beside states</h2><ul><li>World citizens raise problems; experts design at least three options; citizens deliberate and choose</li><li>Policies are tested before they are scaled, and failures are published</li><li>It begins with a duty to respond, not a power to compel: states publish why they adopt or reject</li><li>Legitimacy is earned, not declared</li></ul></section>',
 '<section class="slide"><p class="k">B · Global Citizen Will Platform</p><h2>Federation, not competition</h2><ul><li>Existing movements keep their names and campaigns, and join as Co-Initiators</li><li>Support for concrete proposals is made visible against planetary indicators</li><li>Four channels to decisions: multilateral, legal, electoral, markets</li><li>Influence through legitimacy and numbers, not coercion</li></ul></section>',
 f'<section class="slide"><p class="k">C · Planetary OS</p><h2>Four modules, two money flows</h2><img src="{F}en/2-2.png" alt=""></section>',
 f'<section class="slide"><p class="k">C · Planetary OS</p><h2>Reducing pays: at least 70% of people come out ahead</h2><img src="{F}en/5-2.png" alt=""></section>',
 f'<section class="slide"><p class="k">C · Planetary OS</p><h2>Scaling through a club worth joining</h2><img src="{F}en/6-4.png" alt=""></section>',
 '<section class="slide dark"><p class="k">One question for politics</p><p class="big">"Here is a working design. Will you connect to it?"</p><p>Stage 1: the first edition of the Planetary OS Standard · a public dividend simulator · the launch of Youth GCC</p><p>Join as a Co-Initiator · Read more: the package proposal and the series</p></section>',
]
JA = [
 '<section class="slide dark"><p class="k">パッケージ提案 · 草案</p><h1>限界の内側で、舵を取る</h1><p>文明の転換に向けた3つの提案：Youth GCC、Global Citizen Will Platform、Planetary OS</p></section>',
 f'<section class="slide"><p class="k">なぜ今か</p><h2>この50年で、世界はルールよりずっと大きく変わった</h2><img src="{F}ja/W-3.png" alt=""></section>',
 '<section class="slide"><p class="k">診断</p><h2>不足ではなく、暴走</h2><ul><li>効率化の成果は、過剰な競争に飲み込まれる</li><li>恩恵は資産の価格に流れ、暮らしは楽にならない</li><li>一人ひとりが合理的に行動するほど、全体として共倒れになる（全員が爪先立ちの劇場）</li></ul></section>',
 f'<section class="slide"><p class="k">診断</p><h2>富と排出は、同じところに集中している</h2><img src="{F}ja/2-B.png" alt=""></section>',
 '<section class="slide"><p class="k">転換</p><h2>舵を取らずに育った文明から、限界の内側で舵を取る文明へ</h2><ul><li>地球の限界は、ガードレールとして厳格に定める</li><li>その内側の暮らしと事業は自由に</li><li>データと、あらかじめ合意したルールで、絶えず修正する</li><li>目標は、将来世代の声も含めて民主的に決める</li></ul></section>',
 '<section class="slide"><p class="k">3つの空白と、3つの提案</p><h2>誰が、どのように、何を</h2><div class="cols"><div class="col"><b>A · Youth GCC</b><p>若者主導の地球市民会議。くじ引きの世界市民会議、世界政策機構、世界政策実証局</p></div><div class="col"><b>B · Platform</b><p>既存の運動の連合。支持を目に見える形にし、意思決定につなぐ</p></div><div class="col"><b>C · Planetary OS</b><p>減らすほど得をする動作ルール</p></div></div></section>',
 '<section class="slide"><p class="k">A · Youth GCC</p><h2>国家と並ぶ、もう一つの政治の回路</h2><ul><li>市民が課題を提起し、専門家が少なくとも3つの案をつくり、市民が熟議して選ぶ</li><li>政策は実証してから広げ、失敗も公開する</li><li>強制する力ではなく、応答してもらうしくみから始める（採否の理由を公開）</li><li>正統性は、宣言するものではなく積み重ねるもの</li></ul></section>',
 '<section class="slide"><p class="k">B · Global Citizen Will Platform</p><h2>競争ではなく、連合</h2><ul><li>既存の運動は名前と活動を保ち、共同発起人として加わる</li><li>具体的な提案への支持を、地球の指標と並べて目に見える形にする</li><li>意思決定につなぐ4つの経路：多国間・司法・選挙・市場</li><li>力の源は強制ではなく、正統性と数</li></ul></section>',
 f'<section class="slide"><p class="k">C · Planetary OS</p><h2>4つのモジュールと、2つのお金の流れ</h2><img src="{F}ja/2-2.png" alt=""></section>',
 f'<section class="slide"><p class="k">C · Planetary OS</p><h2>減らすほど得：少なくとも7割の人の手取りがプラスに</h2><img src="{F}ja/5-2.png" alt=""></section>',
 f'<section class="slide"><p class="k">C · Planetary OS</p><h2>参加すると得をするクラブで広げる</h2><img src="{F}ja/6-4.png" alt=""></section>',
 '<section class="slide dark"><p class="k">政治への、一つの問い</p><p class="big">「動く設計図がここにあります。この仕組みにつなぎますか」</p><p>第1段階：Planetary OS の Standard 第1版・公開の還元シミュレーター・Youth GCC の立ち上げ</p><p>共同発起人として参加する · 詳しくはパッケージ提案書と連載へ</p></section>',
]
open(os.path.join(HERE, "index.html"), "w", encoding="utf-8").write(page("en", "Steering Within Limits — slides", "← → to move · F for full screen", EN))
open(os.path.join(HERE, "ja.html"), "w", encoding="utf-8").write(page("ja", "限界の内側で、舵を取る — スライド", "← → で移動 · F で全画面", JA))
print("slides ok")
