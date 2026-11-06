#!/usr/bin/env python3
"""Brand.Life static site generator.
Run from the repo root:  python3 _build/build.py
Writes finished HTML to the repo root so GitHub Pages (free plan) serves it as-is — no server, no database."""
import datetime
import html
import json
import os
import sys

import markdown

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from guides import GUIDES  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://brand.life"
TODAY = datetime.date.today()
ADS = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>'
OWNER = "https://web.works/contact"
PAGES = []
# JEKYLL=1 (default): emit front matter + body and one _layouts/default.html; GitHub Pages renders the shared chrome.
JEKYLL = os.environ.get("JEKYLL", "1") == "1"
# 404 pages are served at any depth, so they need a base URL. Works on brand.life and on <user>.github.io/Brand-Life/.
BASETAG = "<script>(function(){var p=location.pathname.split('/')[1]||'';document.write('<base href=\"'+(p.toLowerCase()==='brand-life'?'/'+p+'/':'/')+'\">');})();</script>"

LOGO = ('<svg viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="11" fill="#16120F"/>'
        '<circle cx="20" cy="20" r="13" fill="none" stroke="#FF4F2B" stroke-width="2.4" stroke-dasharray="62 20" stroke-linecap="round" transform="rotate(-60 20 20)"/>'
        '<path d="M15 12.5h6.2c2.9 0 4.6 1.4 4.6 3.7 0 1.5-.8 2.6-2.1 3.1 1.7.4 2.8 1.7 2.8 3.5 0 2.6-2 4.2-5.1 4.2H15z" fill="#F7F2EA"/>'
        '<circle cx="29.5" cy="29" r="2.2" fill="#0D9488"/></svg>')

NAV = [("tools/", "Free tools"), ("guides/", "Guides"), ("guides/brand-life-cycle.html", "Life Cycle"), ("videos.html", "Videos"),
       ("news.html", "News"), ("contests.html", "Contests"), ("support.html", "Support")]

TOOLS = [
    ("name-generator", "Brand Name Generator", "Dozens of brandable names from your keywords, with a quick .com check.", "✦", "Naming"),
    ("name-tester", "Brand Name Tester", "Score any name for length, rhythm, spelling and the radio test.", "◎", "Naming"),
    ("tagline-generator", "Tagline & Slogan Generator", "Taglines in five tones — bold, warm, clever, premium or simple.", "❝", "Messaging"),
    ("color-palette", "Color Palette Generator", "Harmonious palettes with WCAG contrast checks and CSS export.", "◐", "Identity"),
    ("font-pairing", "Font Pairing Explorer", "Preview proven free Google Font pairings with your own words.", "Aa", "Identity"),
    ("brand-archetype-quiz", "Brand Archetype Quiz", "12 questions to find your primary and secondary archetype.", "♞", "Personality"),
    ("brand-health-score", "Brand Health Score", "Rate your brand across five dimensions and get a priority plan.", "♥", "Strategy"),
    ("style-guide-builder", "Style Guide Builder", "Turn your choices into a printable one-page brand guide.", "▤", "Identity"),
    ("bio-generator", "Personal Brand Bio Generator", "Social, short, medium and speaker bios from one form.", "☺", "Personal brand"),
    ("positioning-statement", "Positioning Statement Builder", "Write the one sentence that drives every brand decision.", "◆", "Strategy"),
]

TIPS = [
    "Say your brand name out loud to someone and ask them to spell it. If they can't, the internet can't find you either.",
    "Pick one color you'll use everywhere. Recognition comes from repetition, not variety.",
    "Replace one adjective on your homepage with a number. 'Fast' becomes 'ready in 48 hours'.",
    "Search your brand name in a private window today. What a stranger sees is your real brand.",
    "Write down three words your brand is NOT. It stops well-meaning people from drifting off-brand.",
    "Your favicon is a logo too. Check it at 16 pixels.",
    "Ask your last five customers why they chose you. Use their exact words in your next headline.",
    "Consistency beats creativity in the first year. Use the same profile photo and bio everywhere.",
    "Before redesigning, list what customers recognize you by. Keep those assets.",
    "Your 'About' page is often the second most-visited page. Make it about the customer's problem, not your history.",
    "A tagline should survive being read by a competitor. If they could use it too, sharpen it.",
    "Track branded searches monthly in Google Search Console. It's a free brand-health meter.",
    "Test your text colors for 4.5:1 contrast. Accessible brands are readable brands.",
    "Put your positioning statement at the top of every creative brief.",
    "Reply to every review this week — good and bad. Responses are brand voice in public.",
    "Make your invoice look like your brand. It's a touchpoint every paying customer sees.",
    "Choose two typefaces and stop. A third is almost always a mistake.",
    "Describe your brand as a person at a party. If it's 'nice', keep going until it's specific.",
    "The best brand stories have a villain — usually the problem your customer faces, not a competitor.",
    "Audit your email signature. It's seen more often than your logo on almost anything else.",
    "Run a tiny contest: invite customers to name a new product. Free ideas, free engagement.",
]


def esc(s):
    return html.escape(s, quote=True)


def hp():
    return '<div class="hp" aria-hidden="true"><label>Leave empty<input name="_hp" tabindex="-1" autocomplete="off"></label></div>'


def status():
    return '<p class="form-status" aria-live="polite"></p>'


def consent_line():
    return ('<p class="fine">By sending this you agree to our <a href="{pre}privacy.html">privacy policy</a>. '
            'Your details go straight to the Brand.Life team. We never sell your data, and you can ask us to delete it at any time.</p>')


def nav_html(pre, key):
    out = []
    for href, label in NAV:
        cur = ' aria-current="page"' if key == href else ""
        out.append(f'<a href="{pre}{href}"{cur}>{label}</a>')
    return "".join(out)


def footer(pre):
    tool_links = "".join(f'<li><a href="{pre}tools/{t[0]}.html">{t[1]}</a></li>' for t in TOOLS[:6])
    return f"""<footer class="site-foot">
 <div class="wrap">
  <div class="foot-grid">
   <div>
    <a class="brand" href="{pre}index.html" style="color:#fff">{LOGO}<span>Brand<span class="dot">.</span>Life</span></a>
    <p style="margin-top:14px">Free tools, guides and expert help to build a brand that lasts — from the first spark to the next renewal.</p>
    <form class="form" data-form="Newsletter signup" data-ok="You're in. The next Brand Notes issue lands on Tuesday." style="margin-top:14px">
     <label for="nl-email" style="color:#fff">Brand Notes — one practical branding idea every Tuesday</label>
     {hp()}
     <input id="nl-email" type="email" name="email" placeholder="you@yourbrand.com" required autocomplete="email">
     <select name="stage" aria-label="Your brand stage"><option value="">Your brand stage (optional)</option><option>Spark — idea stage</option><option>Launch — first customers</option><option>Grow — building presence</option><option>Scale — many people touch the brand</option><option>Renew — refresh or rebrand</option></select>
     <button class="btn" type="submit">Subscribe free</button>
     {status()}
    </form>
   </div>
   <div><h4>Free tools</h4><ul>{tool_links}<li><a href="{pre}tools/">All 10 tools →</a></li></ul></div>
   <div><h4>Get involved</h4><ul>
    <li><a href="{pre}audit.html">Free brand audit</a></li><li><a href="{pre}audit.html#match">Hire branding talent</a></li>
    <li><a href="{pre}contests.html">Contests &amp; prizes</a></li><li><a href="{pre}support.html">Support Brand.Life</a></li>
    <li><a href="{pre}careers.html">Work &amp; write with us</a></li><li><a href="{pre}advertise.html">Advertise &amp; sponsor</a></li></ul></div>
   <div><h4>About</h4><ul>
    <li><a href="{pre}about.html">About us</a></li><li><a href="{pre}contact.html">Contact</a></li>
    <li><a href="{pre}privacy.html">Privacy &amp; cookies</a></li><li><a href="{pre}terms.html">Terms of use</a></li>
    <li><a href="{pre}disclaimer.html">Disclaimer</a></li><li><a href="{pre}trademark.html">Trademark &amp; copyright</a></li>
    <li><a href="{pre}sitemap.html">Site map</a></li></ul></div>
  </div>
  <div class="foot-legal">
   <p>© <span data-year>{TODAY.year}</span> Brand.Life. All original articles, tools, quizzes, frameworks and designs on this site are protected by copyright. All rights reserved.</p>
   <p><b>Trademark notice:</b> "Brand.Life" is the name of this independent educational website. It is not affiliated with, endorsed by or connected to any company, product, agency or service that uses "BrandLife", "Brand Life" or a similar name or mark. All third-party names, logos and marks mentioned belong to their respective owners and are used for identification and commentary only. <a href="{pre}trademark.html">Full disclosure</a>.</p>
   <p>Content is for general education, not legal, financial or trademark advice. Ads are served by Google AdSense; some outbound links may become affiliate links, which never change our recommendations.</p>
  </div>
 </div>
</footer>"""


def render(full, desc, robots, canon, pre, ld, extra_head, nav_key, body, scripts, basetag, nav=None):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
{basetag}
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full)}</title>
<meta name="description" content="{esc(desc)}">
{robots}
<link rel="canonical" href="{canon}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Brand.Life">
<meta property="og:title" content="{esc(full)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{BASE_URL}/assets/img/og.svg">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#16120F">
<meta name="google-adsense-account" content="ca-pub-6620975821265271">
<link rel="icon" href="{pre}assets/img/favicon.svg" type="image/svg+xml">
<link rel="manifest" href="{pre}site.webmanifest">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,600;0,9..144,700;0,9..144,800;1,9..144,700&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/css/style.css">
{ADS}
{ld}
{extra_head}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<div class="owner-strip">Contact, if you are interested in this website / domain name / Sponsorship / Advertisement / Partnership — <a href="{OWNER}" target="_blank" rel="noopener">contact here</a></div>
<header class="site-head">
 <div class="wrap head-row">
  <a class="brand" href="{pre}index.html" aria-label="Brand.Life home">{LOGO}<span>Brand<span class="dot">.</span>Life</span></a>
  <button class="icon-btn menu-btn" aria-expanded="false" aria-controls="nav" aria-label="Open menu"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button>
  <nav class="nav" id="nav" aria-label="Main">{nav if nav is not None else nav_html(pre, nav_key)}<a class="btn small" href="{pre}audit.html">Free brand audit</a>
   <button class="icon-btn" data-theme-toggle aria-label="Switch light or dark theme"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></button>
  </nav>
 </div>
</header>
<main id="main">
{body.strip()}
</main>
{footer(pre)}
<div class="consent" id="consent" hidden role="dialog" aria-label="Cookie notice">
 <p>We use cookies to run this site and, through Google AdSense, to show ads. Choose personalized ads, or essential cookies only with non-personalized ads. See our <a href="{pre}privacy.html">privacy policy</a>.</p>
 <div class="acts"><button class="btn small" data-consent="all">Accept all</button><button class="btn small alt" data-consent="essential">Essential only</button></div>
