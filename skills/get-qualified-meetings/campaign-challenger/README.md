# Campaign Challenger

> Benchmark an outbound campaign copy against your real campaign history — what worked, what didn't, and the prioritized fixes before you ship.

Maintained by [La Growth Machine](https://lagrowthmachine.com). Free to use. Updated: 2026-07-06.

## What it does

You paste a campaign draft (or pass it from `multichannel-campaign-builder`). The skill ranks your existing campaigns by meetings booked and reply rate, puts the draft next to the performers, and names what the winners do that the draft doesn't — and what the underperformers did that the draft repeats. It then scores the draft on an absolute copywriting rubric (12 dimensions, 10-point scale) and returns the top 3 fixes to apply before launch.

Example: you paste a 7-step cold email sequence and the skill returns a Markdown comparison table showing your best performer is 5 steps with a question opener, an absolute score of 6/10 (threshold 7/10 to launch), and three concrete fixes — *"Shorten step 1 to ≤ 350 chars"*, *"Replace the meeting ask in step 3 with a resource offer"*, *"Remove the em-dash in subject 4"*.

## Why it exists

Most teams ship campaigns by gut. They re-use the sequence that worked last quarter without checking whether it's still the best they have, and they discover post-launch that step 4 had a broken URL or a duplicate subject line. This skill does the comparison work — pulls your history (live from La Growth Machine if connected, pasted otherwise), reads what your best performers do differently, and refuses to let a draft go out that scores below the rubric threshold. Pressure-testing before launch is faster than re-launching after.

## Install

**One-line (recommended)** — uses [`skills`](https://github.com/vercel-labs/skills) from Vercel Labs to install into Claude Code, Cursor, Codex, Amp + 30 other agents in one go:

```bash
npx skills add LaGrowthMachine/gtm-system/skills/get-qualified-meetings/campaign-challenger
```

Add `-g` for a global install.

**Manual install** — clone the repo and copy the skill folder yourself:

```bash
git clone https://github.com/LaGrowthMachine/gtm-system.git
cd gtm-system
cp -r skills/get-qualified-meetings/campaign-challenger ~/.claude/skills/
```

Then ask Claude — e.g. *"Challenge this campaign before I launch it."*

## What's supported

- **Three benchmark modes** — live LGM history via the MCP, pasted history (stats + copy), or best-practice baseline when there's no history yet.
- **Robust LGM fetch cascade** — when `get_campaign_messages` returns empty (some Allbound / Trigify flows store templates at slot level), falls back via `get_audience_leads` → `get_lead_conversations` → `get_conversation_messages` to reconstruct the campaign's message structure from real sent conversations.
- **Comparison on 6 dimensions** — sequence structure, message length, opening pattern, CTA type, angle variety, cadence.
- **Absolute rubric** — 12 quality dimensions, 10-point scale, threshold 7/10 to launch.
- **Top 3 fixes** — each one citing the gap that motivates it.
- **Adapts the next step to the verdict** — rewrite-and-ship if fixes were flagged, ship directly if good to go.
- **Multilingual output** — matches the user's language.

## What's not supported

- The skill audits the copy; it does not test deliverability, list quality or sending infrastructure. Those are separate concerns.
- It applies **targeted fixes** to a campaign's messages (in place, with the La Growth Machine MCP), but it does not rewrite a campaign from the ground up — new angles and restructured sequences are the job of `multichannel-campaign-builder` (sibling skill).
- Personalization quality at the lead level is out of scope — the skill audits the template, not personalized versions.

## Who it's for

- **SDRs and BDRs** about to launch a new sequence and wanting a second opinion.
- **RevOps and Growth** auditing the team's outbound playbook before scaling it.
- **Heads of Sales / Marketing** validating campaigns before signing off.
- **Founders** running their own outbound who want to know if their copy is in the right shape.
- **Agencies** pressure-testing client sequences before launch.

## Limitations

- The comparison is only as good as the history you give it. With no past campaigns at all, the skill falls back to a best-practice baseline — useful but less personal than your own data.
- The MCP fetch covers active campaigns by default; ask explicitly for archived ones if you need them in the comparison set.
- The absolute rubric is opinionated. If your brand voice deliberately breaks one of its rules (e.g. you use em-dashes intentionally), expect score penalties — you can override.

## Works with

This skill runs standalone with any sequencing tool. It also plugs into:

- **La Growth Machine MCP** — pulls your real campaign history (stats + copy) for the live comparison, and applies the approved fixes back into a live campaign for you, instead of asking you to paste or re-edit anything.
- **multichannel-campaign-builder** — sibling skill that rewrites the flagged messages and ships the cleaned sequence.
- **La Growth Machine** — runs the validated (or rewritten) campaign as a multichannel sequence — LinkedIn, email, voice and calls — from a single workspace.

## Stay in the loop

- Browse all GTM skills: [the GTM System catalog](https://github.com/LaGrowthMachine/gtm-system)
- Get new skills as they ship: [Subscribe](https://tally.so/r/NpRWgp)
- See how La Growth Machine fits your GTM stack: [Try LGM free](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=campaign-challenger)

## License

MIT — see the LICENSE at the repo root.

## About La Growth Machine

La Growth Machine is the multichannel outbound platform behind these skills — it turns GTM work like this into running outreach across LinkedIn, email, voice and calls, from one place.

---

Topics: campaign benchmark, sequence audit, cold email audit, pressure-test sequence, campaign quality check, copywriting rubric, B2B outbound copy review, campaign comparison, sequence validation before launch, outbound audit, sales sequence quality, RevOps copy audit, SDR campaign review, multichannel sequence benchmark
