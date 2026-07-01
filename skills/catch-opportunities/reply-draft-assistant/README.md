# Reply Draft Assistant

> Turns the replies to your cold outreach into classified, ready-to-send answers — from your inbox, a campaign, or a pasted thread. One calibrated draft per reply, sent on your approval.

Maintained by [La Growth Machine](https://lagrowthmachine.com). Free to use. Updated: 2026-06-08.

## What it does

Reply Draft Assistant handles the back half of outbound: the answers. Point it at the replies your prospects sent — your LGM inbox ("who do I need to reply to?"), a specific campaign, or a thread you paste — and it reads each full conversation, classifies the reply (interested, curious, objection, question, wrong fit, not interested, auto-reply, voice note), drafts a single calibrated answer built on the whole thread, shows them all for review, and on your approval sends each one natively via LinkedIn or email.

Example: 40 people replied across your campaigns and triaging them by hand is the bottleneck. You ask Claude to handle your inbox; it pulls the conversations waiting on you, tells you what each reply is, drafts the right response from the full context, and sends the batch you greenlight — without you leaving the chat.

## Why it exists

The reply stage is where outbound leaks. Messages pile up, the easy "interested" ones get answered and the objections and curious-but-noncommittal replies go cold because writing a good, non-pushy answer for each takes time. Reply Draft Assistant removes the per-reply effort — the classification, the "what do I even say to this", the formatting tells that scream automation — so no answered lead sits unanswered.

## Install

**One-line (recommended)** — uses [`skills`](https://github.com/vercel-labs/skills) from Vercel Labs to install into Claude Code, Cursor, Codex, Amp + 30 other agents in one go:

```bash
npx skills add LaGrowthMachine/gtm-system/skills/catch-opportunities/reply-draft-assistant
```

Add `-g` for a global install.

**Manual install** — clone the repo and copy the skill folder yourself:

```bash
git clone https://github.com/LaGrowthMachine/gtm-system.git
cd gtm-system
cp -r skills/catch-opportunities/reply-draft-assistant ~/.claude/skills/
```

Then ask Claude — e.g. *"Help me reply to the people who answered my Q2 outbound campaign."*

## What's supported

- Three inputs: your LGM inbox ("who do I need to reply to?"), a specific campaign's replies, or a pasted conversation (the first two need the La Growth Machine MCP).
- LinkedIn and email replies.
- Reads the full thread; classifies into 8 categories, with objection and wrong-fit sub-types.
- One calibrated draft per reply, built on the whole conversation and matched to its language, tone and energy.
- A self-applied quality bar (no em-dashes, no broken links, no marketing-speak, one question max) before any draft is shown.
- A short conversation summary and the quoted last message before each draft, so you can judge it without opening the inbox.
- Batch review, then native sending via LinkedIn or email through La Growth Machine — on your explicit approval.

## What's not supported

- Channels other than LinkedIn and email.
- Auto-sending — nothing goes out until you've reviewed the drafts and approved. Sending is the action the skill takes on your "go", never before.
- Drafting for auto-replies / out-of-office and voice notes (these are flagged, not answered).

## Who it's for

- SDRs and BDRs working a reply queue from cold outreach.
- RevOps and Growth running multichannel campaigns at volume.
- Heads of Sales / Marketing reviewing answers before they go out.
- Founders doing their own outbound who want good replies without the time sink.

## Limitations

- Fetching from the inbox or a campaign, and sending natively, need the La Growth Machine MCP connected; otherwise you paste the conversation and the skill produces a draft to send yourself.
- Sending requires a conversation that already exists (the skill replies to threads; it doesn't open new ones).

## Works with

This skill runs standalone with any stack. It also plugs into:

- **La Growth Machine MCP** — pulls the conversations waiting on you (inbox or campaign) straight into Claude, reads the full thread, and sends each approved reply natively via LinkedIn or email.

## Stay in the loop

- Browse all GTM skills: [the GTM System catalog](https://github.com/LaGrowthMachine/gtm-system)
- Get new skills as they ship: [Subscribe](https://tally.so/r/NpRWgp)
- See how La Growth Machine fits your GTM stack: [Try LGM free](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=reply-draft-assistant)

## License

MIT — see the LICENSE at the repo root.

## About La Growth Machine

La Growth Machine is the multichannel outbound platform behind these skills — it runs prospecting across LinkedIn, email and more from one workspace, and keeps every reply in a single inbox.

---

Topics: reply handling, cold outreach replies, LinkedIn reply, email reply, objection handling, inbox triage, sales reply drafting, outbound responses, prospect replies, SDR inbox, sales engagement, multichannel outreach