</div>
<script src="{pre}assets/js/config.js"></script>
<script src="{pre}assets/js/main.js"></script>
{scripts}
</body>
</html>
"""


def page(path, title, desc, body, nav_key=None, scripts="", jsonld=None, extra_head="", noindex=False, basetag=""):
    depth = path.count("/")
    pre = "../" * depth
    canon = BASE_URL + "/" + (path[:-10] if path.endswith("index.html") else path)
    full = title if "Brand.Life" in title else f"{title} | Brand.Life"
    ld = ('<script type="application/ld+json">' + json.dumps(jsonld, ensure_ascii=False) + "</script>") if jsonld else ""
    robots = '<meta name="robots" content="noindex">' if noindex else ""
    body = body.replace("{pre}", pre)
    if JEKYLL:
        fm = {"layout": "default", "full_title": full, "description": desc, "canon": canon, "pre": pre, "nav_key": nav_key or "",
              "jsonld": ld, "robots": robots, "basetag": basetag, "scripts": scripts, "extra_head": extra_head}
        if "{{" in body or "{%" in body:
            raise SystemExit("Liquid-like syntax in body of " + path)
        doc = "---\n" + "".join(f"{k}: {json.dumps(v, ensure_ascii=False)}\n" for k, v in fm.items()) + "---\n" + body.strip() + "\n"
    else:
        doc = render(full, desc, robots, canon, pre, ld, extra_head, nav_key, body, scripts, basetag)
    dest = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(dest) or ROOT, exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(doc)
    if not noindex:
        PAGES.append(canon)


def crumbs(*items):
    parts = ['<a href="{pre}index.html">Home</a>']
    for href, label in items:
        parts.append(f'<a href="{href}">{label}</a>' if href else f"<span>{label}</span>")
    return '<nav class="crumbs" aria-label="Breadcrumb">' + " / ".join(parts) + "</nav>"


def faq_block(items):
    out = "".join(f"<details><summary>{esc(q)}</summary><p>{a}</p></details>" for q, a in items)
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a)}} for q, a in items]}
    return out, ld


LEAD_MINI = """<div class="lead-box">
 <span class="eyebrow">Free · No obligation</span>
 <h3>Get a free brand audit</h3>
 <p class="muted">Tell us where your brand is today. A branding specialist reviews your site and socials and sends back your three biggest opportunities — usually within two business days.</p>
 <form class="form" data-form="Quick brand audit request" data-redirect="{pre}thank-you.html">
  """ + hp() + """
  <div class="row"><input name="name" placeholder="Your name" required autocomplete="name" aria-label="Your name">
  <input type="email" name="email" placeholder="Email" required autocomplete="email" aria-label="Email"></div>
  <input name="website" placeholder="Website or Instagram (optional)" aria-label="Website">
  <select name="need" aria-label="What do you need most?"><option>Brand strategy &amp; positioning</option><option>Name or rename</option><option>Logo &amp; visual identity</option><option>Website that converts</option><option>Personal brand</option><option>Rebrand / refresh</option><option>Not sure — audit everything</option></select>
  <button class="btn" type="submit">Send my free audit request</button>
  """ + status() + """
 </form>
</div>"""


# ------------------------------------------------------------------ HOME
def build_home():
    tool_cards = "".join(
        f'<a class="card" href="{{pre}}tools/{s}.html"><div class="ico">{ico}</div><span class="tag">{cat}</span><h3>{t}</h3><p>{d}</p></a>'
        for s, t, d, ico, cat in TOOLS[:6])
    guide_cards = "".join(
        f'<a class="card" href="{{pre}}guides/{g["slug"]}.html"><span class="tag">{g["cat"]}</span><span class="tag">{g["min"]} min</span><h3>{esc(g["title"])}</h3><p>{esc(g["desc"])}</p></a>'
        for g in GUIDES[:6])
    stages = [
        ("01", "Spark", "Idea → first sale", "Prove a specific group wants this. Name, one-line promise, credible one-page site.", "Positioning Builder", "positioning-statement"),
        ("02", "Launch", "First customers", "Look trustworthy to strangers: consistent identity, first reviews, one or two channels.", "Color Palette Generator", "color-palette"),
        ("03", "Grow", "Category presence", "Become a name people search for: content, referrals, contests, partnerships.", "Brand Health Score", "brand-health-score"),
        ("04", "Scale", "Market leadership", "Protect consistency as more people touch the brand: guidelines, training, trademarks.", "Style Guide Builder", "style-guide-builder"),
        ("05", "Renew", "Reinvention", "Stay relevant without losing equity: refresh what's stale, keep what's recognized.", "Brand Archetype Quiz", "brand-archetype-quiz"),
    ]
    stage_html = "".join(
        f'<button class="stage" type="button" aria-pressed="false"><span class="n">{n}</span><b>{name}</b><small class="muted">{sub}</small>'
        f'<template><div class="card"><h3>{name}: {sub}</h3><p style="color:inherit">{txt}</p><p><a class="btn small grow" href="{{pre}}tools/{slug}.html">Use the {tool}</a> '
        f'<a class="btn small alt" href="{{pre}}guides/brand-life-cycle.html">Read the full framework</a></p></div></template></button>'
        for n, name, sub, txt, tool, slug in stages)
    faq, faq_ld = faq_block([
        ("Is Brand.Life really free?", "Yes. Every tool, quiz and guide is free and works in your browser without an account. The site is supported by advertising, sponsors and voluntary support from readers."),
        ("Do you store what I type into the tools?", "No. The tools run entirely in your browser. Nothing is sent anywhere unless you choose to submit a form, such as the free brand audit."),
        ("What is the free brand audit?", "You share your website or social profile and what you need. A branding specialist reviews it and replies with your three biggest opportunities. There is no obligation to buy anything."),
        ("Can I use names generated here?", "Generated names are suggestions. Before using one, check domain availability and run a trademark search in your market — our naming guide explains how. We don't claim any rights over names you create."),
        ("Is this site connected to any company called BrandLife?", "No. Brand.Life is an independent educational website and is not affiliated with any company that uses a similar name. See our trademark disclosure."),
    ])
    ticker_words = ["Naming", "Positioning", "Identity", "Voice", "Archetypes", "Color", "Typography", "Personal brand", "Rebrand", "Brand health"]
    ticker = "".join(f"{w}<em>✦</em>" for w in ticker_words) * 2
    body = f"""
<section class="hero">
 <div class="wrap hero-grid">
  <div>
   <span class="eyebrow">Free brand-building toolkit</span>
   <h1>Give your brand a <em>longer, stronger</em> life.</h1>
   <p class="lead">Name it, position it, design it and grow it — with 10 free tools, practical guides and a free expert audit. Built for founders, creators, freelancers and small teams.</p>
   <div class="ctas"><a class="btn" href="{{pre}}tools/brand-health-score.html">Get my Brand Health Score</a><a class="btn alt" href="{{pre}}tools/">Explore free tools</a></div>
   <div class="trust"><span><b>10</b>free tools</span><span><b>12</b>in-depth guides</span><span><b>5</b>life-cycle stages</span><span><b>$0</b>no sign-up</span></div>
  </div>
  <div class="ring-card">
   <span class="eyebrow">Today's brand tip</span>
   <p id="daily-tip" style="font:700 1.25rem/1.4 var(--display)">{esc(TIPS[0])}</p>
   <hr style="border:0;border-top:1px solid var(--line);margin:18px 0">
   <form class="form" id="quick-name" action="{{pre}}tools/name-tester.html" method="get">
    <label for="qn">Test a brand name in one click</label>
    <div class="row"><input id="qn" name="name" placeholder="e.g. Northbeam" required><button class="btn grow" type="submit">Score it</button></div>
   </form>
  </div>
 </div>
</section>
<div class="ticker" aria-hidden="true"><span>{ticker}</span></div>
<section>
 <div class="wrap">
  <div class="sec-head"><span class="eyebrow">Free tools</span><h2>Everything you need to build a brand — free, in your browser</h2><p class="muted">No account. No watermark. Nothing you type leaves your device.</p></div>
  <div class="grid g3">{tool_cards}</div>
  <p style="margin-top:24px"><a class="btn alt" href="{{pre}}tools/">See all 10 tools</a></p>
 </div>
</section>
<section class="sec-alt">
 <div class="wrap">
  <div class="sec-head"><span class="eyebrow">The Brand Life Cycle</span><h2>Every brand lives through five stages. Which one are you in?</h2><p class="muted">Doing the right work for the wrong stage is the most expensive branding mistake. Pick your stage to see what to focus on now.</p></div>
  <div class="cycle">{stage_html}</div>
  <div class="stage-detail" id="stage-detail"></div>
 </div>
</section>
<section>
 <div class="wrap hero-grid">
  <div>
   <span class="eyebrow">Free expert review</span>
   <h2>Not sure what's holding your brand back?</h2>
   <p class="muted">Most brands lose customers to one or two fixable gaps: unclear positioning, an inconsistent look, a name nobody can spell, or a website that doesn't convert. A free audit finds them.</p>
   <ul>
    <li>Positioning and message clarity review</li><li>Visual identity and consistency check across your site and socials</li>
    <li>Three prioritized actions you can start this week</li><li>Optional introduction to a vetted designer, strategist or agency</li>
   </ul>
   <p><a href="{{pre}}audit.html">See the full audit and expert-matching options →</a></p>
  </div>
  {LEAD_MINI}
 </div>
</section>
<section class="sec-alt">
 <div class="wrap">
  <div class="sec-head"><span class="eyebrow">Guides</span><h2>Learn branding the practical way</h2></div>
  <div class="grid g3">{guide_cards}</div>
  <p style="margin-top:24px"><a class="btn alt" href="{{pre}}guides/">All guides</a></p>
 </div>
</section>
<section>
 <div class="wrap grid g2" style="align-items:start">
  <div>
   <span class="eyebrow">Watch</span><h2>Branding masterclasses, free</h2>
   <p class="muted">Curated talks and channels from designers, strategists and founders.</p>
   <button class="yt" data-yt="qp0HIF3SfI4" aria-label="Play: Simon Sinek — How great leaders inspire action (TEDx)"></button>
   <p style="margin-top:14px"><a href="{{pre}}videos.html">Open the video library →</a></p>
  </div>
  <div>
   <span class="eyebrow">Fresh daily</span><h2>Branding news</h2>
   <p class="muted" data-news-updated>Headlines from leading branding and design publications, refreshed automatically every day.</p>
   <div data-news="6" data-src="{{pre}}data/news.json"><p class="muted">Loading the latest headlines… If nothing appears, <a href="{{pre}}news.html">open the news page</a>.</p></div>
  </div>
 </div>
</section>
<section class="sec-ink">
 <div class="wrap grid g3">
  <div><span class="eyebrow">Contests</span><h3>Win prizes for your creativity</h3><p class="muted">Monthly naming, tagline and logo challenges with cash prizes, features and mentorship.</p><a class="btn small" href="{{pre}}contests.html">See this month's challenge</a></div>
  <div><span class="eyebrow">Support</span><h3>Keep the tools free</h3><p class="muted">Your support funds new tools, contest prizes and paid opportunities for emerging designers.</p><a class="btn small" href="{{pre}}support.html">Support Brand.Life</a></div>
  <div><span class="eyebrow">Partner</span><h3>Reach brand builders</h3><p class="muted">Sponsor a tool, a contest or our newsletter and reach founders actively building brands.</p><a class="btn small" href="{{pre}}advertise.html">Advertise with us</a></div>
 </div>
</section>
<section>
 <div class="wrap narrow"><span class="eyebrow">FAQ</span><h2>Questions, answered</h2>{faq}</div>
