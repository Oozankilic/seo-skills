---
name: seo-tooling
description: Choose, set up and run free open-source SEO tools instead of paid SaaS. Use when the user asks which SEO tools to use, wants a site crawler or audit tool, a rank tracker, Lighthouse CI, broken link checking, log analysis, keyword data, a Semrush or Ahrefs alternative, or mentions SEOnaut, SerpBear, OpenSEO, SEOMachine, Lighthouse, linkinator, GoAccess, Plausible, Matomo or DataForSEO. Includes Docker recipes.
---

# Open-source SEO tooling

Most SEO tools are not complicated. What costs money is data (search volume, backlink indexes) and continuous monitoring. Open source covers the execution layer well: crawling and audits, rank tracking, analytics, log analysis, CI checks. For competitive keyword and backlink data, bring a pay-as-you-go API (DataForSEO) or keep one read-only paid account.

## Start here: the bundled checker

`scripts/seo_check.py` (standard library only) audits a live site, a single HTML file or a build directory:

```bash
python3 scripts/seo_check.py https://example.com --max-pages 100 --json report.json
python3 scripts/seo_check.py --dir dist/
python3 scripts/seo_check.py --file out/index.html
```

It reports: missing or long titles and descriptions, duplicates across pages, H1 problems, canonical presence and mismatch, noindex, viewport and lang, Open Graph gaps, images without alt, thin pages, http links on https pages, broken internal links, redirect chains, invalid JSON-LD, robots.txt and sitemap status, `llms.txt` presence, and which AI crawlers robots.txt blocks. Use it for the baseline and for verification after changes; add `--dir` to CI on static builds.

## The stack

