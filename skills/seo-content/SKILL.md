---
name: seo-content
description: Write, rewrite or optimize a page for search and AI answer engines. Use when the user wants a blog post, article, guide, landing page, comparison page, meta title and description options, an outline or content brief, internal link suggestions, a readability or on-page score, a content refresh, or asks to "optimize this page for SEO", "make this rank", or "remove AI-sounding writing". For keyword selection see seo-keyword-research; for structured data see seo-schema.
---

# Content for search and answer engines

Produce content that answers the searcher better than what ranks, reads like a competent human wrote it, and is formatted so Google and AI engines can extract the answer. Read `seo-context.md` (voice, audience, banned phrases, key pages) and `internal-links-map.md` if present.

## 1. Brief before draft

Every piece starts with a brief. Fill it from research (see `seo-keyword-research`) and from reading the top results for the target query:

- Primary keyword and three to five secondary terms; intent class.
- Searcher's question or decision in one sentence.
- What the top results cover, what they miss, the angle this page takes.
- Target length from the competition (median of the top results is a good target; do not pad past it).
- Required sections, FAQ questions (from People Also Ask, Reddit, support), internal link targets, external sources to cite.
- Meta title and description drafts, URL slug.
- Author, reviewer, publish and update dates.

## 2. Structure

```
H1: primary keyword, benefit-led, under ~60 characters
Direct answer: 1-2 sentences that answer the query outright (before any hook or story)
Key takeaways: 3-5 standalone, specific claims (not a table of contents)
Introduction: hook, problem, promise; keyword within the first 100 words
H2 sections (4-7): one idea each, 2-3 contain a keyword variation, subheading every 300-400 words
  H3 for sub-steps; never skip levels
FAQ (4-6 questions in natural prompt language, direct answer in the first sentence)
Conclusion: 3-5 takeaways, keyword once, one clear next step
```

Length guidance (from the content programs these skills distil): standard post 1,500 to 3,000 words, pillar guide 3,000 to 5,000, how-to 1,500 to 2,500, news 800 to 1,200. Treat these as ranges, not goals; match the query, cut fluff, split topics that overflow.

## 3. Keywords

- Primary keyword in: H1, first 100 words, two or three H2s, the conclusion, meta title, meta description, URL slug.
- Density around 1 to 2 percent is the historical rule; the real test is that no sentence exists only to hold the keyword. Use variations, question forms and related terms.
- One intent per page. If the draft starts answering a second intent, that is a second page.

## 4. Links

- Internal: three to five per article (up to seven on 3,000+ words). One or two to pillar content, two or three to related posts, at most one product page when it solves a problem the section raises, resources when mentioned. Descriptive anchors ("our guide to podcast analytics"), never "click here". No more than two links per paragraph. Cluster content links to its pillar; pillars link to two or three cluster pieces.
- External: two to four authoritative sources for statistics, studies, tools, expert opinion. Prefer recent primary sources. `rel="sponsored"` or `nofollow` for paid and affiliate links.
- Verify every link resolves.

## 5. Meta elements

- **Title**: about 50 to 60 characters, keyword near the start, unique, honest, brand at the end if room. Formats that work: "How to [goal] in [year]: [qualifier]", "[N] [adjective] ways to [benefit]", "[Topic] guide for [audience]", a question that matches the query, "[benefit] with [method]".
- **Description**: about 150 to 160 characters, keyword, concrete benefit, a reason to click, complete sentence. Formulas: problem? solution. angle. action; benefit with method. support. action; question? answer preview. what they learn. action. For AI engines, make the description literally answer the query.
- **Slug**: lowercase, hyphens, three to five words, keyword, no dates unless the content is dated.
- Offer three to five options per element with character counts and a recommendation; see `references/meta-formulas.md`.

## 6. Readability

