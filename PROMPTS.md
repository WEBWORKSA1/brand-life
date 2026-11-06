# Brand.Life — Phase-wise Build Prompts

Use these prompts in order with an AI coding assistant to rebuild, extend or clone this site. Each phase is self-contained and lists its acceptance checks. The live repo already implements Phases 1–8; Phases 9–10 are the growth roadmap.

---

## Phase 0 — Fixed requirements (paste at the top of every phase)

```
Project: Brand.Life (domain brand.life). Static website hosted free on GitHub Pages (main branch, repo WEBWORKSA1/Brand-Life).
Concept: free brand-building toolkit + guides + free brand audit lead generation, organized around the "Brand Life Cycle"
(Spark → Launch → Grow → Scale → Renew).
Hard rules:
- Plain HTML/CSS/vanilla JS output. A Python generator (_build/build.py) may produce the HTML. No server, no database.
- Every page <head> includes exactly once:
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6620975821265271" crossorigin="anonymous"></script>
  and <meta name="google-adsense-account" content="ca-pub-6620975821265271">. Use Auto ads only — no fake ad slots.
- Top of every page, above the header: "Contact, if you are interested in this website / domain name / Sponsorship /
  Advertisement / Partnership" linking to https://web.works/contact.
- All forms post via fetch to FormSubmit's AJAX endpoint. The destination email is NEVER written in plain text anywhere
  (HTML, JS, README, comments). Store it as two reversed, base64-encoded parts in assets/js/config.js and assemble at runtime.
- Avoid the trademark "BrandLife": use "Brand.Life" only, add a trademark/copyright disclosure page and footer notice.
- AdSense policy: original content only, no copied articles, no misleading buttons near ads, privacy policy with Google
  cookie language, about, contact, terms, disclaimer, ads.txt, sitemap.xml, robots.txt.
- Accessible (labels, contrast ≥ 4.5:1, skip link), responsive (360px → 1440px), dark mode, fast (no frameworks).
```

## Phase 1 — Strategy & research

```
Study at least 35 leading sites across: brand tools (name generators, palette, font pairing, brand kits), brand
assessments/quizzes (lead magnets), branding publications, brand-value research, design-contest marketplaces and
donation platforms. Produce RESEARCH.md with: chosen concept and why, revenue stack ranked by impact, a table of 35
sites with the specific feature each inspired, and a feature checklist.
```
Acceptance: RESEARCH.md exists; every feature in the checklist maps to a page or tool.

## Phase 2 — Design system

```
Create assets/css/style.css: ink #16120F, paper #F7F2EA, spark #FF4F2B, grow #0D6E66, gold #E6A817.
Fonts: Fraunces (display) + Manrope (text) from Google Fonts. Components: owner strip, sticky header with mobile menu,
buttons (primary/alt/grow/small), cards, tags, grids (2/3/4 → 1 col), hero, life-cycle stage switcher, forms
(multi-step with progress bar, pill checkboxes, 5-point scales, honeypot), lead box with offset shadow, tool shell,
swatches, meters, article typography with TOC/tables/blockquotes, lite YouTube button, news list, donation tiers,
FAQ details, footer, cookie consent, print styles. Dark mode via [data-theme] + prefers-color-scheme.
```
Acceptance: renders cleanly at 390px and 1366px; text contrast passes AA.

## Phase 3 — Site generator & shared layout

```
Write _build/build.py that renders every page with one layout: head (meta, canonical, OG, JSON-LD, AdSense), owner strip,
header nav (Free tools, Guides, Life Cycle, Videos, News, Contests, Support + "Free brand audit" button + theme toggle),
main, footer (newsletter form, tool links, get-involved links, legal links, trademark notice), cookie consent, scripts.
Relative paths so the site works on brand.life AND <user>.github.io/Brand-Life/. 404.html uses a runtime <base>.
Also emit sitemap.xml and sitemap.html.
```
Acceptance: `python3 _build/build.py` builds all pages; link checker finds no broken internal links.

## Phase 4 — Ten free tools (assets/js/tools.js)