| Need | Tool | Notes |
|------|------|-------|
| Site crawl and audit with a UI | [SEOnaut](https://github.com/StJudeWasHere/seonaut) | Go + MySQL, Docker. Broken links, redirect issues, duplicate or missing meta, heading order, severity-ranked. Hosted at seonaut.org. Recipe: `docker/seonaut.compose.yml`. |
| Desktop crawler (Screaming Frog alternative) | [LibreCrawl](https://github.com/PhialsBasement/LibreCrawl) | Free desktop crawler. |
| Script-driven crawl | [python-seo-analyzer](https://github.com/sethblack/python-seo-analyzer), [advertools](https://github.com/eliasdabbas/advertools) | Python; advertools also parses sitemaps, robots and SERPs. |
| Broken links | [linkinator](https://github.com/JustinBeckwith/linkinator) | `npx linkinator https://example.com --recurse` |
| Performance, SEO and best-practice audits | [Lighthouse](https://github.com/GoogleChrome/lighthouse) | `npx lighthouse URL --output=json --only-categories=seo,performance` |
| CI budgets | [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci) | Fails the build on regressions. Config below. |
| Rank tracking | [SerpBear](https://github.com/towfiqi/serpbear) | Next.js + SQLite, Docker. Unlimited domains and keywords; Search Console and Google Ads integration; email, Slack and Telegram alerts; needs a SERP scraping provider or proxies. Recipe: `docker/serpbear.compose.yml`. |
| All-in-one (keyword research, rank tracking, audits, backlinks, AI visibility) | [OpenSEO](https://github.com/every-app/open-seo) | Bring a DataForSEO key, pay per request. MCP server plus agent skills (`npx skills add every-app/open-seo`). Self-host on Docker or Cloudflare, or hosted at openseo.so. |
| Content production workspace | [SEOMachine](https://github.com/TheCraigHewitt/seomachine) | Claude Code workspace: research, write, optimize, analyze, publish to WordPress; GA4, Search Console and DataForSEO integrations; Python analysis modules (intent, density, readability, SEO score). |
| Self-hosted analytics | [Plausible](https://github.com/plausible/analytics), [Matomo](https://github.com/matomo-org/matomo) | Cookieless and light, or full-featured. |
| Server log analysis (crawl behaviour, 404s) | [GoAccess](https://github.com/allinurl/goaccess) | `goaccess access.log --log-format=COMBINED -o report.html` |
| Search Console bulk export | [google-search-console-export-all](https://github.com/swalker-888/google-search-console-export-all) | Past the 1,000-row UI limit. |
| SERP API, self-hosted | [openserp](https://github.com/karust/openserp) | Browser-rendered Google results. |
| Sitemaps and robots per framework | next-sitemap, @astrojs/sitemap, nuxt-seo, laravel-sitemap, jekyll-sitemap | See `seo-technical` recipes. |
| Meta tags per framework | next-seo, astro-seo, nuxt-seo, svelte-seo, meta-tags (Rails), jekyll-seo-tag | |
| `llms.txt` | [llms-txt spec](https://github.com/AnswerDotAI/llms-txt), [llmstxt-generator](https://github.com/firecrawl/llmstxt-generator) | See `seo-ai-visibility`. |
| Indexing pings | IndexNow (Bing and partners) | Google's Indexing API is for job postings and live events only. |
| More | [Awesome Open-Source SEO](https://github.com/ZensInk/awesome-open-source-seo) | Curated, tools-only, refreshed monthly. |

## Recommended stacks

- **Small or indie site**: the checker in CI + SerpBear + Plausible or Matomo + Lighthouse CI. Add Search Console. Zero monthly cost beyond a SERP provider for SerpBear (free tiers exist).
- **Content program**: the above + SEOMachine (or this repo's `seo-content`) + OpenSEO with a small DataForSEO budget for volume and difficulty.
- **Agency or multi-site**: SEOnaut scheduled crawls + SerpBear + Search Console bulk exports + OpenSEO + GoAccess on logs.
- **Developer or AI workflow**: the checker + Lighthouse CI + OpenSEO MCP + advertools for custom analysis.

## Recipes

### SEOnaut

```bash
cp docker/seonaut.compose.yml ./docker-compose.seonaut.yml
docker compose -f docker-compose.seonaut.yml up -d
open http://localhost:9000
```

Add the project, run a crawl, export the issue list, feed it into `seo-audit` step 1. Put HTTPS in front with a reverse proxy before exposing it.

### SerpBear

```bash
cp docker/serpbear.compose.yml ./docker-compose.serpbear.yml
# edit USER, PASSWORD, SECRET, APIKEY, NEXT_PUBLIC_APP_URL
docker compose -f docker-compose.serpbear.yml up -d
open http://localhost:3000
```

Then: add the domain, choose a scraper in Settings (serper.dev pay-as-you-go, SearchApi, SerpApi, HasData, or your own proxies; the free providers listed in the README have mostly stopped working), add keywords, set notification SMTP. Connect Search Console for real clicks per keyword and keyword discovery; connect a Google Ads test account for volumes. SerpBear exposes an API for reports.

### OpenSEO

Hosted: sign up at openseo.so, connect the MCP to the agent per their docs. Self-host: follow `docs/SELF_HOSTING_DOCKER.md` or the Cloudflare guide in the repo; you need a DataForSEO API key and pay DataForSEO directly. Install its skills with `npx skills add every-app/open-seo`. Its skills (`seo-audit`, `keyword-research`, `keyword-clustering`, `competitor-analysis`, `local-seo`, `link-prospecting`, `ai-visibility-audit`, `seo-report`) pair with this repo's: use OpenSEO for data, this repo for the code changes.

### Lighthouse CI

`lighthouserc.json` at the repo root:

```json
{
  "ci": {
    "collect": {
      "staticDistDir": "./dist",
      "url": ["http://localhost/index.html", "http://localhost/blog/index.html"]
    },
    "assert": {
      "preset": "lighthouse:recommended",
      "assertions": {
        "categories:seo": ["error", { "minScore": 0.95 }],
        "categories:performance": ["warn", { "minScore": 0.85 }],
        "largest-contentful-paint": ["warn", { "maxNumericValue": 2500 }],
        "cumulative-layout-shift": ["error", { "maxNumericValue": 0.1 }]
      }
    },
    "upload": { "target": "temporary-public-storage" }
  }
}
```

```bash
npm i -D @lhci/cli
npx lhci autorun
```

For server-rendered apps, replace `staticDistDir` with `startServerCommand` and real URLs.

### Search Console exports without the UI limit

Use the bulk export script (or the Search Analytics API directly) to pull queries by page for 16 months into CSV; feed `seo-keyword-research` step 2 and cannibalization checks.

### Log analysis

```bash
goaccess /var/log/nginx/access.log --log-format=COMBINED -o /tmp/report.html
grep -i googlebot /var/log/nginx/access.log | awk '{print $7}' | sort | uniq -c | sort -rn | head
```

Look for: crawl frequency per section, 404s and 5xxs served to bots, parameter URLs eating crawl budget, bots hitting blocked resources.

## Guardrails

- Change the default credentials in every Compose file before exposing a service.
- Scrapers and SERP APIs have terms; respect them and rate limits.
- Keep API keys in `.env`, never in the repo.
- Do not run large crawls against sites you do not own without permission and a gentle rate.