</section>
"""
    ld = [{"@context": "https://schema.org", "@type": "WebSite", "name": "Brand.Life", "url": BASE_URL + "/",
           "description": "Free brand-building tools, guides and expert audits."}, faq_ld,
          {"@context": "https://schema.org", "@type": "Organization", "name": "Brand.Life", "url": BASE_URL + "/", "logo": BASE_URL + "/assets/img/favicon.svg"}]
    tips = "<script>window.BL_TIPS=" + json.dumps(TIPS) + ";</script>"
    page("index.html", "Brand.Life — Free Brand Building Tools, Guides & Brand Audits",
         "Name, position, design and grow your brand with 10 free tools, practical branding guides, the Brand Life Cycle framework and a free expert brand audit.",
         body, nav_key="", jsonld=ld, scripts=tips.replace("</script>", "</script>\n<script>(function(){var d=new Date(),n=Math.floor((d-new Date(d.getFullYear(),0,0))/864e5),e=document.getElementById('daily-tip');if(e)e.textContent=BL_TIPS[n%BL_TIPS.length];})();</script>"))


# ------------------------------------------------------------------ TOOLS
TOOL_BODIES = {}

TOOL_BODIES["name-generator"] = ("""
<form class="form card" id="name-gen">
 <label for="ng-kw">Keywords that describe your brand</label>
 <input id="ng-kw" placeholder="e.g. calm, coffee, morning" value="spark, bright, north">
 <label for="ng-ind">Industry flavor</label>
 <select id="ng-ind"><option value="">None</option><option value="tech">Tech &amp; SaaS</option><option value="food">Food &amp; drink</option><option value="wellness">Health &amp; wellness</option><option value="fashion">Fashion &amp; beauty</option><option value="finance">Finance</option><option value="creative">Creative &amp; media</option><option value="home">Home &amp; living</option><option value="services">Professional services</option></select>
 <label>Name styles</label>
 <div class="checks"><label><input type="checkbox" name="style" value="compound" checked> Compound</label><label><input type="checkbox" name="style" value="blend" checked> Blend</label><label><input type="checkbox" name="style" value="invented" checked> Invented</label><label><input type="checkbox" name="style" value="prefix"> Prefix</label><label><input type="checkbox" name="style" value="real"> Classic</label></div>
 <button class="btn" type="submit">Generate names</button>
 <p class="fine">Your favorites:</p><div id="ng-fav"></div>
</form>
<div class="out" id="ng-out" aria-live="polite"></div>
""", [
    ("How does the brand name generator work?", "It combines your keywords with industry word banks, suffixes, prefixes and invented syllables, then scores every result with the same rules as our Name Tester. Click Generate again for a fresh batch."),
    ("Are the names available?", "We can't guarantee availability. Use the Check .com link for each name, then run a trademark search before you commit."),
    ("Can I use a name I find here?", "Yes — we claim no rights over generated names. Make sure nobody else has rights to it in your market first."),
], "how-to-name-a-brand")

TOOL_BODIES["name-tester"] = ("""
<form class="form card" id="name-test">
 <label for="nt-name">Brand name to test</label>
 <input id="nt-name" name="name" placeholder="Type a name" value="Brand Life">
 <p class="fine">Scores update as you type.</p>
 <div class="score-big" id="nt-score">0</div><div class="meter"><i id="nt-meter"></i></div>
</form>
<div class="card">
 <h3>Breakdown</h3><div class="grid" id="nt-parts" style="gap:10px"></div>
 <h3 style="margin-top:18px">Notes</h3><ul id="nt-notes"></ul>
 <div id="nt-links" style="display:flex;gap:8px;flex-wrap:wrap"></div>
</div>
""", [
    ("What makes a good brand name score?", "Names score highest when they're 4–9 letters, three syllables or fewer, spelled the way they sound, have a natural vowel balance and open on a strong consonant."),
    ("Is a low score a dealbreaker?", "No. Some famous brands would score modestly. The score flags risks so you can decide deliberately — for example, a hard-to-spell name needs more marketing to become searchable."),
    ("Does this check trademarks?", "No. It links to official databases (USPTO and WIPO) so you can search. For anything you'll invest in, ask a trademark attorney for a full clearance search."),
], "how-to-name-a-brand")

TOOL_BODIES["tagline-generator"] = ("""
<form class="form card" id="tagline-gen">
 <label for="tg-brand">Brand name</label><input id="tg-brand" value="Northbeam">
 <label for="tg-benefit">Main benefit (a noun phrase)</label><input id="tg-benefit" value="stress-free bookkeeping">
 <label for="tg-aud">Audience (plural)</label><input id="tg-aud" value="small business owners">
 <label for="tg-verb">Action verb</label><input id="tg-verb" value="grow">
 <label for="tg-tone">Tone</label>
 <select id="tg-tone"><option value="mix">Mix of all tones</option><option value="bold">Bold</option><option value="warm">Warm</option><option value="clever">Clever</option><option value="premium">Premium</option><option value="simple">Simple</option></select>
 <button class="btn" type="submit">Generate taglines</button>
</form>
<div class="out" id="tg-out" aria-live="polite"></div>
""", [
    ("What makes a strong tagline?", "Short (under eight words), specific to you, and focused on what the customer gets. Read it aloud next to a competitor's name — if it still fits, keep editing."),
    ("Tagline vs. slogan?", "A tagline is a long-lived line attached to your brand identity. A slogan usually belongs to a single campaign. This tool helps with both."),
], "brand-voice-guide")

TOOL_BODIES["color-palette"] = ("""
<form class="form card" id="palette">
 <label for="pl-base">Base brand color</label><input type="color" id="pl-base" value="#ff4f2b" style="height:54px;padding:4px">
 <label for="pl-mode">Harmony</label>
 <select id="pl-mode"><option value="mono">Monochrome scale</option><option value="analogous">Analogous</option><option value="complementary">Complementary</option><option value="triadic">Triadic</option><option value="split">Split complementary</option></select>
 <button class="btn alt" type="button" id="pl-random">Random base color</button>
 <p class="fine">Click any swatch to copy its HEX value.</p>
</form>
<div>
 <div class="swatches" id="pl-out"></div>
 <h3 style="margin-top:22px">Accessibility check (WCAG)</h3>
 <div class="article" style="max-width:none"><table id="pl-contrast"></table></div>
 <h3>CSS variables</h3><pre class="card" id="pl-css" style="white-space:pre-wrap;overflow:auto"></pre>
 <button class="copy" type="button" id="pl-copy">Copy CSS</button>
</div>
""", [
    ("How many colors should a brand have?", "Usually one primary, one or two secondary and a neutral range. A rough 60-30-10 split between neutral, secondary and primary keeps things balanced."),
    ("What contrast ratio do I need?", "WCAG AA asks for at least 4.5:1 for normal body text and 3:1 for large text. The table shows which of your colors pass on white or black."),
], "brand-color-psychology")

TOOL_BODIES["font-pairing"] = ("""
<form class="form card" id="fonts">
 <label for="fp-pair">Font pairing</label><select id="fp-pair"></select>
 <label for="fp-text">Your headline</label><input id="fp-text" value="Brands live in the details">
 <p class="fine">All fonts are free and open-licensed via Google Fonts.</p>
</form>
<div class="card">
 <h2 id="fp-h" style="font-size:2.6rem">Brands live in the details</h2>
 <p id="fp-b" style="color:inherit;font-size:1.08rem">Body text is where trust is built. It should be comfortable to read at 16 to 18 pixels, with lines of about 60 to 80 characters, generous spacing and enough weight to stay legible on every screen.</p>
 <h3>Embed code</h3><pre id="fp-code" style="white-space:pre-wrap;overflow:auto;font-size:.85rem"></pre>
 <button class="copy" type="button" id="fp-copy">Copy code</button>
</div>
""", [
    ("Why only two fonts?", "Two typefaces — one for headlines, one for body — give enough contrast for hierarchy while keeping the brand consistent. A third font is rarely necessary."),
    ("Can I use Google Fonts commercially?", "Fonts in the Google Fonts library are published under open licenses such as the SIL Open Font License, which permit commercial use. Check each family's license page to be sure."),
], "brand-identity-design")

TOOL_BODIES["brand-archetype-quiz"] = ("""
<form class="form" id="archetype" style="grid-column:1/-1">
 <div class="grid qs" style="gap:12px"></div>
 <button class="btn" type="submit">Reveal my archetype</button>
</form>
<div class="card" id="aq-result" hidden style="grid-column:1/-1"></div>
""", [
    ("What are brand archetypes?", "Twelve recurring character patterns, drawn from Carl Jung's work and popularized for marketing by Margaret Mark and Carol Pearson. They help keep a brand's personality consistent."),
    ("Is the result scientific?", "No — it's a creative alignment tool, not a psychometric test. Use it to start a conversation about who your brand is."),
], "brand-archetypes")

TOOL_BODIES["brand-health-score"] = ("""
<form class="form" id="health" style="grid-column:1/-1">
 <div class="grid qs" style="gap:12px"></div>
 <button class="btn" type="submit">Calculate my Brand Health Score</button>
</form>
<div id="hs-result" hidden style="grid-column:1/-1">
 <div class="grid g2" style="align-items:start">
  <div class="card"><span class="eyebrow">Your Brand Health Score</span><div class="score-big" id="hs-score">0</div><p><b id="hs-band"></b> · out of 100</p><div class="grid" id="hs-dims" style="gap:10px"></div>
   <h3 style="margin-top:18px">Your top 3 priorities</h3><ol id="hs-actions"></ol></div>
  <div class="lead-box">
   <span class="eyebrow">Free personalized plan</span>
   <h3>Get your 90-day brand plan by email</h3>
   <p class="muted">We'll send your score breakdown with a step-by-step plan for your three weakest areas — reviewed by a branding specialist, free.</p>
   <form class="form" id="hs-lead" data-form="Brand Health Score plan request" data-redirect="{pre}thank-you.html">
    """ + hp() + """
    <input name="name" placeholder="Your name" required aria-label="Your name">
    <input type="email" name="email" placeholder="Email" required aria-label="Email">
    <input name="website" placeholder="Website (optional)" aria-label="Website">
    <label class="fine"><input type="checkbox" name="wants_expert" value="Yes — introduce me to a vetted expert" style="width:auto"> Also introduce me to a vetted branding expert</label>
    <button class="btn" type="submit">Send my free plan</button>
    """ + status() + """
   </form>
  </div>
 </div>
</div>
""", [
    ("What does the Brand Health Score measure?", "Twenty statements across five dimensions: clarity, identity, consistency, visibility and loyalty. Each answer is scored 0–4 and converted to a score out of 100."),
    ("What's a good score?", "80+ is thriving, 60–79 growing, 40–59 fragile and under 40 at risk. The most useful output is your weakest dimension — that's where effort pays back fastest."),
    ("Do you store my answers?", "Only if you request the emailed plan; then your scores are sent with your request so we can personalize it."),
], "measuring-brand-health")

TOOL_BODIES["style-guide-builder"] = ("""
<form class="form card no-print" id="guide-builder">
 <label for="sg-name">Brand name</label><input id="sg-name" value="Northbeam">
 <label for="sg-tag">Tagline</label><input id="sg-tag" value="Books done. Evenings back.">
 <label for="sg-mission">Mission</label><textarea id="sg-mission" rows="2">Give small-business owners their evenings back with clear, monthly bookkeeping.</textarea>
 <label for="sg-aud">Audience</label><input id="sg-aud" value="Owner-operated trades businesses">
 <div class="row"><div><label for="sg-c1">Primary</label><input type="color" id="sg-c1" value="#0d6e66"></div><div><label for="sg-c2">Secondary</label><input type="color" id="sg-c2" value="#16120f"></div></div>
 <div class="row"><div><label for="sg-c3">Accent</label><input type="color" id="sg-c3" value="#ff4f2b"></div><div><label for="sg-c4">Neutral</label><input type="color" id="sg-c4" value="#f7f2ea"></div></div>
 <div class="row"><div><label for="sg-hf">Headline font</label><input id="sg-hf" value="Fraunces"></div><div><label for="sg-bf">Body font</label><input id="sg-bf" value="Manrope"></div></div>
 <label for="sg-voice">We are…</label><input id="sg-voice" value="Straight-talking, organized, reassuring">
 <label for="sg-not">We are not…</label><input id="sg-not" value="Stuffy, salesy, cutesy">
 <button class="btn" type="button" id="sg-print">Print or save as PDF</button>
