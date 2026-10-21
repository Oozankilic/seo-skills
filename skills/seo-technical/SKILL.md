---
name: seo-technical
description: Implement or fix the technical SEO foundations of a web project in code. Use when the user wants to add or fix title and meta tags, canonical URLs, robots.txt, XML sitemaps, redirects, Open Graph and Twitter cards, hreflang, pagination, Core Web Vitals, server-side rendering for SEO, or asks "set up SEO for this Next.js / Astro / Nuxt / SvelteKit / Remix / WordPress / static site". For diagnosing what is wrong, see seo-audit. For JSON-LD, see seo-schema.
---

# Technical SEO

You are implementing, not advising. Find where the project generates `<head>`, sitemaps, robots and redirects, make the change there, and verify it with `curl` and `scripts/seo_check.py`.

## The head of every indexable page

```html
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Primary Keyword: Benefit | Brand</title>                       <!-- ~50-60 chars, unique -->
  <meta name="description" content="...">                                <!-- ~150-160 chars, unique -->
  <link rel="canonical" href="https://example.com/path/">                <!-- absolute, final URL -->
  <meta name="robots" content="index, follow, max-image-preview:large">  <!-- omit or noindex deliberately -->
  <meta property="og:type" content="article">                            <!-- or website / product -->
  <meta property="og:title" content="...">
  <meta property="og:description" content="...">
  <meta property="og:image" content="https://example.com/og/path.png">   <!-- 1200x630, absolute -->
  <meta property="og:url" content="https://example.com/path/">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="alternate" hreflang="en" href="https://example.com/path/">  <!-- multilingual only -->
  <link rel="alternate" hreflang="x-default" href="https://example.com/path/">
  <script type="application/ld+json">{ ... }</script>                    <!-- see seo-schema -->
</head>
```

Rules that matter more than the tags:

- **Unique title and description per URL.** Templated pages must interpolate something meaningful, not just a name.
- **Canonical is absolute and points at the version you want indexed**: same scheme, host and trailing-slash policy as the sitemap and internal links. Never canonicalise to a redirect or 404. Paginated pages canonicalise to themselves, not to page 1.
- **`noindex` goes on**: internal search results, filter and sort variants, tag archives with no value, thank-you and account pages, staging. Never on pages in the sitemap.
- **Everything above must be in the server response**, not injected by client JavaScript after load. Verify with `curl -s URL | head -c 4000`.
- **`lang`** on `<html>`; hreflang only when the alternate actually exists, reciprocal across all variants, with `x-default`.

## robots.txt

```
User-agent: *
Disallow: /api/
Disallow: /admin/
Disallow: /search
Disallow: /*?sort=
Allow: /

Sitemap: https://example.com/sitemap.xml
```

- Never block CSS, JS or image paths needed to render pages.
- Do not use robots.txt to keep a page out of the index; blocked pages can still be indexed from links. Use `noindex` on the page (and let it be crawled) instead.
- AI crawlers: decide deliberately. `OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot`, `ClaudeBot` feed live answers and citations; `GPTBot`, `Google-Extended`, `anthropic-ai`, `CCBot` are about training. Blocking the first group removes the site from AI answers. See `seo-ai-visibility`.
- Serve `robots.txt` with 200 and `text/plain`. A 5xx on robots.txt can stop crawling entirely.

## XML sitemap

- Include only canonical, indexable, 200-status URLs. No redirects, no `noindex`, no parameters, no duplicates with different trailing slashes.
- `lastmod` only if it is real (content change date), otherwise omit it. Skip `priority` and `changefreq`; Google ignores them.
- Over 50,000 URLs or 50 MB: split by page type into a sitemap index. Separate sitemaps per family also make Search Console coverage readable.
- Generate from the data source (routes, CMS, database), not by crawling your own site.
- Reference from robots.txt and submit in Search Console. Resubmit after a migration.
- Image and video sitemaps only when those assets matter for search.

## Status codes and redirects

- One canonical host and scheme. Everything else 301s to it in one hop: `http://` to `https://`, `www` to apex (or the reverse), trailing-slash variants, uppercase paths.
- Moved content: 301 (permanent). Temporary: 302 or 307. Removed with no replacement: 404 or 410, not a redirect to the homepage.
- No chains: update old redirects to point at the final URL. Check with `curl -sIL URL | grep -iE '^(HTTP|location)'`.
- Migrations: map every old URL to its closest new equivalent before launch; keep the map for at least a year; keep old sitemaps live briefly so crawlers pick up the redirects.
- Soft 404s (200 with "not found" copy) must become real 404s.

