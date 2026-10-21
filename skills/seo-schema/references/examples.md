# JSON-LD examples

All URLs absolute, dates ISO 8601 with timezone, enumerations as full schema.org URLs.

## Organization

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://example.com/#org",
  "name": "Example Co",
  "url": "https://example.com/",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://x.com/example",
    "https://www.linkedin.com/company/example",
    "https://github.com/example"
  ],
  "contactPoint": { "@type": "ContactPoint", "contactType": "customer support", "email": "support@example.com" }
}
```

## WebSite with sitelinks search box

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "@id": "https://example.com/#site",
  "name": "Example",
  "url": "https://example.com/",
  "publisher": { "@id": "https://example.com/#org" },
  "potentialAction": {
    "@type": "SearchAction",
    "target": { "@type": "EntryPoint", "urlTemplate": "https://example.com/search?q={search_term_string}" },
    "query-input": "required name=search_term_string"
  }
}
```

## Article / BlogPosting

```json
{
  "@context": "https://schema.org",
  "@type": "BlogPosting",
  "headline": "How to Implement Schema Markup",
  "description": "A practical guide to JSON-LD structured data.",
  "image": ["https://example.com/images/schema-guide-1200x630.png"],
  "datePublished": "2026-01-15T08:00:00+00:00",
  "dateModified": "2026-03-02T10:00:00+00:00",
  "author": { "@type": "Person", "name": "Jane Doe", "url": "https://example.com/authors/jane/", "jobTitle": "Head of Growth" },
  "publisher": { "@id": "https://example.com/#org" },
  "mainEntityOfPage": { "@type": "WebPage", "@id": "https://example.com/blog/schema-guide/" }
}
```

## Product

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Premium Widget",
  "image": ["https://example.com/products/widget-1.jpg"],
  "description": "A widget for professionals.",
  "sku": "WIDGET-001",
  "gtin13": "0123456789012",
  "brand": { "@type": "Brand", "name": "Example Co" },
  "offers": {
    "@type": "Offer",
    "url": "https://example.com/products/widget/",
    "priceCurrency": "USD",
    "price": "99.00",
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
    "shippingDetails": { "@type": "OfferShippingDetails", "shippingRate": { "@type": "MonetaryAmount", "value": "0", "currency": "USD" }, "shippingDestination": { "@type": "DefinedRegion", "addressCountry": "US" } }
  },
  "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.8", "reviewCount": "127" }
}
```

## SoftwareApplication (SaaS)

```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Example App",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "url": "https://example.com/",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD", "description": "Free plan available" },
  "aggregateRating": { "@type": "AggregateRating", "ratingValue": "4.6", "ratingCount": "1250" }
}
```

## FAQPage

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is schema markup?",
      "acceptedAnswer": { "@type": "Answer", "text": "Schema markup is a vocabulary of tags you add to HTML so search engines understand what a page describes." }
    },
    {
      "@type": "Question",
      "name": "Does schema markup improve rankings?",
      "acceptedAnswer": { "@type": "Answer", "text": "Not directly. It makes pages eligible for rich results, which can raise click-through rate." }
    }
  ]
}
```

## HowTo

```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to add JSON-LD to a page",
  "totalTime": "PT15M",
  "step": [
    { "@type": "HowToStep", "name": "Choose the type", "text": "Pick the schema.org type that matches the page.", "url": "https://example.com/guide/#step-1" },
    { "@type": "HowToStep", "name": "Build the object", "text": "Generate the JSON from page data in the template.", "url": "https://example.com/guide/#step-2" },
    { "@type": "HowToStep", "name": "Validate", "text": "Run the Rich Results Test and fix errors.", "url": "https://example.com/guide/#step-3" }
  ]
}
```

## BreadcrumbList

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/" },
    { "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://example.com/blog/" },
    { "@type": "ListItem", "position": 3, "name": "Schema Guide", "item": "https://example.com/blog/schema-guide/" }
  ]
}
```

## LocalBusiness

```json
{
  "@context": "https://schema.org",
  "@type": "Dentist",
  "name": "Example Dental",
  "image": "https://example.com/office.jpg",
  "url": "https://example.com/locations/austin/",
  "telephone": "+1-512-555-0100",
  "priceRange": "$$",
  "address": { "@type": "PostalAddress", "streetAddress": "123 Main St", "addressLocality": "Austin", "addressRegion": "TX", "postalCode": "78701", "addressCountry": "US" },
  "geo": { "@type": "GeoCoordinates", "latitude": 30.2672, "longitude": -97.7431 },
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "08:00", "closes": "18:00" }
  ],
  "sameAs": ["https://www.google.com/maps?cid=1234567890"]
}
```

## Event

```json
{
  "@context": "https://schema.org",
  "@type": "Event",
  "name": "Annual Marketing Conference",
  "startDate": "2026-06-15T09:00:00-07:00",
  "endDate": "2026-06-15T17:00:00-07:00",
  "eventStatus": "https://schema.org/EventScheduled",
  "eventAttendanceMode": "https://schema.org/OnlineEventAttendanceMode",
  "location": { "@type": "VirtualLocation", "url": "https://example.com/conference/" },
  "image": "https://example.com/conference.jpg",
  "description": "A one-day online conference.",
  "offers": { "@type": "Offer", "url": "https://example.com/conference/tickets/", "price": "199", "priceCurrency": "USD", "availability": "https://schema.org/InStock", "validFrom": "2026-01-01T00:00:00+00:00" },
  "organizer": { "@id": "https://example.com/#org" }
}
```

## Person (author page)

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://example.com/authors/jane/#person",
  "name": "Jane Doe",
  "url": "https://example.com/authors/jane/",
  "jobTitle": "Head of Growth",
  "worksFor": { "@id": "https://example.com/#org" },
  "sameAs": ["https://www.linkedin.com/in/janedoe", "https://x.com/janedoe"]
}
```

## Rendering patterns

React / Next.js:

```tsx
<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />
```

Astro: `<script type="application/ld+json" set:html={JSON.stringify(schema)} />`

Nuxt: `useSchemaOrg([defineArticle({ ... })])` or `useHead({ script: [{ type: 'application/ld+json', innerHTML: JSON.stringify(schema) }] })`

WordPress (PHP, in a plugin): `add_action('wp_head', fn() => printf('<script type="application/ld+json">%s</script>', wp_json_encode($schema, JSON_UNESCAPED_SLASHES)));`

Escape `</script>` inside strings when serialising (`JSON.stringify(schema).replace(/</g, '\\u003c')`) to avoid breaking out of the script tag.
