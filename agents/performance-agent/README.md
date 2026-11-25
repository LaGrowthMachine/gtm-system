# Performance Agent

Every Monday, Performance Agent reads your La Growth Machine campaigns and replies. You get each running campaign
marked On target, Watch or To fix, the replies to answer first, and the first fix ready: the weak step of your
campaign already rewritten and scored. **It never changes a campaign and never sends a message on its own: you
decide.**

## 1. Install (5 minutes)

| Client | How |
|---|---|
| Claude (claude.ai or the desktop app) | Settings → Capabilities → Skills → Upload skill → pick this zip. |
| Cowork | Same as Claude: upload the zip as a skill. |
| Claude Code | Unzip into `~/.claude/skills/` so you get `~/.claude/skills/performance-agent/SKILL.md`. |
| Another agent (Cursor, ChatGPT, Codex…) | Unzip it anywhere and tell your agent: "Read performance-agent/SKILL.md and follow it." Connect the same tools in that agent. |

## 2. Connect

| Connector | Needed for | Claude / Cowork | Claude Code |
|---|---|---|---|
| La Growth Machine MCP | Required: everything | Settings → Connectors → Add custom connector → `https://mcp.lagrowthmachine.com` | `claude mcp add --transport http lgm https://mcp.lagrowthmachine.com` |
| Scheduled tasks of your client | Optional: the Monday run | Cowork: scheduled tasks | `/schedule` |
| Python 3 | Optional: the objection playbook (step 6) keeps its numbers with a small script | Code execution, on by default | Installed on most machines |

The first call opens a browser tab to sign in. **There is no API key to copy, and you should never paste one in the
chat.**

## 3. Tell it about your offer

Before the first rewrite or reply draft, the agent asks what you sell, to whom and how you talk, then keeps it in
`context/offer.md`. The weekly review itself does not need it.

## 4. Run

Say, for example:

- "How are my campaigns doing this week? Tell me what to fix first."
- "Which replies should I answer first today?"
- "Go through my threads to decide."
- "Apply Fix #1 on <campaign>."
- "What objections do we get?"

When your workspace has several sender identities, the first run asks what to review: your campaigns only, some
identities, or the whole workspace. It remembers the answer. Say "track the whole workspace" to change it.

## 5. What it does and where it stops

| Step | What it does | It stops to ask you |
|---|---|---|
| 1 | Reads the running campaigns of the scope you chose and your replies, marks each campaign, sorts the replies by urgency, rewrites the weak step of up to 3 campaigns to fix and scores each rewrite out of 10. Shows it all in a two-tab dashboard. | Only on the first run, for the scope |
| 2 | Drafts your replies, call requests first | Yes, you approve every draft before it is sent |
| 3 | Goes through the threads waiting for your call (a thumbs-up after the last message, no news for 45 days, a "no" nobody recorded): you say follow up, close as lost, mark as won or keep open, and it qualifies the lead in La Growth Machine | Yes, one answer per lead |
| 4 | Applies a fix you picked. If the campaign is running, it duplicates it first and fixes the copy. | Yes, before anything is written |
| 5 | Sets the Monday run | Yes, only if you want it |
| 6 | On request: your objections, ranked, with battle cards | Which campaigns and which period |

Thresholds used for the status (LinkedIn acceptance 30%, LinkedIn reply 25%, email open 60%, email reply 6%, bounce
under 15%) are written in `skills/weekly-performance-advisor/SKILL.md`. A campaign with fewer than 20 leads
contacted is listed but not scored. Campaign rates are since launch (La Growth Machine gives no weekly window for
them). The reply counts are this week's.

## 6. Run it every Monday (optional)

At the end of the first run the agent offers to set it. If your client cannot, set it yourself:

| Client | How |
|---|---|
| Cowork | Create a scheduled task, every Monday at 8 am, with the prompt: "Run the performance-agent skill in Generate mode for my identities, update the existing cockpit." |
| Claude Code | `/schedule` with the same prompt. |
| claude.ai | No schedule yet. On Monday, say "How are my campaigns doing this week?". |

The ↻ Refresh button of the dashboard works in Cowork once the Monday task exists. In other clients, ask again.

The week-over-week deltas start after two weeks of runs: the agent keeps one small snapshot per week in `.lgm-wpa/`
of your project.

## 7. Feedback

At the end of a run the agent lists what could be better. Open an issue on
https://github.com/LaGrowthMachine/gtm-system.

---

Performance Agent · version 0.1.4 · maintained by La Growth Machine.
