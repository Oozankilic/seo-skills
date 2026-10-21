---
name: seo-audit
description: Audit a website's SEO and deliver a short, evidence-backed list of the changes most likely to grow useful organic traffic. Use when the user says "SEO audit", "SEO health check", "technical SEO review", "why am I not ranking", "on-page SEO", "check my meta tags", "pre-launch SEO review", "we migrated and traffic dropped", or wants to know what to fix first. Covers both the codebase (templates, config) and the live site (crawl, status codes, Search Console).
---

# SEO Audit

Goal: find the work that would most improve the site's useful organic traffic and explain it so a non-expert can act on it. Research broadly, recommend selectively.

Read the project's `seo-context.md` first (see the `seo` skill). You need to know what the business does, who it serves and which pages make money. If that file is missing, infer it from the site and confirm with one question.

## Priority order

Audit in this order. A failure higher up makes everything below it moot.

1. **Crawlability and indexation**: can search engines reach and index the pages that matter?
2. **Technical foundations**: status codes, redirects, speed, mobile, HTTPS, rendering.
3. **On-page**: titles, descriptions, headings, URLs, internal links, images.
4. **Content quality**: does each important page answer its searcher better than the pages that currently rank?
5. **Authority**: links and mentions.

## Procedure

### 1. Orient (30 minutes of work, not a week)

- Run `scripts/seo_check.py <site> --max-pages 100`. Keep the JSON output as the crawl sample.
- Fetch `robots.txt`, the sitemap(s) and the homepage navigation. List the site's **page families** from the sitemap, not just from the crawl sample: product, pricing, comparison or alternative, tools and templates, guides, categories, services, locations, docs, blog.
- In the codebase, find where `<head>` is generated (layout, metadata config, SEO component, CMS plugin), where the sitemap and robots come from, and how redirects are configured. Note anything generated client-side only.
- If Search Console is available: export queries and pages for the last 3 and 16 months. If a rank tracker (SerpBear) exists, pull its history. If a crawler like SEOnaut has run, read its issue list.
- If the crawl is broken or nearly empty (certificate error, 5xx, one page, everything behind JavaScript), investigate that before anything else. Check redirect and certificate variants (`http`, `https`, `www`, non-`www`). A dead domain with a live successor flips the whole recommendation to "redirect the old domain".

### 2. Investigate every family that matters to the goal

For each family that could bring buyers, read at least two pages' main content: the best performer and a typical or worst one. Ask of each page:

- What decision or question does its searcher have?
- Does the page answer it with specific, accurate, sourced information, or does it swap a name, location or keyword into a shared template?
- Compare against the top results for that query. What do they provide that this page does not?

Check the basics on any page you might name: status code, canonical (the URL the page declares as its preferred version), index directives, how visitors reach it internally, how many clicks from the homepage.

Siblings that perform very differently are a lead. Investigate intent, content specificity, links and authority. A sibling that already ranks near the top is something to protect, not rewrite.

Run the live checks now, not after drafting: search the head term and the variants buyers use, note where the site's page sits and which page it is, with date and country. Request 20 results; a page not seen is "not in the first 20 results". A failed lookup is `unknown`.

### 3. Technical checklist

Work through this list; the checker script covers most of the first two blocks automatically.

**Crawlability**
- `robots.txt` does not block important paths, CSS or JS; references the sitemap.
- Sitemap exists, is reachable, is referenced in robots.txt, contains only canonical, indexable, 200-status URLs, and is current. Large sites: split by page type.
- Important pages within three clicks of the homepage. No orphan pages (in sitemap but no internal links).
- Parameterised URLs, faceted navigation, session IDs, infinite scroll handled (canonical, `noindex`, or robots rules).

**Indexation**
- `site:domain` count versus expected. Search Console coverage report if available.
- No `noindex` on pages that should rank. No `index` on pages that should not (search results, filters, staging, thank-you pages).
- Canonicals: every page has one; self-referencing on unique pages; HTTP to HTTPS; `www` consistency; trailing-slash consistency; no canonical pointing at a redirect or a 404.
- Redirect chains and loops; soft 404s (200 status with "not found" content); duplicate content without canonicals.

**Rendering**
- Primary content and links present in the initial HTML, or server-rendered. Client-only rendering of titles, meta tags or content is a finding.
- `curl -sL <url> | grep -i '<title>'` is the quick test; compare with what the browser shows.

**Speed and Core Web Vitals**
- Largest Contentful Paint under 2.5 s, Interaction to Next Paint under 200 ms, Cumulative Layout Shift under 0.1. Run Lighthouse or PageSpeed Insights on one template per family; field data from Search Console's CWV report if available.
- Usual causes: unoptimised images, render-blocking JS and CSS, slow TTFB, web fonts without `font-display`, layout shift from images without dimensions or injected banners.

**Mobile, security, URLs**
- Responsive, viewport set, tap targets, same content as desktop.
- HTTPS everywhere, valid certificate, no mixed content, HTTP redirects to HTTPS, HSTS is a bonus.
- URLs readable, lowercase, hyphenated, no needless parameters, consistent.

### 4. On-page checklist

