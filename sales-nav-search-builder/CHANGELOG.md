# Changelog

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] — 2026-05-18

Initial public release.

### Features

- Generate Sales Navigator search URLs from a JSON spec
- 10 ID-based enum filters with full LinkedIn reference mapping:
  - Industry (350+ entries)
  - Function (26)
  - Seniority level (10)
  - Company headcount (9)
  - Company type (8)
  - Years in current company / Years in current position / Years of experience (5 ranges each)
  - Profile language (22)
  - Region (country list covering the COUNTRY_REGION level of LinkedIn's Bing Geo taxonomy — see `references/geo-locations.md` for schema and extension)
- 5 text filters: First name, Last name, Current job title, Past job title, Keywords
- Boolean search support in Keywords, Current job title, and Past job title:
  - AND, OR, NOT, "...", (...) operators
  - Automatic validation: balanced parens, balanced quotes, uppercase operators, curly quote detection, wildcard detection, operator count (≤15), character count (≤2,000), nesting depth (≤4), stop word warnings, multi-word phrase warnings
- 4 toggle filters: Changed jobs, Posted on LinkedIn, Past colleague, Follows your company
- INCLUDED / EXCLUDED selection types for every filter
- Comprehensive boolean patterns guide for common B2B prospecting use cases (C-suite normalization, fractional/freelance exclusion, tool stack signals)
- Regression tests that reproduce 5 real Sales Navigator URLs (captured November 2026 — May 2026): multi-enum filters, text + toggles, CURRENT_TITLE boolean, PAST_TITLE boolean, and KEYWORDS top-level (with `spellCorrectionEnabled:true`)
- 4 ready-to-run example specs: marketing leaders, sales/RevOps with tool stack, founders, recent job changers
- Integration with the [La Growth Machine MCP](https://mcpapp.lagrowthmachine.com/mcp) via the `import_lead_from_linkedin_search` tool for one-click lead import from the generated URL

### Architecture notes

- `KEYWORDS` is structurally different from all other filters: it lives at the top level of the query object as `keywords:<value>` (not wrapped in `filters:List`), paired with `spellCorrectionEnabled:true`. The builder extracts KEYWORDS from the spec before constructing the `filters:List` block. This was verified against a live captured URL.

### Known limitations

- Filters that require LinkedIn entity URN lookup are out of scope: Current/Past company, geography beyond the curated country list, School, Groups, Persona, Account/Lead lists, Connections of.
- Boolean patterns are English-oriented. For non-English titles, adapt to local equivalents.