## Rendering

- Prefer server-side rendering or static generation for any page you want indexed. Client-side-only apps need SSR, prerendering, or at least server-rendered head tags and content.
- Content loaded on scroll or on click is not reliably indexed. Core content must be in the HTML.
- Links must be `<a href>`, not click handlers. Pagination needs real URLs (`?page=2` or `/page/2/`), each self-canonical, with the next page linked.
- Check for hydration-only content, delayed meta updates, and `<head>` tags added by a router after navigation (fine for users, but verify the first server response).

## Core Web Vitals

Targets at the 75th percentile: LCP under 2.5 s, INP under 200 ms, CLS under 0.1. Measure with Lighthouse (lab) and Search Console or CrUX (field).

Fixes by metric:
- **LCP**: preload the hero image or font, serve images in AVIF/WebP at the displayed size, inline critical CSS, cut TTFB (cache, CDN, edge), avoid lazy-loading the LCP element.
- **INP**: break long tasks, defer non-critical JS, reduce third-party scripts, avoid heavy work in input handlers.
- **CLS**: set `width` and `height` (or `aspect-ratio`) on images and embeds, reserve space for ads and banners, use `font-display: optional` or `swap` with matched fallbacks, avoid inserting content above existing content.

Add a Lighthouse CI budget in CI so regressions fail the build (recipe in `seo-tooling`).

## Images

- Descriptive file names and alt text (what the image shows, keyword only when natural, under about 125 characters).
- Responsive `srcset`, modern formats, compression, explicit dimensions, lazy-load below the fold, eager-load the LCP image.
- Open Graph image: 1200x630, absolute URL, generated per page where titles vary.

## URLs and site structure

- Lowercase, hyphens, short, descriptive, keyword included when natural. Subfolders, not subdomains, for content that should share authority (`site.com/blog/`, not `blog.site.com`).
- Hub and spoke: category or pillar pages link to their children, children link back and to siblings. Important pages within three clicks of the homepage.
- Breadcrumbs with `BreadcrumbList` schema on deep pages.

## Internationalisation

- One URL per language and region variant (`/de/`, `/en-gb/` or separate domains). Not cookies, not `Accept-Language` alone.
- Reciprocal hreflang across all variants plus `x-default`. Generate from the same route table as the sitemap. hreflang can also live in the sitemap.
- Translate titles, descriptions and slugs; do not canonicalise translations to the source language.

## Indexing faster

- Submit the sitemap in Search Console and Bing Webmaster Tools.
- IndexNow (Bing, Yandex, others) accepts URL pings; implement on publish and update.
- Google's Indexing API is only for `JobPosting` and `BroadcastEvent` pages; scripts that use it for other content violate the terms.
- Internal links from already-indexed, frequently crawled pages (homepage, hub pages) are the reliable way to get new pages crawled.

## Framework recipes

See `references/framework-recipes.md` for Next.js (App and Pages router), Astro, Nuxt, SvelteKit, Remix, WordPress, Jekyll/Hugo and plain HTML: where metadata lives, how to generate sitemaps and robots, how to emit JSON-LD, and which packages to use.

## Verification

```bash
# head tags as the crawler sees them
curl -s https://example.com/path/ | grep -iE '<title>|name="description"|rel="canonical"|name="robots"|og:image'
# redirect chain
curl -sIL http://example.com/path | grep -iE '^(HTTP|location)'
# robots and sitemap
curl -s https://example.com/robots.txt; curl -s https://example.com/sitemap.xml | head -40
# full crawl report
python3 scripts/seo_check.py https://example.com --max-pages 100
```

Then: Rich Results Test for schema, PageSpeed Insights for CWV, Search Console URL Inspection for indexability of one page per family.

## Guardrails

- Show the diff before changing robots.txt, canonicals, redirects or index directives on production.
- Do not add `noindex` and keep the page in the sitemap; do not block in robots.txt and expect de-indexing.
- Do not canonicalise paginated or translated pages to a single page.
- Do not generate a sitemap by crawling the site; derive it from the source of truth.
