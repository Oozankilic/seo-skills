---
name: seo-local
description: Improve visibility in Google Maps, the local pack and local search for businesses with physical locations or service areas. Use when the user mentions local SEO, Google Business Profile (GBP), Google Maps ranking, local pack, "near me" searches, location pages, NAP consistency, citations, reviews, multi-location SEO, or a rank grid. For national organic work see seo-audit and seo-keyword-research.
---

# Local SEO

Work out why a business does or does not show in Google Maps and the local pack near its customers, and fix the highest-leverage thing first.

Inputs: business name (or its Google `cid` / place ID, most reliable), its coordinate or service area, one to three keywords customers actually search ("emergency plumber", not the brand).

## What decides local rankings

In rough order of weight: relevance (primary and secondary categories, services, the content of the website), distance (searcher to business, or service area), prominence (review count, rating, recency and replies; links and mentions; citations in directories; website authority). Profile completeness and activity (photos, posts, Q&A) matter after those.

## Procedure

### 1. Find the listing

Locate the Google Business Profile. For a chain, collect every location in one pass. Match by `cid` or place ID when you have one; name matching collides with chains and look-alikes.

### 2. Snapshot the local SERP

For the main keyword near the business coordinate, record the top three to five competitors and the business's own position. Tools: OpenSEO local SERP tools, a rank grid tool, or manual searches with the location set. Note date, keyword and coordinate for every observation.

### 3. Compare profiles head to head

For the business and the top two competitors: primary category, additional categories, claimed status, review count, average rating, review recency, owner reply rate, hours completeness, photo count, services and attributes, description, website link.

The website link must deep-link to that location's page on the project domain, not a homepage or a stale domain.

### 4. Reviews

Pull reviews for the business and the strongest competitor. Compare volume, recency, rating, and how many got an owner reply. Recommend a review request process (after service, by SMS or email, direct link) and a reply cadence. Never recommend gating (asking only happy customers) or incentives that violate Google's policy.

### 5. Rank grid

A grid of searches around the business (3x3 is usually enough; 5x5 only for wide service areas; every point is a paid or manual search, so say the cost first) separates "ranks at the storefront only" from "ranks across the service area" and names who wins where the business does not. Confirm the centre coordinate before running it; a grid centred on the wrong place is worse than none. A missing rank at a point means the business was not in the results returned there; read it with that point's result count (a full set means outranked, a near-empty set means a sparse SERP).

### 6. Website side

- One page per location with: name, address, phone exactly as on the profile, embedded map, hours, services, photos, local reviews or testimonials, staff, directions and parking, local FAQ, and `LocalBusiness` (or subtype) schema with `address`, `geo`, `telephone`, `openingHoursSpecification` (see `seo-schema`).
- Service-area businesses: service pages per city or area with genuine local content, not swapped names (see `seo-programmatic`, Locations).
- City and service in title, H1 and URL (`/locations/austin/`, `/plumber-austin/`).
- Internal links from the main navigation or a locations hub to every location page.
- NAP (name, address, phone) identical everywhere: website footer, profile, directories, social.

### 7. Citations and links

Consistent listings on the major aggregators and the directories that matter for the category and region (chambers of commerce, associations, local news, supplier pages). Local link prospecting: `seo-link-building`.

### 8. Q&A and posts

Only once the basics are competitive. Seed the profile Q&A with real customer questions and answers; post updates with photos on a cadence you can keep.

## Priority rule

Category and claim problems outrank everything. Then reviews and the website link. Then location page content and schema. Then citations. Then posting cadence.

## Multi-location

Build the snapshot table for the whole chain, then deep-dive (reviews, grid, posts, Q&A) up to five locations; for more, ask which one to three matter most and default to the weakest profile in the densest market.

## Output

1. **Snapshot**: category, rating, review count, claimed status (one row per location).
2. **The one fix**: the single highest-leverage change.
3. **Head to head**: signal | this business | best competitor | gap.
4. **Maps coverage**: what the grid shows, where visibility drops, who wins there.
5. **Website changes**: location pages, schema, NAP fixes, with file paths when you have the code.
6. **Q&A and posting**: only when the basics are competitive.
7. **What to do next**: ordered list.
8. **How this was made**: tools, dates, coordinates, keywords, what was checked by hand.

## Guardrails

- Do not run large grids or many keywords without stating the cost.
- Do not infer local pack strength from national organic metrics.
- Never recommend review gating, fake reviews, keyword-stuffed business names, fake addresses or virtual offices presented as locations.
- Match listings by ID, not by name.