</form>
<div class="card" id="sg-preview"></div>
""", [
    ("What should a brand style guide include?", "At minimum: mission, audience, logo rules, color values, typography, and voice. That's enough to keep anyone who creates content on-brand."),
    ("How do I save it?", "Click Print or save as PDF and choose Save as PDF in your browser's print dialog. Only the guide is printed."),
], "brand-identity-design")

TOOL_BODIES["bio-generator"] = ("""
<form class="form card" id="bio-gen">
 <label for="bg-name">Full name</label><input id="bg-name" value="Alex Rivera">
 <label for="bg-role">Role or title</label><input id="bg-role" value="brand strategist">
 <label for="bg-who">Who you help</label><input id="bg-who" value="first-time founders">
 <label for="bg-result">The result you deliver (starts with a verb)</label><input id="bg-result" value="launch brands people remember">
 <label for="bg-proof">Proof (optional)</label><input id="bg-proof" value="40+ brands launched since 2019">
 <label for="bg-fun">A human detail (optional)</label><input id="bg-fun" value="hunting for the city's best espresso">
 <label for="bg-cta">Call to action (optional)</label><input id="bg-cta" value="Say hi via the link below.">
</form>
<div class="out" id="bg-out" aria-live="polite"></div>
""", [
    ("First or third person?", "First person feels personal on social and your own site. Third person suits speaker introductions, press and company team pages."),
    ("How long should a bio be?", "Social bios are usually limited to about 150–160 characters. A short bio is 1–2 sentences; a medium bio about 60–100 words."),
], "personal-branding-guide")

TOOL_BODIES["positioning-statement"] = ("""
<form class="form card" id="positioning">
 <label for="ps-aud">Target audience</label><input id="ps-aud" placeholder="owner-operated trades businesses">
 <label for="ps-need">Their need or problem</label><input id="ps-need" placeholder="are drowning in receipts">
 <label for="ps-brand">Brand name</label><input id="ps-brand" placeholder="Northbeam">
 <label for="ps-cat">Category</label><input id="ps-cat" placeholder="bookkeeping service">
 <label for="ps-ben">Key benefit</label><input id="ps-ben" placeholder="delivers clean books every month with a 15-minute call">
 <label for="ps-comp">Main alternative</label><input id="ps-comp" placeholder="general accounting firms">
 <label for="ps-diff">Your difference</label><input id="ps-diff" placeholder="only serve trades and price monthly with no surprises">
</form>
<div class="card">
 <span class="eyebrow">Your positioning statement</span>
 <p id="ps-out" style="font:700 1.35rem/1.45 var(--display);color:inherit"></p>
 <button class="copy" type="button" id="ps-copy">Copy</button>
 <h3 style="margin-top:18px">Quick check</h3><ul id="ps-check"></ul>
</div>
""", [
    ("Is a positioning statement the same as a tagline?", "No. It's an internal tool that guides decisions. Your tagline and headlines are derived from it, written for customers."),
    ("How often should I revisit it?", "Whenever your audience, offer or competition changes meaningfully — and at least once a year."),
], "brand-strategy-template")

TOOL_INTROS = {
    "name-generator": "Type a few words that capture your brand and generate dozens of brandable names. Every suggestion is scored for sayability and spelling, and you can check the .com in one click.",
    "name-tester": "A great name is easy to say, easy to spell and easy to find. Test any name against the radio test and four other criteria professional namers use.",
    "tagline-generator": "Fill in four blanks and get a dozen tagline starting points in the tone you choose. Use them as raw material, then sharpen the best one.",
    "color-palette": "Start with one brand color and build a full palette using classic color harmonies. Every color is checked for WCAG text contrast so your brand stays readable.",
    "font-pairing": "Preview twelve proven pairings of free Google Fonts using your own headline, then copy the embed code.",
    "brand-archetype-quiz": "Answer 12 quick questions to discover which of the 12 brand archetypes leads your brand's personality — and which one supports it.",
    "brand-health-score": "Rate 20 statements honestly. You'll get a score out of 100, a breakdown across five brand dimensions and your three highest-impact priorities.",
    "style-guide-builder": "Fill in your brand basics and watch a one-page style guide build itself. Print it or save it as a PDF to share with your team or designer.",
    "bio-generator": "Answer seven prompts to get four ready-to-use bios: social, short, medium and speaker — with character counts.",
    "positioning-statement": "Positioning is the one sentence every brand decision should trace back to. Fill in the blanks and get instant feedback on clarity and differentiation.",
}


def build_tools():
    cards = "".join(
        f'<a class="card" href="{s}.html"><div class="ico">{ico}</div><span class="tag">{cat}</span><h3>{t}</h3><p>{d}</p></a>'
        for s, t, d, ico, cat in TOOLS)
    body = f"""<section><div class="wrap">{crumbs((None, "Free tools"))}
<div class="sec-head"><span class="eyebrow">Free brand tools</span><h1>10 free tools to build your brand</h1><p class="muted">Naming, messaging, identity, personality and strategy — each tool runs in your browser, needs no account and never stores what you type.</p></div>
<div class="grid g3">{cards}</div></div></section>
<section class="sec-alt"><div class="wrap narrow">{LEAD_MINI}</div></section>"""
    page("tools/index.html", "Free Brand Building Tools", "Free brand name generator, name tester, tagline generator, color palette tool, font pairing, archetype quiz, brand health score and more.", body, nav_key="tools/")
    guide_by = {g["slug"]: g for g in GUIDES}
    for s, t, d, ico, cat in TOOLS:
        ui, faqs, gslug = TOOL_BODIES[s]
        faq, faq_ld = faq_block(faqs)
        g = guide_by[gslug]
        wide = s in ("brand-archetype-quiz", "brand-health-score")
        shell = f'<div class="tool-shell"{" style=\"grid-template-columns:1fr\"" if wide else ""}>{ui}</div>'
        related = [x for x in TOOLS if x[0] != s][:3]
        rel = "".join(f'<a class="card" href="{x[0]}.html"><span class="tag">{x[4]}</span><h3>{x[1]}</h3><p>{x[2]}</p></a>' for x in related)
        body = f"""<section><div class="wrap">{crumbs(("{pre}tools/", "Free tools"), (None, t))}
<div class="sec-head"><span class="eyebrow">{cat} · free tool</span><h1>{t}</h1><p class="muted">{TOOL_INTROS[s]}</p></div>
{shell}
<div class="cta-inline no-print"><div><h3>Want a professional to look at this?</h3><p style="margin:0;opacity:.9">Get a free brand audit from a specialist — no obligation.</p></div><a class="btn" href="{{pre}}audit.html">Request free audit</a></div>
</div></section>
<section class="sec-alt no-print"><div class="wrap grid g2" style="align-items:start">
 <div><span class="eyebrow">Learn more</span><h2>Read: {esc(g["title"])}</h2><p class="muted">{esc(g["desc"])}</p><a class="btn alt" href="{{pre}}guides/{g["slug"]}.html">Read the guide</a></div>
 <div><span class="eyebrow">FAQ</span>{faq}</div>
</div></section>
<section class="no-print"><div class="wrap"><h2>More free tools</h2><div class="grid g3">{rel}</div></div></section>"""
        ld = [{"@context": "https://schema.org", "@type": "WebApplication", "name": t, "applicationCategory": "BusinessApplication",
               "operatingSystem": "Any (web browser)", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
               "url": f"{BASE_URL}/tools/{s}.html", "description": d}, faq_ld]
        page(f"tools/{s}.html", f"{t} — Free Online Tool", f"{d} Free, no sign-up, runs in your browser.", body,
             nav_key="tools/", jsonld=ld, scripts='<script src="{pre}assets/js/tools.js"></script>'.replace("{pre}", "../"))


# ------------------------------------------------------------------ GUIDES
def build_guides():
    cats = {}
    for g in GUIDES:
        cats.setdefault(g["cat"], []).append(g)
    cards = "".join(
        f'<a class="card" href="{g["slug"]}.html"><span class="tag">{g["cat"]}</span><span class="tag">{g["min"]} min read</span><h3>{esc(g["title"])}</h3><p>{esc(g["desc"])}</p></a>'
        for g in GUIDES)
    body = f"""<section><div class="wrap">{crumbs((None, "Guides"))}
<div class="sec-head"><span class="eyebrow">Branding guides</span><h1>Practical branding guides</h1><p class="muted">Clear, research-based guides written for people who have to actually build the brand — not just talk about it. Updated regularly.</p></div>
<div class="grid g3">{cards}</div></div></section>"""
    page("guides/index.html", "Branding Guides: Strategy, Naming, Identity & Growth", "Free in-depth guides on brand strategy, naming, identity design, brand voice, personal branding, rebranding and measuring brand health.", body, nav_key="guides/")
    for i, g in enumerate(GUIDES):
        md = markdown.Markdown(extensions=["tables", "toc", "sane_lists"])
        content = md.convert(g["body"])
        heads = []
        for tok in md.toc_tokens:
            heads.append((tok["id"], tok["name"]))
        toc = ""
        if len(heads) >= 3:
            toc = '<div class="toc"><b>In this guide</b><ol>' + "".join(f'<li><a href="#{h}">{n}</a></li>' for h, n in heads) + "</ol></div>"
        tool_cta = ""
        if g["tool"]:
            ts, tl = g["tool"]
            tool_cta = f'<div class="cta-inline"><div><h3>{tl}</h3><p style="margin:0;opacity:.9">Free tool · runs in your browser</p></div><a class="btn" href="{{pre}}tools/{ts}.html">Open tool</a></div>'
        nxt = GUIDES[(i + 1) % len(GUIDES)]
        related = [x for x in GUIDES if x["slug"] != g["slug"] and x["cat"] == g["cat"]][:2] + [nxt]
        seen, rel = set(), []
        k = 2
        while len(related) < 6:
            related.append(GUIDES[(i + k) % len(GUIDES)]); k += 1
        for x in related:
            if x["slug"] not in seen and x["slug"] != g["slug"]:
                seen.add(x["slug"]); rel.append(x)
        rel_html = "".join(f'<a class="card" href="{x["slug"]}.html"><span class="tag">{x["cat"]}</span><h3>{esc(x["title"])}</h3><p>{esc(x["desc"])}</p></a>' for x in rel[:3])
        # split content roughly in half to place the audit CTA mid-article
        parts = content.split("<h2", 3)
        if len(parts) >= 4:
            content = parts[0] + "<h2" + parts[1] + "<h2" + parts[2] + tool_cta + "<h2" + parts[3]
            tail_cta = ""
        else:
            tail_cta = tool_cta
        body = f"""<section><div class="wrap">
{crumbs(("{pre}guides/", "Guides"), (None, g["cat"]))}
<article class="article">
<span class="eyebrow">{g["cat"]}</span>
<h1 style="font-size:clamp(2rem,4.4vw,3.2rem)">{esc(g["title"])}</h1>
<p class="byline">By the Brand.Life Editorial Team · {g["min"]} min read · Updated <time datetime="{TODAY.isoformat()}">{TODAY.strftime("%B %Y")}</time></p>
<p class="muted" style="font-size:1.15rem">{esc(g["desc"])}</p>
{toc}
{content}
{tail_cta}
<div class="lead-box" style="margin-top:40px">
 <span class="eyebrow">Free brand audit</span><h3>Want an expert to apply this to your brand?</h3>
 <p class="muted">Send us your site or socials. We'll reply with your three biggest brand opportunities — free.</p>
 <a class="btn" href="{{pre}}audit.html">Request my free audit</a>
