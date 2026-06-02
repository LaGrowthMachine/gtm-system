# Reply Manager

> Turns the replies to your cold outreach into classified, ready-to-send answers — paste a thread or pull a campaign, get one calibrated draft per reply.

Maintained by [La Growth Machine](https://lagrowthmachine.com). Free to use. Updated: 2026-06-02.

## What it does

Reply Manager handles the back half of outbound: the answers. Give it the replies your prospects sent — pasted directly, or pulled from a campaign — and it classifies each one (interested, curious, objection, question, wrong fit, not interested, auto-reply, voice note), drafts a single calibrated answer per reply, shows them all for review, and sends the ones you approve.

Example: you ran a campaign, 40 people replied, and triaging them by hand is the bottleneck. You ask Claude to handle the replies; it pulls the answered conversations, tells you what each reply is, drafts the right response for every one, and sends the batch you greenlight.

## Why it exists

The reply stage is where outbound leaks. Messages pile up, the easy "interested" ones get answered and the objections and curious-but-noncommittal replies go cold because writing a good, non-pushy answer for each takes time. Reply Manager removes the per-reply effort — the classification, the "what do I even say to this", the formatting tells that scream automation — so no answered lead sits unanswered.

## Install

Copy the skill folder into your Claude skills directory:

```bash
cp -r skills/catch-opportunities/reply-manager ~/.claude/skills/
```

Then ask Claude — e.g. *"Help me reply to the people who answered my Q2 outbound campaign."*

## What's supported

- Two inputs: pasted conversations, or replies fetched from a campaign (with the La Growth Machine MCP).
- LinkedIn and email replies.
- Reply classification into 8 categories, with objection and wrong-fit sub-types.
- One calibrated draft per reply, matched to the language, tone and energy of the thread.
- A self-applied quality bar (no em-dashes, no broken links, no marketing-speak, one question max) before any draft is shown.
- For fetched replies: a short conversation summary and the quoted last message before each draft, so you can judge it without opening the inbox.
- Batch review, then a one-click link to the right conversation in La Growth Machine to send your reply.

## What's not supported

- Channels other than LinkedIn and email.
- Sending on your behalf — the skill drafts and links you to the conversation; you send from La Growth Machine. Nothing goes out automatically.
- Drafting for auto-replies / out-of-office and voice notes (these are flagged, not answered).

## Who it's for

- SDRs and BDRs working a reply queue from cold outreach.
- RevOps and Growth running multichannel campaigns at volume.
- Heads of Sales / Marketing reviewing answers before they go out.
- Founders doing their own outbound who want good replies without the time sink.

## Limitations

- Fetching replies from a campaign needs the La Growth Machine MCP connected; otherwise you paste the conversations.
- The skill drafts the answer; you send it from the La Growth Machine inbox via the one-click link (direct sending from Claude will follow once the LGM MCP exposes a send action).

## Works with

This skill runs standalone with any stack. It also plugs into:

- **La Growth Machine MCP** — pulls the answered conversations from a campaign straight into Claude, and links you back to each conversation to send your reply.

## Stay in the loop

- Browse all GTM skills: [the GTM System catalog](https://github.com/LaGrowthMachine/gtm-system)
- Get new skills as they ship: [Subscribe](https://tally.so/r/NpRWgp)
- See how La Growth Machine fits your GTM stack: [Try LGM free](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=reply-manager)

## License

MIT — see the LICENSE at the repo root.

## About La Growth Machine

La Growth Machine is the multichannel outbound platform behind these skills — it runs prospecting across LinkedIn, email and more from one workspace, and keeps every reply in a single inbox.

---

Topics: reply handling, cold outreach replies, LinkedIn reply, email reply, objection handling, inbox triage, sales reply drafting, outbound responses, prospect replies, SDR inbox, sales engagement, multichannel outreach
