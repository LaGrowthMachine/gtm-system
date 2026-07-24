# Team Performance Dashboard

> A head-of-sales cockpit for your La Growth Machine outbound — who's generating the most replies and conversions, which hot leads are going cold, and how to clone your best reps' campaigns across the team — built live from your own LGM data.

Maintained by [La Growth Machine](https://lagrowthmachine.com). Free to use. Updated: 2026-07-22.

## What it does

You ask for your team dashboard. The skill pulls every sender's running campaigns and inbox from La Growth Machine, ranks each rep on reply rate, your success event (signups / meetings / deals) and conversion, mines what your top campaigns do differently, classifies your real replies, and renders a **live four-tab artifact** — rebuilt from your own data every time you run it:

- **Team Performance** — the hot leads going cold (each linking straight to that rep's inbox), a response-speed + backlog read, and one **sortable all-KPI table** per rep (contacted, LinkedIn acceptance, LinkedIn/email reply, awaiting, median response, outcome, conversion, value €).
- **Playbooks** — reply-handling plays and per-channel campaign best practices (subject/length → open, invite/voice/warming → acceptance), sourced from what actually works in your account.
- **Reply Quality** — your principal objection to coach on, a radar of what your team replies to, a priority table (battle card, most-cited competitor, targeting signals), and the best-handled reply to clone.
- **Help** — every metric, calculation and definition in one place.

Example: you ask *"how's my team doing this week?"* and the dashboard opens on six hot leads sitting unanswered for weeks, ranks your reps — one leads on replies, another on volume, a third on conversion — and flags the rep whose replies land but never convert, with a one-click **Improve conversion rate** button.

## Why it exists

Outbound tools show account totals, not *"which rep should I coach, on what, and with whose playbook."* A head of sales opening ten campaigns still can't see who converts best versus who just gets replies, which hot lead is going cold under which rep, or what the top campaign does that the others don't. This skill turns your live LGM data into a per-rep cockpit that separates *reply rate* from *actual conversion* — so coaching goes to what moves pipeline, and what works on one rep's campaign gets applied to the rest.

## Install

**One-line (recommended)** — uses [`skills`](https://github.com/vercel-labs/skills) from Vercel Labs to install into Claude Code, Cursor, Codex, Amp + 30 other agents in one go:

```bash
npx skills add LaGrowthMachine/gtm-system/skills/get-qualified-meetings/team-performance-dashboard
```

Add `-g` for a global install.

**Manual install** — clone the repo and copy the skill folder yourself:

```bash
git clone https://github.com/LaGrowthMachine/gtm-system.git
cd gtm-system
cp -r skills/get-qualified-meetings/team-performance-dashboard ~/.claude/skills/
```

Then ask Claude — e.g. *"Build my team performance dashboard."* The first run does a short setup (~10-15 min: connect LGM, pick your success event and how you track it, optional value layer); every run after that just rebuilds the dashboard.

## Recommended companion skills

The dashboard only needs the LGM MCP to run — but its **Fix** buttons hand work off to other GTM skills. Install these so every button works end to end. Grab the whole set in one line:

```bash
npx skills add LaGrowthMachine/gtm-system
```

Or add just the ones you want:

| Companion skill | Powers | Install |
|---|---|---|
| `campaign-challenger` | the **Improve reply / conversion rate** buttons | `npx skills add LaGrowthMachine/gtm-system/skills/get-qualified-meetings/campaign-challenger` |
| `campaign-impact-analyzer` | the optional **value / € layer** (with a CRM MCP) | `npx skills add LaGrowthMachine/gtm-system/skills/get-qualified-meetings/campaign-impact-analyzer` |
| `sales-nav-search-builder` | targeting / low-acceptance fixes | `npx skills add LaGrowthMachine/gtm-system/skills/fuel-my-pipeline/sales-nav-search-builder` |
| `won-deal-icp-finder` | list-quality / bounce fixes | `npx skills add LaGrowthMachine/gtm-system/skills/fuel-my-pipeline/won-deal-icp-finder` |

Everything is optional. Without a companion, its button falls back to a copy-paste prompt that includes the download link — nothing breaks.

## What's supported

- **Four-tab live artifact** — Team Performance, Playbooks, Reply Quality, Help, rebuilt from your own live data each run.
- **Per-rep ranking** — every sender ranked on reply rate, with a single sortable table carrying every KPI (reply is active-routine; outcome, conversion and value are all-time).
- **Configurable success event** — measure signups, meetings booked, deals, account creations, or your own.
- **Value (€) layer** — attribute campaign-driven revenue per rep when a CRM or Stripe source is connected.
- **Hot leads to close** — buying-intent replies still unanswered, each linking to that rep's LGM inbox.
- **Cross-rep coaching** — what your best campaigns do differently, mined into named patterns and one-click **Fix** prompts for the reps who are behind.
- **Reply quality** — real reply classification, your principal objection, a competitor read, and the best-handled reply to clone.
- **Deepen it in batches** — the dashboard builds fast; then classify more conversations on demand (this week's replies, the last 50, or everything awaiting), in timed bites, and the Reply Quality tab sharpens each time. Not on LGM? Run it from a conversation export.
- **Optional Monday auto-refresh** — a weekly routine keeps the dashboard fresh; a button triggers it on demand.

## What's not supported

- **LGM MCP required** — this is not a paste-an-export skill; the dashboard is built from live LGM data, so the MCP has to be connected (the skill guides the install if it isn't).
- **No write-back to LGM** — reply classifications and diagnoses are shown for you to validate and act on in LGM; the skill never changes your data.
- **A conversion source for the outcome/value layer** — without a CRM, Airtable, Stripe or CSV, the dashboard still runs on reply data; the outcome, conversion and value fields stay in their empty state.
- **Cold-outbound-calibrated benchmarks** — baked defaults (LinkedIn reply ≥25%, email reply ≥6%); very different motions (nurture, warm relance) may read stricter than they should.

## Who it's for

- **Heads of Sales / SDR managers** running a weekly team review and reply pipeline.
- **GTM engineers / RevOps** tracking per-rep outbound health and conversion.
- **Founders** who want to see who converts best and clone it across the team.

## Limitations

- Per-rep response time and some per-channel reads need enough volume; thin samples show a directional value or an empty state.
- **Trends need history** — week-over-week deltas come alive after 2+ weekly runs.
- Campaigns under **20 contacts** are listed but not scored — rates on tiny volume aren't reliable.
- The artifact is light-theme.

## Works with

This skill needs the La Growth Machine MCP to run. It also plugs into:

- **La Growth Machine MCP** — pulls every rep's campaigns, stats and inbox live (required).
- **`campaign-impact-analyzer`** (+ a CRM MCP) — powers the value/€ layer.
- **`campaign-challenger`** — the "Improve reply / conversion rate" buttons hand the flagged campaign + diagnosis straight to it.
- **`sales-nav-search-builder` / `won-deal-icp-finder`** — targeting and list-quality fixes.

## Stay in the loop

- Browse all GTM skills: [the GTM System catalog](https://github.com/LaGrowthMachine/gtm-system)
- Get new skills as they ship: [Subscribe](https://tally.so/r/NpRWgp)
- See how La Growth Machine fits your GTM stack: [Try LGM free](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=team-performance-dashboard)

## License

MIT — see the LICENSE at the repo root.

## About La Growth Machine

La Growth Machine is the multichannel outbound platform behind these skills — it turns GTM work like this into running outreach across LinkedIn, email, voice and calls, from one place.

---

Topics: team performance dashboard, per-rep outbound, sales team cockpit, who converts best, reply rate by rep, SDR manager dashboard, outbound conversion rate, per-identity performance, sales coaching dashboard, objection handling by rep, hot leads to close, campaign playbook, La Growth Machine analytics, head of sales cockpit, outbound KPIs by member, conversion vs reply rate
