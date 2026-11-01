#!/usr/bin/env python3
"""Generates index.html + memes.html. Re-run after adding memes to _build/memes.json + img/vault."""
import json, html, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CA = "0x65dE619562d1d1DB09E1a552C9e94C8BFA30c951"
PAIR = "0xa209D0B77F9b36437768325e06c83924598315ef"
BUY = "https://app.uniswap.org/swap?chain=ethereum&outputCurrency=" + CA
CHART = "https://dexscreener.com/ethereum/0xa209d0b77f9b36437768325e06c83924598315ef"
X = "https://x.com/MaccaGator_ETH"
SITE = "https://maccaeth.com"
memes = json.load(open(os.path.join(R, "_build/memes.json")))
primary = [m for m in memes if not m.get("bonus")]
bonus = [m for m in memes if m.get("bonus")]
e = html.escape

ICON_X = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.9 2H22l-7.6 8.7L23 22h-6.8l-5.3-6.9L4.8 22H1.7l8.1-9.3L1 2h7l4.8 6.3L18.9 2zm-1.2 18h1.9L7.4 3.9H5.4L17.7 20z"/></svg>'
ICON_UNI = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2l3 6 6 1-4.5 4.3 1 6.2L12 16.6 6.5 19.5l1-6.2L3 9l6-1z"/></svg>'
ICON_CH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><path d="M3 20h18M5 16l4-5 4 3 6-8"/></svg>'

def head(title, desc, path):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta name="theme-color" content="#0d0418">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Macca the Gator">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/og.jpg">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@MaccaGator_ETH">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{SITE}/og.jpg">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/fonts/yellowtail-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/bungee-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/css/styles.css?v=2">
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"WebSite","name":"Macca the Gator ($Macca)","url":SITE+"/"})}</script>
</head>
<body>
<div class="crt" aria-hidden="true"></div>
<canvas id="trail" aria-hidden="true"></canvas>
'''

def hud(active):
    def a(href, label, key):
        return f'<a href="{href}"{" class=\"on\"" if key==active else ""}>{label}</a>'
    base = "" if active == "home" else "/"
    return f'''<header class="hud" id="hud">
  <a class="brand" href="/" aria-label="Macca the Gator home"><img src="/img/logo-200.webp" alt="" width="42" height="42"><b>Macca</b></a>
  <nav class="nav" id="nav" aria-label="Main">
    {a(base+"#about","Story","about")}{a(base+"#missions","Missions","missions")}{a(base+"#howto","How to Buy","howto")}{a("/memes","Meme Vault","memes")}{a(base+"#faq","FAQ","faq")}
  </nav>
  <div class="hud-r">
    <div class="wanted" id="wanted" aria-label="Wanted level" title="Wanted level rises as you scroll"><i>★</i><i>★</i><i>★</i><i>★</i><i>★</i><i>★</i></div>
    <div class="cash" id="cash" title="Market cap (DexScreener)">$--------</div>
    <button class="burger" id="burger" aria-label="Menu" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
  </div>
</header>
'''

def ca_box(idn="ca"):
    return f'''<div class="ca" data-reveal>
  <span class="lbl">CA · ETH</span>
  <code id="{idn}">{CA}</code>
  <button type="button" data-copy="#{idn}">Copy CA</button>
</div>'''

def cta(style=""):
    return f'''<div class="cta"{style}>
  <a class="btn" href="{BUY}" target="_blank" rel="noopener">{ICON_UNI} Buy on Uniswap</a>
  <a class="btn cy" href="{CHART}" target="_blank" rel="noopener">{ICON_CH} Chart</a>
  <a class="btn gold" href="{X}" target="_blank" rel="noopener">{ICON_X} Follow on X</a>
</div>'''

def footer():
    return f'''<footer>
  <div class="wrap">
    <div class="foot">
      <div><a class="brand" href="/"><img src="/img/logo-200.webp" alt="" width="42" height="42" loading="lazy"><b>Macca the Gator</b></a>
      <p class="mono" style="margin-top:10px;color:var(--mut);font-size:13px">$Macca · Ethereum · Stay pink.</p></div>
      <nav aria-label="Footer">
        <a href="{BUY}" target="_blank" rel="noopener">Uniswap</a>
        <a href="{CHART}" target="_blank" rel="noopener">DexScreener</a>
        <a href="{X}" target="_blank" rel="noopener">X / @MaccaGator_ETH</a>
        <a href="/memes">Meme Vault</a>
      </nav>
    </div>
    <div class="disc">
      <p><strong>Parody disclaimer:</strong> Fan-made parody memecoin. Not affiliated with, endorsed by, or connected to Rockstar Games, Take-Two Interactive, or Grand Theft Auto. All trademarks belong to their respective owners.</p>
      <p style="margin-top:10px"><strong>Not financial advice:</strong> $Macca is a memecoin with no intrinsic value, no expectation of financial return, no team promises and no roadmap. It is for entertainment only. Crypto is highly volatile — you can lose everything you put in. Always verify the contract address, DYOR, and never invest more than you can afford to lose.</p>
    </div>
    <p class="copy">CA {CA}<br>© 2026 Macca the Gator community · maccaeth.com</p>
  </div>
