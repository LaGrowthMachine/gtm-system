# Outreach Agent

Give Outreach Agent your leads and your offer. It keeps the leads that fit, picks LinkedIn, email or both, writes the
sequence and a message for each lead, then builds the campaign in La Growth Machine as a draft. **It never launches
a campaign: you review it and you give the green light.**

## 1. Install (5 minutes)

| Client | How |
|---|---|
| Claude (claude.ai or the desktop app) | Settings → Capabilities → Skills → Upload skill → pick this zip. |
| Cowork | Same as Claude: upload the zip as a skill. |
| Claude Code | Unzip into `~/.claude/skills/` so you get `~/.claude/skills/outreach-agent/SKILL.md`. |
| Another agent (Cursor, ChatGPT, Codex…) | Unzip it anywhere and tell your agent: "Read outreach-agent/SKILL.md and follow it." Connect the same tools in that agent. |

## 2. Connect

| Connector | Needed for | Claude / Cowork | Claude Code |
|---|---|---|---|
| La Growth Machine MCP | Required: everything | Settings → Connectors → Add custom connector → `https://mcp.lagrowthmachine.com` | `claude mcp add --transport http lgm https://mcp.lagrowthmachine.com` |
| Web reading of your client | Optional: a line about each lead's company in the messages | On by default in Claude | On by default |

The first call opens a browser tab to sign in. **There is no API key to copy, and you should never paste one in the
chat.**

## 3. Tell it about your offer

On the first run the agent asks what you sell, to whom and how you talk, then keeps it in `context/offer.md`.

## 4. Run

Say, for example:

- "Build a campaign for the Heads of Sales who joined our webinar. Invite them to a demo." (attach the export)
- "Get a campaign ready for the RevOps Managers in my Clay list. Present our new offer."
- "Write a campaign for the Founders from my Sales Navigator search. Start on LinkedIn." (paste the URL)
- "Reach the Growth leads who liked our last post. Keep it short and personal." (paste the post URL)

Your leads can come from a La Growth Machine audience, a LinkedIn or Sales Navigator search, the people who liked or
commented on a post, the attendees of a LinkedIn event, or a file (CSV, Clay or Apollo export, webinar list). They can
start a new campaign or feed one you already have.

Two shortcuts are built in:

| You want | Say | What happens |
|---|---|---|
| A campaign on the people who engaged with a LinkedIn post, same message for all, in a few minutes | "Create a campaign from this post: <URL>" | It reads the post, imports the likers and commenters, writes the sequence from the post's idea and builds the draft (formerly the `post-to-campaign` skill) |
| Only the copy of a sequence, no leads yet | "Write me a multichannel campaign for <target>" | 3 angles to choose from, then every LinkedIn and email message ready to paste, and the draft built if you want it (formerly the `multichannel-campaign-builder` skill) |

## 5. What it does and where it stops

| Step | What it does | It stops to ask you |
|---|---|---|
| 1 | Takes your brief: the offer, the target, what a good reply is | Only for what is missing |
| 2 | Asks if the leads start a new campaign or feed an existing one, then reads or imports them | Yes, on the audience |
| 3 | Keeps the leads that fit your target, each with a reason | Only on the unclear ones |
| 4 | Picks LinkedIn first, email first or both, from your own results and the industry of the leads | Yes, if emails must be found (it shows the cost first) |
| 5 | Offers 3 angles (or takes yours), then writes every message | Yes, on the angle and on the messages |
| 6 | Builds the campaign as a draft, from your closest campaign or a La Growth Machine template, or gives you the exact structure to set up | Yes, on the structure, then before the first write |
| 7 | Writes the personal part of each lead's messages | Yes, you review the table |
| 8 | Pushes the leads into the campaign's audience | Yes, before attaching the audience |
| 9 | Tells you what to check before you launch | No |

Guardrails: it never launches, never adds leads to a running campaign without telling you, announces every credit
before spending it and stops at 50 credits per run.

## 6. Feedback

At the end of a run the agent lists what could be better. Open an issue on
https://github.com/LaGrowthMachine/gtm-system.

---

Outreach Agent · version 0.1.3 · maintained by La Growth Machine.
