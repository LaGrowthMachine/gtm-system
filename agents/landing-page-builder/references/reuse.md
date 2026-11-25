# Reuse, translate, duplicate or create

Before writing a new page, check whether an existing one already answers. The registry is `landings/LANDINGS.md`:
read it before deciding, update it after every new page or new version.

## The test

For each main query (or each contextual hint of the ad), read the intent on the SERP, then ask whether the closest
existing page answers it: Yes, Partly or No. Write the table in the arc file, annex "Queries × page alignment".

| Result | Decision | Example (invented) |
|---|---|---|
| The page answers and the ads can align on it | **Reuse** as is, adjust the ads | - |
| Same arc, same mix of queries, another country or language | **Translate**, with what the country needs (currency, local reviews) | The English page translated to German, with two local reviews |
| The page misses the main query, and fixing the ads would mean dropping half the keywords | **Duplicate the closest page** under a new slug | `project-tool` missed 44% of the volume of "project tracking software": duplicated as `project-tracking` |
| Nothing close | **Create** from the most recent page as a technical base | - |

## Rules

- **One page per ad group** (AI-chat ads: one angle = one group = one page). Never the home page.
- **A page under test is frozen.** Do not change it: duplicate it. Note the end date of the test in the registry.
- **A colleague's page that covers the topic**: take its substance in your style, and tell them.
- **No overlap** between two live pages (same H1, same angle). If two arcs collide, write what sets each apart.
- **New version of a live page**: same slug, the old version kept in its folder (`index-v1.html`), `landing_version`
  raised, the switch date noted.

## Choosing the technical base

Take the most recent page that already has what the new one needs. Write the choice in the registry so the next page
starts from the best version.

| Need | Base to look for |
|---|---|
| Conquest (comparison table, competitor reviews themes, switching steps) | Your latest alternative page |
| Generic search (category of tools, table by type of tool) | Your latest category page |
| Persona or retargeting (before and after, stories) | The shortest and cleanest page |
| Integrations, stack | A page with a workflow and integration badges |
| Human support, services | A page with the people and how they help |

An old page with an older generation of components is never a base.

## The registry `landings/LANDINGS.md`

```markdown
| Slug | Type | Arc | Campaign or query set | Version | Status | Frozen until | Best version of |
|---|---|---|---|---|---|---|---|
| rival-alt | ads, conquest | arc.md v2 | Search · Rivalboard alternative | rival-alt-v3 | live since 2026-11-03 | 2026-12-01 (A/B test) | comparison table, switching steps |
```