</footer>
<div class="radio" id="radio"><div class="eq" aria-hidden="true"><i></i><i></i><i></i><i></i></div><span class="lbl2">RADIO: <span id="station">FLAMINGO FM</span></span><button type="button" id="radioBtn" aria-pressed="false">TUNE</button></div>
<div class="minimap" aria-hidden="true"><div class="sweep"></div><span class="dot" style="left:22%;top:30%"></span><span class="dot" style="left:70%;top:62%;background:var(--cyan);box-shadow:var(--cglow)"></span><span class="dot" style="left:60%;top:20%;background:var(--sun)"></span><svg class="prog" viewBox="0 0 100 100"><circle id="progc" cx="50" cy="50" r="48" fill="none" stroke="#ff2fa8" stroke-width="4" stroke-dasharray="301.6" stroke-dashoffset="301.6" transform="rotate(-90 50 50)"/></svg><span class="me"></span></div>
<div id="toast" role="status" aria-live="polite"><b>MISSION PASSED!</b><span>CA copied · +RESPECT</span></div>
<script src="/js/vendor/lenis.min.js" defer></script>
<script src="/js/vendor/gsap.min.js" defer></script>
<script src="/js/vendor/ScrollTrigger.min.js" defer></script>
<script src="/js/main.js?v=2" defer></script>
</body>
</html>
'''

def tile(m, i):
    return f'''<button type="button" class="gi vm-btn" data-full="/img/vault/meme-{m["n"]}.webp" data-cap="{e(m["cap"])}" data-reveal>
  <span class="n">#{m["n"]}</span>
  <img src="/img/vault/meme-{m["n"]}-480.webp" alt="{e(m["cap"])}" width="{m["w"]}" height="{m["h"]}" loading="lazy" decoding="async">
  <figcaption>{e(m["cap"])}</figcaption>
</button>'''

LB = '''<div id="lb" hidden role="dialog" aria-modal="true" aria-label="Meme viewer">
  <button type="button" class="lbb lb-x" aria-label="Close">✕</button>
  <button type="button" class="lbb lb-p" aria-label="Previous">‹</button>
  <figure><img id="lbimg" alt=""><figcaption id="lbcap"></figcaption></figure>
  <button type="button" class="lbb lb-n" aria-label="Next">›</button>
</div>'''

PALM = '<svg viewBox="0 0 200 400" aria-hidden="true"><path d="M104 400c-6-90-4-170 6-250l-8-1c-12 80-14 160-8 251z"/><path d="M106 150c-30-30-70-40-104-30 30 0 60 12 84 40-30-10-62-6-86 12 34-10 62-4 90 8-18 14-30 38-32 66 12-26 28-46 50-58l2-2c4 26 16 48 34 62-10-22-14-44-12-66 26 8 46 26 60 50-6-32-26-56-52-66 30-4 58 6 82 26-18-32-50-46-84-42 22-18 52-26 84-20-34-16-70-10-98 14 6-30 28-54 56-66-36 4-64 30-74 62z"/></svg>'

CITY = '''<svg viewBox="0 0 1600 400" preserveAspectRatio="xMidYMax slice" aria-hidden="true"><defs><linearGradient id="bg1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b0750"/><stop offset="1" stop-color="#14022a"/></linearGradient></defs>
<g fill="url(#bg1)" stroke="#ff2fa8" stroke-opacity=".55" stroke-width="2">
<path d="M0 400V250h60v-40h50v60h40V180h70v220z"/><path d="M220 400V140h30V90h20v50h40v260z"/><path d="M310 400V220h80v-30h40v210z"/><path d="M430 400V120l50-40 50 40v280z"/><path d="M530 400V230h90v170z"/><path d="M620 400V160h40v-50h60v50h30v240z"/><path d="M750 400V60h14V20h12v40h14v340z"/><path d="M790 400V200h100v200z"/><path d="M890 400V130h70v270z"/><path d="M960 400V240h60v-60h50v220z"/><path d="M1070 400V100l40-30 40 30v300z"/><path d="M1150 400V210h90v190z"/><path d="M1240 400V150h60v-40h40v290z"/><path d="M1340 400V240h80v160z"/><path d="M1420 400V170h70v230z"/><path d="M1490 400V260h110v140z"/></g>
<g fill="#21f3ff" opacity=".8" class="winds">'''+ ''.join(f'<rect x="{x}" y="{y}" width="6" height="8"/>' for x,y in [(240,170),(260,210),(450,150),(470,200),(650,190),(700,240),(760,90),(770,140),(905,160),(930,210),(1090,130),(1110,190),(1260,180),(1300,230),(1440,200),(1460,260),(70,280),(345,250)]) + '''</g>
<g fill="#ff5ec4" opacity=".9">'''+ ''.join(f'<rect x="{x}" y="{y}" width="6" height="8"/>' for x,y in [(250,250),(480,260),(640,290),(780,200),(910,300),(1100,250),(1280,300),(1450,320),(560,270),(820,260),(1180,250),(990,290)]) + '''</g></svg>'''

def index():
    feat = primary[:6]
    gal = "\n".join(tile(m, i) for i, m in enumerate(feat))
    return head("Macca the Gator ($Macca) — Leonida's Pink Menace on Ethereum",
                "Leonida's hit show. Ethereum's pink bag. Macca the Gator ($Macca) — a fan-made parody memecoin on Ethereum. Buy on Uniswap.", "/") + hud("home") + f'''
