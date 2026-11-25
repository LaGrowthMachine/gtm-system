# From the arc to the structure of the page

The structure is a table the user approves before any HTML. Each row is a section, each section carries a box of the
arc. The patterns behind each section are in `{SKILL_BASE}/skills/build-page/references/section-patterns.md`, the
stacks by page type in `page-anatomy.md` next to it.

## Arc box → section

| # | Section | Box | What it carries |
|---|---|---|---|
| - | Header | - | Logo clickable to the home page + the primary call to action. No demo button |
| 1 | Hero | entry angle + 6 | H1 on 2 lines · the query in plain words (search) · subline = the guide · the form · the trust line · a proof line (ratings, customer count) · visual = the interface that shows the promise |
| 2 | Logo bar | 7 | 6 to 9 customer logos with a number; on desktop traffic, a result per logo on hover |
| 3 | Problem or comparison | 3 (+7) | One line of problem, or the comparison table (a competitor with a sourced price, or categories of tools) |
| 4 | Why us (2x2 grid, cards of the same height) | 4 → 6 | 4 pillars in the order of the hero's work, each with a small interface that shows the result |
| 5 | Proof | 7 | Stories or 3 reviews word for word. Can shrink to the logos on hover |
| 6 | Get started in N steps | 8 | Conquest: switching in 3 or 4 steps, with an anchor `id` the hero links to |
| 7 | FAQ | 5 | 3 or 4 questions: the main objection, the switch, "what happens after the trial", one SERP question |
| 8 | Final call to action | 8 | Title = the transformation, the form, a discreet demo link under it |
| - | Sticky mobile bar | - | The call to action, shown when the hero form leaves the screen |

"Only the hero changes between variants, the rest follows the arc." Remove a section rather than add one. A section
that carries no box of the arc goes.

## The structure table

The user approves this table (🔒). Write it in the arc file, section "Structure vN".

```markdown
Rules of this page: <query in plain words> · <price: sourced and dated / none> · <...>.

| # | Section | Arc box | Content | Taken from |
|---|---|---|---|---|
| 1 | Hero | angle + 6 | H1 "The Rivalboard alternative. / Plans your team can read." · form · Free trial · No credit card | new |
| 2 | Logos | 7 | 8 logos, "2,000+ teams" | landing `rival-alt` v2 |
| 3 | Comparison | 3 + 7 | 6 rows, price sourced and dated | new, price checked on <date> |
| ... | | | | |

Removed compared with <base>: ... · To check with the product team: ...
```

"Taken from" names the existing page, the section of a reference page (its substance only) or "new".

## What makes a good structure

| Check | Why |
|---|---|
| One goal: every button leads to the primary action | Every other link leaks visitors |
| The idea is understood in a few seconds | Visitors from an ad decide on the first screen |
| One title per section, the problem in one line | A sales page goes to the essential |
| No "step by step" section when a 2x2 grid says it | Fewer sections, more read |
| Search: each SERP question has its place on the page | The visitor came with that question |
| Search: the query is written in plain words on the first screen | The visitor checks they are in the right place |
| Conquest: the visitor who typed a competitor name looks for an alternative | The page answers "alternative", not "who we are" |
| Every section carries a box of the arc | The page stays one story |

Several rounds on the structure are normal. Answer each numbered point, then show the new table.
