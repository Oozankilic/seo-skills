# Framework recipes

Where metadata, sitemaps, robots and JSON-LD live in common stacks. Verify package names against the project's lockfile before adding dependencies.

## Next.js (App Router)

- **Metadata**: export `metadata` or `generateMetadata()` from `layout.tsx` / `page.tsx`. Set `metadataBase` in the root layout so relative `canonical` and `openGraph.images` resolve to absolute URLs.

```ts
export async function generateMetadata({ params }): Promise<Metadata> {
  const post = await getPost(params.slug);
  return {
    title: `${post.title} | Brand`,
    description: post.excerpt,
    alternates: { canonical: `/blog/${post.slug}/`, languages: { en: `/blog/${post.slug}/`, de: `/de/blog/${post.slug}/` } },
    openGraph: { type: 'article', title: post.title, description: post.excerpt, images: [`/og/${post.slug}.png`], publishedTime: post.date },
    robots: post.draft ? { index: false, follow: false } : undefined,
  };
}
```

- **Sitemap**: `app/sitemap.ts` exporting `MetadataRoute.Sitemap`; return the list from your data source. For large sites use `generateSitemaps()` to split.
- **robots**: `app/robots.ts` exporting `MetadataRoute.Robots` with the sitemap URL.
- **JSON-LD**: render `<script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }} />` inside the page component (server component, so it is in the HTML).
- **OG images**: `app/.../opengraph-image.tsx` with `ImageResponse`.
- **Redirects**: `next.config.js` `redirects()` for permanent moves (`permanent: true` gives 308; use middleware if you need 301 specifically).
- **Rendering**: server components and static generation by default; avoid `'use client'` on page shells that carry content.

## Next.js (Pages Router)

- `next/head` per page, or the `next-seo` package (`NextSeo`, `ArticleJsonLd`, `DefaultSeo`).
- `next-sitemap` generates `sitemap.xml` and `robots.txt` at build (`next-sitemap.config.js` with `siteUrl`, `exclude`, `transform`).
- Use `getStaticProps`/`getServerSideProps` so content and head tags are server-rendered.

## Astro

- Head tags in the layout component; props for title, description, canonical, image. Use `Astro.site` and `Astro.url` for absolute URLs. The `astro-seo` component covers title, description, OG, Twitter and `noindex`.
- `@astrojs/sitemap` integration generates `sitemap-index.xml`; set `site` in `astro.config.mjs`; filter drafts with `filter`. Add `Sitemap:` to a static `public/robots.txt`.
- JSON-LD: `<script type="application/ld+json" set:html={JSON.stringify(schema)} />`.
- Content collections give you `lastmod` and draft flags for free.
- Redirects: `redirects` in `astro.config.mjs` or the host's config (`_redirects`, `vercel.json`).

## Nuxt 3

- `useSeoMeta()` / `useHead()` in pages and layouts. `nuxt-seo` (`@nuxtjs/seo`) bundles `nuxt-sitemap`, `nuxt-robots`, `nuxt-schema-org`, `nuxt-og-image` and `nuxt-link-checker`; set `site.url` in `nuxt.config.ts`.
- Without the bundle: `@nuxtjs/sitemap` and `@nuxtjs/robots` modules.
- Schema: `useSchemaOrg([defineArticle({...})])` from `nuxt-schema-org`.
- SSR on by default; keep it on for indexable routes (`routeRules` with `prerender: true` for static pages).

## SvelteKit

- `<svelte:head>` in `+page.svelte` with data from `+page.server.ts`. The `svelte-seo` component covers common tags.
- Sitemap: a `src/routes/sitemap.xml/+server.ts` endpoint that returns XML built from your data; set `prerender = true`. Same pattern for `robots.txt`.
- JSON-LD: `{@html '<script type="application/ld+json">' + JSON.stringify(schema) + '</script>'}` inside `<svelte:head>`.
- Ensure `ssr = true` for indexable routes; `csr`-only pages are invisible to crawlers.

## Remix / React Router (framework mode)

- `meta()` export per route returns title, description, canonical (`tagName: 'link'`), OG tags.
- Sitemap and robots as resource routes (`routes/sitemap[.]xml.tsx` returning `Response` with XML).
- JSON-LD via a `<script type="application/ld+json">` in the route component, or the `"script:ld+json"` key in `meta()`.
- Redirects: `redirect()` in loaders with status 301.

## WordPress

- Use one SEO plugin (Yoast SEO, Rank Math or The SEO Framework) for titles, descriptions, canonicals, robots meta, sitemaps, breadcrumbs and base schema. Do not run two.
- Settings to check: permalink structure (`/%postname%/`), discourage-search-engines unchecked, sitemap enabled, category/tag archives noindexed when thin, attachment pages redirected to the file, `www`/`https` canonical host in Site Address.
- Theme: one H1 per template, `lang` attribute, image dimensions, lazy loading (core does this), `font-display`.
- Speed: caching plugin, image optimisation, limit plugins, defer non-critical JS.
- Custom schema: Yoast schema API filters or Rank Math's; otherwise a small plugin that echoes JSON-LD in `wp_head` for the post type.
- Publishing via REST: the Yoast meta fields are exposed when a small plugin registers them (SEOMachine ships one).

## Static site generators

- **Jekyll**: `jekyll-seo-tag` (title, description, canonical, OG, JSON-LD) and `jekyll-sitemap`. Set `url` in `_config.yml`.
- **Hugo**: `.Site.BaseURL`, built-in sitemap template (`sitemap.xml`), `robots.txt` via `enableRobotsTXT`, write a `partials/seo.html` for head tags and JSON-LD using page params.
- **Eleventy**: a head include fed by front matter; `@11ty/eleventy-plugin-rss` style data for a sitemap template (`sitemap.njk` with `permalink: /sitemap.xml`).
- **Docusaurus / VitePress / MkDocs**: sitemap and canonical come from config (`url`, `baseUrl`); check the `head` option for OG defaults.

## Plain HTML

- Put the head block from `seo-technical` in every page; keep a shared partial if the build allows.
- Hand-maintain `sitemap.xml` and `robots.txt` or generate them with a small script from the file list.
- Host-level redirects: Netlify `_redirects`, Vercel `vercel.json`, Cloudflare `_redirects` or rules, nginx `return 301`, Apache `.htaccess`.

## Hosting

- Netlify / Vercel / Cloudflare Pages: redirects and headers files; make sure the `www` and apex both exist and one redirects to the other.
- nginx: `server { listen 80; return 301 https://$host$request_uri; }`, plus a `www` server block that redirects. `add_header Strict-Transport-Security "max-age=31536000" always;` once HTTPS is stable.
- CDN cache: cache HTML with short TTL and purge on publish; cache assets with long TTL and hashed file names.
