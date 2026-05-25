# Multichannel Campaign Builder

> Turns a natural-language brief into a complete multichannel outbound campaign — a full LinkedIn + email sequence, every message ready to copy.

Maintained by [La Growth Machine](https://lagrowthmachine.com). Free to use.

## What it does

You describe who you want to reach and why:

> "Build a multichannel campaign for RevOps leaders at B2B SaaS scale-ups. We sell a pipeline-attribution tool. It's a cold list — no signal."

The skill picks the campaign type, builds 3 distinct angles, and generates the full sequence — every touch, every channel, calibrated to the campaign type and channel mix, and self-checked against copywriting quality standards. Each message comes back ready to copy.

## Why it exists

Writing a campaign sequence by hand is slow and inconsistent: the first message is sharp, the follow-ups drift into "just checking in", angles repeat, the CTA asks for a meeting too early. This skill encodes the copywriting discipline that experienced outbound teams apply — angle variety, the Permissionless Value Promise CTA framework, channel-specific rules, anti-AI-tells, a 12-dimension quality check — and applies it to every message in the sequence.

## Install

Clone the repo and copy the skill folder into your Claude skills directory:

```bash
git clone https://github.com/LaGrowthMachine/gtm-system.git
cd gtm-system
cp -r skills/get-qualified-meetings/multichannel-campaign-builder ~/.claude/skills/
```

Then ask Claude — e.g. *"Write me a multichannel outbound campaign for Heads of Sales at mid-market SaaS companies."*

## What's supported

- **Campaign types** — social selling (signal-triggered), employee advocacy (engaging a colleague's post engagers), cold outbound (no signal).
- **Channel mixes** — LinkedIn-only, email-only, multichannel.
- **Full sequence** — invite note, DMs, emails, follow-ups, breakup — calibrated to the chosen cadence.
- **3 angle options** before any copy, with a recommendation on which to lead with.
- **Self quality-check** on every message against a 12-dimension standard, with automatic rewrite of weak messages.

## Who it's for

- SDRs and BDRs building outbound sequences
- Sales managers and RevOps launching campaigns
- Founders running their own prospecting
- Growth marketers running ABM or social-selling motions
- Agencies building campaigns for clients

## Limitations

- It generates copy — it does not send it. To run the sequence you still need an outreach tool.
- It is self-contained: it asks you for your product and target inline. It does not read external context files.
- The patterns assume English-language outbound. For other languages, adapt the message patterns to local equivalents.

## Works with

This skill runs standalone with any outreach stack. It also plugs into:

- **campaign-challenger** — pair it with this skill to pressure-test the sequence before launch. Ask Claude to generate and benchmark in one go: *"Generate a multichannel campaign for X and benchmark it against my past campaigns."*
- **La Growth Machine MCP** — once the MCP exposes campaign creation, Claude creates the campaign in LGM directly from the generated sequence. Until then, the skill links you to set it up in the LGM app.

## Stay in the loop

- Browse all GTM skills: [the GTM System catalog](../../../README.md)
- Get new skills as they ship: [Subscribe](https://tally.so/r/NpRWgp)
- See how La Growth Machine fits your GTM stack: [Try LGM free](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=multichannel-campaign-builder)

## License

MIT — see the LICENSE at the repo root.

## About La Growth Machine

La Growth Machine is a multichannel sales engagement platform that helps B2B teams run outbound on LinkedIn, email and more — from a single workspace.

---

Topics: outbound campaign, multichannel sequence, cold email sequence, LinkedIn outreach, sales prospecting, campaign copywriting, outreach sequence, social selling, employee advocacy, cold outbound, B2B outbound, sales engagement, follow-up emails, campaign generator
