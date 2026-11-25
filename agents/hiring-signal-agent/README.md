# Hiring Signal Agent

Tell Hiring Signal Agent which roles to watch. It finds the companies hiring for them, reads every job post, finds the
person who owns the hire in each company, writes their messages from the post, then feeds a La Growth Machine
campaign. **It never launches a campaign: you do.**

Built and tested by La Growth Machine on its own hiring campaigns. The outline is a frame: on your first campaign the
agent sets it up with your offer.

## 1. Install (10 minutes)

| Client | How |
|---|---|
| Claude (claude.ai or the desktop app) | Settings → Capabilities → Skills → Upload skill → pick this zip. |
| Cowork | Same as Claude: upload the zip as a skill. |
| Claude Code | Unzip into `~/.claude/skills/` so you get `~/.claude/skills/hiring-signal-agent/SKILL.md`. |
| Another agent (Cursor, ChatGPT, Codex…) | Unzip it anywhere and tell your agent: "Read hiring-signal-agent/SKILL.md and follow it." Connect the same tools in that agent. |

## 2. Connect

| Connector | Needed for | Claude / Cowork | Claude Code |
|---|---|---|---|
| La Growth Machine MCP | Required: the campaign, Sales Navigator, the push | Settings → Connectors → Add custom connector → `https://mcp.lagrowthmachine.com` | `claude mcp add --transport http lgm https://mcp.lagrowthmachine.com` |
| Apify MCP | Required: the LinkedIn job posts and the company websites | Settings → Connectors → Add custom connector → `https://mcp.apify.com` | `claude mcp add --transport http apify https://mcp.apify.com` |
| Web search of your client | Required: the career pages (Welcome to the Jungle, Teamtailor, Ashby, Greenhouse…) | On by default in Claude | On by default |
| Firecrawl | Optional: a fallback to read a company website or a career page | Settings → Connectors → the Firecrawl MCP | The `firecrawl` command line |
| Python 3 and a `.env` file | Optional: email enrichment (step 5) with the Apify lead finder | Your client's secrets for the two keys | `.env` next to the script |

Both ask you to sign in the first time. **A free Apify account is enough to test**: the free plan gives a monthly
credit. **There is no API key to paste in the chat.**

Email enrichment only (step 5): copy `tools/apify/lgm-lead-enrichment/.env.example` to `.env` in the same folder and
put your Apify token and your La Growth Machine API key in it, or store the two keys in your client's secrets. Without
them everything works except the enrichment. Never paste a key in the chat.

## 3. Tell it about your offer

On the first run the agent asks what you sell, to whom and how you talk, and keeps it in `context/offer.md`. On your
first campaign it then sets up the outline with you: which missions of a job post your offer covers, what you say for
each, and what the last message offers to send.

**Costs.** Apify runs (job posts, websites) are billed on your Apify account: the agent says the estimate before each
run, and the free plan's monthly credit covers a test. A La Growth Machine account is needed for the campaign.

## 4. Run

Say, for example:

- "Create a campaign for the companies hiring SDRs." The first time, no campaign exists: the agent builds one from
  the validated outline (as a draft), then feeds it.
- "Find the companies hiring a Head of Growth in Paris." It finds the campaign that covers this role and feeds it.
- "Add 10 leads to the campaign <name>."

**The first campaign takes about 20 to 30 minutes**: the agent first checks that your offer does the work of the role
(a role like HR or finance is usually not a signal for a sales tool, and it says so before any search), asks the
period, the company size, the language and the sender, reads 5 real posts, then sets the outline with you. A region
("PACA", "Bay Area") is a search filter: it feeds the campaign of the role, it never creates a new one. The next
runs take a few minutes.

The model campaign to duplicate is shared: « Template Hiring Signal | Apify x La Growth Machine »
(https://app.lagrowthmachine.com/campaigns_shared/6afd83a77b678cc317a833c6).

The agent keeps one small file per campaign in a `campaigns/` folder of the project you work in (roles, place, size,
sender). It never holds lead data.

## 5. What it does and where it stops

| Step | What it does | It stops to ask you |
|---|---|---|
| 0 | Finds the campaign that covers your brief, or builds one from the outline | If two campaigns fit, or on any doubt. Before building. |
| 1 to 4 | Job posts, each company's website, the right person, leaves out who is already contacted | Only on doubts |
| 5 | Finds the emails | Yes, on the credits (5 La Growth Machine credits per lead) |
| 6 and 7 | Writes the messages and shows you the table | Yes, you approve the table |
| 8 | Pushes the leads into the audience | No, once the table is approved |

Guardrails: it never launches a campaign, announces costs and stops at 50 La Growth Machine credits per run, writes
to the person who owns the problem (never HR), and keeps files that name people in `local/` only.

An example of the messages it writes, from the original campaigns of La Growth Machine (an outreach platform):
"Hi Claire, saw you're hiring a head of growth to build your outbound engine. To help before they start, we have an
agent that finds the teams you sell to and prepares the campaign to reach them. Is someone on this until then or is
it waiting for them?"

## 6. Feedback

At the end of a run the agent proposes what to improve (a mission it did not know, a case to add to the outline).
Edit the outline and the families for your offer as you go: they are yours. Open an issue on
https://github.com/LaGrowthMachine/gtm-system for anything in the agent itself.

---

Hiring Signal Agent · version 0.4.0 · maintained by La Growth Machine.
