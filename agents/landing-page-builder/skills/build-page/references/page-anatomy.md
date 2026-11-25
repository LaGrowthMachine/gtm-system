# Page anatomy

The section stack of each page type. The validated structure of the master decides the final list. This file checks
that nothing required is missing. Sections marked **required** are always there.

## The universal stack

| # | Section | Status | Background |
|---|---|---|---|
| 1 | Header | required | as the hero |
| 2 | Hero (angle + guide + primary action) | required | dark |
| 3 | Problem, or before and after | recommended | light |
| 4 | Pillars or use cases (cards grid, 4 at most) | recommended | light alt |
| 5 | Proof (logos with a number, reviews, a story) | required when you have it | light |
| 6 | How it works, or steps to switch | when the action needs it | light alt |
| 7 | FAQ | recommended | light, centered |
| 8 | Final call to action | required | dark |
| 9 | Footer | depends on the type | dark |

Alternate the light backgrounds. Never two consecutive sections of the same color, unless the blocks inside look
clearly different. Dark at the top and at the bottom bookends the page.

## The header by page type

| Page type | Header | Footer |
|---|---|---|
| Ads conversion page | Logo (clickable to the home page) + one call to action. No menu | None or a single line |
| SEO, product, comparison page living on the site | The site navigation, provided by the site builder: draft a placeholder bar only | The site footer, same |
| Webinar registration | Logo + "Register" | One line |

## Defaults by page type

### Ads conversion page (search, AI-chat ads, social retargeting)
Header · Hero with email form · Logo bar · Problem or comparison · Pillars (2x2) · Proof · FAQ (3-4) · Final call to
action with form · Sticky mobile bar. Only the hero changes between variants; the rest follows the arc.

### Product or feature page (an integration, one feature, an installable tool)
Header · Hero with the primary action (signup, or install tabs when the product installs by command or URL) · Before
and after · Use cases (4 cards) · Proof · FAQ · Final call to action. When the hero holds the install, every later
button anchors back to it.

### SEO page (answers a query, ranks)
Site header · Hero that names the query in plain words · The answer, early, in plain prose · Sections that answer the
"People also ask" questions · Proof · FAQ (the SERP questions) · Final call to action. Indexed: no noindex.

### Comparison or alternative page
Header · Hero ("The Rivalboard alternative" or "Acme vs Rivalboard") · Comparison table (sourced and dated if prices
show) · What the competitor does well, where it blocks · Pillars where you win · Proof from people who switched ·
Steps to switch · FAQ (objections, migration) · Final call to action.

### Webinar registration
Header · Hero (the result the session gives, date and time, form) · What you will leave with (3 points) · Who speaks
(face and role) · Final form.

### Case study
Header · Hero (customer and the outcome in their words) · The challenge · The approach (3 steps) · The results ·
Quote with a face · Call to action "Get this for your team".

### Hub or catalogue
Header · Hero with 2 actions (start, browse) · Catalogue by category · How to start · FAQ · Final call to action.

## Rules on the anatomy

- **The primary action is anchored.** It has an `id` in the hero (`hero-cta`, `install`, `register`). Buttons lower
  on the page anchor back to it instead of repeating it, except the final call to action, which repeats the form.
- **4 cards at most** in a grid. Beyond that, choice paralysis: cut, or link to the full list.
- **The FAQ is centered** and narrow (about 760px).
- **Trust signals sit right under the primary action** (free trial, no card, read-only mode), not scattered.
- **Every section carries a box of the arc.** A section that carries none goes.