- **Titles**: unique per page, primary keyword near the start, about 50 to 60 characters, click-worthy, brand at the end. Findings: duplicates, truncation, missing, stuffed.
- **Descriptions**: unique, about 150 to 160 characters, keyword, value proposition, a reason to click. Findings: duplicates, auto-generated junk, missing.
- **Headings**: one H1 containing the primary topic, logical H1 to H2 to H3 order, headings describe content rather than style it.
- **Content**: keyword and topic clear in the first 100 words; depth sufficient for the query; answers the intent; thin pages (tag archives, empty categories, near-duplicates, doorway pages).
- **Images**: descriptive file names, alt text on every meaningful image, compressed, modern formats, dimensions set, lazy loading below the fold.
- **Internal links**: important pages well linked, descriptive anchors, no broken links, no excessive boilerplate links. Orphans and buried money pages are the typical findings.
- **Keyword targeting**: each important page has one clear target; title, H1 and URL agree; no two pages chasing the same intent (cannibalization; confirm with Search Console query-to-page data when available).
- **Structured data**: present on the page types that qualify (see `seo-schema`), valid, matches visible content.

### 5. Content quality (E-E-A-T)

- **Experience**: first-hand use, original data, real examples.
- **Expertise**: named authors with credentials, accurate detail, sourced claims.
- **Authority**: cited by others, recognised in the space.
- **Trust**: accurate, transparent about the business, contact and policy pages, visible dates, HTTPS.
- Depth: comprehensive for the query, answers follow-ups, current, better than what ranks.

Common patterns by site type:
- **SaaS**: thin feature pages, missing comparison and alternative pages, blog disconnected from product pages, no glossary.
- **E-commerce**: thin categories, duplicate product descriptions, missing Product schema, faceted duplicates, out-of-stock pages that 404.
- **Blogs**: stale posts, cannibalization, no clusters, weak internal linking, no author pages.
- **Local**: inconsistent name/address/phone, no LocalBusiness schema, no location pages, unclaimed Business Profile.

### 6. Shortlist, then choose

Write a working table (not the deliverable) with five to ten serious candidates from at least three kinds of opportunity:

- an existing page underperforming the demand it targets
- real demand with no page that answers it (feature, framework, use-case queries from the product's own claims count)
- a winning page to protect or correct
- an access, indexing or redirect defect costing visits
- helping existing visitors take the next step

Columns: pages | problem observed | evidence (query cluster, volume if known, position and page, date) | proposed change | who searches and why they matter | plausible benefit | effort | main uncertainty.

If one more lookup would change a row's rank (a volume you lack, a sibling you did not check, a query you never ran live), do that lookup before deciding.

Choose one to three. None of these decide on their own: the volume of one query, how easy the fix is, a crawler warning, a hypothetical position-one figure, a redirect repair with no demonstrated loss. Every other row goes to "What else we checked" with a real reason ("demand is a quarter of the leader's and the page already ranks seventh").

### 7. Size the benefit honestly

- Name the mechanism: new ranking, higher position, or more clicks at the current position. A page that already ranks already gets part of the volume.
- Size against the query cluster the change serves; note overlap, do not add variants as if they were different people.
- Search volume is not visits. Use a stated click-share assumption in a labelled scenario table.
- Unknown baseline means "total potential visits", not "additional visits".
- Never invent a conversion rate or revenue. Directional assessments are fine when there is no number.

### 8. Review, then write

Before writing, have a second agent (or a fresh self-review) argue the case for the strongest rejected row, confirm the lead recommendation's evidence is in the draft, check every material diagnosis survived as a recommendation or a table row, and check dates, geography and rank conventions. Fix what it finds.

## Output format

1. **Your next SEO move**: two or three bullets. First action, next action, what is already working.
2. **Recommendations**: one to three, priority order. Each is a heading naming the action and the page or group, then **Do this** (2 to 4 bullets starting with a verb, linking the page), **Why** (observed gap, who searches, plausible benefit, main uncertainty), and a small evidence table (geography and date in the header, positions as "#10 (page 1)" or "not in the first 20 results", "estimated" on volume columns). Optionally a two-row scenario table labelled hypothetical.
3. **What else we checked**: Opportunity | What we found | Decision. One row per shortlist row that did not become a recommendation, runner-up first with the sentence on why the leader beats it, plus one row grouping maintenance items (the checker's warnings that do not change the decision).
4. **How this report was made**: crawl sample size, page families read, live checks with query, country, date, position, what tools reported versus what you verified, limits.

When the fixes are code changes, add a **Implementation plan** section: file paths, what changes, how to verify, rollout risk.

## Guardrails

- Calm, plain tone. Gloss each term of art on first use.
- Observations are not causes. Do not claim a penalty, an indexing exclusion or the reason for a ranking from a warning or a pattern.
- Retrieval date is not observation date. Say when a ranking was observed, or `unknown`.
- Missing backlink or ranking data means "no recorded data", not a problem.
- Difficulty and volume are inputs, not goals.
- Do not recommend rewriting a page that ranks near the top for its target.
- Do not change robots, canonicals, redirects or index directives on production without showing the diff and reasoning first.

See `references/checklist.md` for the condensed one-page checklist to paste into an issue.
