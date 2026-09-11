# Outbound Nurture Engine

> Turns the replies your outbound did not convert yet ("not now", "happy to connect", went quiet) into a running nurture wave: the right content for each lead, written onto the lead, and a campaign that carries the touches every six weeks.

Maintained by [La Growth Machine](https://lagrowthmachine.com). Free to use. Updated: 2026-09-11.

Built with the La Growth Machine Creator cohort. Thanks to **Nicolas Baechel**, **Roxane Leroy** and **Fırat Berber** for the use cases and the rules that shaped it: nurture on a six-week rhythm, ask before you send content, never pitch-slap, and pick social proof that looks like the lead.

## What it does

Most replies to cold outreach are neither a yes nor a no. "Come back in October." "Happy to connect." "Interesting, send me something." Then silence, and the lead leaves the sequence with the enrichment paid and the conversation dead. Outbound Nurture Engine finds those leads in your inbox, reads each full thread to understand what they said and what they care about, and matches each one with one to three pieces of your own content: a case study that looks like their company, a playbook on the problem they named, a guide in their language. It writes one ready-to-insert sentence per content onto the lead in La Growth Machine, duplicates your nurture template campaign, fills its three messages with those sentences as variables, and assigns the wave's audience. You review everything first, then launch the campaign in the app.

Example: 40 people replied to your last two campaigns without booking. You say *"nurture my not-now leads, our content is under /gtm-playbooks/ and the template campaign is called Nurture template."* The skill lists the 23 leads worth nurturing (and the 4 it leaves to the reply assistant), shows each lead's three contents with the reason, the sentences that will go on the lead, the three campaign messages, and the pains no content covers yet. On your go, it writes the leads, creates the campaign copy and hands you the link to launch.

## Why it exists

The positive-reply rate of an outbound motion is decided after the reply as much as before it. Leads who defer or hesitate rarely get a structured follow-up: the seller either chases too soon, drops them, or sends the same PDF to everyone. Meanwhile the content that would move them exists, unread, on the website or in a Drive. This skill connects the two. Every new campaign feeds new leads into nurture; every new piece of content re-activates the leads it fits; and the gaps between what leads ask for and what the library holds become the content plan. The effect compounds with time, which a one-off follow-up never does.

## Install

**One-line (recommended)** — uses [`skills`](https://github.com/vercel-labs/skills) from Vercel Labs to install into Claude Code, Cursor, Codex, Amp + 30 other agents in one go:

```bash
npx skills add LaGrowthMachine/gtm-system/skills/catch-opportunities/outbound-nurture-engine
```

Add `-g` for a global install.

**Manual install** — clone the repo and copy the skill folder yourself:

```bash
git clone https://github.com/LaGrowthMachine/gtm-system.git
cd gtm-system
cp -r skills/catch-opportunities/outbound-nurture-engine ~/.claude/skills/
```

Then ask Claude — e.g. *"Nurture the leads who replied 'not now' to my Q2 campaigns with our case studies in Notion."*

Requires Python 3.8+ for the engine (`scripts/build.py`, no dependencies).

## What's supported

- Three inputs: your La Growth Machine inbox (replies from the last 90 days, or a set of campaigns), a CSV export from any outreach tool, or pasted threads.
- Four situations: "not now" with a return date or event, vague or non-committal replies, conversations that went silent after an exchange, and leads already in a previous wave.
- Three content sources, cumulative: a website section discovered from its sitemap (you name the category or folder, e.g. `/gtm-playbooks/`), a Notion database or page, a Google Drive folder. Or a pasted list.
- A living library index: re-run the skill after publishing a piece and it is eligible immediately; contents are tagged on the same axes as the leads (pain, persona, industry, company size, stage, language).
- Deterministic matching by a script: pain first, then persona, industry, size and stage; language mismatch excludes; a content already sent to a lead is never picked again; a generic fallback keeps every lead's set complete and is flagged.
- One ready-to-insert sentence per content, written on the lead as a custom attribute and validated (one line, one link, no punctuation glued to the URL, no dash, no template token).
- The nurture campaign: your template duplicated, its three messages filled with the lead variables, the wave's audience assigned. Cadence, likes and follow-ups run natively in La Growth Machine.
- A content-gap report: the pains your waiting leads voiced that no content covers, ranked by how many leads wait.

## What's not supported

- Launching the campaign. The skill leaves it ready; you review and launch it in the app, on purpose.
- Answering a lead who is waiting for a reply. Those are routed to `reply-draft-assistant`.
- Sending content to a lead who said no. Firm refusals and unsubscribes are left alone.
- Channels other than LinkedIn and email.

## Who it's for

- Founders and solo sellers who run their own outbound and lose deals in the follow-up.
- SDRs and BDRs with a queue of "not now" replies and no system to come back to them.
- Outbound agencies nurturing on behalf of clients who do not answer their own leads.
- Heads of Sales and RevOps who want the positive-reply rate to climb without more volume.
- Content and demand teams who want to know which content the pipeline actually needs.

## Limitations

- Writing the leads and the campaign needs the La Growth Machine MCP; without it the skill delivers the wave (leads, contents, sentences, messages) for you to apply by hand.
- The skill expects one nurture template campaign in your workspace (three message steps spaced about six weeks, a like or visit between them). It describes the shape if you have none.
- Custom attributes 8, 9 and 10 are used by default; the skill asks which slots are free and can use any three (slots 11 to 20 once your MCP accepts them on lead updates).
- Reading Notion or Google Drive needs their MCP connected; otherwise paste the list.
- Matching is only as good as the tags. The skill tags what it reads; review the first index once.
- English content is offered to every lead; content in another language only to leads who wrote in that language.

## Works with

This skill runs standalone with any stack. It also plugs into:

- **La Growth Machine MCP** — pulls the replied conversations, reads each full thread, writes the chosen contents onto each lead, duplicates and fills the nurture campaign, assigns the audience.
- **Notion MCP** — reads a database or page of resources as the content library; can hold the library index on claude.ai.
- **Google Drive MCP** — reads a folder of case studies, decks and guides as the content library.

## Stay in the loop

- Browse all GTM skills: [the GTM System catalog](../../../README.md)
- Get new skills as they ship: [Subscribe](https://tally.so/r/NpRWgp)
- See how La Growth Machine fits your GTM stack: [Try LGM free](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=outbound-nurture-engine)

## License

MIT — see the LICENSE at the repo root.

## About La Growth Machine

La Growth Machine is the multichannel outbound platform behind these skills — it runs prospecting across LinkedIn, email and more from one workspace, and keeps every reply in a single inbox.

---

Topics: lead nurturing, nurture sequence, not now replies, follow-up cadence, re-engage cold leads, warm leads, positive reply rate, sales follow-up, content-led outbound, case study matching, LinkedIn nurture campaign, outbound content strategy, SDR follow-up, lead re-engagement, multichannel outreach
