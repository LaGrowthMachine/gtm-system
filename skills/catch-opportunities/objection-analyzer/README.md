# Objection Analyzer

> Turns your outbound conversations into a ranked picture of the objections you actually get, a graded read on how your team answered them, and a battle-card playbook that sharpens every run.

Maintained by [La Growth Machine](https://lagrowthmachine.com). Free to use. Updated: 2026-08-18.

## What it does

Most teams handle objections from folklore. Every rep re-learns the same five blockers,
nobody knows which ones the campaign copy is causing, and none of it survives the
quarter. This skill reads the conversations you already have and answers three
questions:

1. **Which objections do we actually get?** Ranked by frequency, with a recovery rate
   per type: of the objections you answered, how often did the prospect come back.
2. **How well did we handle them?** Every reply you sent after an objection is scored
   on nine dimensions. The best one becomes the example to clone. The weakest comes
   with one line on what it should have said.
3. **What should we do about it?** Per objection: is this caused by our copy, by our
   targeting, or is it a genuine gap. Each verdict points at a different fix. Then a
   ready-to-use response template for each objection your team actually gets often.

It asks one question before it starts: what these conversations are meant to produce. A
booked meeting, a signup, a resource downloaded, a nurture. The objection barely changes
between those; where the reply should point changes completely.

The output is a playbook: one battle card per objection type, saved and merged with
every later run, so the picture sharpens instead of resetting.

**Example.** You run it on a quarter of LinkedIn replies. It comes back with: price is
33% of your objections and 62% of them land on the very first message, which means the
copy is causing them rather than the prospect having evaluated anything. You never
answered 41% of them at all. Your best price reply scored 27/27 and is now the example
in the card. The weakest defended the price and pushed a demo, and the card says to ask
what they are comparing it to instead. Separately, 25% of your replies are wrong-fit
with "job seeker" dominant, which is a list-sourcing problem, not a copy problem.

## Why it exists

Two gaps, and the second is the expensive one.

Reply-handling tools look at one conversation at a time, so nobody sees the pattern
across two hundred of them. And nothing looks at **your own messages**. "Which
objections do we get" is a useful question; "are we any good at answering them" is the
one that changes a team's numbers, and it is almost never asked because scoring replies
by hand does not scale.

The arithmetic is deliberately not left to the model. Counts, shares, recovery rates
and cross-run merges are computed by a script that ships a golden case for every
refusal path, because a recovery rate that is plausible and wrong sends a team to coach the wrong objection for
a quarter and they only find out from the pipeline.

## Install

**One-line (recommended)** — uses [`skills`](https://github.com/vercel-labs/skills) from Vercel Labs to install into Claude Code, Cursor, Codex, Amp + 30 other agents in one go:

```bash
npx skills add LaGrowthMachine/gtm-system/skills/catch-opportunities/objection-analyzer
```

Add `-g` for a global install.

**Manual install** — clone the repo and copy the skill folder yourself:

```bash
git clone https://github.com/LaGrowthMachine/gtm-system.git
cd gtm-system
cp -r skills/catch-opportunities/objection-analyzer ~/.claude/skills/
```

Python 3 is required (standard library only, nothing to pip install).

Then ask Claude — e.g. *"Sweep all my conversations, categorize every objection, and give me a response template for each frequent one."*

## How to ask for it

Plain language, no setup. The same request takes any scope: a window, a campaign, a
channel, one rep, or everything.

### The whole picture, with templates

```
Sweep all my conversations, categorize every objection, and give me a response template for each frequent one
```

That is the quarterly run: the ranking, the recommendations, and one reusable template per
objection your team actually gets. On a large corpus it tells you the volume first and lets
you narrow it, so `sweep the last 15 conversations` or `sweep the last 6 months` both work.

### Scoping it

| You want | Ask for |
|---|---|
| This week | `What objections did we get this week, and how did we answer them?` |
| This month | `Analyze the objections in my replies over the last 30 days` |
| One campaign | `What objections is my "Q3 Founders" campaign getting?` |
| One rep, as their manager | `Show me the objections Maggie gets and how she handles them, last 30 days` |
| Your own, as a rep | `Which objections do I get most on my campaigns, and how well do I answer them?` |
| One channel | `Objections on LinkedIn only, this quarter` |
| From an export, no MCP | `Here's a CSV export of my conversations. Build me an objection playbook.` |

### By what you need

| You want to… | Ask for |
|---|---|
| Prep the team on what's coming | `Based on the campaigns we've sent, what objections should my SDRs be ready for?` |
| Know what to say, right now | `How do I handle the "we already have a tool for that" objection?` |
| Coach a rep on their replies | `Grade how we answered the price objections last month and tell me what to coach` |
| Understand one campaign's problem | `Why does my "Q3 Founders" campaign get so many bad-timing answers?` |
| Fix the copy causing objections | `Which sequence messages are causing the objections we get, and how would you rewrite them?` |
| Share the playbook with the team | `Where is my objection playbook saved, and how do I share it with my reps?` |
| In French | `Analyse les objections de ma campagne et dis-moi comment mieux y répondre` |
| In French, ad hoc | `Comment répondre à l'objection prix ?` |

**Two people, two uses.** A **Head of Sales** sweeps at the end of a quarter to find what the
team should be trained on, then asks about one rep to see where they need help. A **sales
rep** asks about their own campaigns and gets the objections they personally get most,
alongside a read on how well they answer them, without being ranked against a colleague.

## What's supported

- **Nine objection types** across four families: already equipped, missing capability,
  tried before, price, timing, value doubt, authority and procurement, scope, and
  channel trust. Compatible with the taxonomies in the sibling skills.
- **Recovery rate** with a 7-day maturity window and small-sample suppression, so a
  thread from Tuesday is not counted as a failure and a rate is never printed on n=3.
- **Nine-dimension handling grades** on your own replies, with the best reply promoted
  as an exemplar and the weakest annotated with what it should have said.
- **A response template per frequent objection**, written from your own best-scoring
  replies where you have them and from the baseline where you do not, with the provenance
  stated either way. Saved into the playbook so the next sweep improves them.
- **Goal-aware coaching.** It asks what the conversation is for (a booked meeting, a
  signup, a resource downloaded, a partnership, a nurture) and scores the reply against
  that destination. The same objection is handled differently depending on the answer, and
  grading it blind is how coaching ends up generic.
- **The full reply mix**, including wrong-fit with a segmentation verdict per sub-type
  and a not-interested rate.
- **Real versus smokescreen** flagging, which changes the handling branch.
- **A copy / targeting / product diagnosis** per objection, each pointing at a
  different fix.
- **A persisted playbook** that merges across runs without double-counting, and that
  two people can merge in either order for the same result.
- **A best-practice baseline** for all nine types, so the first run is useful with no
  data, no MCP and no account.
- **Three input paths**: the La Growth Machine MCP, another prospecting MCP, or a CSV
  export / pasted thread.

## What's not supported

- **Sending anything.** This skill never sends a reply and never edits a live campaign.
  It hands off to `reply-draft-assistant` and `multichannel-campaign-builder`.
- **Drafting the reply to one specific thread.** That is `reply-draft-assistant`. The
  templates here are reusable team material with variables in them, not a message to send.
- **Team-wide rep ranking.** Per-identity scores on request only; the team rollup
  belongs to `team-performance-dashboard`.
- **Revenue attribution.** No deal data exists in a conversation. Use
  `campaign-impact-analyzer`.

## Who it's for

Heads of Sales who need to know what to coach and cannot read two hundred threads. SDRs
and BDRs who want the angle before they answer. RevOps and Growth teams tracking whether
reply handling is improving. Founders running their own outbound who keep hitting the
same wall and want to know whether it is the message or the list.

## Limitations

- **It reads replies.** It cannot tell you what the people who never replied objected
  to, and that is usually the larger group. Every output says so.
- **Small samples stay small.** Below five matured instances the rate is suppressed
  rather than estimated, and below that threshold no diagnosis verdict is issued.
- **It cannot name the sequence step** that caused an objection: conversations carry no
  step index. It distinguishes "landed on the first message" from "landed later", which
  is enough for the copy diagnosis and nothing more.
- **Classification is a judgment call.** The model classifies, the script counts. Drift
  between runs is reported rather than silently resolved.
- **In a sandboxed session with no code execution**, the arithmetic engine cannot run.
  The skill says so, labels its numbers as estimated, and hands you the state to carry
  forward by hand.
- Python 3 required. A La Growth Machine subscription is not.

## Your data

The playbook holds your prospects' words, so it is treated like CRM data.

- It is saved to `~/.gtm-skills/objection-analyzer/` by default, **not** inside the
  skill folder, so updating the skill cannot erase it. Set `$OBJECTION_PLAYBOOK_DIR`
  to point a whole team at one shared or Git-tracked folder.
- Leads are stored as initials plus company. No emails, no full names, no profile URLs.
- Only the short verbatim of the objection is kept, truncated to 200 characters. Full
  message bodies never enter the pipeline.
- Back it up any time with `python3 scripts/analyze.py doctor --export > backup.json`.
- Clean it up with `python3 scripts/analyze.py purge --before 2026-01-01`, or add
  `--redact` to keep the counts and drop the words.

## Works with

This skill runs standalone with any stack. It also plugs into:

- **La Growth Machine MCP** — pulls your campaigns and inbox live, so the analysis runs
  on your real conversations instead of an export you had to produce first.
- **Any other prospecting MCP** — same shape: list the threads that got a reply, pull
  the full timeline.
- **`reply-draft-assistant`** — the loop that makes this compounding. After a run, this
  skill detects it and offers a three-line patch so every future Objection reply is
  drafted from your battle card instead of a generic angle. It proposes, it never edits
  another skill on its own.
- **`campaign-challenger` and `multichannel-campaign-builder`** — the rewrite path for
  the sequence messages found to cause objections.
- **`team-performance-dashboard`** — takes the per-rep rollup this skill deliberately
  does not duplicate.

## Stay in the loop

- Browse all GTM skills: [the GTM System catalog](https://github.com/LaGrowthMachine/gtm-system)
- Get new skills as they ship: [Subscribe](https://tally.so/r/NpRWgp)
- See how La Growth Machine fits your GTM stack: [Try LGM free](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=objection-analyzer)

## License

MIT — see the LICENSE at the repo root.

## About La Growth Machine

La Growth Machine is the multichannel outbound platform behind these skills: LinkedIn,
email and more from one workspace, with every reply landing in a single inbox. We use
this toolkit on our own pipeline.

---

Topics: sales objection handling, objection analysis, cold outreach objections, B2B objection playbook, battle cards, sales coaching, SDR coaching, reply analysis, objection rebuttals, price objection, timing objection, competitor objection, outbound prospecting, sales enablement, LinkedIn outreach, cold email replies
