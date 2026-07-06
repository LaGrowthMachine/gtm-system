# Multichannel Campaign Builder

> Turn a natural-language brief into a complete outbound campaign — a full sequence of LinkedIn and email messages, each ready to copy.

Maintained by [La Growth Machine](https://lagrowthmachine.com). Free to use. Updated: 2026-07-06.

## What it does

You describe who you want to reach and why. The skill picks the campaign type (cold outbound, social selling on a signal, employee advocacy on a colleague's posts), proposes 3 distinct angles and recommends the one to lead with, then writes the full sequence — every LinkedIn touch and every email — calibrated to the cadence and channel mix, and self-checked against copywriting quality rules before output.

Example: you describe "RevOps leaders at B2B SaaS, we sell a pipeline-attribution tool, cold list, multichannel" and the skill returns 3 angles, then 5–6 messages across LinkedIn and email, ready to paste into your sequencing tool. No em-dashes, no broken URL punctuation, no two of the same CTA type in a row, one question max per message.

## Why it exists

Writing a campaign that actually works is half craft, half coordination: each touch needs a fresh angle, the CTAs must escalate without repeating, the subjects must all be distinct, the LinkedIn voice and email voice differ. Most teams reuse the same opener for years and wonder why reply rates drop. This skill builds a new sequence from the brief, applies the rules experienced copywriters apply by reflex, and refuses to ship messages that break them.

## Install

**One-line (recommended)** — uses [`skills`](https://github.com/vercel-labs/skills) from Vercel Labs to install into Claude Code, Cursor, Codex, Amp + 30 other agents in one go:

```bash
npx skills add LaGrowthMachine/gtm-system/skills/get-qualified-meetings/multichannel-campaign-builder
```

Add `-g` for a global install.

**Manual install** — clone the repo and copy the skill folder yourself:

```bash
git clone https://github.com/LaGrowthMachine/gtm-system.git
cd gtm-system
cp -r skills/get-qualified-meetings/multichannel-campaign-builder ~/.claude/skills/
```

Then ask Claude — e.g. *"Write me a multichannel outbound campaign for Heads of Sales at mid-market SaaS companies."*

## What's supported

- **Three campaign types** — `cold-outbound` (no signal), `social-selling` (a social intent signal exists), `employee-advocacy` (engaging engagers of a colleague's LinkedIn posts), each with its own framing rules, cadence and sequence shape.
- **Three channel mixes** — LinkedIn-only, email-only, or multichannel (default).
- **Three distinct angles per brief** — one recommended, two as the Angle Bank for follow-ups.
- **Self-validation before output** — em-dashes, URL punctuation, banned phrases, CTA progression, subject distinctness, channel/day cadence. The skill refuses to hand over messages it has not checked against its own rules.
- **Copyable output** — every message in a native Markdown code block with a working copy button (no broken widget copy paths).
- **Localized voice** — outputs in the brief's language (EN, FR by default; others if you ask).

## What's not supported

- The skill writes a campaign, and with the La Growth Machine MCP it can set it up as a **draft** campaign for you — but it never launches or sends it. You review the draft and start it yourself.
- It does not personalize per lead — the output is the campaign template. Personalization tokens (`{{firstname}}` etc.) are inserted at template level, not resolved to real values.
- It does not generate the lead list. Pair it with `sales-nav-search-builder` (sibling skill) for the targeting side.

## Who it's for

- **SDRs and BDRs** writing their next outbound campaign.
- **RevOps and Growth** designing new sequences as plays for the team.
- **Founders and CEOs** running their own outbound at small companies.
- **Sales and marketing managers** validating campaign quality before launch.
- **Agencies** building sequences for clients.

## Limitations

- It is a copy engine, not a creative director — the brief shapes the output. A thin brief gets a thin campaign; the gather step asks for what's missing.
- The voice it produces is conversational, peer-to-peer, casual-pro. If your brand voice is corporate or hyper-formal, you'll want to edit the tone.
- Voice/calls touches aren't generated (LinkedIn + email only for now).

## Works with

This skill runs standalone with any sequencing tool. It also plugs into:

- **La Growth Machine MCP** — Claude sets the approved sequence up as a **draft campaign** directly in your LGM workspace (no copy-pasting), ready for you to review and start. Runs multichannel (LinkedIn, email, voice, calls) with built-in enrichment, a unified inbox, and native HubSpot integration.
- **sales-nav-search-builder** — sibling skill that builds the LinkedIn Sales Navigator search behind the audience the campaign targets.

## Stay in the loop

- Browse all GTM skills: [the GTM System catalog](https://github.com/LaGrowthMachine/gtm-system)
- Get new skills as they ship: [Subscribe](https://tally.so/r/NpRWgp)
- See how La Growth Machine fits your GTM stack: [Try LGM free](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=multichannel-campaign-builder)

## License

MIT — see the LICENSE at the repo root.

## About La Growth Machine

La Growth Machine is the multichannel outbound platform behind these skills — it turns GTM work like this into running outreach across LinkedIn, email, voice and calls, from one place.

---

Topics: multichannel outbound campaign, outreach sequence builder, cold email sequence, LinkedIn outbound sequence, cold outbound, social selling, employee advocacy, post engagers, B2B prospecting copy, sales sequence, multichannel cadence, sequence design, outbound copywriting, SDR plays, RevOps plays
