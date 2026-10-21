#!/usr/bin/env python3
"""seo_check.py: zero-dependency SEO checker for a live site, one HTML file or a build directory.

Usage:
  python3 seo_check.py https://example.com [--max-pages 50] [--max-links 200] [--json out.json]
  python3 seo_check.py --file path/to/page.html
  python3 seo_check.py --dir dist/ [--base-url https://example.com]

Checks per page: status, title and description (presence, length, duplicates), H1 count, canonical
(presence, mismatch with final URL), robots noindex, viewport, lang, Open Graph and Twitter card, images
without alt, word count (thin pages), http:// links on https pages, JSON-LD (parse errors, types),
hreflang presence, response time.
Site-level (URL mode): robots.txt (status, sitemap line, AI crawler rules), sitemap (status, URL count),
llms.txt presence, redirect chains, broken internal links.

Standard library only. Exit code 2 when errors were found, 1 on warnings only, 0 when clean.
"""

import argparse
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from html.parser import HTMLParser

USER_AGENT = "seo-skills-check/1.0 (+https://github.com/Oozankilic/seo-skills)"
TIMEOUT = 20
AI_CRAWLERS = {
    "oai-searchbot": "ChatGPT search results and citations",
    "chatgpt-user": "ChatGPT on-demand page fetch",
    "gptbot": "OpenAI model training (no effect on live answers)",
    "perplexitybot": "Perplexity index and citations",
    "perplexity-user": "Perplexity on-demand fetch",
    "claudebot": "Claude web index and citations",
    "claude-user": "Claude on-demand fetch",
    "claude-searchbot": "Claude search",
    "anthropic-ai": "Anthropic training (legacy token)",
    "google-extended": "Gemini training (no effect on Search or AI Overviews)",
    "googlebot": "Google Search, AI Overviews, AI Mode",
    "bingbot": "Bing, Copilot and partners",
    "ccbot": "Common Crawl datasets",
    "bytespider": "ByteDance",
}
SKIP_EXT = (".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif", ".svg", ".pdf", ".zip", ".mp4", ".mp3",
            ".css", ".js", ".ico", ".woff", ".woff2", ".ttf", ".xml", ".json", ".txt", ".webmanifest")


# ----------------------------------------------------------------------------- parsing

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = None
        self._in_title = False
        self.metas = []
        self.links = []
        self.headings = Counter()
        self._in_heading = None
        self.h1_texts = []
        self.anchors = []
        self.imgs = []
        self.jsonld = []
        self._in_ld = False
        self._skip = 0
        self.text_parts = []
        self.lang = None

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v if v is not None else "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang")
        elif tag == "title" and self._skip == 0:
            self._in_title = True
            if self.title is None:
                self.title = ""
        elif tag == "meta":
            self.metas.append(a)
        elif tag == "link":
            self.links.append(a)
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.headings[tag] += 1
            self._in_heading = tag
            if tag == "h1":
                self.h1_texts.append("")
        elif tag == "a":
            if a.get("href"):
                self.anchors.append(a)
        elif tag == "img":
            self.imgs.append(a)
        elif tag == "script":
            if (a.get("type") or "").strip().lower() == "application/ld+json":
                self._in_ld = True
                self.jsonld.append("")
            self._skip += 1
        elif tag in ("style", "noscript", "template"):
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._in_heading = None
        elif tag in ("script", "style", "noscript", "template"):
            self._skip = max(0, self._skip - 1)
            if tag == "script":
                self._in_ld = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif self._in_ld:
            self.jsonld[-1] += data
        elif self._skip == 0:
            self.text_parts.append(data)
            if self._in_heading == "h1" and self.h1_texts:
                self.h1_texts[-1] += data

    # convenience accessors
    def meta(self, name=None, prop=None):
        for m in self.metas:
            if name and (m.get("name") or "").lower() == name:
                return (m.get("content") or "").strip()
            if prop and (m.get("property") or "").lower() == prop:
                return (m.get("content") or "").strip()
        return None

    def link_rel(self, rel):
        return [l for l in self.links if rel in (l.get("rel") or "").lower().split()]

    def text(self):
        return re.sub(r"\s+", " ", " ".join(self.text_parts)).strip()


