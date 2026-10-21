# Answer engine and AI citation content patterns

Reusable blocks for featured snippets, People Also Ask, voice answers, Google AI Overviews and citations in ChatGPT, Perplexity, Claude and Gemini.

## Answer engine patterns (featured snippets, PAA, voice)

### Definition block ("What is X?")

```markdown
## What is [term]?

[Term] is [one-sentence definition]. [One or two sentences on key characteristics]. [Why it matters or how it is used].
```

Keep the first sentence under about 40 to 60 words in total for the block. Google lifts paragraph snippets from exactly this shape.

### Step-by-step block ("How to X")

```markdown
## How to [goal]

[One-sentence overview.]

1. **[Step name]**: [one or two sentence action]
2. **[Step name]**: [one or two sentence action]
3. **[Step name]**: [one or two sentence action]

[Optional: expected outcome or time estimate.]
```

Five to eight steps is the usual list snippet length.

### Comparison table ("X vs Y")

```markdown
## [A] vs [B]: [descriptor]

| Criterion | [A] | [B] |
|-----------|-----|-----|
| [1] | ... | ... |
| [2] | ... | ... |
| Best for | ... | ... |

**Bottom line**: [one or two sentence recommendation by need].
```

### Pros and cons ("Is X worth it?")

```markdown
## Advantages and disadvantages of [topic]

### Pros
- **[Benefit]**: [specific explanation]

### Cons
- **[Drawback]**: [specific explanation]

**Verdict**: [balanced one or two sentences].
```

### FAQ block

```markdown
## Frequently asked questions

### [Question exactly as people ask it]?

[Direct answer in the first sentence.] [Two or three sentences of support.]
```

Use natural phrasing ("How do I..." not "How does one..."), question words, PAA and community questions. 50 to 100 words per answer. Pair with `FAQPage` schema when the questions are visible.

### Listicle ("Best X", "N ways to X")

```markdown
## [N] best [items] for [purpose]

[One or two sentences on selection criteria.]

### 1. [Item]
[Why it is included, two or three sentences with specifics.]
```

## Generative engine patterns (citations in AI answers)

### Statistic with source

```markdown
[Claim]. According to [organisation, year], [specific number and timeframe]. [Why it matters].
```

Sourced statistics measurably raise citation rates. Always name the source.

### Expert quote

```markdown
"[Direct quote]," says [Name], [role] at [organisation]. [One sentence of interpretation].
```

### Authoritative claim

```markdown
[Topic] [is / requires / involves] [specific claim]. [Source] [found / reports] [evidence]. This means [implication or action].
```

### Self-contained answer

```markdown
**[Topic or question]**: [complete answer that stands alone without the rest of the page, with a number or example, in two or three sentences].
```

### Evidence sandwich

```markdown
[Claim].

Evidence:
- [Data point with source]
- [Data point with source]
- [Data point with source]

[Conclusion that turns the evidence into an action].
```

## Page-level signals AI engines weigh

- Direct answer in the first one or two sentences of the page and in the meta description.
- Key takeaways block near the top with specific, standalone claims.
- One idea per H2 or H3 so a section can be cited alone.
- Named author with credentials, reviewer credit, visible last-updated date, year in time-sensitive titles.
- Primary content in server-rendered HTML; no login or JavaScript-only content.
- Video embed or link that covers the same topic (cross-validation).
- Presence on the surfaces AI engines read: community threads, Q&A sites, directories, review sites, YouTube.

## Domain-specific authority signals

- **Technology**: precise terminology, version numbers and dates, links to official docs, code samples.
- **Health**: peer-reviewed sources with publication details, credentials (MD, RN), study limits, review dates.
- **Finance**: regulators named, numbers with timeframes, "educational, not advice" note, recognised institutions.
- **Legal**: statutes and jurisdiction named, disclaimers, when to consult a professional.
- **Business and marketing**: case studies with measured results, industry reports, percentages with timeframes, named practitioners.

## Voice search

Conversational question forms ("what is", "how do I", "where can I", "why does", "when should I"). Lead with an answer under 30 words in plain language; include local context where relevant.
