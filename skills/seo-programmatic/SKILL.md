---
name: seo-programmatic
description: Build SEO pages at scale from templates and data without producing thin content. Use when the user mentions programmatic SEO, pSEO, template pages, pages at scale, location pages, "[keyword] in [city]" pages, integration pages, comparison or "vs" pages, "alternatives" pages, glossary pages, directory pages, persona pages, or generating hundreds of landing pages. For auditing existing pages see seo-audit; for structured data see seo-schema.
---

# Programmatic SEO

Many pages from one template and a dataset. It works when every page carries value specific to that page; it fails (thin content, doorway pages, manual actions) when the only difference between pages is a swapped variable.

## Principles

1. **Unique value per page.** Conditional sections, page-specific data, original analysis, not just the name substituted into shared copy.
2. **Proprietary data wins.** Defensibility, strongest first: data you created, data derived from your product, user-generated, licensed, public.
3. **Subfolders, not subdomains.** `site.com/templates/resume/`, never `templates.site.com`.
4. **Real search intent per page.** Every page answers something people actually search.
5. **Quality over count.** One hundred good pages beat ten thousand thin ones.
6. **No doorway pages, stuffing or duplicates.**

## The 12 playbooks

| Playbook | Pattern | Example |
|----------|---------|---------|
| Templates | "[type] template" | resume template |
| Curation | "best [category]" | best website builders |
| Conversions | "[X] to [Y]" | 10 USD to EUR |
| Comparisons | "[X] vs [Y]" | Webflow vs WordPress |
| Examples | "[type] examples" | landing page examples |
| Locations | "[service] in [location]" | dentists in Austin |
| Personas | "[product] for [audience]" | CRM for real estate |
| Integrations | "[A] [B] integration" | Slack Asana integration |
| Glossary | "what is [term]" | what is churn |
| Translations | same content, other languages | localized pages |
| Directory | "[category] tools" | AI copywriting tools |
| Profiles | "[entity name]" | a company, person or product page |

Choose by what you have: proprietary data (directory, profiles), integrations (integrations), a design or creative product (templates, examples), several audiences (personas), locations (locations), a utility product (conversions), expertise (glossary, curation), a competitive market (comparisons, alternatives). Playbooks stack: "best coworking spaces in San Diego".

Detailed playbook notes are in `references/playbooks.md`.

## Procedure

### 1. Validate the pattern

- Identify the repeating structure and the variables. Count the realistic combinations.
- Check demand: aggregate volume, distribution between head and tail, trend. Sample 20 variants in a keyword tool or Search Console; if most have zero demand, cut the set.
- Look at who ranks for a sample: if every result is a major marketplace with deep data, a thin template will not compete.

### 2. Data

- Source per field, update cadence, licence. Mark which fields are unique per page and which are shared.
- Minimum data threshold per page: define it (for example, at least three unique facts, one data table, one specific example). Pages below the threshold are not generated, or are generated `noindex` until they qualify.

### 3. Template

- Title and H1 pattern with the keyword; unique intro written from page data (not a shared paragraph); data-driven sections; conditional blocks that only render when data exists; FAQ built from page-specific questions; related pages; CTA matched to intent.
- Unique meta title and description per page from data.
- Schema per page type (`Product`, `LocalBusiness`, `FAQPage`, `BreadcrumbList`, `SoftwareApplication`).
- Breadcrumbs and a hub page per playbook.

### 4. Internal linking

- Hub and spoke: category hub links to every spoke; spokes link to the hub and to related spokes (same city, same category, next and previous). No orphans.
- Put the hub in the main navigation or footer so link equity reaches it.
- Sitemap per page type so coverage is readable in Search Console.

### 5. Indexation

- Prioritise high-demand variants; `noindex` very thin variants; keep sitemaps clean.
- Roll out in batches (hundreds, not tens of thousands) and watch indexation rate before releasing more.
- Watch crawl budget on large sites: avoid parameter duplicates and infinite combinations.

### 6. Pre-launch checklist

- [ ] Each page passes the unique-value threshold
- [ ] Unique titles, descriptions, H1 and intro from data
- [ ] Schema valid on a sample page (Rich Results Test)
- [ ] Hub exists, every spoke linked, related spokes linked
- [ ] In sitemap, crawlable, no conflicting noindex
- [ ] `scripts/seo_check.py --dir <build>` shows no duplicate titles or descriptions
- [ ] Page speed acceptable on the template (Lighthouse)

### 7. After launch

Track indexation rate (Search Console coverage), rankings on a sample (SerpBear), traffic and engagement per playbook, conversion. Watch for thin content notices, ranking drops, manual actions, crawl errors. Prune or merge pages that do not earn impressions after a few months.

## Common failures

- Swapping the city name in identical copy.
- Several pages for the same keyword (cannibalization).
- Generating pages with no demand.
- Stale or wrong data.
- Pages built for the crawler with no use for a person.

## Output

A strategy document (opportunity, playbook choice, data plan, uniqueness rules, rollout plan) and a page template spec (URL pattern, title and description patterns, section outline with data bindings, schema, internal links).