def parse_html(body):
    p = PageParser()
    try:
        p.feed(body)
        p.close()
    except Exception:  # malformed HTML should not crash the run
        pass
    return p


# ----------------------------------------------------------------------------- fetching

class _RedirectRecorder(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        super().__init__()
        self.chain = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        self.chain.append((req.full_url, code, newurl))
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url, method="GET"):
    rec = _RedirectRecorder()
    opener = urllib.request.build_opener(rec)
    req = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*"})
    start = time.time()
    out = {"url": url, "status": None, "final_url": url, "chain": [], "content_type": "", "body": "", "error": None, "elapsed": 0.0}
    try:
        with opener.open(req, timeout=TIMEOUT) as resp:
            out["status"] = resp.status
            out["final_url"] = resp.geturl()
            out["content_type"] = resp.headers.get("Content-Type", "")
            if method == "GET":
                raw = resp.read(5_000_000)
                charset = resp.headers.get_content_charset() or "utf-8"
                out["body"] = raw.decode(charset, errors="replace")
    except urllib.error.HTTPError as e:
        out["status"] = e.code
        out["final_url"] = e.geturl() if hasattr(e, "geturl") else url
    except Exception as e:  # DNS, timeout, SSL
        out["error"] = f"{type(e).__name__}: {e}"
    out["chain"] = rec.chain
    out["elapsed"] = round(time.time() - start, 2)
    return out


def head_status(url):
    r = fetch(url, method="HEAD")
    if r["status"] in (405, 403, 501, None) and r["error"] is None:
        r = fetch(url, method="GET")
    return r


# ----------------------------------------------------------------------------- url helpers

def normalize(url):
    u = urllib.parse.urlsplit(url)
    path = u.path or "/"
    return urllib.parse.urlunsplit((u.scheme.lower(), u.netloc.lower(), path, u.query, ""))


def same_site(a, b):
    ha = urllib.parse.urlsplit(a).netloc.lower().removeprefix("www.")
    hb = urllib.parse.urlsplit(b).netloc.lower().removeprefix("www.")
    return ha == hb


def is_html_candidate(url):
    path = urllib.parse.urlsplit(url).path.lower()
    return not path.endswith(SKIP_EXT)


# ----------------------------------------------------------------------------- page checks

class Report:
    def __init__(self):
        self.pages = {}
        self.site = []  # list of (severity, message)

    def add(self, page, severity, code, message):
        self.pages.setdefault(page, []).append({"severity": severity, "code": code, "message": message})

    def site_issue(self, severity, code, message):
        self.site.append({"severity": severity, "code": code, "message": message})


