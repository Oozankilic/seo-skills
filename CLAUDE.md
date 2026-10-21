# seo-skills

A library of SEO skills for AI coding agents. Nothing in this repo is an application; the deliverables are the `SKILL.md` files, the checker script and the templates.

## Layout

- `skills/<name>/SKILL.md`: one skill per directory. Frontmatter has `name` and `description`; the description is what triggers the skill, so it lists the phrases a user would say.
- `skills/<name>/references/*.md`: long material a skill links to (examples, pattern libraries, recipes). Keep `SKILL.md` under about 300 lines; move the rest here.
- `skills/seo/SKILL.md`: the entry point. It routes to the other skills and holds the shared principles. When you add a skill, add a row to its routing table and to `README.md`.
- `scripts/seo_check.py`: zero-dependency Python 3 site checker. Standard library only; do not add imports outside the standard library.
- `templates/`: files a project copies and fills in.
- `docker/`: Compose recipes for the self-hosted tools.
- `SOURCES.md`: attribution for the projects this repo distills.

## When you are using these skills in another project

Start with `skills/seo/SKILL.md`. Fill `templates/seo-context.md` for the project before auditing or writing. Run `scripts/seo_check.py` to get a baseline before and after changes.

## When you are editing this repo

- Write in plain, direct English. Short bullets, one idea each. No em dashes.
- Procedures over prose: an agent should be able to follow a skill top to bottom.
- Thresholds (character counts, link counts, word counts) are guidance, not law. Say so where it matters.
- Never add a claim about how search engines work that you cannot source to Google documentation or to the projects in `SOURCES.md`.
- After changing `scripts/seo_check.py`, run it against a live site and a local HTML directory:

```bash
python3 scripts/seo_check.py https://example.com --max-pages 5
python3 scripts/seo_check.py --dir /path/to/built/site
```
