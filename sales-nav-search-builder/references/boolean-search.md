# Boolean Search Guide

Boolean operators let the user target prospects with surgical precision in 3 Sales Navigator fields: `KEYWORDS`, `CURRENT_TITLE`, `PAST_TITLE`. This guide is for Claude when constructing or validating boolean strings.

## Where Boolean works

| Field | Type name | What it searches |
|---|---|---|
| Keywords (global search bar) | `KEYWORDS` | Entire profile: headline, summary, every job description, skills, education |
| Current job title | `CURRENT_TITLE` | Job titles marked "Present" only |
| Past job title | `PAST_TITLE` | Job titles with a defined end date |

**Rule of thumb**: prefer `CURRENT_TITLE` when targeting people in their current role. `KEYWORDS` is a shotgun — broader reach but noisier. `PAST_TITLE` is rarely useful except for niche plays (e.g., "ex-Salesforce" prospects).

## The 5 operators

```
AND       both terms must match              CMO AND SaaS
OR        either term matches                CMO OR "Chief Marketing Officer"
NOT       exclude term                       CMO NOT Fractional
"..."     exact phrase (straight quotes)     "Head of Growth"
(...)     grouping                           (CMO OR CRO) AND SaaS
```

**Precedence (highest to lowest)**: `()` > `""` > `NOT` > `AND` > `OR`

When in doubt, wrap groups in parens. LinkedIn evaluates left-to-right within the same precedence level.

## Hard rules — non-negotiable

1. **Operators MUST be uppercase**: `AND`, `OR`, `NOT`. Lowercase `and` is treated as a search term, not an operator.
2. **Only straight quotes** (`"`). Curly quotes (`"` `"`) silently break the query. Beware of copy-paste from Notion, Google Docs, Word — they auto-curl quotes.
3. **No wildcards**. `Manag*` does not match Manager/Management. Use OR: `(Manager OR Management OR Managing)`.
4. **No proximity operators**. NEAR, BEFORE, etc. don't exist.
5. **Stop words are ignored**: `by`, `in`, `with`, `the`, `a`, `an`, `to`, `for`, `of`, `on`, `and` (lowercase). LinkedIn drops them silently. So `"Head of Sales"` is matched as `Head Sales` — usually fine but worth knowing.
6. **Operator limit**: ~15 operators per field. Past that, LinkedIn truncates or rejects.
7. **Character limit**: ~2,000 characters per field.
8. **Nesting limit**: 3-4 levels of parens max. Deeper nesting causes unpredictable behavior.

## Common B2B prospecting patterns (reusable building blocks)

### C-suite role normalization

People list the same job differently. Always normalize:

```
CMO equivalents:
("CMO" OR "Chief Marketing Officer" OR "Head of Marketing" OR "VP Marketing" OR "VP of Marketing")

CRO / Head of Sales equivalents:
("CRO" OR "Chief Revenue Officer" OR "Head of Sales" OR "VP Sales" OR "VP of Sales" OR "SVP Sales")

CEO / Founder equivalents:
(CEO OR "Chief Executive Officer" OR Founder OR Co-Founder OR "Co-Founder" OR Owner)

CFO equivalents:
(CFO OR "Chief Financial Officer" OR "Head of Finance" OR "VP Finance")

CTO equivalents:
(CTO OR "Chief Technology Officer" OR "VP Engineering" OR "Head of Engineering")
```

### Sales/RevOps mid-management

```
("Head of Sales Operations" OR "Sales Operations Manager" OR "Sales Ops" OR "RevOps" OR "Revenue Operations" OR "Head of Revenue Operations")

("SDR Manager" OR "BDR Manager" OR "Head of SDR" OR "Head of BDR" OR "Sales Development Manager")

("Growth Manager" OR "Head of Growth" OR "Growth Marketing Manager" OR "Demand Generation Manager")
```

### Standard exclusions ("noise filter")

Always exclude these when targeting full-time decision-makers:

```
NOT (Fractional OR Freelance OR Consultant OR Advisor OR Intern OR Assistant OR Student OR Junior OR Retired OR Former OR Ex)
```

The "Fractional CMO" pattern is the most common false positive — many guides flag this explicitly.

### B2B SaaS context filter (for KEYWORDS field)

When you need to narrow to B2B SaaS prospects via the keywords search:

```
(SaaS OR "B2B" OR "Software" OR "Platform" OR "Cloud") AND ("subscription" OR "MRR" OR "ARR" OR "pipeline")
```

## Composition patterns

### Pattern 1 — Multi-title decision-makers, clean

```
(CMO OR "Chief Marketing Officer" OR "VP Marketing" OR "Head of Marketing") NOT (Fractional OR Freelance OR Intern OR Assistant)
```

Use case: targeting marketing leaders for an outbound campaign without getting Fractional CMOs.

### Pattern 2 — Function + Seniority + Domain

```
(Director OR VP OR "Vice President" OR Head) AND (Sales OR Revenue OR "Go-to-Market" OR "GTM") NOT (Assistant OR Intern OR Junior)
```

Use case: senior commercial leaders, agnostic on exact title.

### Pattern 3 — Specific tools/skills (KEYWORDS field)

```
("Sales Navigator" OR "outbound" OR "LinkedIn automation" OR "cold email") AND ("SDR" OR "BDR" OR "Sales Development")
```

Use case: finding people who actively use outbound tools — strong signal of a mature outbound function.

### Pattern 4 — Tech stack signal (KEYWORDS field)

```
(Salesforce OR HubSpot OR Pipedrive) AND (Outreach OR Salesloft OR "Sales Navigator" OR Apollo)
```

Use case: people who mention specific tools in their profile — signal of a mature outbound stack.

## Common mistakes Claude must avoid

| Mistake | Wrong | Right |
|---|---|---|
| Lowercase operators | `CMO or Founder` | `CMO OR Founder` |
| Curly quotes | `"Head of Sales"` | `"Head of Sales"` |
| Multi-word without quotes | `Head of Sales OR Director` | `"Head of Sales" OR Director` |
| Wildcards | `Manag*` | `(Manager OR Management)` |
| Missing parens for OR | `CMO OR CRO AND SaaS` | `(CMO OR CRO) AND SaaS` (otherwise precedence gives `CMO OR (CRO AND SaaS)`) |
| Over-nesting | `((((A OR B) AND C) OR D) AND E)` | flatten when possible |
| Negating without parens | `NOT Assistant OR Intern` | `NOT (Assistant OR Intern)` |

## Decision tree for Claude

When the user describes a role, ask yourself:

1. **Is the role likely written in multiple ways?** → wrap variants in `(... OR ... OR ...)`
2. **Is there a common false positive?** → add `NOT (...)` at the end
3. **Is the role multi-word?** → wrap in straight quotes
4. **Is precedence ambiguous?** → wrap groups in parens
5. **Did I use 15+ operators?** → split into two searches or trim

Always run the result through `scripts/validate_boolean.py` before encoding it into the URL. Validation catches lowercase operators, unbalanced parens, curly quotes, wildcards, and operator-count overruns.

## Where Boolean does NOT work

These filters are enum-based or entity-based — boolean strings have no effect:
- Industry, Function, Seniority, Headcount, Company type
- Region/Geography, Profile language
- Current/Past company (entity URN), School, Groups
- All toggle filters (Changed jobs, Posted on LinkedIn, etc.)

Trying to put `("Software" OR "SaaS")` in the Industry filter will not work — Industry takes an ID, not a string. Use the enum reference instead.
