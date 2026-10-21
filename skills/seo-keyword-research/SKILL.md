---
name: seo-keyword-research
description: Find, score, cluster and map keywords to pages. Use when the user asks for keyword research, "what should we rank for", search volume, keyword difficulty, search intent, topic clusters, keyword mapping, content gaps, striking-distance queries, competitor keywords, or keyword cannibalization. Works with Search Console exports, free sources, or paid data (DataForSEO via OpenSEO, SerpBear's Google Ads integration).
---

# Keyword research, clustering and mapping

Goal: turn seed topics or existing data into a prioritised set of query clusters, each mapped to one page (existing or new). Business fit and intent fit beat raw volume.

Read `seo-context.md` first: the business, the goal, the markets and the pages that make money decide which clusters matter.

## Data sources, in order of trust

1. **Search Console** (first-party). Queries already earning impressions, especially **striking distance** terms at positions 5 to 20 with meaningful impressions. These are the fastest wins. Export queries and pages for 3 and 16 months; query-plus-page combinations reveal cannibalization.
2. **Paid keyword data** when available: DataForSEO through OpenSEO (volume, difficulty, intent, CPC, trends, SERP features), SerpBear's keyword ideas via a Google Ads account, or whatever the project already pays for.
3. **Free signals** when no data: Google autocomplete and "People also ask", related searches, competitor page titles and headings, Reddit and forum threads, product reviews, support tickets, sales call notes, the product's own feature names.
4. **Rank tracker history** (SerpBear) for what moved recently.

Never invent volumes. Write `unknown` and say which source would fill it.

## Procedure

### 1. Normalise the seeds

Turn the request into three to six distinct research angles: product category terms, problem terms, comparison and alternative terms, use-case or audience terms, feature terms, "how to" terms. Note market, language and location; local demand differs from national.

### 2. Start from first-party demand

If Search Console is available, pull queries at position 5 to 20 with at least ~50 impressions. Attach difficulty and intent if you have a data source. This list, ranked by impressions, is the first opportunity set; work it before broad discovery.

### 3. Discover

For each angle, gather candidates (one to five seeds per call if using a tool). Pull competitor ranking keywords when a competitor is named: group them into themes (product and category, alternatives and comparisons, templates and tools, guides, branded, local). Filter for business fit; do not treat every competitor keyword as desirable.

### 4. Hydrate and clean

Attach volume, difficulty, intent, CPC and trend where available. Remove duplicates, irrelevant terms, branded-only terms (other brands), and terms needing a different product or audience. Treat close variants (plural, word order) as one bucket, not several.

### 5. Classify intent

| Intent | Signals | Page type |
|--------|---------|-----------|
| Informational | how, what, why, guide, examples | article, guide, glossary |
| Commercial | best, top, vs, alternative, review, pricing | comparison, listicle, alternatives page |
| Transactional | buy, download, signup, template, tool, near me | product, landing, tool page |
| Navigational | brand or product names | homepage, product page (usually not a target) |

When intent is ambiguous and would change the recommendation, check the live SERP for that query: the page types ranking tell you the intent Google has settled on.

### 6. Cluster by intent, not by words

- Same SERP intent and overlapping ranking pages belong together. Check overlap for borderline terms: if two queries return mostly the same top results, one page serves both.
- Different buyer stage, SERP format or audience means a different cluster even when the words match.
- Fewer than ten usable terms: produce a simple map, do not over-cluster.

### 7. Map each cluster to one page

- Existing URL if it fits (use saved key pages and current rankings).
- New page recommendation with page type, working title and required sections.
- "Do not target / later" bucket for weak or off-strategy clusters, with the reason.

### 8. Find cannibalization

Two or more URLs targeting the same intent, or one query sending impressions to several pages in Search Console. Decide which page keeps the intent; the others get merged, redirected, re-targeted or de-emphasised (internal links and canonical). Only report cannibalization with evidence.

### 9. Prioritise by practical opportunity

Score each cluster on:
- fit with the product, page or goal
- clarity of intent
- difficulty the site can plausibly compete with (compare site authority with what ranks)
- demand signal (volume, CPC as a proxy for value)
- SERP shape (features that steal clicks, number of ads)
- for local: local pack presence and proximity fit

A small query can matter to a high-value business; an easy one is not automatically worthwhile.

## Output

**For research**
1. **The opportunity**: one or two sentences naming the best theme and why the site can win it now.
2. **Target these now**: table of keyword, intent, volume, difficulty, CPC, page to make or update.
3. **Why these**: one bullet of evidence per keyword that needs justifying.
4. **Longer list**: same columns.
5. **Risks and caveats**: ambiguous intent, missing metrics as `unknown`, close variants counted once.
6. **What to do next**: cluster, brief, save, or build.

**For clustering and mapping**
1. **The map**: how many clusters, pages to create, pages to update, cannibalization found.
2. **Clusters**: cluster, primary keyword, intent, target page, priority.
3. **Page briefs**: per cluster, the page type, the searcher's problem, required sections, internal links.
4. **Cannibalization**: query, competing URLs, which to keep (only with evidence).
5. **What to do next**.

Label target pages as proposed when no URL data was supplied. Say where the keyword data came from and its date.

## Guardrails

- Do not invent metrics; `unknown` is an answer.
- Lexical similarity alone never decides a cluster; SERP intent wins.
- Prefer business fit and intent fit over the biggest number.
- Do not re-buy research that already exists in the project (check `seo-context.md` research log); reuse results under about 30 days old for discovery, but re-check a live ranking before it drives a recommendation.
- Ask before saving keywords into a shared tracker or overwriting tags.
