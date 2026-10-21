---
name: seo-schema
description: Add, fix or validate structured data (schema.org JSON-LD) so pages qualify for rich results. Use when the user mentions schema markup, structured data, JSON-LD, rich snippets, rich results, FAQ schema, Product schema, Article schema, Organization schema, BreadcrumbList, LocalBusiness, HowTo, Event, SoftwareApplication, or star ratings in search results. For the rest of on-page SEO see seo-technical and seo-audit.
---

# Schema markup

Structured data tells search engines what a page is about in a machine-readable form and makes the page eligible (not guaranteed) for rich results: star ratings, FAQ drop-downs, breadcrumbs, product price and availability, event dates, sitelinks search box.

## Principles

1. **Accuracy first.** Markup must describe content that is visible on the page. Marking up reviews, prices or FAQs that are not on the page violates Google's guidelines and can earn a manual action.
2. **JSON-LD only.** One `<script type="application/ld+json">` per page, in the server-rendered HTML (head or end of body). Microdata and RDFa work but are harder to maintain.
3. **Google's supported types only, for rich results.** Other schema.org types are harmless but do nothing visible. Check the current list in Google Search Central's structured data gallery before promising a rich result.
4. **Validate before deploying, monitor after.** Rich Results Test for eligibility, Schema Markup Validator for syntax, Search Console Enhancements reports for errors over time.
5. **Generate from data, not by hand.** Build the object in the template from the same fields that render the page so they cannot drift.

## Which type for which page

| Page | Type | Required | Recommended |
|------|------|----------|-------------|
| Homepage / about | `Organization` | name, url | logo, sameAs (social profiles), contactPoint |
| Homepage | `WebSite` | name, url | potentialAction SearchAction (sitelinks search box) |
| Blog post, news | `Article` / `BlogPosting` / `NewsArticle` | headline, image, datePublished, author | dateModified, publisher, description, mainEntityOfPage |
| Product | `Product` | name, image, offers (price, priceCurrency, availability) | sku, brand, aggregateRating, review, gtin |
| SaaS / app page | `SoftwareApplication` | name, offers, applicationCategory | operatingSystem, aggregateRating |
| FAQ section | `FAQPage` | mainEntity (Question + acceptedAnswer) | only on pages with visible Q&A; Google now shows FAQ rich results mainly for government and health sites, but the markup still helps AI answer engines |
| Tutorial | `HowTo` | name, step | totalTime, tool, supply (rich result retired for most sites; still useful for machine readability) |
| Any deep page | `BreadcrumbList` | itemListElement (position, name, item) | |
| Local business page | `LocalBusiness` (or subtype) | name, address | geo, telephone, openingHoursSpecification, priceRange, image |
| Event, webinar | `Event` | name, startDate, location | endDate, offers, performer, organizer, eventStatus, eventAttendanceMode |
| Recipe, video, job, course, dataset | their types | see Google docs | |
| Author page | `Person` | name | url, sameAs, jobTitle, worksFor |

Complete JSON-LD examples for each are in `references/examples.md`.

## Combining types

Use `@graph` with `@id` references so one page can carry Organization, WebSite, BreadcrumbList and Article without repeating the publisher:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", "@id": "https://example.com/#org", "name": "Example", "url": "https://example.com/", "logo": "https://example.com/logo.png" },
    { "@type": "WebSite", "@id": "https://example.com/#site", "url": "https://example.com/", "publisher": { "@id": "https://example.com/#org" } },
    { "@type": "BreadcrumbList", "itemListElement": [ ... ] },
    { "@type": "Article", "headline": "...", "publisher": { "@id": "https://example.com/#org" }, "mainEntityOfPage": "https://example.com/blog/post/" }
  ]
}
```

## Procedure

1. Identify the page type and which rich result is realistic for it (check the gallery). Say up front when a type will not produce a visible result.
2. Check for existing markup: `curl -s URL | grep -o '<script type="application/ld+json">.*</script>'` and the Rich Results Test. Plugins (Yoast, Rank Math, Shopify themes) often already emit Organization, WebSite, Breadcrumb and Article; do not duplicate them, extend them.
3. Build the object in the template from page data. Dates in ISO 8601 with timezone, URLs absolute, enumerations exact (`https://schema.org/InStock`), prices as strings with `priceCurrency`.
4. Render it server-side. Confirm it is in the raw HTML response.
5. Validate: Rich Results Test (eligibility and warnings) and validator.schema.org (syntax). Fix errors; warnings are optional fields.
6. Run `scripts/seo_check.py` on the page; it reports JSON-LD types found and JSON parse errors.
7. After deploy, watch Search Console Enhancements for the type.

## Common mistakes

- Missing required properties (Product without offers, Article without image or datePublished).
- Relative URLs, dates without timezone, numbers as numbers where strings are expected (`"price": "99.00"`).
- Review or rating markup on pages without visible reviews; self-serving reviews on Organization or LocalBusiness (not allowed).
- FAQPage on pages where the questions are not visible, or where the same FAQ is repeated site-wide.
- Multiple conflicting Organization or WebSite blocks from theme plus plugin.
- Markup injected client-side after load; verify the server response.
- Breadcrumb items whose `item` URLs 404 or redirect.

## Guardrails

- Never mark up content the user cannot see on that page.
- Never fabricate ratings, review counts, prices or availability.
- Do not promise a rich result; say "eligible for".
- Keep `@id` values stable; changing them resets entity identity for crawlers.