```
Build in vanilla JS, each initialising only when its container exists:
1 Brand Name Generator (keywords + industry word banks + styles; score each; .com check link; favorites in localStorage)
2 Brand Name Tester (length, rhythm/syllables, spelling/radio test, vowel flow, opening consonant → /100 + notes + USPTO/WIPO links)
3 Tagline Generator (5 tones × templates, copy buttons)
4 Color Palette Generator (HSL harmonies, WCAG contrast table, CSS variables export)
5 Font Pairing Explorer (12 Google Font pairs, live preview, embed code)
6 Brand Archetype Quiz (12 questions → primary + secondary of 12 archetypes)
7 Brand Health Score (20 statements, 5 dimensions, score/band/meters/top-3 actions, gated emailed 90-day plan = lead)
8 Style Guide Builder (live one-page guide, print to PDF)
9 Personal Brand Bio Generator (social/short/medium/speaker with character counts)
10 Positioning Statement Builder (template + quality checks)
Each tool page: intro, tool, audit CTA, related guide, FAQ with FAQPage JSON-LD, WebApplication JSON-LD, 3 related tools.
```
Acceptance: headless browser run of every tool with zero JS errors.

## Phase 5 — Content (AdSense-ready)

```
Write 12 original guides (800–1,200 words each) in _build/guides.py: What is a brand; The Brand Life Cycle; Brand
strategy template; How to name a brand; Brand identity design; Brand voice; Personal branding; Rebranding; 12 brand
archetypes; Color psychology; Small-business branding 30-day plan; Measuring brand health. Each: TOC, tables,
mid-article tool CTA, end audit lead box, Article JSON-LD, related guides. Cite only verifiable facts.
```
Acceptance: no thin pages; every guide links to at least one tool and the audit.

## Phase 6 — Lead generation & monetization pages

```
audit.html: 3-step Free Brand Audit (services → brand/stage/budget/timeline/challenge → contact + expert intro opt-in),
"Get matched with experts" form, "Join the expert network" form, FAQ. Mini lead box on home + tools index.
contests.html: open challenges with prizes, entry form, sponsor-a-prize form, official rules (18+, no purchase, skill-based).
support.html: $5/$15/$50/$150 tiers, payment-link switch from config.js, pledge form, allocation breakdown, not-a-charity note.
careers.html: 6 paid remote roles + application form. advertise.html: 6 packages + media-kit form.
```
Acceptance: every form reaches the relay with a subject line; thank-you redirect works.

## Phase 7 — Automation & media

```
_build/fetch_news.py: pull titles/links/dates from 9 branding RSS feeds into data/news.json (skip failures, never store
article text). Browser fallback: if news.json is empty, fetch 5 feeds live via rss2json and cache 6 hours on the device.
Optional .github/workflows/refresh.yml (daily cron) runs fetch_news.py + build.py and commits. Pages deploys from the
main branch with GitHub's built-in Jekyll (one shared _layouts/default.html). Home shows 6 headlines, news.html shows 40.
Daily brand tip rotates by day of year. videos.html: lite YouTube embeds, curated channels, topic playlists.
```
Acceptance: workflow green; news.json non-empty after first scheduled run.

## Phase 8 — Compliance, QA & launch

```
Pages: about, contact, privacy (Google advertising cookie disclosure + opt-out links + consent), terms, disclaimer,
trademark & copyright (independence from "BrandLife", nominative use, takedown process), 404, thank-you (noindex).
Files: ads.txt (google.com, pub-6620975821265271, DIRECT, f08c47fec0942fa0), robots.txt, sitemap.xml, manifest, _config.yml (no .nojekyll — Jekyll must run).
QA: grep the repo for the contact email (must return nothing), confirm AdSense script count = 1 per page, owner strip on
every page, broken-link check, mobile + desktop screenshots.
```

## Phase 9 — Growth (next)

- Point brand.life DNS to GitHub Pages and add a `CNAME` file; enable "Enforce HTTPS".
- Submit sitemap in Google Search Console; apply for AdSense once the domain is live.
- Add 2 guides per week targeting long-tail queries ("how to trademark a business name", "logo file formats", "brand guidelines template").
- Industry landing pages: "branding for restaurants / dentists / SaaS / coaches" with tailored audit forms.
- Swap the registrar link for an affiliate link; add a vetted "recommended tools" page.

## Phase 10 — Scale

- Paid "Brand Kit Pro" (PDF style guide + templates) via a payment link.
- Expert directory pages with paid featured listings.
- Monthly "Brand Life Report" (survey-based) to earn press and backlinks.
