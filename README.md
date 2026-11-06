# Brand.Life

Free brand-building tools, guides and expert audits — organized around the **Brand Life Cycle** (Spark → Launch → Grow → Scale → Renew).
Static site, hosted free on GitHub Pages.

## What's inside

| Area | Files |
|---|---|
| 10 free tools | `tools/*.html`, logic in `assets/js/tools.js` |
| 12 guides | `guides/*.html`, source in `_build/guides.py` |
| Lead generation | `audit.html` (3-step audit, expert matching, expert network), lead boxes site-wide, Brand Health Score plan |
| Monetization | Google AdSense auto ads on every page, `advertise.html`, `support.html`, `contests.html` (sponsors) |
| Self-updating | `data/news.json` refreshed daily by `.github/workflows/pages.yml`; daily rotating tip |
| Compliance | privacy, terms, disclaimer, trademark, about, contact, `ads.txt`, `sitemap.xml`, `robots.txt` |
| Docs | `RESEARCH.md` (concept + 35-site study), `PROMPTS.md` (phase-wise build prompts) |

## Editing

1. Edit `_build/build.py` (pages) or `_build/guides.py` (articles).
2. Run `pip install markdown && python3 _build/build.py`.
3. Commit and push to `main`. The workflow rebuilds and publishes automatically.

## Settings you can change without code

`assets/js/config.js`:
- `payments` — paste PayPal / Stripe / Buy Me a Coffee links to turn on instant checkout on the Support page.
- `_k` — encoded form relay key. Keep it encoded; never put a plain address in the site.

## Hosting

GitHub Pages (free plan), **Deploy from a branch → `main` / `(root)`**. GitHub's built-in Jekyll wraps every page in
`_layouts/default.html` (shared head, AdSense code, owner banner, header, footer), so each page file holds only its own content.

- Turn it on once: **Settings → Pages → Build and deployment → Source: Deploy from a branch → main → / (root) → Save**.
- Custom domain: add a `CNAME` file containing `brand.life`, point DNS to GitHub Pages, then enable *Enforce HTTPS*.
- News updates itself in the browser (live RSS, cached 6 hours per visitor). For a server-side daily refresh, paste
  `_build/github-actions-workflow.yml` into `.github/workflows/refresh.yml` via the GitHub web editor.

## Forms

Forms post to FormSubmit. The very first submission triggers a one-time activation email from FormSubmit to the site owner's inbox; click the link once and all forms go live.

## Trademark

"Brand.Life" is an independent website, not affiliated with any company using "BrandLife" or similar marks. See `trademark.html`.