def check_page(report, page_id, parsed, final_url=None, status=None, elapsed=None, is_https=None):
    add = lambda sev, code, msg: report.add(page_id, sev, code, msg)

    if status is not None and status != 200:
        add("error", "status", f"HTTP {status}")
        if status >= 400:
            return

    title = (parsed.title or "").strip()
    if not title:
        add("error", "title-missing", "no <title>")
    else:
        n = len(title)
        if n < 30:
            add("warn", "title-short", f"title is {n} chars (aim for ~50-60): {title!r}")
        elif n > 65:
            add("warn", "title-long", f"title is {n} chars, likely truncated in SERPs: {title!r}")

    desc = parsed.meta(name="description")
    if not desc:
        add("warn", "description-missing", "no meta description")
    else:
        n = len(desc)
        if n < 70:
            add("info", "description-short", f"description is {n} chars (aim for ~150-160)")
        elif n > 170:
            add("warn", "description-long", f"description is {n} chars, likely truncated (aim for ~150-160)")

    h1 = parsed.headings.get("h1", 0)
    if h1 == 0:
        add("error", "h1-missing", "no <h1>")
    elif h1 > 1:
        add("warn", "h1-multiple", f"{h1} <h1> elements")

    if parsed.headings.get("h3", 0) and not parsed.headings.get("h2", 0):
        add("info", "heading-skip", "h3 used without any h2")

    robots = (parsed.meta(name="robots") or "").lower()
    googlebot = (parsed.meta(name="googlebot") or "").lower()
    if "noindex" in robots or "noindex" in googlebot:
        add("warn", "noindex", "page is noindex (fine if intentional)")

    canon = parsed.link_rel("canonical")
    if not canon:
        add("warn", "canonical-missing", "no rel=canonical")
    else:
        href = (canon[0].get("href") or "").strip()
        if len(canon) > 1:
            add("error", "canonical-multiple", f"{len(canon)} canonical tags")
        if not href:
            add("error", "canonical-empty", "canonical href is empty")
        elif not href.startswith("http"):
            add("warn", "canonical-relative", f"canonical is not absolute: {href}")
        elif final_url and normalize(href).rstrip("/") != normalize(final_url).rstrip("/"):
            add("info", "canonical-mismatch", f"canonical {href} differs from fetched URL {final_url}")

    if not parsed.meta(name="viewport"):
        add("error", "viewport-missing", "no viewport meta (mobile usability)")
    if not parsed.lang:
        add("warn", "lang-missing", "<html> has no lang attribute")

    if not parsed.meta(prop="og:title"):
        add("info", "og-title-missing", "no og:title")
    if not parsed.meta(prop="og:description"):
        add("info", "og-description-missing", "no og:description")
    if not parsed.meta(prop="og:image"):
        add("warn", "og-image-missing", "no og:image (link previews will have no image)")
    if not parsed.meta(name="twitter:card"):
        add("info", "twitter-card-missing", "no twitter:card")

    missing_alt = [i for i in parsed.imgs if "alt" not in i and (i.get("role") or "") != "presentation"]
    if missing_alt:
        srcs = ", ".join((i.get("src") or "?")[:60] for i in missing_alt[:3])
        add("warn", "img-alt-missing", f"{len(missing_alt)} image(s) without alt attribute: {srcs}")

    words = len(parsed.text().split())
    if words < 300:
        add("warn" if words < 100 else "info", "thin-content", f"only {words} words of visible text")

    if is_https:
        http_links = [a["href"] for a in parsed.anchors if a["href"].lower().startswith("http://")]
        if http_links:
            add("info", "http-links", f"{len(http_links)} link(s) to http:// URLs")

    for i, blob in enumerate(parsed.jsonld):
        try:
            data = json.loads(blob.strip() or "null")
        except json.JSONDecodeError as e:
            try:
                data = json.loads(blob.strip(), strict=False)
                add("warn", "jsonld-control-chars", f"JSON-LD block {i + 1} has raw newlines or control characters inside strings; strict validators reject it")
            except json.JSONDecodeError:
                add("error", "jsonld-invalid", f"JSON-LD block {i + 1} does not parse: {e}")
                continue
        types = []
        items = data if isinstance(data, list) else [data]
        for item in items:
            if not isinstance(item, dict):
                continue
            graph = item.get("@graph")
            nodes = graph if isinstance(graph, list) else [item]
            for node in nodes:
                if isinstance(node, dict) and node.get("@type"):
                    t = node["@type"]
                    types.append(",".join(t) if isinstance(t, list) else str(t))
        add("info", "jsonld-types", f"JSON-LD types: {', '.join(types) or 'none'}")

    hreflang = parsed.link_rel("alternate")
    hreflang = [l for l in hreflang if l.get("hreflang")]
    if hreflang:
        langs = [l.get("hreflang") for l in hreflang]
        if "x-default" not in langs:
            add("info", "hreflang-no-default", f"hreflang present ({len(langs)}) but no x-default")

    if elapsed is not None and elapsed > 2.5:
        add("warn", "slow-response", f"response took {elapsed}s (server time, not full page load)")


# ----------------------------------------------------------------------------- site-level checks

