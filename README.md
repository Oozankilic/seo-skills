# seo-skills

SEO skills for AI coding agents (Claude Code, Codex, Cursor, OpenClaw and any agent that reads `SKILL.md` files).

Install this repo into a web project and the agent gains a complete, opinionated SEO playbook: how to audit a site, fix the technical foundations, research and map keywords, write pages that rank and get cited by AI answer engines, add structured data, build links, and monitor results with free, self-hosted tools instead of paid SaaS.

The knowledge is distilled from six open-source projects (see [SOURCES.md](SOURCES.md)): SEOnaut, SerpBear, OpenSEO, SEOMachine, SoPilot and the Awesome Open-Source SEO list.

## Install

**Agent Skills CLI (any agent)**

```bash
npx skills add Oozankilic/seo-skills
```

**Claude Code plugin**

```
/plugin marketplace add Oozankilic/seo-skills
/plugin install seo-skills@seo-skills
```

**Manual (any project)**

```bash
git clone https://github.com/Oozankilic/seo-skills.git /tmp/seo-skills
cp -r /tmp/seo-skills/skills/* .claude/skills/
```

Or add the repo as a git submodule and point your agent's skills path at `skills/`.

## Skills

| Skill | Use it when |
|-------|-------------|
| `seo` | Entry point. Decides which skill applies, holds the shared principles and the standard workflow. |
| `seo-audit` | "Why aren't we ranking?", health check, pre-launch review, migration check. Covers codebase and live-site audits. |
| `seo-technical` | Implement or fix meta tags, canonicals, robots.txt, sitemaps, redirects, Core Web Vitals, rendering, i18n. Framework recipes for Next.js, Astro, Nuxt, SvelteKit, Remix, WordPress, static HTML. |
| `seo-schema` | Add or fix JSON-LD structured data and rich results. |
| `seo-keyword-research` | Find, score, cluster and map keywords to pages. Spot cannibalization. Works with or without paid data. |
| `seo-content` | Write, rewrite or optimize a page or article: briefs, structure, meta elements, internal links, readability, answer-engine formatting, removing AI writing tells. |
| `seo-ai-visibility` | GEO/AEO: get cited in ChatGPT, Perplexity, Gemini and Google AI Overviews. AI crawler access, `llms.txt`, citation patterns, visibility audit. |
| `seo-programmatic` | Build many pages from templates and data without producing thin content. 12 playbooks. |
| `seo-local` | Google Business Profile, local pack, location pages, NAP consistency. |
| `seo-link-building` | Link prospecting, directory submissions, outreach drafts, backlink hygiene. |
| `seo-tooling` | The free, open-source stack: SEOnaut, SerpBear, OpenSEO, Lighthouse CI, linkinator, GoAccess and more. Docker recipes included. |

## Included tooling

- `scripts/seo_check.py`: zero-dependency Python crawler that audits a live site, a single HTML file, or a static build directory. Reports missing or duplicate titles and descriptions, heading problems, canonical issues, noindex, Open Graph gaps, images without alt, thin pages, broken internal links, redirect chains, invalid JSON-LD, robots.txt and sitemap status, and which AI crawlers are blocked.
- `templates/seo-context.md`: per-project context file (business, goals, keywords, key pages, competitors) that every skill reads first.
- `templates/internal-links-map.md`: catalog of link targets for internal linking.
- `docker/`: ready-to-run Compose files for SEOnaut (site audits) and SerpBear (rank tracking).

```bash
python3 scripts/seo_check.py https://example.com --max-pages 50
python3 scripts/seo_check.py --dir dist/
```

## Typical workflows

**New site or feature before launch**
1. `seo-technical`: head tags, canonical, robots, sitemap, OG, schema, CWV.
2. `scripts/seo_check.py --dir <build>` on the build output.
3. `seo-schema` for the page types that qualify for rich results.
4. After deploy: run the checker on the live URL, submit the sitemap, set up SerpBear.

**Existing site that should grow**
1. Fill `templates/seo-context.md` for the project.
2. `seo-audit`: shortlist five to ten opportunities, pick one to three.
3. `seo-keyword-research` to validate demand, `seo-content` to build or fix the pages.
4. `seo-ai-visibility` to check AI crawler access and citation gaps.
5. Monitor with SerpBear and Search Console.

**Content program**
1. `seo-keyword-research` to cluster and map.
2. `seo-content` per page: brief, draft, optimize pass, meta options, internal links.
3. `seo-link-building` for the linkable assets.

## Principles the skills share

- SEO serves the reader. Never trade accuracy or usefulness for a keyword.
- Research broadly, recommend selectively. Lead with one to three moves backed by evidence.
- Observations are not causes. A crawler warning does not prove a penalty.
- Never invent metrics. Write `unknown` when a tool returns nothing.
- Protect what already ranks. Do not rewrite a page that sits near the top for its query.
- One page, one intent. Split or merge pages by SERP intent, not by word similarity.
- AI answer engines are a traffic channel now. Direct answers first, cited facts, named authors, visible dates.

## Contributing

Each skill lives in `skills/<name>/SKILL.md` with optional `references/` for long material. Keep `SKILL.md` focused on procedure and decisions; put examples and lists in references. Run `python3 scripts/seo_check.py` against a site after changing the script.

## License

MIT. See [LICENSE](LICENSE). Source projects keep their own licenses, listed in [SOURCES.md](SOURCES.md).
