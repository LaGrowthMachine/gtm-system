# Campaign Impact Analyzer

> Rank your outreach campaigns by what actually drives pipeline — deals created, meetings booked — by cross-referencing La Growth Machine campaigns with your CRM deals.

Maintained by [La Growth Machine](https://lagrowthmachine.com). Free to use. Updated: 2026-05-26.

## What it does

You ask which campaigns are working. The skill pulls your campaigns (from La Growth Machine) and your deals (from HubSpot), matches each deal back to the campaign that touched the contact via a multi-key cascade (LGM lead ID → email → name + company), and ranks campaigns by **real revenue impact** — not by reply rate. For each campaign: a verdict (continue / stop / adapt / investigate) and the recommended next step.

Example: you ask "which of my campaigns is actually driving pipeline?" and the skill returns a widget with 4 KPI cards (campaigns analyzed, deals attributed, pipeline value, win rate), a ranked table with verdicts, and a callout naming the single top next step — e.g. *"Adapt 'Cold list — RevOps EMEA' — 15% reply rate but 1 deal on 60 leads; challenge the copy."*

## Why it exists

Reply rate is what most outreach tools rank by. But replies aren't revenue. A campaign with a 12% reply rate and 0 deals is a worse campaign than one with a 4% reply rate and 8 deals — and most teams can't see that easily because the campaign data lives in one tool and the deal data lives in another. This skill does that cross-reference in one pass, names which campaigns to continue, stop or adapt, and points at the single next move worth making.

## Install

**One-line (recommended)** — uses [`skills`](https://github.com/vercel-labs/skills) from Vercel Labs to install into Claude Code, Cursor, Codex, Amp + 30 other agents in one go:

```bash
npx skills add LaGrowthMachine/gtm-system/skills/get-qualified-meetings/campaign-impact-analyzer
```

Add `-g` for a global install.

**Manual install** — clone the repo and copy the skill folder yourself:

```bash
git clone https://github.com/LaGrowthMachine/gtm-system.git
cd gtm-system
cp -r skills/get-qualified-meetings/campaign-impact-analyzer ~/.claude/skills/
```

Then ask Claude — e.g. *"Rank my campaigns by deals."*

## What's supported

- **Cross-source ranking** — joins LGM campaigns with HubSpot deals on email (primary), LGM lead ID (strongest signal when set up), or first-name + last-name (lower confidence fallback).
- **Three input modes per side** (LGM, HubSpot) — MCP-connected (auto), or pasted CSV / export.
- **Per-campaign verdict** — continue / stop / adapt / investigate, with a one-line cited motive.
- **Pattern D dashboard** — KPI cards + ranked table + actionable callout in a single widget.
- **Adaptive next step** — if at least one campaign needs adapting, the CTA chains into `campaign-challenger` and `multichannel-campaign-builder` to diagnose and rewrite the weakest.
- **Multi-pipeline aware** — HubSpot accounts often have several pipelines; the skill asks which one to analyze when more than one is present.

## What's not supported

- CRMs other than HubSpot (Salesforce, Pipedrive, etc.) — paste exports for now, native support comes later.
- Native pause / duplicate of LGM campaigns from inside the skill — the LGM MCP doesn't expose those yet. The skill recommends what to do; you act in the app.
- Scheduled / recurring analysis (e.g. every Monday) — coming when the LGM MCP supports it.

## Who it's for

- **RevOps** running campaign attribution and pipeline reviews.
- **Heads of Sales / Marketing** defending campaign decisions with deal data, not reply rates.
- **Founders** running their own outbound who want to know what to scale and what to kill.
- **Growth leads** auditing channel and campaign ROI before reallocating budget.

## Limitations

- The cross-reference matches on **email** by default. Deals whose contact email doesn't appear in any campaign's leads come back as "non-attributed".
- For users without a CRM MCP, the skill needs a deal export pasted — the analysis is only as fresh as that paste.
- Pipeline value depends on how the CRM tracks deal amounts. Missing amounts → ranking falls back to deal count.

## Works with

This skill runs standalone — paste both datasets and it works. It also plugs into:

- **La Growth Machine MCP** — pulls your campaigns live (no CSV juggling).
- **HubSpot MCP** — pulls your deals live, with stages and pipeline value.
- **campaign-challenger** + **multichannel-campaign-builder** — for any campaign flagged "adapt", chain into them to diagnose the copy and rewrite the sequence in one go.
- **La Growth Machine** — its native HubSpot integration writes the exact campaign behind every deal back into your CRM, so attribution is live in your dashboards too.

## Stay in the loop

- Browse all GTM skills: [the GTM System catalog](../../../README.md)
- Get new skills as they ship: [Subscribe](https://tally.so/r/NpRWgp)
- See how La Growth Machine fits your GTM stack: [Try LGM free](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=campaign-impact-analyzer)

## License

MIT — see the LICENSE at the repo root.

## About La Growth Machine

La Growth Machine is the multichannel outbound platform behind these skills — it turns GTM work like this into running outreach across LinkedIn, email, voice and calls, from one place.

---

Topics: campaign impact analysis, campaign ROI, outbound campaign performance, deal attribution, CRM x outreach analysis, campaign ranking by revenue, B2B outbound analytics, pipeline attribution, LGM HubSpot integration, multichannel campaign audit, sales attribution, RevOps pipeline review