- 8th to 10th grade reading level for general audiences; sentences average 15 to 20 words, max about 25; paragraphs two to four sentences; 80 percent active voice.
- Lists for steps and sets, tables for comparisons, bold for the takeaway in a paragraph, white space.
- Define jargon on first use. Specific numbers over vague claims. Real examples from the domain.
- Vary sentence length; read it aloud.

## 7. Answer engine and AI citation formatting

AI engines (ChatGPT, Perplexity, Gemini, Google AI Overviews) extract the earliest clear answer, prefer sourced statistics, named experts and self-contained statements, and parse by section.

- Direct answer in the first one or two sentences; thesis before narrative.
- Key takeaways block near the top.
- One idea per heading; a section should make sense quoted on its own.
- Statistics with source and year; expert quotes with name and role; claims structured as "[topic] is [claim]. [Source] found [evidence]. This means [implication]."
- Named author with credentials, reviewer where possible, visible "last updated" date, current year in titles of time-sensitive topics.
- FAQ questions phrased the way people type prompts.
- Definition, step list, comparison table, pros and cons, and listicle blocks that match the query shape (patterns in `references/aeo-geo-patterns.md`).
- Embed or link a relevant video where it adds context; AI engines cross-reference video transcripts.
- Repurpose onto surfaces AI engines read (community threads, Q&A sites, LinkedIn, YouTube) with attribution back to the page.

## 8. Remove AI writing tells

Before finishing, scan for the patterns in `references/ai-writing-tells.md`: em dashes, "delve", "leverage", "robust", "in today's fast-paced world", "it's worth noting", "whether you're a X, Y or Z", "not just X, it's Y", sentences starting with "By [gerund]", triplets everywhere, empty intensifiers. Replace with plain words, commas, colons or parentheses. Vary sentence structure. Cut filler.

## 9. Optimize pass (existing or new content)

Score and report, then fix. Use the checker on the live page when it exists.

- Keyword placement map (H1, first 100 words, H2 count, body, conclusion, meta).
- Structure (one H1, 4 to 7 H2, no skipped levels, section balance).
- Links (internal count and anchors, external sources, broken links).
- Meta (lengths, keyword, uniqueness, click reason).
- Readability metrics.
- Answer-engine checklist (direct answer, takeaways, FAQ, author, date).
- Featured snippet chance: question H2 with a 40 to 60 word answer, numbered list of 5 to 8 items, or a comparison table.
- AI-tell scan.

Output: score out of 100 by category, critical fixes with exact location, quick wins, strategic improvements, three meta title and description options, internal link suggestions with placement and anchor text, publishing status (ready, minor fixes, revision).

## 10. Refresh strategy

Refresh when a piece is 12+ months old, statistics are stale, practice changed, competitors passed it, or rankings declined. Keep what works, update numbers and screenshots, add missing sections, fix links to newer content, re-target if the query shifted, and update the visible date only when the change is substantive. Do not touch a page that already ranks near the top for its query beyond fixing errors.

## Pre-publish checklist

- [ ] Brief followed; one intent; unique angle versus top results
- [ ] Direct answer first; key takeaways; FAQ in prompt language
- [ ] Keyword in H1, first 100 words, 2 to 3 H2s, conclusion, meta, slug
- [ ] 3 to 5 internal links with descriptive anchors; 2 to 4 external sources; all links work
- [ ] Title ~50 to 60 chars; description ~150 to 160 chars; both unique
- [ ] One H1; logical heading order; subheading every 300 to 400 words
- [ ] 8th to 10th grade; short paragraphs; lists and tables where they help
- [ ] Named author, date, sources; facts verified
- [ ] Images with descriptive names, alt text, compression
- [ ] Schema for the page type (Article, FAQPage) matches visible content
- [ ] No AI tells; brand voice held

## Guardrails

- Never pad to hit a word count. Never sacrifice accuracy for a keyword.
- Do not make claims without a source; mark anything unverified for the human reviewer.
- Do not plagiarise or paraphrase a competitor's structure wholesale; write a better answer to the same intent.
- Follow the project's banned words and voice rules in `seo-context.md`.
