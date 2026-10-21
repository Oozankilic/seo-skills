# SEO audit checklist (one page)

Copy into an issue or PR description and tick as you go. `seo_check.py` covers items marked (auto).

## Crawl and index
- [ ] robots.txt reachable, does not block important paths, CSS or JS, references sitemap (auto)
- [ ] Sitemap reachable, referenced from robots.txt, contains only canonical 200 URLs (auto: existence and count)
- [ ] No important page is noindex (auto)
- [ ] Every page has a canonical; self-referencing on unique pages; consistent scheme, host and trailing slash (auto: presence and mismatch)
- [ ] No redirect chains or loops; HTTP redirects to HTTPS (auto)
- [ ] No soft 404s; 404 pages return 404
- [ ] Important pages within 3 clicks of the homepage; no orphans
- [ ] Parameter, facet and search-result URLs controlled

## Rendering and speed
- [ ] Title, meta, content and links present in initial HTML or server-rendered
- [ ] LCP < 2.5 s, INP < 200 ms, CLS < 0.1 on one template per page family
- [ ] Images sized, compressed, modern format, lazy below the fold
- [ ] Fonts with font-display; no render-blocking third-party scripts above the fold
- [ ] Responsive, viewport set, same content on mobile (auto: viewport)
- [ ] HTTPS everywhere, no mixed content (auto: http:// links)

## On-page
- [ ] Unique titles, ~50 to 60 chars, keyword near start (auto)
- [ ] Unique descriptions, ~150 to 160 chars, reason to click (auto)
- [ ] One H1 per page with the primary topic; logical heading order (auto: H1 count)
- [ ] URL readable, lowercase, hyphenated
- [ ] Alt text on meaningful images (auto)
- [ ] Open Graph title, description, image; Twitter card (auto)
- [ ] `lang` attribute; hreflang pairs reciprocal with x-default where multilingual (auto: presence)
- [ ] Structured data valid and matching content (auto: JSON parses; validate types with Rich Results Test)
- [ ] Thin pages identified (auto: word count < 300)
- [ ] Internal links: descriptive anchors, no broken links (auto), money pages well linked

## Content and authority
- [ ] Each important page has one target intent; no cannibalization
- [ ] Important pages answer the query better than the current top results
- [ ] Named authors, visible dates, sourced claims, contact and policy pages
- [ ] Stale content identified for refresh
- [ ] Backlink profile reviewed; toxic or lost links noted (`unknown` if no data)

## AI search
- [ ] robots.txt does not block OAI-SearchBot, ChatGPT-User, PerplexityBot, ClaudeBot unless intended (auto)
- [ ] Direct answer in the first two sentences of key pages
- [ ] `llms.txt` present (optional, auto: existence)

## Monitoring
- [ ] Search Console verified, sitemap submitted
- [ ] Rank tracker (SerpBear) tracking the target queries
- [ ] Lighthouse CI budget on the main templates
