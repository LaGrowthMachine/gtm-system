# Weekly Performance Advisor

> A two-tab weekly cockpit for your La Growth Machine outbound — what to do this week (replies to handle, campaigns to fix) and how you're performing (campaign health, reply trends) — built live from your own LGM data.

Maintained by [La Growth Machine](https://lagrowthmachine.com). Free to use. Updated: 2026-07-08.

## What it does

You ask for your weekly dashboard. The skill pulls your running campaigns and your inbox from La Growth Machine, scores each campaign against baked 3-zone benchmarks, classifies your untagged replies, and renders a **live two-tab artifact** — rebuilt from your own data every time you run it:

- **To do** — your moves this week, the replies to handle **sorted by urgency** (call requests and longest-waiting first), and the only-🔴 campaigns to fix, each with a one-click **Fix this** button that hands the campaign + diagnosis to the right skill.
- **Weekly performance** — total replies and positive replies, volume-weighted health gauges (on target / watch / to fix), the full campaign panorama, and week-over-week + trailing-30-day trends.

Example: you ask *"how are my campaigns doing this week?"* and the dashboard opens on your to-do list — *"answer 2 call requests, rewrite the intro on 'Website visitor EU' (LinkedIn reply 6%, below floor)"* — sorts your actionable replies hottest-first, and on the second tab shows your reply volume up or down vs last week.

## Why it exists

Outbound tools show cumulative stats, not *"what do I do Monday morning."* Open ten campaigns and you still can't tell which reply is going cold, which campaign is genuinely broken versus just noisy, or whether this week beat last. This skill turns your live LGM data into a single weekly cockpit: an action list you work top-down, and a performance read that separates *to fix* from *fine* — so the week goes to what actually moves pipeline.

## Install

**One-line (recommended)** — uses [`skills`](https://github.com/vercel-labs/skills) from Vercel Labs to install into Claude Code, Cursor, Codex, Amp + 30 other agents in one go:

```bash
npx skills add LaGrowthMachine/gtm-system/skills/get-qualified-meetings/weekly-performance-advisor
```

Add `-g` for a global install.

**Manual install** — clone the repo and copy the skill folder yourself:

```bash
git clone https://github.com/LaGrowthMachine/gtm-system.git
cd gtm-system
cp -r skills/get-qualified-meetings/weekly-performance-advisor ~/.claude/skills/
```

Then ask Claude — e.g. *"Build my weekly performance dashboard."* The first run does a short setup (connect LGM, pick the identity to track, optional deal layer); every run after that just rebuilds the dashboard.

## Recommended companion skills

The dashboard only needs the LGM MCP to run — but its buttons hand work off to other GTM skills. Install these so every **Fix this** and **Draft replies** button works end to end. Grab the whole set in one line:

```bash
npx skills add LaGrowthMachine/gtm-system
```

Or add just the ones you want:

| Companion skill | Powers | Install |
|---|---|---|
| `reply-draft-assistant` | the **Draft replies** button (inbox triage + drafting) | `npx skills add LaGrowthMachine/gtm-system/skills/catch-opportunities/reply-draft-assistant` |
| `campaign-challenger` | **Fix this** on message / copy issues | `npx skills add LaGrowthMachine/gtm-system/skills/get-qualified-meetings/campaign-challenger` |
| `sales-nav-search-builder` | **Fix this** on targeting / low acceptance | `npx skills add LaGrowthMachine/gtm-system/skills/fuel-my-pipeline/sales-nav-search-builder` |
| `won-deal-icp-finder` | **Fix this** on list quality / bounce | `npx skills add LaGrowthMachine/gtm-system/skills/fuel-my-pipeline/won-deal-icp-finder` |
| `campaign-impact-analyzer` | the optional **deals / € layer** (with a CRM MCP) | `npx skills add LaGrowthMachine/gtm-system/skills/get-qualified-meetings/campaign-impact-analyzer` |

Everything is optional. Without a companion, its button falls back to a copy-paste prompt that tells you which skill to install first — nothing breaks.

## What's supported

- **Two-tab live artifact** — To do + Weekly performance, rebuilt from your own live data each run.
- **3-zone campaign health** — on target / watch / to fix, scored per active channel and **weighted by the primary channel** (a weak secondary leg flags "email leg to fix", not the whole campaign).
- **Reply triage** — untagged replies classified (interested / neutral / not interested / wrong fit) and **sorted by urgency**, with a one-click handoff to `reply-draft-assistant`.
- **One-click Fix this** — each struggling campaign routes to `campaign-challenger`, `sales-nav-search-builder`, or `won-deal-icp-finder` with the campaign and its diagnosis pre-loaded.
- **Trends** — week-over-week and trailing-30-day deltas from a local weekly snapshot.
- **Multi-identity** — track one identity or union several for a team-wide view.
- **Optional deal/€ layer** — via `campaign-impact-analyzer` when a CRM MCP is connected.
- **Optional Monday auto-refresh** — set up a weekly routine so the dashboard stays fresh.

## What's not supported

- **LGM MCP required** — this is not a paste-an-export skill; the dashboard is built from live LGM data, so the MCP has to be connected (the skill guides the install if it isn't).
- **No write-back to LGM** — reply classifications and campaign statuses are shown for you to validate and act on in LGM; the skill never changes your LGM data.
- **CRMs other than HubSpot** for the deal layer — coming later; without a CRM the "Deals from campaigns" box stays empty.
- **Cold-outbound-calibrated benchmarks** — baked defaults; very different motions (nurture, warm relance) may read stricter than they should.

## Who it's for

- **Heads of Sales / SDR managers** running a Monday pipeline and reply review.
- **SDRs and founders** who want one *"what do I do this week"* cockpit instead of ten campaign tabs.
- **RevOps / Growth** tracking outbound health week over week.

## Limitations

- The positive-reply count is drawn from replies **awaiting your answer**; a reply you already handled this week may not be counted.
- **Trends need history** — week-over-week and 30-day deltas come alive after 2+ weekly runs.
- Campaigns under **20 contacts** are listed but not scored — rates on tiny volume aren't reliable.
- The artifact is light-theme.

## Works with

This skill needs the La Growth Machine MCP to run. It also plugs into:

- **La Growth Machine MCP** — pulls your campaigns, stats and inbox live (required).
- **`campaign-impact-analyzer`** (+ a CRM MCP) — adds the deals/€ layer to the dashboard.
- **`reply-draft-assistant`** — the "Draft replies" button hands your urgent replies straight to it.
- **`campaign-challenger` / `sales-nav-search-builder` / `won-deal-icp-finder`** — the per-campaign "Fix this" buttons route here to rewrite copy, rebuild targeting, or clean a bouncing list.

## Stay in the loop

- Browse all GTM skills: [the GTM System catalog](https://github.com/LaGrowthMachine/gtm-system)
- Get new skills as they ship: [Subscribe](https://tally.so/r/NpRWgp)
- See how La Growth Machine fits your GTM stack: [Try LGM free](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=weekly-performance-advisor)

## License

MIT — see the LICENSE at the repo root.

## About La Growth Machine

La Growth Machine is the multichannel outbound platform behind these skills — it turns GTM work like this into running outreach across LinkedIn, email, voice and calls, from one place.

---

Topics: weekly performance dashboard, outbound cockpit, campaign health, reply triage, LinkedIn and email reply rate, campaign benchmarks, SDR weekly review, pipeline dashboard, La Growth Machine analytics, outbound reporting, Monday cockpit, campaigns to fix, outbound KPIs, reply rate trends