</div>
</article></div></section>
<section class="sec-alt"><div class="wrap"><h2>Keep reading</h2><div class="grid g3">{rel_html}</div></div></section>"""
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": g["title"], "description": g["desc"],
              "author": {"@type": "Organization", "name": "Brand.Life Editorial Team"}, "publisher": {"@type": "Organization", "name": "Brand.Life"},
              "dateModified": TODAY.isoformat(), "mainEntityOfPage": f"{BASE_URL}/guides/{g['slug']}.html"}
        page(f"guides/{g['slug']}.html", g["title"], g["desc"], body, nav_key=("guides/brand-life-cycle.html" if g["slug"] == "brand-life-cycle" else "guides/"), jsonld=ld)


# ------------------------------------------------------------------ AUDIT / LEAD GEN
def build_audit():
    services = ["Brand strategy & positioning", "Name or rename", "Logo & visual identity", "Brand guidelines", "Website that converts",
                "Packaging", "Personal brand", "Rebrand / refresh", "Social media branding", "Not sure — audit everything"]
    svc = "".join(f'<label><input type="checkbox" name="services" value="{esc(s)}"> {esc(s)}</label>' for s in services)
    body = f"""<section class="hero"><div class="wrap hero-grid">
<div>
 {crumbs((None, "Free brand audit"))}
 <span class="eyebrow">Free · 2 minutes · No obligation</span>
 <h1>Find out exactly what's holding your brand back.</h1>
 <p class="lead">A branding specialist reviews your website and social presence and sends back a short, honest audit with your three highest-impact fixes. If you want help implementing them, we'll introduce you to a vetted expert who fits your budget.</p>
 <div class="kpis" style="margin-top:28px">
  <div class="kpi"><b>3</b><small class="muted">prioritized fixes</small></div><div class="kpi"><b>2</b><small class="muted">business days, usually</small></div>
  <div class="kpi"><b>$0</b><small class="muted">cost, always</small></div><div class="kpi"><b>0</b><small class="muted">spam or pressure</small></div>
 </div>
 <h3 style="margin-top:30px">What we review</h3>
 <ul><li><b>Positioning:</b> can a stranger tell what you do, for whom and why you're different within five seconds?</li>
 <li><b>Identity:</b> logo, color, type and imagery — and whether they're consistent across touchpoints.</li>
 <li><b>Message:</b> headline, value proposition, proof and calls to action.</li>
 <li><b>Visibility:</b> how you appear in search, on your Google Business Profile and on social.</li></ul>
</div>
<div class="lead-box" id="audit">
 <form class="form" data-form="Full brand audit request" data-steps data-redirect="{{pre}}thank-you.html">
  <div class="steps-bar"><i></i><i></i><i></i></div>
  {hp()}
  <div class="step">
   <h3>1. What do you need help with?</h3>
   <div class="checks" data-need-one>{svc}</div>
   <button class="btn" type="button" data-next>Continue</button>
  </div>
  <div class="step" hidden>
   <h3>2. About your brand</h3>
   <input name="brand" placeholder="Brand or business name" required aria-label="Brand name">
   <input name="website" placeholder="Website or main social profile" aria-label="Website">
   <select name="stage" required aria-label="Stage"><option value="">Where is your brand today?</option><option>Spark — idea, not launched</option><option>Launch — first customers</option><option>Grow — steady sales, want more presence</option><option>Scale — established, growing team</option><option>Renew — feels dated or off-strategy</option></select>
   <div class="row">
    <select name="budget" aria-label="Budget"><option value="">Budget for help (optional)</option><option>Under $500</option><option>$500 – $2,000</option><option>$2,000 – $10,000</option><option>$10,000 – $50,000</option><option>$50,000+</option><option>Just the free audit for now</option></select>
    <select name="timeline" aria-label="Timeline"><option value="">Timeline (optional)</option><option>ASAP</option><option>Within 1 month</option><option>1–3 months</option><option>Just exploring</option></select>
   </div>
   <textarea name="challenge" rows="3" placeholder="What's your biggest brand challenge right now?" aria-label="Biggest challenge"></textarea>
   <div style="display:flex;gap:10px"><button class="btn alt" type="button" data-prev>Back</button><button class="btn" type="button" data-next>Continue</button></div>
  </div>
  <div class="step" hidden>
   <h3>3. Where should we send your audit?</h3>
   <input name="name" placeholder="Your name" required autocomplete="name" aria-label="Your name">
   <input type="email" name="email" placeholder="Email" required autocomplete="email" aria-label="Email">
   <div class="row"><input name="phone" placeholder="Phone (optional)" autocomplete="tel" aria-label="Phone"><input name="country" placeholder="Country" aria-label="Country"></div>
   <label class="fine"><input type="checkbox" name="expert_intro" value="Yes" style="width:auto" checked> Introduce me to a vetted expert if it would help</label>
   {consent_line()}
   <div style="display:flex;gap:10px"><button class="btn alt" type="button" data-prev>Back</button><button class="btn" type="submit">Get my free audit</button></div>
  </div>
  {status()}
 </form>
</div>
</div></section>
<section class="sec-alt" id="match"><div class="wrap grid g2" style="align-items:start">
 <div>
  <span class="eyebrow">Hire branding talent</span>
  <h2>Get matched with a vetted designer, strategist or agency</h2>
  <p class="muted">Skip the endless portfolio scrolling. Tell us the project and budget; we'll introduce up to three pre-screened professionals who fit — usually within three business days. Free for clients.</p>
  <form class="form card" data-form="Expert match request" data-redirect="{{pre}}thank-you.html">
   {hp()}
   <select name="talent" required aria-label="Who do you need?"><option value="">Who do you need?</option><option>Brand strategist</option><option>Logo / identity designer</option><option>Naming specialist</option><option>Web designer / developer</option><option>Copywriter</option><option>Full-service branding agency</option><option>Personal brand coach</option></select>
   <div class="row"><select name="budget" aria-label="Budget"><option>Under $1,000</option><option>$1,000 – $5,000</option><option>$5,000 – $20,000</option><option>$20,000+</option></select>
   <select name="start" aria-label="Start"><option>Start ASAP</option><option>Within a month</option><option>In 1–3 months</option></select></div>
   <textarea name="project" rows="3" placeholder="Describe the project in a few sentences" required aria-label="Project"></textarea>
   <div class="row"><input name="name" placeholder="Your name" required aria-label="Your name"><input type="email" name="email" placeholder="Email" required aria-label="Email"></div>
   {consent_line()}
   <button class="btn grow" type="submit">Match me with experts</button>
   {status()}
  </form>
 </div>
 <div>
  <span class="eyebrow">For professionals</span>
  <h2>Are you a branding pro? Join the expert network</h2>
  <p class="muted">We send qualified brand projects to independent designers, strategists, copywriters and agencies. Apply once; we'll review your portfolio and get in touch when there's a fit.</p>
  <form class="form card" data-form="Expert network application" data-ok="Thanks — we review applications every week and will be in touch.">
   {hp()}
   <div class="row"><input name="name" placeholder="Name or studio" required aria-label="Name"><input type="email" name="email" placeholder="Email" required aria-label="Email"></div>
   <input name="portfolio" type="url" placeholder="Portfolio URL" required aria-label="Portfolio URL">
   <div class="checks"><label><input type="checkbox" name="skills" value="Strategy"> Strategy</label><label><input type="checkbox" name="skills" value="Identity"> Identity</label><label><input type="checkbox" name="skills" value="Naming"> Naming</label><label><input type="checkbox" name="skills" value="Web"> Web</label><label><input type="checkbox" name="skills" value="Copy"> Copy</label><label><input type="checkbox" name="skills" value="Packaging"> Packaging</label></div>
   <div class="row"><input name="location" placeholder="City / country" aria-label="Location"><select name="min_project" aria-label="Minimum project"><option>Min. project under $1k</option><option>Min. $1k–$5k</option><option>Min. $5k–$20k</option><option>Min. $20k+</option></select></div>
   {consent_line()}
   <button class="btn alt" type="submit">Apply to the network</button>
   {status()}
  </form>
 </div>
</div></section>
<section><div class="wrap narrow"><h2>Audit FAQ</h2>{faq_block([
        ("Is the audit really free?", "Yes. There's no fee and no obligation to hire anyone. We offer it because helpful audits build trust and some people choose to work with an expert from our network afterwards."),
        ("Who reviews my brand?", "A branding specialist from the Brand.Life team or our vetted expert network, depending on your industry and needs."),
        ("How are experts vetted?", "We review portfolios, client references and communication. Experts agree to transparent pricing and to respect client confidentiality."),
        ("Will you share my details?", "Only with the expert(s) you've asked to be introduced to, and only the details needed for your project. We never sell your data. See our privacy policy."),
    ])[0]}</div></section>"""
    page("audit.html", "Free Brand Audit & Branding Expert Matching", "Get a free brand audit with three prioritized fixes, or get matched with vetted brand strategists, designers and agencies.", body, nav_key="audit.html")


# ------------------------------------------------------------------ VIDEOS / NEWS
CHANNELS = [
    ("The Futur", "https://www.youtube.com/@thefutur", "Branding, pricing and creative business lessons from Chris Do and team."),
    ("Satori Graphics", "https://www.youtube.com/@SatoriGraphics", "Logo design process, critiques and branding tutorials."),
    ("Will Paterson", "https://www.youtube.com/@WillPaterson", "Logo design, lettering and freelance design life."),
    ("HubSpot Marketing", "https://www.youtube.com/@HubSpotMarketing", "Inbound marketing, brand building and content strategy."),
    ("TED", "https://www.youtube.com/@TED", "Talks on storytelling, persuasion, design and leadership."),
    ("Google Fonts", "https://www.youtube.com/@googlefonts", "Typography basics and type-design stories."),
]
TOPICS = ["brand strategy explained", "how to design a logo", "brand identity design process", "personal branding tips",
          "brand archetypes explained", "rebranding case study", "how to name a business", "color theory for branding",
          "brand voice and tone", "building a brand on a budget", "brand positioning framework", "typography for beginners"]


def build_videos():
    ch = "".join(f'<a class="card" href="{u}" target="_blank" rel="noopener"><span class="tag hot">Channel</span><h3>{n}</h3><p>{d}</p></a>' for n, u, d in CHANNELS)
    tp = "".join(f'<a class="card" href="https://www.youtube.com/results?search_query={t.replace(" ", "+")}" target="_blank" rel="noopener"><span class="tag">Playlist</span><h3>{t.capitalize()}</h3><p>Opens the latest videos on YouTube</p></a>' for t in TOPICS)
    body = f"""<section><div class="wrap">{crumbs((None, "Videos"))}
