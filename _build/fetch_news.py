#!/usr/bin/env python3
"""Refresh data/news.json from public RSS/Atom feeds. Runs daily in GitHub Actions (see .github/workflows/pages.yml).
Only titles, links, source names and dates are stored — never article text. Failing feeds are skipped."""
import datetime
import email.utils
import json
import os
import re
import urllib.request
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FEEDS = [
    ("Branding Strategy Insider", "https://brandingstrategyinsider.com/feed/"),
    ("The Branding Journal", "https://www.thebrandingjournal.com/feed/"),
    ("Marketing Week", "https://www.marketingweek.com/feed/"),
    ("Creative Review", "https://www.creativereview.co.uk/feed/"),
    ("Dieline", "https://thedieline.com/blog?format=rss"),
    ("Logo Design Love", "https://www.logodesignlove.com/feed"),
    ("Adweek", "https://www.adweek.com/feed/"),
    ("HubSpot Marketing Blog", "https://blog.hubspot.com/marketing/rss.xml"),
    ("Branding News", "https://www.branding.news/feed/"),
]
UA = "Mozilla/5.0 (compatible; BrandLifeNewsBot/1.0; +https://brand.life/news.html)"
PER_FEED = 6


def text(el):
    return re.sub(r"\s+", " ", (el.text or "").strip()) if el is not None else ""


def parse_date(s):
    if not s:
        return None
    try:
        return email.utils.parsedate_to_datetime(s)
    except Exception:
        pass
    try:
        return datetime.datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def fetch(name, url):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = r.read()
    root = ET.fromstring(data)
    out = []
    ns = {"a": "http://www.w3.org/2005/Atom"}
    items = root.findall(".//item")
    if items:
        for it in items[:PER_FEED]:
            out.append((text(it.find("title")), text(it.find("link")), parse_date(text(it.find("pubDate")))))
    else:
        for it in root.findall(".//a:entry", ns)[:PER_FEED]:
            link = it.find("a:link", ns)
            out.append((text(it.find("a:title", ns)), link.get("href") if link is not None else "",
                        parse_date(text(it.find("a:updated", ns)) or text(it.find("a:published", ns)))))
    return [{"title": t, "link": l, "source": name, "_d": d} for t, l, d in out if t and l.startswith("http")]


def main():
    items = []
    for name, url in FEEDS:
        try:
            got = fetch(name, url)
            items.extend(got)
            print(f"ok   {name}: {len(got)}")
        except Exception as e:  # keep going; one bad feed must not break the site
            print(f"skip {name}: {e}")
    epoch = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    for it in items:
        d = it.pop("_d")
        if d and d.tzinfo is None:
            d = d.replace(tzinfo=datetime.timezone.utc)
        it["_s"] = d or epoch
        it["date"] = d.strftime("%b %d, %Y") if d else ""
    items.sort(key=lambda x: x["_s"], reverse=True)
    for it in items:
        it.pop("_s")
    path = os.path.join(ROOT, "data", "news.json")
    if not items and os.path.exists(path):
        print("No items fetched; keeping previous news.json")
        return
    payload = {"updated": datetime.datetime.utcnow().strftime("%b %d, %Y %H:%M UTC"), "items": items[:60]}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=1)
    print(f"wrote {len(payload['items'])} items")


if __name__ == "__main__":
    main()
