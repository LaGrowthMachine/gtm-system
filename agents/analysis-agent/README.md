# Analysis Agent

Ask Analysis Agent anything about your outreach, whenever a doubt comes up. It reads your full La Growth Machine
activity history, across every campaign, step, message and sender identity, answers with your numbers and gives you
one next step. **It only reads: nothing changes in your campaigns without you.**

## 1. Install (5 minutes)

| Client | How |
|---|---|
| Claude (claude.ai or the desktop app) | Settings → Capabilities → Skills → Upload skill → pick this zip. |
| Cowork | Same as Claude: upload the zip as a skill. |
| Claude Code | Unzip into `~/.claude/skills/` so you get `~/.claude/skills/analysis-agent/SKILL.md`. |
| Another agent (Cursor, ChatGPT, Codex…) | Unzip it anywhere and tell your agent: "Read analysis-agent/SKILL.md and follow it." Connect the same tools in that agent. |

## 2. Connect

| Connector | Needed for | Claude / Cowork | Claude Code |
|---|---|---|---|
| La Growth Machine MCP, with `ask_your_outbound` | Required: everything (Ultimate plan or trial, see below) | Settings → Connectors → Add custom connector → `https://mcp.lagrowthmachine.com` | `claude mcp add --transport http lgm https://mcp.lagrowthmachine.com` |

The first call opens a browser tab to sign in. **There is no API key to copy, and you should never paste one in the
chat.**

**Plan:** the full history (the `ask_your_outbound` tool of the MCP) comes with the La Growth Machine Ultimate plan
and the free trial. Our team opens the access on your workspace. Without it, the agent tells you and answers what it
can from the campaign stats.

## 3. Run

Ask in plain words, for example:

- "Rank my messages by reply rate across all my campaigns this year."
- "Which step of my campaigns loses the most leads?"
- "Does an invitation note get me more replies? Check the last 6 months."
- "Which replied leads never reached my CRM?"
- "Compare my sender identities. Who gets the most replies?"

Then keep digging: "And for founders only, on LinkedIn?"

The first question asks what to read when your workspace has several sender identities: your campaigns only, some
identities, or the whole workspace.

## 4. What you get

| Part | What it is |
|---|---|
| The answer | One or two sentences, with the number |
| The table | The numbers behind it, with campaign, message and identity names |
| The limits | The period read, what was left out for low volume, what could bias the reading |
| The next step | One concrete move. If it means changing a campaign, it is a suggestion: you decide |

Good to know:

- Questions over long periods can be refused by the server when your account is very active. The agent then narrows
  the period (about 6 months for the heavier questions) and tells you.
- Replies that reached your CRM are visible for the native HubSpot and Pipedrive syncs only.
- Email opens are noisy (Apple Mail opens every email): read them as a trend, not a fact.

For a fixed review every Monday (campaigns to fix, replies to answer first), use Performance Agent.

## 5. Feedback

At the end of a run the agent lists what could be better. Open an issue on
https://github.com/LaGrowthMachine/gtm-system.

---

Analysis Agent · version 0.1.1 · maintained by La Growth Machine.