def check_robots(report, base):
    r = fetch(urllib.parse.urljoin(base, "/robots.txt"))
    info = {"status": r["status"], "sitemaps": [], "blocked_ai": {}, "blocks_all": False}
    if r["error"] or r["status"] != 200:
        report.site_issue("warn", "robots-missing", f"robots.txt not reachable (status {r['status']}, {r['error'] or ''})".strip())
        return info
    if "text/plain" not in r["content_type"].lower() and "<html" in r["body"][:500].lower():
        report.site_issue("error", "robots-html", "robots.txt returns HTML, crawlers will ignore it")
    # A group is one or more consecutive User-agent lines followed by rules; rules apply to every agent in the group.
    groups = defaultdict(list)  # agent -> list of (directive, value)
    current, in_rules = [], False
    for raw in r["body"].splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip().lower(), val.strip()
        if key == "user-agent":
            if in_rules:
                current, in_rules = [], False
            current.append(val.lower())
            groups.setdefault(val.lower(), [])
        elif key == "sitemap":
            info["sitemaps"].append(val)
        elif key in ("disallow", "allow") and current:
            in_rules = True
            for ua in current:
                groups[ua].append((key, val))
    star = groups.get("*", [])
    if ("disallow", "/") in star and not any(d[0] == "allow" for d in star):
        info["blocks_all"] = True
        report.site_issue("error", "robots-blocks-all", "robots.txt disallows / for all user agents")
    for ua, what in AI_CRAWLERS.items():
        if ("disallow", "/") in groups.get(ua, []):
            info["blocked_ai"][ua] = what
    if info["blocked_ai"]:
        names = ", ".join(f"{k} ({v})" for k, v in info["blocked_ai"].items())
        report.site_issue("info", "robots-ai-blocked", f"robots.txt fully blocks: {names}")
    if not info["sitemaps"]:
        report.site_issue("info", "robots-no-sitemap", "robots.txt has no Sitemap: line")
    return info


def check_sitemap(report, base, candidates):
    urls = candidates or [urllib.parse.urljoin(base, "/sitemap.xml"), urllib.parse.urljoin(base, "/sitemap_index.xml")]
    found = None
    for u in urls:
        r = fetch(u)
        if r["status"] == 200 and r["body"].lstrip().startswith("<"):
            found = (u, r["body"])
            break
    if not found:
        report.site_issue("warn", "sitemap-missing", f"no sitemap found at {', '.join(urls)}")
        return {"url": None, "count": 0}
    u, body = found
    locs = re.findall(r"<loc>\s*(.*?)\s*</loc>", body, flags=re.I | re.S)
    locs = [html.unescape(l.strip()) for l in locs]
    is_index = "<sitemapindex" in body[:2000].lower()
    kind = "sitemap index with %d child sitemaps" % len(locs) if is_index else "sitemap with %d URLs" % len(locs)
    report.site_issue("info", "sitemap-found", f"{u}: {kind}")
    if not is_index:
        off_host = [l for l in locs if l.startswith("http") and not same_site(l, base)]
        if off_host:
            report.site_issue("warn", "sitemap-foreign-urls", f"{len(off_host)} sitemap URL(s) on another host, e.g. {off_host[0]}")
        http_urls = [l for l in locs if l.startswith("http://")] if base.startswith("https://") else []
        if http_urls:
            report.site_issue("warn", "sitemap-http-urls", f"{len(http_urls)} sitemap URL(s) use http:// on an https site")
    return {"url": u, "count": len(locs), "index": is_index, "locs": locs}


def check_llms_txt(report, base):
    r = head_status(urllib.parse.urljoin(base, "/llms.txt"))
    if r["status"] == 200:
        report.site_issue("info", "llms-txt", "llms.txt present")
    else:
        report.site_issue("info", "llms-txt-missing", "no llms.txt (optional; see seo-ai-visibility)")


# ----------------------------------------------------------------------------- crawl

