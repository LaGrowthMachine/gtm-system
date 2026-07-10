# Won-Deal ICP Finder

> Turn your closed-won deals into a proven ideal customer profile — then go find more accounts like them.

Maintained by [La Growth Machine](https://lagrowthmachine.com). Free to use. Updated: 2026-05-25.

## What it does

Most teams prospect against the ICP they *assume*. This skill builds the ICP your revenue *proves*. Point it at your deals and it ranks your biggest wins from the last 12 months by deal value — selecting them by value rather than a closed-won status that may not exist in your CRM — finds where acquisition source actually lives in your HubSpot (standard or custom field), clusters the winning companies into a handful of named **ICP archetypes** — each with objective criteria and a one-click way to find more like it — and ranks the acquisition sources behind your biggest deals.

Example: you point it at your won deals and it surfaces two archetypes — "mid-market FinTech & SaaS in FR/DE" and "large-enterprise Logistics" — each with a "find more companies like this" button, then shows that LinkedIn produced the most of your big deals. If your CRM can't tell you *which campaign* won them, it flags that gap.

## Why it exists

"Who are our best customers, and how do we find more of them?" is the question behind every account-based targeting plan, ICP refresh and QBR — and it's usually answered from memory. Doing it properly means summing revenue per account across multiple deals, separating the whales from a repeatable motion, and reading which channel truly produced the money (not which one gets the credit). That's slow to do by hand and easy to get wrong. This skill does the arithmetic deterministically and leaves you the judgment.

## Install

**One-line (recommended)** — uses [`skills`](https://github.com/vercel-labs/skills) from Vercel Labs to install into Claude Code, Cursor, Codex, Amp + 30 other agents in one go:

```bash
npx skills add LaGrowthMachine/gtm-system/skills/fuel-my-pipeline/won-deal-icp-finder
```

Add `-g` for a global install.

**Manual install** — clone the repo and copy the skill folder yourself:

```bash
git clone https://github.com/LaGrowthMachine/gtm-system.git
cd gtm-system
cp -r skills/fuel-my-pipeline/won-deal-icp-finder ~/.claude/skills/
```

Then ask Claude — e.g. *"Audit my biggest HubSpot deals and tell me my proven ICP."*

## What's supported

- HubSpot deal pull via the HubSpot MCP, or a HubSpot CSV export (no connector needed).
- Value-based selection that works whether or not your CRM uses a closed-won status: it picks deals carrying a value in the last 12 months, detects a won stage/flag if one exists, and always excludes lost deals.
- Deal-value discovery: finds the field that holds value when it isn't the standard `amount` (override with `--value-field`).
- Acquisition-source discovery: finds the right field across deal / company / contact, standard or custom (override with `--source-field`).
- ICP archetypes — named, criteria-based company clusters, each with a one-click "find more like this" via `sales-nav-search-builder`.
- Top acquisition sources ranked by frequency, with the value behind each, plus a flag when there's no campaign-level detail.
- Revenue concentration (top-1 / top-5 / top-10 share) and segmentation by industry, size bucket and geography — whichever fields your data carries.
- Robust amount parsing (`$1,234.56` and `1 234,56 €`), a configurable time window (`--since-days`, default 365), and clear refusals that tell you to confirm the value/won fields rather than guessing.

## What's not supported

- It analyzes the deals you give it; it doesn't pull or enrich data on its own beyond a HubSpot MCP fetch.
- It won't invent firmographics your CRM doesn't store — missing industry/size fields are reported, not guessed.
- It is not a statistics package: with very few won accounts, it labels conclusions as directional.

## Who it's for

- **RevOps** running ICP refreshes and account-based targeting.
- **Heads of Sales / Marketing** validating where the revenue actually comes from before the next QBR.
- **Founders** in founder-led sales who want to formalize the customers they keep winning.
- **Growth leads** deciding which channel and segment to double down on.

## Limitations

- The acquisition-channel breakdown is only as good as the source data on your deals. If your CRM's source fields are thin, the channel ranking is partial — the skill tells you when that's the case.
- The HubSpot MCP is HubSpot's own connector; the CSV fallback works with no connector at all.
- Value is read from your deal-value field (`amount` by default; point it elsewhere with `--value-field`, e.g. ARR/ACV or a custom field).

## Works with

This skill runs standalone with any stack. It also plugs into:

- **HubSpot MCP** — pulls your recent won deals and company firmographics, and introspects the schema to find where acquisition source lives, so you skip the export.
- **sales-nav-search-builder** — the companion skill behind each archetype's "find more companies like this" button; turns an ICP archetype into a ready LinkedIn Sales Navigator search.
- **La Growth Machine** — its native HubSpot integration writes the exact campaign behind each deal back into your CRM, so you can see which outreach produced your best deals and scale it — then run that outreach across LinkedIn, email, voice and calls.

## Stay in the loop

- Browse all GTM skills: [the GTM System catalog](../../../README.md)
- Get new skills as they ship: [Subscribe](https://tally.so/r/NpRWgp)
- See how La Growth Machine fits your GTM stack: [Try LGM free](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=won-deal-icp-finder)

## License

MIT — see the LICENSE at the repo root.

## About La Growth Machine

La Growth Machine is the multichannel outbound platform behind these skills — it turns GTM work like this into running outreach across LinkedIn, email, Twitter and phone, from one place.

---

Topics: proven ICP, ideal customer profile, closed-won analysis, best customer analysis, won deal audit, revenue by account, customer segmentation, look-alike accounts, account-based targeting, HubSpot deal analysis, acquisition source analysis, channel attribution, ICP refinement, RevOps analysis, pipeline review