<div id="loader" aria-hidden="true">
  <div><img class="ld-logo" src="/img/logo-200.webp" alt="" width="120" height="120"><h2>Leonida</h2>
  <div class="bar"><i id="ldbar"></i></div>
  <p class="tip" id="ldtip">TIP: Always verify the contract address before you swap.</p></div>
</div>
<main>
<section class="hero" id="top">
  <div class="sky" data-depth="0.05"></div>
  <div class="sun" data-depth="0.15"></div>
  <div class="city" data-depth="0.3">{CITY}</div>
  <div class="grid"></div>
  <div class="palm l" data-depth="0.6">{PALM}</div>
  <div class="palm r" data-depth="0.6">{PALM}</div>
  <div class="wrap hero-in">
    <div>
      <p class="kick">NEW MISSION AVAILABLE · ETHEREUM</p>
      <h1 class="title" id="title">Macca<small>THE GATOR · $MACCA</small></h1>
      <p class="tagline" id="typer" data-lines="Leonida's hit show. Ethereum's pink bag.|Flamingo blood. Palm trees. One coin.|From the Goodtime State to the chain.|Vice City Animals. Community edition.">Leonida's hit show. Ethereum's pink bag.</p>
      <p class="lead">Leonida's favorite pink menace — flamingo-blood martini in one claw, stash-base figurine energy in the other. The community put him on Ethereum.</p>
      {cta()}
      {ca_box("ca")}
    </div>
    <div class="hero-card">
      <div class="tilt" id="tilt">
        <span class="tag">PLAYER 1 · MACCA</span>
        <picture><source media="(max-width:700px)" srcset="/img/banner-m.webp"><img src="/img/banner.webp" alt="Macca the Gator cruising a pink convertible through neon Vice City at sunset, martini in claw" width="1500" height="500" fetchpriority="high"></picture>
        <img class="logo-badge" src="/img/logo-400.webp" alt="Macca the Gator logo" width="400" height="400">
      </div>
    </div>
  </div>
  <div class="scrollcue">SCROLL TO START ▼</div>
</section>

<div class="marq" aria-hidden="true"><div class="track">{"".join("<span>"+t+"</span>" for t in ["$MACCA ★","FLAMINGO BLOOD","PALM TREES","ONE COIN ★","STAY PINK","HOLD BAGS","SKIP THE HEIST ★","LEONIDA","ON ETHEREUM ★"]*2)}</div></div>
<div class="marq alt" aria-hidden="true"><div class="track">{"".join("<span>"+t+"</span>" for t in ["VICE CITY ANIMALS","COMMUNITY EDITION ★","GOODTIME STATE","UNISWAP","DEXSCREENER ★","@MACCAOFETH"]*3)}</div></div>