<div class="sec-head"><span class="eyebrow">Video library</span><h1>Free branding masterclasses</h1><p class="muted">Hand-picked talks, channels and always-fresh topic playlists. Videos play from YouTube only when you click.</p></div>
<div class="grid g2" style="align-items:start">
 <div><button class="yt" data-yt="qp0HIF3SfI4" aria-label="Play: Simon Sinek — How great leaders inspire action"></button><h3 style="margin-top:14px">Start with why</h3><p class="muted">Simon Sinek's classic talk on why purpose-led brands inspire loyalty — the idea behind Purpose, the first layer in our <a href="{{pre}}guides/what-is-a-brand.html">five-layer brand model</a>.</p></div>
 <div class="card"><h3>How to learn from videos</h3><ol><li>Watch one video per topic, not ten.</li><li>Pause and apply it to your brand using the matching <a href="{{pre}}tools/">free tool</a>.</li><li>Write down one decision you'll make because of it.</li></ol><p><a class="btn small" href="{{pre}}contests.html">Join this month's contest</a></p></div>
</div>
<h2 style="margin-top:48px">Channels worth subscribing to</h2><div class="grid g3">{ch}</div>
<h2 style="margin-top:48px">Topic playlists</h2><div class="grid g4">{tp}</div>
<p class="fine" style="margin-top:24px">Videos and channels belong to their creators. Brand.Life is not affiliated with them. Suggest a video: <a href="{{pre}}contact.html?topic=Suggest%20a%20video">send it to us</a>.</p>
</div></section>"""
    page("videos.html", "Branding Videos & Masterclasses", "Curated free branding videos, YouTube channels and topic playlists on strategy, logo design, naming, personal branding and more.", body, nav_key="videos.html")


SOURCES = [("Branding Strategy Insider", "https://brandingstrategyinsider.com/"), ("The Branding Journal", "https://www.thebrandingjournal.com/"),
           ("Marketing Week", "https://www.marketingweek.com/"), ("Creative Review", "https://www.creativereview.co.uk/"),
           ("Dieline", "https://thedieline.com/"), ("Logo Design Love", "https://www.logodesignlove.com/"),
           ("Adweek", "https://www.adweek.com/"), ("HubSpot Marketing Blog", "https://blog.hubspot.com/marketing")]


def build_news():
    src = "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{n}</a></li>' for n, u in SOURCES)
    body = f"""<section><div class="wrap">{crumbs((None, "News"))}
<div class="grid g2 news-grid" style="align-items:start">
<div>
 <span class="eyebrow">Updated automatically every day</span><h1>Branding news</h1>
 <p class="muted" data-news-updated>The latest headlines from respected branding, design and marketing publications.</p>
 <div data-news="40" data-src="{{pre}}data/news.json"><p class="muted">Loading headlines… The feed refreshes daily. Meanwhile, browse our sources on the right.</p></div>
</div>
<aside class="card"><h3>Our sources</h3><ul>{src}</ul><p class="fine">Headlines link to the original publisher. We show titles only and never copy articles.</p>
<hr style="border:0;border-top:1px solid var(--line)"><h3>Get the weekly digest</h3><p class="muted">The best of the week's branding news, with our take — every Tuesday.</p><a class="btn small" href="#nl-email">Subscribe free</a></aside>
</div></div></section>"""
    page("news.html", "Branding News — Updated Daily", "Daily branding, design and marketing headlines from leading publications, refreshed automatically.", body, nav_key="news.html",
         extra_head="<style>.news-grid{grid-template-columns:2fr 1fr}@media (max-width:860px){.news-grid{grid-template-columns:1fr}}</style>")


# ------------------------------------------------------------------ CONTESTS / SUPPORT / CAREERS / ADVERTISE
def month_name(offset=0):
    m = (TODAY.month - 1 + offset) % 12 + 1
    return datetime.date(2000, m, 1).strftime("%B")


def build_contests():
    body = f"""<section class="hero"><div class="wrap">{crumbs((None, "Contests"))}
<span class="eyebrow">Monthly creative challenges</span><h1>Brand Challenges: create, compete, win.</h1>
<p class="lead muted">Every month we publish a brief for a fictional brand. Submit a name, a tagline or a logo concept. Winners receive cash prizes, a feature on Brand.Life and a portfolio review from a working professional.</p>
<div class="grid g3" style="margin-top:30px">
 <div class="card"><span class="tag hot">Open now · <span data-mo="0">{month_name()}</span></span><h3>Name the Brand</h3><p>Brief: a refillable household-cleaning startup for small apartments. Suggest a name and a one-line reason.</p><p><b>Prize:</b> $150 + feature</p></div>
 <div class="card"><span class="tag hot">Open now · <span data-mo="0">{month_name()}</span></span><h3>Tagline Sprint</h3><p>Brief: a neighborhood bike-repair shop that comes to you. Write a tagline under eight words.</p><p><b>Prize:</b> $100 + feature</p></div>
 <div class="card"><span class="tag">Opens <span data-mo="1">{month_name(1)}</span></span><h3>Logo Concept Challenge</h3><p>Brief: an independent bookshop and café. Submit a logo concept as a link to your file.</p><p><b>Prize:</b> $300 + portfolio review</p></div>
</div></div></section>
<section class="sec-alt"><div class="wrap grid g2" style="align-items:start">
<div class="lead-box">
 <h2>Enter a challenge</h2>
 <form class="form" data-form="Contest entry" data-ok="Entry received! Winners are announced in the first week of next month.">
  {hp()}
  <select name="challenge" required aria-label="Challenge"><option value="">Choose a challenge</option><option data-mo-tpl="Name the Brand — #0">Name the Brand — {month_name()}</option><option data-mo-tpl="Tagline Sprint — #0">Tagline Sprint — {month_name()}</option><option data-mo-tpl="Logo Concept Challenge — #1 (early entry)">Logo Concept Challenge — {month_name(1)} (early entry)</option></select>
  <textarea name="entry" rows="3" placeholder="Your name idea, tagline, or a link to your logo file" required aria-label="Entry"></textarea>
  <textarea name="rationale" rows="2" placeholder="Why it works (one or two sentences)" aria-label="Rationale"></textarea>
  <div class="row"><input name="name" placeholder="Your name" required aria-label="Your name"><input type="email" name="email" placeholder="Email" required aria-label="Email"></div>
  <label class="fine"><input type="checkbox" name="rules" value="Accepted" required style="width:auto"> I'm 18+ and accept the contest rules below. My entry is my own original work.</label>
  <button class="btn" type="submit">Submit my entry</button>
  {status()}
 </form>
</div>
<div>
 <h2>Sponsor a prize</h2>
 <p class="muted">Put your brand in front of thousands of creative founders and designers. Sponsors fund a prize pool, set a brief (with our help), and get logo placement on the challenge, the newsletter and the winner announcement.</p>
 <form class="form card" data-form="Contest sponsorship inquiry" data-ok="Thanks! We'll send the sponsorship kit within two business days.">
  {hp()}
  <div class="row"><input name="company" placeholder="Company" required aria-label="Company"><input name="name" placeholder="Your name" required aria-label="Your name"></div>
  <input type="email" name="email" placeholder="Work email" required aria-label="Email">
  <select name="prize_pool" aria-label="Prize pool"><option>$250 – $500 prize pool</option><option>$500 – $2,000 prize pool</option><option>$2,000+ prize pool</option><option>Product or service prize</option></select>
  <button class="btn grow" type="submit">Request sponsorship kit</button>
  {status()}
 </form>
</div>
</div></section>
<section><div class="wrap narrow"><h2>Official rules (summary)</h2>
<ul>
<li><b>Eligibility:</b> open to individuals aged 18 or over, where permitted by law. Void where prohibited. No purchase or payment necessary to enter or win.</li>
<li><b>Entry period:</b> each challenge runs from the first to the last day of the stated month (23:59 UTC). One entry per person per challenge.</li>
<li><b>Judging:</b> entries are judged by the Brand.Life team and invited professionals on originality (40%), fit to the brief (40%) and clarity of rationale (20%). This is a contest of skill, not chance.</li>
<li><b>Prizes:</b> paid within 30 days of the winner confirming their details, via a payment method agreed with the winner. Winners are responsible for any taxes.</li>
<li><b>Ownership:</b> you keep the rights to your entry. By entering you grant Brand.Life permission to display your entry and name on the site, newsletter and social channels in connection with the contest. If a sponsor wishes to acquire rights to a winning entry, that is agreed separately with the creator.</li>
<li><b>Originality:</b> entries must be your own work and must not infringe anyone's trademarks or copyright. Infringing entries are disqualified.</li>
<li><b>Privacy:</b> entry details are used only to run the contest and contact entrants. See our <a href="{{pre}}privacy.html">privacy policy</a>.</li>
</ul></div></section>"""
    page("contests.html", "Branding Contests & Prizes — Monthly Brand Challenges", "Enter monthly naming, tagline and logo challenges for cash prizes and features, or sponsor a prize to reach creative founders.", body, nav_key="contests.html",
         scripts="<script>(function(){var n=new Date(),m=function(o){return new Date(n.getFullYear(),n.getMonth()+o,1).toLocaleString('en',{month:'long'});};document.querySelectorAll('[data-mo]').forEach(function(e){e.textContent=m(+e.getAttribute('data-mo'));});document.querySelectorAll('[data-mo-tpl]').forEach(function(e){e.textContent=e.getAttribute('data-mo-tpl').replace('#0',m(0)).replace('#1',m(1));});})();</script>")


def build_support():
    body = f"""<section class="hero"><div class="wrap hero-grid">
<div>{crumbs((None, "Support"))}
 <span class="eyebrow">Keep the tools free</span><h1>Support Brand.Life</h1>
 <p class="lead">Brand.Life is free for everyone. Reader support pays for new tools, contest prizes, paid writing and design opportunities for emerging talent, and the marketing that helps more small brands find these resources.</p>
 <h3>Where your support goes</h3>
 <div class="grid g2">
  <div class="card"><h3>40% · New tools</h3><p>Development of new free tools and improvements to existing ones.</p></div>
  <div class="card"><h3>25% · Talent</h3><p>Paying emerging writers, designers and reviewers.</p></div>
  <div class="card"><h3>20% · Prizes</h3><p>Monthly contest prize pools.</p></div>
  <div class="card"><h3>15% · Operations</h3><p>Hosting, research, promotion and outreach.</p></div>
 </div>
</div>
<div class="lead-box">
 <h2>Choose an amount</h2>
 <div class="tiers">
  <button class="tier" type="button" data-amount="5" aria-pressed="false"><b>$5</b>Coffee</button>
  <button class="tier" type="button" data-amount="15" aria-pressed="true"><b>$15</b>Supporter</button>
  <button class="tier" type="button" data-amount="50" aria-pressed="false"><b>$50</b>Prize booster</button>
  <button class="tier" type="button" data-amount="150" aria-pressed="false"><b>$150</b>Patron</button>
 </div>
 <div id="pay-links" style="display:flex;gap:10px;flex-wrap:wrap;margin-top:16px"></div>
 <div id="pledge-mode">
  <p class="muted" style="margin-top:16px">Make a pledge and we'll send you a secure payment link with your thank-you note. You can choose one-time or monthly.</p>
  <form class="form" data-form="Support pledge" data-redirect="{{pre}}thank-you.html">
   {hp()}
   <div class="row"><input id="amount" name="amount" type="number" min="1" value="15" required aria-label="Amount in USD"><select name="frequency" aria-label="Frequency"><option>One-time</option><option>Monthly</option></select></div>
   <div class="row"><input name="name" placeholder="Your name" required aria-label="Your name"><input type="email" name="email" placeholder="Email" required aria-label="Email"></div>
   <select name="direct_to" aria-label="Direct my support to"><option>Wherever it's needed most</option><option>New tools</option><option>Contest prizes</option><option>Paying emerging talent</option></select>
   <label class="fine"><input type="checkbox" name="public_thanks" value="Yes" style="width:auto"> List my name on the supporters wall</label>
   <button class="btn" type="submit">Pledge support</button>
   {status()}
  </form>
 </div>
 <p class="fine">Brand.Life is not a registered charity; support is not tax-deductible. Supporters receive no goods or services in return beyond our thanks.</p>
