# Sourcing Agent

Give Sourcing Agent a search, a post or a list and your target. It reads every profile, keeps the people worth
contacting, each with the reason, and builds a La Growth Machine audience ready for your next campaign. **It
contacts nobody.**

## 1. Install (5 minutes)

| Client | How |
|---|---|
| Claude (claude.ai or the desktop app) | Settings → Capabilities → Skills → Upload skill → pick this zip. |
| Cowork | Same as Claude: upload the zip as a skill. |
| Claude Code | Unzip into `~/.claude/skills/` so you get `~/.claude/skills/sourcing-agent/SKILL.md`. |
| Another agent (Cursor, ChatGPT, Codex…) | Unzip it anywhere and tell your agent: "Read sourcing-agent/SKILL.md and follow it." Connect the same tools in that agent. |

## 2. Connect

| Connector | Needed for | Claude / Cowork | Claude Code |
|---|---|---|---|
| La Growth Machine MCP | Required: everything | Settings → Connectors → Add custom connector → `https://mcp.lagrowthmachine.com` | `claude mcp add --transport http lgm https://mcp.lagrowthmachine.com` |
| Python 3 | Recommended: the Sales Navigator search is built by a small script. Without it, the agent builds the URL by hand. | Code execution, on by default | Installed on most machines |

The first call opens a browser tab to sign in. **There is no API key to copy, and you should never paste one in the
chat.** A Sales Navigator search is imported through a LinkedIn identity that has Sales Navigator.

## 3. Tell it who you sell to

On the first run the agent asks who you sell to and who to leave out, then keeps it in `context/offer.md`.

## 4. Run

Say, for example:

- "Find the Heads of Sales in my Sales Navigator search. Keep SaaS companies only." (paste the URL)
- "Find VP Sales at fintech companies of 50 to 500 people in France." (no URL: it builds the search)
- "Go through the people who liked our last post. Keep the ones who match our target." (paste the post URL)
- "Sort my webinar list. Keep the decision makers in sales." (attach the export)
- "Find more people like the leads who replied yes to my last campaign."

## 5. What it does and where it stops

| Step | What it does | It stops to ask you |
|---|---|---|
| 0 | For lookalikes: reads the campaign, keeps the positive replies, describes what they share | Yes, on the target |
| 1 | Without a URL: builds the Sales Navigator search from your target | Yes, before the import |
| 2 | Asks if the leads go to a new audience or feed an existing campaign, then reads or imports them | Yes, on the audience |
| 3 | Reads every profile and sorts it: match, to review, no match, with a reason | On the unclear ones, in one batch |
| 4 | Puts the matches in the audience and shows you the table of leads and reasons | Yes, on the audience name |

Guardrails: it contacts nobody, never adds leads to a running campaign without your yes, announces every credit
before spending it and stops at 50 credits per run. Your answers on unclear titles are kept, so it does not ask
twice.

Next step: launch a campaign on the audience, or hand it to Outreach Agent to write a message for each lead.

## 6. Good to know

- **Lookalikes read your replies one by one** when they are not qualified in La Growth Machine (up to 40). Qualify
  your replies in the app (interested, not interested…) and it reads them in one call. On a campaign without an
  objective, "Converted" only means "replied": the agent does not count it as a yes.
- **The Sales Navigator search** is built by a small script: Claude needs to run code (on by default in Claude and
  Cowork). Say "just the URL" if you only want the link.
- **Imports run in the background**, 5 to 20 minutes. Some plans use credits for them: the agent says so first.
- **After a LinkedIn import, company size and industry are often empty.** The agent says which criteria it could not
  judge and keeps those leads "to review" rather than guessing.
- **Your target lists** (titles that count, titles that don't, companies to leave out) are saved in a `campaigns/`
  folder of the project you work in, when your client can write files. They hold no lead data.

## 7. Feedback

At the end of a run the agent lists what could be better. Open an issue on
https://github.com/LaGrowthMachine/gtm-system.

---

Sourcing Agent · version 0.1.1 · maintained by La Growth Machine.
