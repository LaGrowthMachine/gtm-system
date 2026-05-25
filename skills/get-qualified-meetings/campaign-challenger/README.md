# Campaign Challenger

> Challenges an outbound campaign copy by benchmarking it against the campaigns you've already run — what worked, what didn't, what the winners do differently.

Maintained by [La Growth Machine](https://lagrowthmachine.com). Free to use.

## What it does

You give it a campaign copy — a draft sequence, or messages already written:

> "Is this campaign as strong as my best ones?"

It pulls your existing campaign performance, ranks what worked, and tells you concretely how the draft stacks up — which past campaign it resembles, and what the top performers did that this draft doesn't. You get two reads: comparative (vs your own history) and absolute (vs copywriting standards).

## Why it exists

"Is this campaign good?" usually gets answered by gut feel. The data to answer it properly — which of your past campaigns actually booked meetings, and what their copy did differently — exists, but it's scattered and nobody has time to cross-reference it. This skill does that comparison systematically, so a draft gets pressure-tested against real performance before it goes live.

## Install

Clone the repo and copy the skill folder into your Claude skills directory:

```bash
git clone https://github.com/LaGrowthMachine/gtm-system.git
cd gtm-system
cp -r skills/get-qualified-meetings/campaign-challenger ~/.claude/skills/
```

Then ask Claude — e.g. *"Benchmark this cold email sequence against my past campaigns."*

## What's supported

- **Three input modes** — pull campaign history automatically (LGM MCP connected), work from stats and copy you paste, or run a best-practice baseline when you have no history yet.
- **Comparative read** — ranks your past campaigns by meetings booked, then shows what the winners do that the draft doesn't.
- **Absolute read** — scores the draft against a 12-dimension copywriting standard.
- **Concrete output** — names the specific differences, not a vague verdict.

## Who it's for

- SDRs and sales managers pressure-testing a campaign before launch
- RevOps comparing a new sequence to what has historically converted
- Founders and growth marketers who want a second opinion grounded in data
- Anyone with a campaign draft and a "is this actually good?" question

## Limitations

- The comparative read needs campaign history — with no past campaigns, it runs the best-practice baseline instead.
- Without the LGM MCP, it relies on the stats and copy you paste; the quality of the benchmark depends on what you provide.
- It evaluates copy — it does not send or launch anything.

## Works with

This skill runs standalone with any outreach stack. It also plugs into:

- **La Growth Machine MCP** — when connected, it pulls your campaigns, their stats and their copy automatically, so the benchmark runs on your real history instead of numbers you paste.

## Stay in the loop

- Browse all GTM skills: [the GTM System catalog](../../../README.md)
- Get new skills as they ship: [Subscribe](https://tally.so/r/NpRWgp)
- See how La Growth Machine fits your GTM stack: [Try LGM free](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=campaign-challenger)

## License

MIT — see the LICENSE at the repo root.

## About La Growth Machine

La Growth Machine is a multichannel sales engagement platform that helps B2B teams run outbound on LinkedIn, email and more — from a single workspace.

---

Topics: campaign benchmark, outbound campaign audit, sequence review, campaign copy analysis, sales campaign comparison, cold email audit, campaign performance, copy benchmarking, pre-launch campaign check, B2B outbound