</div></div></section>
<section class="sec-alt"><div class="wrap grid g3">
 <div class="card"><h3>Sponsor a tool</h3><p>Fund a tool for a year and get a tasteful "made possible by" credit.</p><a class="btn small alt" href="{{pre}}advertise.html">Learn more</a></div>
 <div class="card"><h3>Fund a prize</h3><p>Back a monthly challenge and meet the next generation of brand talent.</p><a class="btn small alt" href="{{pre}}contests.html">See contests</a></div>
 <div class="card"><h3>Spread the word</h3><p>Share a tool with one founder who needs it. It's the most valuable free support there is.</p><a class="btn small alt" href="{{pre}}tools/">Pick a tool</a></div>
</div></section>"""
    page("support.html", "Support Brand.Life — Donate & Sponsor", "Support free brand-building tools, contest prizes and paid opportunities for emerging creative talent.", body, nav_key="support.html")


def build_careers():
    roles = [("Freelance branding writer", "Remote · paid per article", "Write practical, original guides on strategy, naming, identity and growth. Real-world branding experience required."),
             ("Contributing designer", "Remote · paid per project", "Create diagrams, templates and contest briefs. Strong typography and identity portfolio."),
             ("Expert reviewer", "Remote · paid per audit", "Review free brand audits for small businesses. 5+ years in brand strategy or design."),
             ("Community & contest host", "Remote · part-time", "Run monthly challenges, judge entries and grow the community."),
             ("Partnerships & sponsorship lead", "Remote · commission", "Bring on sponsors for tools, contests and the newsletter."),
             ("Campus & creator ambassadors", "Remote · rewards-based", "Share Brand.Life tools with design students and creator communities.")]
    rc = "".join(f'<div class="card"><span class="tag">{w}</span><h3>{t}</h3><p>{d}</p></div>' for t, w, d in roles)
    opts = "".join(f"<option>{t}</option>" for t, _, _ in roles)
    body = f"""<section><div class="wrap">{crumbs((None, "Careers"))}
<div class="sec-head"><span class="eyebrow">Hiring talent</span><h1>Work and write with Brand.Life</h1><p class="muted">We're building the most useful free branding resource on the web — and we pay people who help. All roles are remote and flexible.</p></div>
<div class="grid g3">{rc}</div></div></section>
<section class="sec-alt"><div class="wrap narrow"><div class="lead-box">
<h2>Apply</h2>
<form class="form" data-form="Talent application" data-ok="Application received. We review every application and reply within two weeks.">
 {hp()}
 <select name="role" required aria-label="Role"><option value="">Choose a role</option>{opts}<option>Something else</option></select>
 <div class="row"><input name="name" placeholder="Full name" required aria-label="Full name"><input type="email" name="email" placeholder="Email" required aria-label="Email"></div>
 <div class="row"><input name="portfolio" type="url" placeholder="Portfolio / LinkedIn URL" required aria-label="Portfolio"><input name="location" placeholder="Location / time zone" aria-label="Location"></div>
 <textarea name="why" rows="4" placeholder="What would you bring to Brand.Life? Link one piece of work you're proud of." required aria-label="Why"></textarea>
 {consent_line()}
 <button class="btn" type="submit">Send application</button>
 {status()}
</form></div></div></section>"""
    page("careers.html", "Careers & Paid Opportunities", "Paid remote opportunities for branding writers, designers, expert reviewers, contest hosts and ambassadors.", body, nav_key="careers.html")


def build_advertise():
    packs = [("Newsletter sponsor", "One featured slot in Brand Notes, our weekly email to founders and marketers."),
             ("Tool sponsor", "\"Made possible by\" credit and a relevant offer on one of our free tools, for 3, 6 or 12 months."),
             ("Contest partner", "Fund a monthly challenge, set the brief and receive the winning entries' showcase."),
             ("Sponsored guide", "A clearly labeled, genuinely useful guide on a topic you know well, edited to our standards."),
             ("Expert network listing", "For agencies and studios: priority consideration for qualified project introductions."),
             ("Domain & site partnership", "Interested in this website or the Brand.Life domain itself? Contact the owner via the link at the top of every page.")]
    pc = "".join(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in packs)
    body = f"""<section><div class="wrap">{crumbs((None, "Advertise"))}
<div class="sec-head"><span class="eyebrow">Advertise &amp; partner</span><h1>Reach people actively building brands</h1><p class="muted">Brand.Life visitors are founders, freelancers, creators and marketers in the middle of naming, designing and growing a brand — the moment they're choosing tools and partners.</p></div>
<div class="grid g3">{pc}</div>
<p class="fine" style="margin-top:16px">All sponsored content is clearly labeled. We only partner with products we'd recommend to a friend. Display advertising is served by Google AdSense.</p>
</div></section>
<section class="sec-alt"><div class="wrap narrow"><div class="lead-box">
<h2>Request the media kit</h2>
<form class="form" data-form="Advertising / partnership inquiry" data-ok="Thanks — the media kit is on its way within two business days.">
 {hp()}
 <div class="row"><input name="company" placeholder="Company" required aria-label="Company"><input name="name" placeholder="Your name" required aria-label="Your name"></div>
 <div class="row"><input type="email" name="email" placeholder="Work email" required aria-label="Email"><input name="website" placeholder="Company website" aria-label="Website"></div>
 <select name="topic" aria-label="Interest"><option>Newsletter sponsor</option><option>Tool sponsor</option><option>Contest partner</option><option>Sponsored guide</option><option>Expert network listing</option><option>Sponsorship (general)</option><option>Domain / website acquisition</option></select>
 <select name="budget" aria-label="Budget"><option>Under $500 / month</option><option>$500 – $2,000 / month</option><option>$2,000+ / month</option><option>Not sure yet</option></select>
 <textarea name="goals" rows="3" placeholder="What would a great result look like?" aria-label="Goals"></textarea>
 <button class="btn" type="submit">Send inquiry</button>
 {status()}
</form>
<p class="fine">For website, domain name, sponsorship, advertising or partnership inquiries you can also use the <a href="{OWNER}" target="_blank" rel="noopener">owner contact page</a>.</p>
</div></div></section>"""
    page("advertise.html", "Advertise, Sponsor & Partner", "Sponsor Brand.Life's newsletter, tools or contests, or publish a labeled sponsored guide to reach founders building brands.", body, nav_key="advertise.html")


# ------------------------------------------------------------------ ABOUT / CONTACT / LEGAL
def simple(path, title, desc, inner, key=None):
    body = f'<section><div class="wrap">{crumbs((None, title))}<div class="article">{inner}</div></div></section>'
    page(path, title, desc, body, nav_key=key)


def build_static():
    simple("about.html", "About Brand.Life", "Brand.Life is an independent, free resource that helps founders, creators and small teams build brands that last.", f"""
<span class="eyebrow">About</span><h1>A brand is alive. We help it thrive.</h1>
<p>Brand.Life is an independent, free resource for anyone building a brand: first-time founders, freelancers, creators, nonprofits and small marketing teams. We believe good branding shouldn't require an agency budget — it requires clear decisions, a few good tools and the discipline to be consistent.</p>
<h2>What we do</h2>
<ul><li><b>Free tools</b> that run in your browser and never store what you type.</li><li><b>Practical guides</b> built around the Brand Life Cycle — Spark, Launch, Grow, Scale and Renew.</li><li><b>Free brand audits</b> and introductions to vetted professionals when you need hands-on help.</li><li><b>Monthly challenges</b> that give emerging creative talent a stage and a paycheck.</li></ul>
<h2>Our editorial standards</h2>
<p>Every guide is written for usefulness first. We cite primary sources where we use data, avoid unverifiable claims, label sponsored content clearly and update articles when things change. Advertising and partnerships never influence our recommendations. Spot something wrong? <a href="contact.html?topic=Correction">Tell us</a> and we'll fix it.</p>
<h2>How we're funded</h2>
<p>Brand.Life is supported by display advertising (Google AdSense), clearly labeled sponsorships, optional reader support and introductions to experts in our network. The tools and guides are free and always will be.</p>
<h2>Independence</h2>
<p>Brand.Life is not affiliated with any company that uses "BrandLife", "Brand Life" or similar names. See our <a href="trademark.html">trademark &amp; copyright disclosure</a>.</p>
<p><a class="btn" href="audit.html">Get a free brand audit</a> <a class="btn alt" href="contact.html">Contact us</a></p>""")

    body = f"""<section><div class="wrap grid g2" style="align-items:start">
<div>{crumbs((None, "Contact"))}<span class="eyebrow">Contact</span><h1>Talk to us</h1>
<p class="muted">Questions, corrections, partnership ideas or press — we read everything and reply within two business days.</p>
<div class="grid" style="gap:12px">
 <a class="card" href="audit.html"><h3>Need help with your brand?</h3><p>Request a free brand audit instead — it's faster.</p></a>
 <a class="card" href="advertise.html"><h3>Advertising &amp; sponsorship</h3><p>Media kit and packages.</p></a>
 <a class="card" href="{OWNER}" target="_blank" rel="noopener"><h3>Website, domain or partnership</h3><p>Interested in this website or domain name? Contact the owner.</p></a>
</div></div>
<div class="lead-box"><form class="form" data-form="Contact message" data-ok="Message sent. We'll reply within two business days.">
 {hp()}
 <label for="c-topic">Topic</label>
 <select id="c-topic" name="topic"><option>General question</option><option>Correction</option><option>Suggest a video</option><option>Press</option><option>Partnership</option><option>Sponsorship</option><option>Advertising</option><option>Privacy request</option><option>Something else</option></select>
 <div class="row"><input name="name" placeholder="Your name" required aria-label="Your name"><input type="email" name="email" placeholder="Email" required aria-label="Email"></div>
 <textarea name="message" rows="6" placeholder="Your message" required aria-label="Message"></textarea>
 {consent_line()}
 <button class="btn" type="submit">Send message</button>
 {status()}
</form></div>
</div></section>"""
    page("contact.html", "Contact Brand.Life", "Contact the Brand.Life team with questions, corrections, partnership or press inquiries.", body, nav_key="contact.html")

    upd = TODAY.strftime("%B %d, %Y")
    simple("privacy.html", "Privacy Policy & Cookies", "How Brand.Life collects, uses and protects information, including cookies and Google AdSense advertising.", f"""
