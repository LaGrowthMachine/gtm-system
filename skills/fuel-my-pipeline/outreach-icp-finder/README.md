# Outreach ICP Finder

> Turns the outreach you already ran — who you contacted, who replied, who showed interest — into a proven ideal customer profile, a "stop contacting" list, and a one-click search for more of the people who actually reply.

Maintained by [La Growth Machine](https://lagrowthmachine.com). Free to use. Updated: 2026-09-07.

Built with the La Growth Machine Creator cohort — thanks to **Jude** and **Bolaji** for the use cases that shaped it.

## What it does

You point it at your outreach data — your La Growth Machine workspace through its MCP, or a CSV export from whatever tool you prospect with — and ask:

> "Who actually replies to my cold outreach? Which job titles, industries and company sizes should I double down on, and which ones am I wasting touches on?"

The skill assembles one row per contacted lead (job title, industry, location, company size, campaign, accepted, replied, reply label), labels replies where your tool didn't (interested / not now / not interested / out of office / other), and runs a deterministic engine that computes reply and positive-reply rates per segment with 95% confidence intervals, lift against your baseline, and a check for segments that only look good because one strong campaign targeted them. You get 2–3 named ICP archetypes proven by your own replies, each with a "find more people like this" button that builds the matching LinkedIn Sales Navigator search, plus the segments measurably below baseline — the ones to stop contacting.

## Why it exists

Most ICPs are written before the first campaign and never checked against what happened. Meanwhile the answer is sitting in the outreach tool: hundreds or thousands of contacted leads, each with a title, a company and a yes/no on whether they replied. Nobody analyzes it because the exports are messy, the segments are small, and it's easy to fool yourself — a segment "with a 25% reply rate" is often 4 replies out of 16, or a persona that one good campaign happened to target.

This skill does the analysis properly: it pools segments that are too small to say anything, shows intervals instead of point estimates, separates real interest from polite refusals, and flags campaign confounding before it becomes a targeting decision. It also tells you what your data *can't* say — which attributes were missing on your leads — because a profile with a blind spot is worth knowing about.

## Install

**One-line (recommended)** — uses [`skills`](https://github.com/vercel-labs/skills) from Vercel Labs to install into Claude Code, Cursor, Codex, Amp + 30 other agents in one go:

```bash
npx skills add LaGrowthMachine/gtm-system/skills/fuel-my-pipeline/outreach-icp-finder
```

Add `-g` for a global install.

**Manual install** — clone the repo and copy the skill folder yourself:

```bash
git clone https://github.com/LaGrowthMachine/gtm-system.git
cd gtm-system
cp -r skills/fuel-my-pipeline/outreach-icp-finder ~/.claude/skills/
```

Then ask Claude — e.g. *"Here's my lemlist export from the last 4 months — who actually replies, and who should I stop contacting?"* or, with the La Growth Machine MCP connected, *"Analyze my campaigns since March and tell me my real ICP."*

**Prerequisites:** [Claude Code](https://claude.com/product/claude-code) (or any other supported agent) and Python 3 for the analysis engine. For the "find more like this" button, install the sibling skill [`sales-nav-search-builder`](../sales-nav-search-builder/README.md).

## What's supported

- **Three data lanes** — the La Growth Machine MCP (campaign logs + lead attributes + a labeled sample of real replies), a CSV export from any sales engagement or cold-outreach tool (lemlist, Instantly, Smartlead, HeyReach, Apollo, Waalaxy, Expandi, Outreach, Salesloft…), or another tool's MCP mapped to the same columns. Headers are matched loosely in English and French.
- **Job-title normalization** — 8 seniority levels (Owner / Founder, C-level, VP, Director / Head, Manager / Lead, Senior IC, Individual contributor, Entry) and 12 functions (Sales, Marketing / Growth, RevOps / GTM Ops, General management, Product, Engineering / Data, Finance, People / HR, Customer Success, Consulting, Operations, Legal), EN/FR/DE title patterns, editable in `references/title-taxonomy.json`.
- **Reply labeling** — a fixed five-label vocabulary (POSITIVE, NOT_NOW, NEGATIVE, OOO, OTHER); tool-native labels ("Interested", "Not interested", "Meeting booked", "Pas intéressé"…) are normalized automatically.
- **Statistically guarded engine** (`scripts/analyze.py`) — Wilson 95% intervals, lift vs baseline, minimum-volume pooling (30 contacted leads per segment by default), campaign-confounding detection with a stratified lift, 2-D crosstabs, attribute-coverage reporting, and explicit refusals when the data is too thin (fewer than 100 contacted leads or 20 replies). Ships a regression suite (`--test`).
- **Actionable output** — 2–3 ICP archetypes as cards with a "find more people like this" button (routes to `sales-nav-search-builder`), a "stop contacting" list, and the data gaps that limit the profile.

## What's not supported

- Revenue-based ICP (which customers *paid* the most) — that's the sibling skill [`won-deal-icp-finder`](../won-deal-icp-finder/README.md). This one is about engagement upstream of the deal.
- Company-size data when the source doesn't carry it (LinkedIn-only tools and La Growth Machine lead records don't) — the dimension is skipped and reported as a gap.
- Message-level A/B analysis (which copy performs) — see `campaign-challenger` and `campaign-impact-analyzer`.
- Automatic reply labeling at scale: labeling is done on a bounded sample (typically up to 120–150 replies) so the run stays fast; unlabeled replies still count as replies.

## Who it's for

- **SDRs and BDRs** who want to know which titles and industries actually answer them.
- **Heads of Sales and Growth** refining the ICP with evidence before the next quarter's targeting.
- **RevOps and GTM engineers** auditing a lead reservoir or a data vendor's list quality.
- **Founders** doing their own outbound and wondering who to stop contacting.
- **Agencies and freelance GTM consultants** proving to a client which personas respond — from the client's own data.

## Limitations

- **You only learn about who you contacted.** The profile is your ICP *within the universe you targeted*; a persona you never reached can't appear. The output says so.
- **Volume matters.** Below ~100 contacted leads and ~20 replies the engine refuses rather than guess. Below a few hundred leads, expect many segments to be "inconclusive" — that's an honest answer, not a bug.
- **Reply ≠ interest** unless replies are labeled. Without labels the engine profiles on any reply and says so; label them (or use a tool that does) to profile on real interest.
- **Attribute coverage depends on the source.** Cold-email exports often carry email + company only; the persona side of the ICP is then blind, and the report tells you.
- **Confounding is flagged, not eliminated.** A segment concentrated in one campaign gets a stratified lift; with only one campaign in the data, no check is possible.

## Works with

This skill runs standalone with any stack. It also plugs into:

- **La Growth Machine MCP** — pulls campaign outcomes per lead from your workspace's activity logs, hydrates lead attributes from your audiences, labels a sample of real reply threads, and, once the profile is built, turns an archetype into a ready-to-use audience in one click.
- **`sales-nav-search-builder`** (sibling skill) — each archetype's "find more like this" button builds the matching LinkedIn Sales Navigator search.
- **`won-deal-icp-finder`** (sibling skill) — cross-check the engagement ICP against the revenue ICP from your CRM.

## Stay in the loop

- Browse all GTM skills: [the GTM System catalog](../../../README.md)
- Get new skills as they ship: [Subscribe](https://tally.so/r/NpRWgp)
- See how La Growth Machine fits your GTM stack: [Try LGM free](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=outreach-icp-finder)

## License

MIT — see the LICENSE at the repo root.

## About La Growth Machine

La Growth Machine is the multichannel outbound platform behind these skills — it turns GTM work like this into running outreach across LinkedIn, email, voice and calls, from one place.

---

Topics: ideal customer profile, ICP analysis, reply rate by segment, who replies to cold outreach, positive reply rate, outbound analytics, cold email analysis, LinkedIn outreach analysis, lead engagement analysis, persona analysis, job title analysis, sales engagement data, lemlist export, Instantly export, Smartlead export, HeyReach export, outbound targeting, data-driven ICP, B2B prospecting, SDR analytics, RevOps