def crawl(start, max_pages, max_links, report):
    start = normalize(start)
    base = f"{urllib.parse.urlsplit(start).scheme}://{urllib.parse.urlsplit(start).netloc}/"
    is_https = start.startswith("https://")
    if not is_https:
        report.site_issue("warn", "not-https", "start URL is http://; the site should be served over https")

    queue = [start]
    seen = {start}
    crawled = {}
    discovered = Counter()
    titles, descs = defaultdict(list), defaultdict(list)

    while queue and len(crawled) < max_pages:
        url = queue.pop(0)
        r = fetch(url)
        page_id = url
        if r["error"]:
            report.add(page_id, "error", "fetch-error", r["error"])
            crawled[url] = r
            continue
        if len(r["chain"]) > 1:
            path = " -> ".join([r["chain"][0][0]] + [c[2] for c in r["chain"]])
            report.add(page_id, "warn", "redirect-chain", f"{len(r['chain'])} redirects: {path}")
        elif len(r["chain"]) == 1 and url == start:
            report.site_issue("info", "start-redirect", f"start URL redirects ({r['chain'][0][1]}) to {r['final_url']}")
        crawled[url] = r
        if r["final_url"] != url and normalize(r["final_url"]) in crawled and normalize(r["final_url"]) != url:
            continue  # duplicate of an already crawled page
        ct = r["content_type"].lower()
        if "html" not in ct:
            if r["status"] == 200:
                report.add(page_id, "info", "not-html", f"content-type {ct or 'unknown'}, skipped")
            else:
                report.add(page_id, "error", "status", f"HTTP {r['status']}")
            continue
        parsed = parse_html(r["body"])
        check_page(report, page_id, parsed, final_url=r["final_url"], status=r["status"], elapsed=r["elapsed"], is_https=is_https)
        if r["status"] != 200:
            continue
        t = (parsed.title or "").strip()
        d = parsed.meta(name="description") or ""
        if t:
            titles[t].append(page_id)
        if d:
            descs[d].append(page_id)
        noindex = "noindex" in (parsed.meta(name="robots") or "").lower()
        for a in parsed.anchors:
            href = a["href"].strip()
            if href.startswith(("#", "mailto:", "tel:", "javascript:", "data:")):
                continue
            rel = (a.get("rel") or "").lower()
            absu = urllib.parse.urljoin(r["final_url"], href)
            absu = normalize(absu)
            if not absu.startswith(("http://", "https://")):
                continue
            if not same_site(absu, base):
                continue
            discovered[absu] += 1
            if absu in seen or not is_html_candidate(absu) or "nofollow" in rel:
                continue
            if urllib.parse.urlsplit(absu).netloc.lower() != urllib.parse.urlsplit(base).netloc.lower():
                continue  # www vs non-www: check as link only
            seen.add(absu)
            queue.append(absu)

    for t, pages in titles.items():
        if len(pages) > 1:
            report.site_issue("warn", "duplicate-title", f"{len(pages)} pages share the title {t[:70]!r}: " + ", ".join(pages[:4]))
    for d, pages in descs.items():
        if len(pages) > 1:
            report.site_issue("warn", "duplicate-description", f"{len(pages)} pages share a meta description: " + ", ".join(pages[:4]))

    # broken internal links: check discovered URLs not crawled
    remaining = [u for u in discovered if u not in crawled][:max_links]
    broken = []
    for u in remaining:
        r = head_status(u)
        if r["error"] or (r["status"] and r["status"] >= 400):
            broken.append((u, r["status"] or r["error"], discovered[u]))
        elif len(r["chain"]) > 1:
            report.site_issue("info", "redirect-chain-link", f"{u} goes through {len(r['chain'])} redirects")
    for u, st, n in broken:
        report.site_issue("error", "broken-link", f"{u} returns {st} (linked from {n} place(s))")
    for u, r in crawled.items():
        if r["status"] and r["status"] >= 400:
            report.site_issue("error", "broken-link", f"{u} returns {r['status']} (linked from {discovered.get(u, 0)} place(s))")

    return {"base": base, "crawled": len(crawled), "discovered": len(discovered), "link_checked": len(remaining), "queued_unchecked": max(0, len(discovered) - len(crawled) - len(remaining))}


# ----------------------------------------------------------------------------- local modes

def check_file(report, path, base_url=None):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        body = f.read()
    parsed = parse_html(body)
    check_page(report, path, parsed, final_url=None, status=None, elapsed=None, is_https=(base_url or "").startswith("https://"))
    return parsed