<h1>Privacy Policy</h1><p class="byline">Last updated {upd}</p>
<p>This policy explains what information Brand.Life ("we", "us") collects when you use brand.life, how we use it and the choices you have.</p>
<h2>Information you give us</h2>
<p>When you submit a form — such as a brand audit request, newsletter signup, contest entry, application or message — we receive the details you enter (for example your name, email address, website and message). Form submissions are delivered to us by FormSubmit (formsubmit.co), a form-processing service. We use these details only to respond to you, provide what you asked for, run contests, and, if you asked for an introduction, share the relevant project details with the expert(s) you agreed to be introduced to. We do not sell your personal information.</p>
<h2>Tools</h2>
<p>Our tools run in your browser. What you type into a tool is not sent to us unless you choose to submit an accompanying form. Some preferences (such as dark mode, saved name ideas and your cookie choice) are stored in your browser's local storage on your device only.</p>
<h2>Cookies and advertising</h2>
<p>We use Google AdSense to show ads. Third-party vendors, including Google, use cookies to serve ads based on a user's prior visits to this website or other websites. Google's use of advertising cookies enables it and its partners to serve ads to you based on your visit to this site and/or other sites on the internet.</p>
<p>You may opt out of personalized advertising by visiting Google's <a href="https://www.google.com/settings/ads" target="_blank" rel="noopener">Ads Settings</a>. You can also opt out of some third-party vendors' use of cookies for personalized advertising at <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener">aboutads.info</a>. Learn more about <a href="https://policies.google.com/technologies/partner-sites" target="_blank" rel="noopener">how Google uses information from sites that use its services</a>.</p>
<p>When you first visit, our cookie notice lets you choose "Accept all" or "Essential only". If you choose essential only, we request non-personalized ads. Visitors in the European Economic Area, the UK and Switzerland may also see a consent message provided through Google's certified consent tools.</p>
<h2>Other third parties</h2>
<ul><li><b>Google Fonts</b> delivers our typefaces; your browser connects to Google's servers to download them.</li><li><b>YouTube</b> videos load from youtube-nocookie.com only after you click play.</li><li><b>GitHub Pages</b> hosts this website and may log basic technical information such as IP addresses for security.</li></ul>
<h2>Your rights</h2>
<p>Depending on where you live (for example under the GDPR, UK GDPR, CCPA/CPRA or PIPEDA), you may have the right to access, correct, delete or restrict use of your personal information, and to object to certain processing. To make a request, use our <a href="contact.html?topic=Privacy%20request">contact form</a> with the topic "Privacy request".</p>
<h2>Retention and security</h2>
<p>We keep form submissions only as long as needed for the purpose you submitted them for, or as required by law, and take reasonable measures to protect them.</p>
<h2>Children</h2>
<p>Brand.Life is intended for adults. We do not knowingly collect information from children under 13 (or the equivalent minimum age in your country). Contests are open only to people aged 18 or over.</p>
<h2>Changes</h2>
<p>We may update this policy and will change the date above when we do.</p>""")

    simple("terms.html", "Terms of Use", "The terms that apply when you use Brand.Life's website, tools, guides, contests and forms.", f"""
<h1>Terms of Use</h1><p class="byline">Last updated {upd}</p>
<p>By using brand.life you agree to these terms. If you don't agree, please don't use the site.</p>
<h2>Use of the site</h2><p>You may use the site and tools for personal and commercial brand-building purposes. Don't misuse the site: no scraping at scale, interfering with its operation, submitting spam through forms, or using it for anything unlawful.</p>
<h2>Our content</h2><p>Articles, tools, quizzes, frameworks (including the Brand Life Cycle presentation), designs and code on this site are owned by Brand.Life or its licensors and protected by copyright. You may quote short excerpts with attribution and a link. Please don't republish whole articles.</p>
<h2>Your output</h2><p>Names, taglines, palettes, bios and documents you create with our tools are yours to use. We make no claim to them. You are responsible for checking that anything you use — especially names and logos — doesn't infringe someone else's rights.</p>
<h2>No professional advice</h2><p>Content is general information, not legal, trademark, financial or professional advice. See our <a href="disclaimer.html">disclaimer</a>.</p>
<h2>Expert introductions</h2><p>When we introduce you to an independent professional, any agreement is between you and that professional. We are not a party to it and are not responsible for their work, though we take quality feedback seriously.</p>
<h2>Contests</h2><p>Contests are governed by the rules published on the <a href="contests.html">contests page</a>.</p>
<h2>Third-party links and ads</h2><p>We link to other sites and display ads served by Google. We don't control third-party content and aren't responsible for it.</p>
<h2>Liability</h2><p>The site is provided "as is". To the extent permitted by law, Brand.Life is not liable for indirect or consequential losses arising from use of the site.</p>
<h2>Changes</h2><p>We may update these terms; continued use means you accept the updated version.</p>""")

    simple("disclaimer.html", "Disclaimer", "Brand.Life content is for general education and is not legal, trademark or financial advice.", """
<h1>Disclaimer</h1>
<p>The information on Brand.Life is published in good faith for general educational purposes. We work to keep it accurate and current, but we make no warranties about its completeness or reliability.</p>
<h2>Not legal or trademark advice</h2><p>Guidance on naming, domains and trademarks is general. Trademark law differs by country and depends on specific facts. Before adopting or investing in a name or logo, consult a qualified trademark attorney.</p>
<h2>Tool results</h2><p>Scores, quiz results and generated suggestions are heuristics designed to support creative decisions. They are not scientific assessments and don't guarantee commercial outcomes or legal availability.</p>
<h2>Examples</h2><p>Example businesses such as "Northbeam" are fictional and used for illustration. References to real brands are for commentary and education and do not imply endorsement.</p>
<h2>Advertising and affiliate links</h2><p>Brand.Life displays ads through Google AdSense. Some outbound links (for example to domain registrars) may be or become affiliate links, which can earn us a commission at no cost to you. This never affects our recommendations.</p>""")

    simple("trademark.html", "Trademark & Copyright Disclosure", "Brand.Life's trademark and copyright disclosure, independence statement and notice-and-takedown process.", """
<h1>Trademark &amp; Copyright Disclosure</h1>
<h2>Independence</h2>
<p>"Brand.Life" is the name of this independent educational website, operated at the domain brand.life. Brand.Life is <b>not affiliated with, endorsed by, sponsored by or connected to</b> any company, agency, product, platform or service that uses the names "BrandLife", "Brand Life", "Brandlife" or any similar name, logo or mark, in any country. Any similarity is coincidental. We do not use any third party's logo, trade dress or branding.</p>
<h2>Our marks and content</h2>
<p>The Brand.Life name and logo, the site design, and all original articles, tools, quizzes, scoring methods, frameworks, illustrations and code are © Brand.Life. All rights reserved. The "Brand Life Cycle" as presented on this site is our original presentation of widely discussed brand-management ideas; we claim no exclusive rights over the general concept of brand life cycles.</p>
<h2>Third-party marks</h2>
<p>Names of companies, products, publications, YouTube channels and services mentioned on this site (for example in guides, news headlines or video recommendations) are trademarks of their respective owners. They are used only for identification, commentary and education under nominative fair use, and their mention does not imply any affiliation or endorsement.</p>
<h2>Third-party content</h2>
<p>News headlines link to the original publishers; we display titles only. Embedded videos are hosted by YouTube and remain the property of their creators. Fonts are open-licensed via Google Fonts.</p>
<h2>Archetype framework</h2>
<p>The 12 brand archetypes draw on the work of Carl Jung and the marketing framework popularized by Margaret Mark and Carol Pearson. Our quiz questions and descriptions are original.</p>
<h2>Notice and takedown</h2>
<p>If you believe content on Brand.Life infringes your trademark or copyright, please send a notice through our <a href="contact.html?topic=Something%20else">contact form</a> including: your contact details, the work or mark concerned, the URL of the material, a statement of good-faith belief that the use is unauthorized, and a statement that your notice is accurate. We review every notice promptly and remove or correct material where appropriate.</p>""")

    page("thank-you.html", "Thank You", "Thanks for contacting Brand.Life.", """<section class="hero"><div class="wrap narrow" style="text-align:center">
<span class="eyebrow">Received</span><h1>Thank you — it's on its way to us.</h1>
<p class="lead muted" style="margin:0 auto">We reply within two business days. While you wait, try a free tool or read a guide.</p>
<div class="ctas" style="justify-content:center;display:flex;gap:12px;margin-top:24px"><a class="btn" href="tools/">Explore free tools</a><a class="btn alt" href="guides/">Read the guides</a></div>
</div></section>""", noindex=True)

    page("404.html", "Page Not Found", "This page doesn't exist.", """<section class="hero"><div class="wrap narrow" style="text-align:center">
<span class="eyebrow">404</span><h1>This page has reached the end of its life cycle.</h1>
<p class="lead muted" style="margin:0 auto">Let's get you somewhere useful.</p>
<div class="ctas" style="justify-content:center;display:flex;gap:12px;margin-top:24px"><a class="btn" href="index.html">Go home</a><a class="btn alt" href="tools/">Free tools</a></div>
</div></section>""", noindex=True, basetag=BASETAG)


def build_sitemap():
    groups = [("Main", [("index.html", "Home"), ("audit.html", "Free brand audit & expert matching"), ("videos.html", "Videos"), ("news.html", "News"),
                        ("contests.html", "Contests"), ("support.html", "Support"), ("careers.html", "Careers"), ("advertise.html", "Advertise")]),
              ("Free tools", [("tools/index.html", "All tools")] + [(f"tools/{t[0]}.html", t[1]) for t in TOOLS]),
              ("Guides", [("guides/index.html", "All guides")] + [(f"guides/{g['slug']}.html", g["title"]) for g in GUIDES]),
              ("About & legal", [("about.html", "About"), ("contact.html", "Contact"), ("privacy.html", "Privacy"), ("terms.html", "Terms"),
                                 ("disclaimer.html", "Disclaimer"), ("trademark.html", "Trademark & copyright")])]
    inner = "".join(f'<div class="card"><h3>{n}</h3><ul>' + "".join(f'<li><a href="{h}">{esc(l)}</a></li>' for h, l in items) + "</ul></div>" for n, items in groups)
    page("sitemap.html", "Site Map", "Every page on Brand.Life.", f'<section><div class="wrap">{crumbs((None, "Site map"))}<h1>Site map</h1><div class="grid g2">{inner}</div></div></section>')
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in PAGES:
        xml.append(f"  <url><loc>{u}</loc><lastmod>{TODAY.isoformat()}</lastmod></url>")
    xml.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w").write("\n".join(xml) + "\n")


def write_layout():
    nav = "".join(f'<a href="{{{{ page.pre }}}}{h}"{{% if page.nav_key == "{h}" %}} aria-current="page"{{% endif %}}>{l}</a>' for h, l in NAV)
    lay = render("{{ page.full_title | escape }}", "{{ page.description | escape }}", "{{ page.robots }}", "{{ page.canon }}", "{{ page.pre }}",
                 "{{ page.jsonld }}", "{{ page.extra_head }}", None, "{{ content }}", "{{ page.scripts }}", "{{ page.basetag }}", nav=nav)
    os.makedirs(os.path.join(ROOT, "_layouts"), exist_ok=True)
    open(os.path.join(ROOT, "_layouts", "default.html"), "w", encoding="utf-8").write(lay)


if __name__ == "__main__":
    if JEKYLL:
        write_layout()
    build_home(); build_tools(); build_guides(); build_audit(); build_videos(); build_news()
    build_contests(); build_support(); build_careers(); build_advertise(); build_static(); build_sitemap()
    print(f"Built {len(PAGES)} indexable pages.")