<section id="about">
  <div class="wrap">
    <div class="sec-h" data-reveal><span class="num">01</span><h2>The <em>Story</em></h2><p>// STRAIGHT OUTTA VICE CITY, LEONIDA</p></div>
    <div class="about">
      <div class="dossier" data-reveal>
        <p>Leonida's favorite pink menace. Macca the Gator is the star of the hit Goodtime State TV show — flamingo-blood martini in one claw, stash-base figurine energy in the other. Official merch put him on the map; the community put him on Ethereum.</p>
        <p>Straight outta Vice City, Leonida. Pink scales, purple shades, palm-print shirt, and zero escape plan. Macca went from in-game billboards and the $400 Goodtime State collector's box to the chain — same grin, same cocktail, now on ETH.</p>
        <p>$Macca is a community-driven parody memecoin celebrating Leonida's cartoon king. <strong>Hold bags. Skip the heist. Stay pink.</strong></p>
        <div class="stats" id="stats">
          <div class="stat"><span>DRIP</span><span class="b"><i data-w="98"></i></span><span>98</span></div>
          <div class="stat"><span>CHARISMA</span><span class="b"><i data-w="100"></i></span><span>100</span></div>
          <div class="stat"><span>STEALTH</span><span class="b"><i data-w="7"></i></span><span>07</span></div>
          <div class="stat"><span>PINKNESS</span><span class="b"><i data-w="100"></i></span><span>MAX</span></div>
          <div class="stat"><span>ESCAPE PLAN</span><span class="b"><i data-w="0"></i></span><span>00</span></div>
        </div>
      </div>
      <div class="polaroids" data-reveal>
        <figure class="pol"><img src="/img/gallery/fig-cigar.webp" alt="Macca figurine with a cigar" loading="lazy"><span>stash-base energy</span></figure>
        <figure class="pol"><img src="/img/gallery/fig-neon-city.webp" alt="Macca figurine against a neon city" loading="lazy"><span>Vice City nights</span></figure>
        <figure class="pol"><img src="/img/gallery/fig-animals.webp" alt="Vice City animal figurines" loading="lazy"><span>the whole crew</span></figure>
      </div>
    </div>
  </div>
</section>

<section id="missions">
  <div class="wrap">
    <div class="sec-h" data-reveal><span class="num">02</span><h2>Mission <em>Select</em></h2><p>// CHOOSE YOUR NEXT MOVE</p></div>
    <div class="missions">
      <a class="mission m-buy" href="{BUY}" target="_blank" rel="noopener" data-tilt data-reveal><span class="bgimg" style="background-image:url(/img/banner-m.webp)"></span><span class="mtag">MISSION 01</span><div class="in"><h3>The Pink Swap</h3><p>Grab $Macca on Uniswap — Ethereum mainnet, exact CA pre-filled.</p><span class="go">Buy on Uniswap</span></div></a>
      <a class="mission m-chart" href="{CHART}" target="_blank" rel="noopener" data-tilt data-reveal><span class="bgimg" style="background-image:url(/img/gallery/poster-leonida.webp)"></span><span class="mtag">MISSION 02</span><div class="in"><h3>Stake Out the Chart</h3><p>Watch the candles from the safehouse on DexScreener.</p><span class="go">Open Chart</span></div></a>
      <a class="mission m-x" href="{X}" target="_blank" rel="noopener" data-tilt data-reveal><span class="bgimg" style="background-image:url(/img/vault/meme-07-480.webp)"></span><span class="mtag">MISSION 03</span><div class="in"><h3>Join the Crew</h3><p>Follow @MaccaGator_ETH on X for the drops, raids and memes.</p><span class="go">Follow on X</span></div></a>
    </div>
    <div class="live" id="live" data-reveal>
      <div><small>PRICE</small><b data-stat="price">—</b></div>
      <div><small>MARKET CAP</small><b data-stat="mcap">—</b></div>
      <div><small>24H</small><b data-stat="chg">—</b></div>
      <div><small>LIQUIDITY</small><b data-stat="liq">—</b></div>
    </div>
  </div>
</section>

<section id="howto">
  <div class="wrap">
    <div class="sec-h" data-reveal><span class="num">03</span><h2>How to <em>Buy</em></h2><p>// TUTORIAL MISSION · UNISWAP · ETHEREUM</p></div>
    <div class="steps">
      <div class="step" data-reveal><span class="ck">✓ COMPLETE</span><h3>Get a Wallet</h3><p>Install MetaMask, Rabby, Coinbase Wallet or any Ethereum wallet. Back up your seed phrase offline — never share it.</p></div>
      <div class="step" data-reveal><span class="ck">✓ COMPLETE</span><h3>Load Up ETH</h3><p>Buy ETH on an exchange and send it to your wallet on Ethereum mainnet. Keep a little extra for gas.</p></div>
      <div class="step" data-reveal><span class="ck">✓ COMPLETE</span><h3>Open Uniswap</h3><p>Hit our <a href="{BUY}" target="_blank" rel="noopener">Uniswap link</a> — $Macca is pre-filled. Or paste the CA: <code>{CA}</code></p></div>
      <div class="step" data-reveal><span class="ck">✓ COMPLETE</span><h3>Swap &amp; Stay Pink</h3><p>Choose your ETH amount, set slippage if needed, confirm the swap. Welcome to Leonida.</p></div>
    </div>
    <div class="cta" style="justify-content:center;margin-top:34px">
      <a class="btn" href="{BUY}" target="_blank" rel="noopener">{ICON_UNI} Start Mission on Uniswap</a>
    </div>
    <div style="max-width:640px;margin:0 auto">{ca_box("ca2")}</div>
    <p class="cheat">CHEAT CODE: type <kbd>MACCA</kbd> anywhere on the page.</p>
  </div>
