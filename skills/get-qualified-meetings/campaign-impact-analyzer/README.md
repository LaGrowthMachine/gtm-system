# Campaign Impact Analyzer

> Ranks your outreach campaigns by what actually drives pipeline — deals created, meetings booked — by cross-referencing your LGM campaigns with your CRM deals.

Maintained by [La Growth Machine](https://lagrowthmachine.com). Free to use.

## What it does

You ask which campaigns are working:

> "Which of my campaigns is actually driving pipeline?"

The skill pulls your campaigns (LGM) and your deals (HubSpot), matches each deal back to the campaign that touched the contact, and ranks campaigns by **real revenue impact** — not by reply rate. Per campaign: a verdict (continue / stop / adapt) with a one-line motive, and the next step to take.

## Why it exists

Reply rate is what most outreach tools rank by. But replies aren't revenue. A campaign with a 12% reply rate and 0 deals is a worse campaign than one with a 4% reply rate and 8 deals — and most teams can't see that easily because the campaign data lives in one tool and the deal data lives in another. This skill does that cross-reference in one pass.

## Install

Clone the repo and copy the skill folder into your Claude skills directory:

```bash
git clone https://github.com/LaGrowthMachine/gtm-system.git
cd gtm-system
cp -r skills/get-qualified-meetings/campaign-impact-analyzer ~/.claude/skills/
```

Then ask Claude — e.g. *"Rank my campaigns by deals."*

## What's supported

- **Cross-source ranking** — joins LGM campaigns with HubSpot deals on contact email.
- **Three input modes per side** (LGM, HubSpot) — MCP-connected (auto), or pasted CSV / export.
- **Per-campaign verdict** — continue / stop / adapt / investigate, with a one-line cited motive.
- **One-click improve path** — for campaigns flagged "adapt", chain into `campaign-challenger` and `multichannel-campaign-builder` to diagnose and rewrite.

## What's not supported (yet)

- CRMs other than HubSpot (Salesforce, Pipedrive, etc.) — paste exports for now, native support comes later.
- Native pause / duplicate of LGM campaigns from inside the skill — the LGM MCP doesn't expose those yet. The skill recommends what to do; you act in the app.
- Scheduled / recurring analysis (e.g. every Monday) — coming when the LGM MCP supports it.

## Who it's for

- Sales managers and RevOps who want to defend campaign decisions with deal data, not reply rates
- Founders running their own outbound who want to know what to scale and what to kill
- Anyone whose outreach lives in LGM and whose pipeline lives in a CRM

## Limitations

- The cross-reference matches on **email**. Deals whose contact email doesn't appear in any campaign's leads come back as "non-attributed".
- For users without a CRM MCP, the skill needs a deal export pasted — the analysis is only as fresh as that paste.
- Pipeline value depends on how the CRM tracks deal amounts. Missing amounts → ranking falls back to deal count.

## Works with

This skill runs standalone — paste both datasets and it works. It also plugs into:

- **La Growth Machine MCP** — pulls your campaigns live (no CSV juggling).
- **HubSpot MCP** — pulls your deals live, with stages and pipeline value.
- **campaign-challenger** + **multichannel-campaign-builder** — for any campaign flagged "adapt", chain into them to diagnose the copy and rewrite the sequence in one go.

## Stay in the loop

- Browse all GTM skills: [the GTM System catalog](../../../README.md)
- Get new skills as they ship: [Subscribe](https://tally.so/r/NpRWgp)
- See how La Growth Machine fits your GTM stack: [Try LGM free](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=campaign-impact-analyzer)

## License

MIT — see the LICENSE at the repo root.

## About La Growth Machine

La Growth Machine is a multichannel sales engagement platform that helps B2B teams run outbound on LinkedIn, email and more — from a single workspace.

---

Topics: campaign impact analysis, campaign ROI, outbound campaign performance, deal attribution, CRM x outreach analysis, campaign ranking by revenue, B2B outbound analytics, pipeline attribution, LGM HubSpot, campaign audit