def check_dir(report, root, base_url=None):
    titles, descs = defaultdict(list), defaultdict(list)
    count = 0
    for dirpath, _, files in os.walk(root):
        for fn in sorted(files):
            if not fn.lower().endswith((".html", ".htm")):
                continue
            path = os.path.join(dirpath, fn)
            parsed = check_file(report, path, base_url)
            count += 1
            t = (parsed.title or "").strip()
            d = parsed.meta(name="description") or ""
            if t:
                titles[t].append(path)
            if d:
                descs[d].append(path)
    for t, pages in titles.items():
        if len(pages) > 1:
            report.site_issue("warn", "duplicate-title", f"{len(pages)} files share the title {t[:70]!r}: " + ", ".join(pages[:4]))
    for d, pages in descs.items():
        if len(pages) > 1:
            report.site_issue("warn", "duplicate-description", f"{len(pages)} files share a meta description: " + ", ".join(pages[:4]))
    for name in ("robots.txt", "sitemap.xml", "llms.txt"):
        p = os.path.join(root, name)
        report.site_issue("info", name.replace(".", "-"), f"{name} {'present' if os.path.exists(p) else 'not found'} in build root")
    return count


# ----------------------------------------------------------------------------- output

ORDER = {"error": 0, "warn": 1, "info": 2}


def print_report(report, summary):
    def line(issue):
        return f"  [{issue['severity'].upper():5}] {issue['code']}: {issue['message']}"

    print("=" * 78)
    print("SEO CHECK")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    print("=" * 78)
    if report.site:
        print("\nSITE")
        for i in sorted(report.site, key=lambda x: ORDER[x["severity"]]):
            print(line(i))
    counts = Counter()
    for page, issues in report.pages.items():
        for i in issues:
            counts[i["severity"]] += 1
    for i in report.site:
        counts[i["severity"]] += 1
    print("\nPAGES")
    for page, issues in report.pages.items():
        real = [i for i in issues if i["severity"] != "info" or i["code"] == "jsonld-types"]
        if not real:
            print(f"\n{page}\n  ok")
            continue
        print(f"\n{page}")
        for i in sorted(issues, key=lambda x: ORDER[x["severity"]]):
            print(line(i))
    print("\n" + "-" * 78)
    print(f"errors: {counts['error']}  warnings: {counts['warn']}  info: {counts['info']}")
    return counts


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("url", nargs="?", help="start URL to crawl")
    ap.add_argument("--file", help="check a single HTML file")
    ap.add_argument("--dir", help="check every .html file under a directory (static build output)")
    ap.add_argument("--base-url", help="site URL for --dir/--file mode (enables https checks)")
    ap.add_argument("--max-pages", type=int, default=50, help="pages to crawl (default 50)")
    ap.add_argument("--max-links", type=int, default=200, help="additional internal links to status-check (default 200)")
    ap.add_argument("--json", metavar="PATH", help="write the full report as JSON")
    ap.add_argument("--quiet", action="store_true", help="only print the summary line")
    args = ap.parse_args()

    report = Report()
    if args.file:
        check_file(report, args.file, args.base_url)
        summary = {"mode": "file", "file": args.file}
    elif args.dir:
        n = check_dir(report, args.dir, args.base_url)
        summary = {"mode": "dir", "dir": args.dir, "files": n}
    elif args.url:
        url = args.url if args.url.startswith("http") else "https://" + args.url
        site = crawl(url, args.max_pages, args.max_links, report)
        robots = check_robots(report, site["base"])
        check_sitemap(report, site["base"], robots.get("sitemaps"))
        check_llms_txt(report, site["base"])
        summary = {"mode": "crawl", "start": url, "pages crawled": site["crawled"], "internal URLs discovered": site["discovered"],
                   "extra links status-checked": site["link_checked"], "links not checked (raise --max-links)": site["queued_unchecked"]}
    else:
        ap.print_help()
        return 0

    if args.quiet:
        counts = Counter(i["severity"] for i in report.site)
        for issues in report.pages.values():
            counts.update(i["severity"] for i in issues)
        print(f"errors: {counts['error']}  warnings: {counts['warn']}  info: {counts['info']}")
    else:
        counts = print_report(report, summary)

    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump({"summary": summary, "site": report.site, "pages": report.pages}, f, indent=2)
        print(f"json written to {args.json}")

    if counts["error"]:
        return 2
    if counts["warn"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