</section>

<section id="vault">
  <div class="wrap">
    <div class="sec-h" data-reveal><span class="num">04</span><h2>Meme <em>Vault</em></h2><p>// EVIDENCE BOARD · {len(primary)} FILES RECOVERED</p></div>
    <div class="gal">
{gal}
    </div>
    <div class="center"><a class="btn cy" href="/memes">Open the full Meme Vault →</a></div>
  </div>
</section>

<section id="faq">
  <div class="wrap">
    <div class="sec-h" data-reveal><span class="num">05</span><h2>Intel <em>FAQ</em></h2><p>// KNOW BEFORE YOU GO</p></div>
    <div class="faq">
      <details data-reveal><summary>What is $Macca?</summary><p>Macca the Gator ($Macca) is a community-driven parody memecoin on Ethereum celebrating Leonida's pink cartoon gator. It is a fan meme — no utility, no roadmap, just vibes.</p></details>
      <details data-reveal><summary>What chain is it on?</summary><p>Ethereum mainnet. The main liquidity pair is on Uniswap: <code>{PAIR}</code></p></details>
      <details data-reveal><summary>What is the contract address?</summary><p><code>{CA}</code> — always double-check it before swapping. Anything else is not us.</p></details>
      <details data-reveal><summary>Where do I buy?</summary><p>On <a href="{BUY}" target="_blank" rel="noopener">Uniswap</a> with ETH. Track it on <a href="{CHART}" target="_blank" rel="noopener">DexScreener</a>.</p></details>
      <details data-reveal><summary>Where is the community?</summary><p>On X at <a href="{X}" target="_blank" rel="noopener">@MaccaGator_ETH</a>.</p></details>
      <details data-reveal><summary>Is this official Rockstar / GTA?</summary><p>No. This is a fan-made parody memecoin. Not affiliated with, endorsed by, or connected to Rockstar Games, Take-Two Interactive, or Grand Theft Auto.</p></details>
    </div>
  </div>
</section>

<section class="final">
  <div class="wrap">
    <h2 data-reveal>Stay Pink.</h2>
    <p data-reveal>Hold bags. Skip the heist.</p>
    {cta()}
  </div>
</section>
</main>
{LB}
''' + footer()

def memes_page():
    grid = "\n".join(tile(m, i) for i, m in enumerate(primary))
    bon = "\n".join(tile(m, i) for i, m in enumerate(bonus))
    return head("Meme Vault — Macca the Gator ($Macca)", "The $Macca meme vault: Macca the Gator causing pink chaos across Leonida. Fan-made parody memes.", "/memes") + hud("memes") + f'''
<main>
<section class="page-top"><div class="wrap"><h1>Meme Vault</h1><p>// {len(memes)} FILES · CLICK TO ENLARGE · ← → TO BROWSE</p>
{cta(' style="justify-content:center"')}</div></section>
<section style="padding-top:40px"><div class="wrap">
  <div class="gal">
{grid}
  </div>
  {('<div class="sec-h" style="margin-top:60px"><h2>Bonus <em>Files</em></h2><p>// EXTRA DROPS</p></div><div class="gal" style="columns:4 200px">' + bon + '</div>') if bonus else ''}
  <div class="sec-h" style="margin-top:60px"><h2>Meme <em>Kit</em></h2><p>// DOWNLOAD &amp; SPREAD THE PINK</p></div>
  <div class="cta"><a class="btn" href="/kit/macca-logo.png" download>Logo PNG</a><a class="btn cy" href="/kit/macca-banner.jpg" download>Banner JPG</a></div>
  <div style="max-width:640px">{ca_box("ca")}</div>
</div></section>
</main>
{LB}
''' + footer()

open(os.path.join(R, "index.html"), "w").write(index())
open(os.path.join(R, "memes.html"), "w").write(memes_page())
print("built", len(primary), "primary +", len(bonus), "bonus")
