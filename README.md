# GTM Skills for Claude

> The open-source GTM toolkit for Claude: skills and an MCP server to run outbound from the chat.

Source your next list, turn a LinkedIn post's engagers into a campaign, write multichannel LinkedIn and email campaigns, pressure-test them against what already converted, rank your live campaigns by revenue, and handle every reply. Each skill works on its own with any stack. Connect the **La Growth Machine** MCP and Claude acts inside your workspace: it imports audiences, pulls your inbox, and sends your replies. Free, open source, MIT licensed.

[Browse skills](#catalog) · [Quick start](#install-everything-in-one-command) · [Skills library](https://lagrowthmachine.com/claude-skills/?utm_source=github&utm_medium=readme&utm_campaign=github-gtm-skills-library&utm_content=hero-skills-library) · [MCP server](https://lagrowthmachine.com/mcp/?utm_source=github&utm_medium=readme&utm_campaign=github-gtm-skills-library&utm_content=hero-mcp) · [MCP Toolkit](https://lagrowthmachine.com/mcp-toolkit/?utm_source=github&utm_medium=readme&utm_campaign=github-gtm-skills-library&utm_content=hero-mcp-toolkit) · Built by [La Growth Machine](https://lagrowthmachine.com/?utm_source=github&utm_medium=readme&utm_campaign=github-gtm-skills-library&utm_content=hero-brand)

---

## Who it's for

- RevOps and SalesOps wiring outreach into the CRM and the rest of the stack
- GTM and Growth Engineers automating the prospecting workflow
- Heads of Sales and Marketing, and CROs, who want qualified pipeline without the busywork
- Founders running their own outbound

## Agents

Each agent is one skill that runs a whole job, with the skills it needs inside its folder. Install one agent and you
get the job done end to end. They work in Claude (claude.ai, the desktop app, Cowork), Claude Code, Cursor, Codex and
any agent that reads a `SKILL.md`. On the first run, each agent asks what you sell and to whom (`context/offer.md`).

| Agent | What it does | Replaces the skills |
|---|---|---|
| [Outreach Agent](agents/outreach-agent/SKILL.md) | Takes your leads from any source (an audience, a Sales Navigator search, a post's engagers, an event, a CSV or Clay list) and your offer, keeps the ones that fit, picks LinkedIn, email or both, writes a message for each lead and builds the campaign as a draft in La Growth Machine. You launch. | `post-to-campaign`, `multichannel-campaign-builder` |
| [Sourcing Agent](agents/sourcing-agent/SKILL.md) | Finds the right people from a search, a post, a list or the yeses of a past campaign, reads every profile and keeps the matches with a reason, in an audience ready for your next campaign. Contacts nobody. | `sales-nav-search-builder`, `audience-icp-filter` |
| [Performance Agent](agents/performance-agent/SKILL.md) | Every Monday: your campaigns on target, to watch or to fix, the replies to answer first, the threads to decide, and the first fix with the weak step already rewritten. | `weekly-performance-advisor`, `campaign-challenger`, `reply-draft-assistant`, `objection-analyzer` |
| [Analysis Agent](agents/analysis-agent/SKILL.md) | Answers any question on your full outreach history with your numbers and one next step. Read-only. Needs the La Growth Machine Ultimate plan or a trial. | |
| [Hiring Signal Agent](agents/hiring-signal-agent/SKILL.md) | Finds the companies hiring for the roles you watch, the person who owns the hire, and writes each message from the job post. Uses Apify for the job posts. | |
| [Landing Page Builder](agents/landing-page-builder/SKILL.md) | Builds the message, the narrative arc, the structure and the copy of a landing page, then an HTML draft for your designer or site builder. | |

## Catalog

The standalone skills are organized into 4 categories, mirroring the GTM motion.

### Fuel my pipeline
Sourcing, list building, ICP — keeping the lead reservoir full.

| Skill | Type | What it does |
|---|---|---|
| [won-deal-icp-finder](skills/fuel-my-pipeline/won-deal-icp-finder/SKILL.md) | use-case | Audit your biggest closed-won deals to find your proven ICP and a look-alike target list |
| [outreach-icp-finder](skills/fuel-my-pipeline/outreach-icp-finder/SKILL.md) | use-case | Find your proven ICP from the outreach you already ran — who actually replies and shows interest, who to stop contacting — from La Growth Machine or any outreach tool's export |

### Get qualified meetings
Campaigns, copywriting, sequences — what converts into meetings.

| Skill | Type | What it does |
|---|---|---|
| [campaign-impact-analyzer](skills/get-qualified-meetings/campaign-impact-analyzer/SKILL.md) | use-case | Rank campaigns by real revenue impact — cross-references LGM campaigns with HubSpot deals |
| [team-performance-dashboard](skills/get-qualified-meetings/team-performance-dashboard/SKILL.md) | use-case | Rank each sender on reply rate, your success event and conversion, surface hot leads going cold, and clone your best reps' campaigns across the team |

### Catch opportunities
Reply handling, intent detection — not letting opportunities go cold.

| Skill | Type | What it does |
|---|---|---|
| [outbound-nurture-engine](skills/catch-opportunities/outbound-nurture-engine/SKILL.md) | use-case | Nurture the replies you did not convert yet (not now, vague, went quiet): match each lead with your own content, write it onto the lead, and fill a 6-week nurture campaign in LGM |

### Secure my channels
Channel health, deliverability, identities — protecting the outbound engine.

*Coming soon.*

---

## Install everything in one command

The fastest way: install all the GTM skills **and** the LGM MCP server (so Claude can act inside your La Growth Machine workspace) in one go.

```bash
curl -fsSL https://raw.githubusercontent.com/LaGrowthMachine/gtm-system/main/install.sh | sh
```

This installs:

- **The GTM agents and skills** — for Claude Code, Cursor, and Codex (`skills.sh.json` points the installer to `agents/`; the skills inside an agent install with it, never on their own) (via the [Vercel Labs `skills`](https://github.com/vercel-labs/skills) CLI under the hood)
- **The LGM MCP** — registered with Claude Code via `claude mcp add --scope user --transport http` (user scope → config stored in `~/.claude.json`, available in every project). No API key to copy: on first use a browser tab opens to sign in to La Growth Machine (OAuth). New to LGM? You can create a free account from that tab.

The script is idempotent — re-running it is safe. Want to review before running?

```bash
curl -fsSL https://raw.githubusercontent.com/LaGrowthMachine/gtm-system/main/install.sh -o lgm-install.sh
less lgm-install.sh
sh lgm-install.sh
```

**Prerequisites:** [Claude Code](https://claude.com/product/claude-code) (or [Cursor](https://cursor.sh), [Codex](https://github.com/openai/codex), [Amp](https://ampcode.com), any other supported agent) and Node.js ≥ 18.

---

## Other ways to install

### Install one skill at a time

If you only need a specific skill (no MCP), use the [Vercel Labs `skills`](https://github.com/vercel-labs/skills) CLI directly:

```bash
npx skills add LaGrowthMachine/gtm-system/agents/sourcing-agent
npx skills add LaGrowthMachine/gtm-system/skills/fuel-my-pipeline/won-deal-icp-finder
```

Replace the path with any agent or skill above. Add `-g` for a global install. Works with Claude Code, Cursor, Codex, Amp + 30 other agents.

### Manual install

Clone the repo and copy the skill folder yourself:

```bash
git clone https://github.com/LaGrowthMachine/gtm-system.git
cd gtm-system
cp -r agents/sourcing-agent ~/.claude/skills/
```

### LGM MCP on Claude.ai (web)

Claude.ai accepts HTTP MCP connectors natively. Add the LGM MCP manually:

> Settings → Connectors → Add custom connector → `https://mcp.lagrowthmachine.com`

Then upload an agent's folder (zipped) as a skill and ask Claude, e.g. *"Find RevOps leaders in EMEA SaaS and build me an audience."*

---

## La Growth Machine MCP

These skills work with any outreach stack. Install the **LGM MCP** to execute the operational steps natively from Claude — no copy-pasting between tools.

**[See the full MCP page →](https://lagrowthmachine.com/mcp/?utm_source=github&utm_medium=readme&utm_campaign=github-gtm-skills-library&utm_content=mcp-section)**

| Skill | Without LGM MCP | With LGM MCP |
|---|---|---|
| The agents | Not usable: they act in your La Growth Machine workspace | Read, sort, write and build campaigns, always waiting for your go before anything goes out |
| won-deal-icp-finder | Works on a HubSpot export you paste | Pulls deals live, attribution clean |
| outreach-icp-finder | Works on a CSV export from any outreach tool | Pulls campaign outcomes, lead attributes and real reply threads live, then turns the ICP into an audience |
| campaign-impact-analyzer | Works on pasted campaigns and deals | Cross-references LGM campaigns with HubSpot deals in one click |
| team-performance-dashboard | Needs the LGM MCP — the dashboard is built from live LGM data | Ranks every rep on reply rate, your success event and conversion from live data, with per-rep coaching |

### Connect the MCP

The La Growth Machine MCP is hosted (remote): there's nothing to run locally, and no API key to copy. On first use a browser tab opens to sign in to La Growth Machine (OAuth) — new accounts can be created from that tab. Once connected, Claude can act in your workspace: import audiences, read campaigns and stats, pull your inbox, and send replies.

**Claude Code** (and Cursor, Codex, Amp):

```bash
claude mcp add --scope user --transport http LaGrowthMachine \
  https://mcp.lagrowthmachine.com
```

**Manual config** (clients that read an MCP JSON config):

```json
{
  "mcpServers": {
    "LaGrowthMachine": {
      "type": "http",
      "url": "https://mcp.lagrowthmachine.com"
    }
  }
}
```

**Claude.ai (web):** Settings → Connectors → Add custom connector → `https://mcp.lagrowthmachine.com`

The one-line installer at the top sets this up for you automatically.

### Available tools

The MCP exposes your La Growth Machine workspace to Claude. The skills above orchestrate these tools into full workflows.

**Campaigns — read**

| Tool | What it does |
|---|---|
| `list_campaigns` | List and filter your campaigns by status or name |
| `get_campaign_stats` | Acceptance, reply and conversion rates for a campaign |
| `get_campaign_messages` | The message sequence of a campaign, with its editable source |
| `get_campaign_steps` | The steps of a campaign sequence — channel, order, whether a message is attached |

**Campaigns — build & edit**

| Tool | What it does |
|---|---|
| `duplicate_campaign` | Copy a campaign into an editable draft, without launching it |
| `add_campaign_step_message` | Write the message for an empty campaign step |
| `edit_campaign_message` | Rewrite a campaign step's message |
| `rename_campaign` | Rename a campaign (the name must be unique) |
| `set_campaign_audience` | Assign or change the audience of a campaign that hasn't started yet |
| `set_campaign_auto_enrich` | Turn auto-enrichment of a campaign's leads on or off |
| `set_campaign_out_of_office` | Turn out-of-office auto-rescheduling on or off |
| `set_campaign_crm_sync` | Turn HubSpot / Pipedrive sync on or off (campaign must be paused) |
| `set_campaign_skip_rules` | Turn the "skip already contacted" rule on or off |

**Audiences & leads**

| Tool | What it does |
|---|---|
| `list_audiences` | Every audience with id, name and lead count — how you resolve an audience id by name |
| `get_audience` | Details and import status of an audience |
| `get_audience_leads` | Leads in an audience, full record (contact, company, enrichment status, custom attributes) |
| `create_audience_from_linkedin_url` | Build an audience from a LinkedIn / Sales Navigator search, a post's engagers or an event's attendees |
| `create_lead` | Create or update a lead and attach it to an audience |
| `enrich_lead` | Find a lead's pro email and/or refresh their LinkedIn fields — spends credits, confirms the cost first |
| `get_enrich_result` | Poll the result of an enrichment request |
| `get_credits` | Your credit balance — check it before enriching |

**Leads & conversations**

| Tool | What it does |
|---|---|
| `get_lead_conversations` | A lead's conversations across channels |
| `get_conversation_messages` | The full message thread of a conversation |
| `get_lead_logs` | Activity log for a lead (sent, accepted, replied…) |

**Inbox**

| Tool | What it does |
|---|---|
| `get_conversations_to_reply` | Conversations waiting on your reply |
| `get_unread_conversations` | Unread conversations |
| `get_favourite_conversations` | Starred conversations |
| `search_conversations` | Filter the whole inbox (campaign, channel, date, status…) |

**Send & manage**

| Tool | What it does |
|---|---|
| `send_linkedin_message` | Send a LinkedIn message (text or voice note) |
| `send_email_message` | Send an email, with thread-aware replies |
| `snooze_conversation` / `unsnooze_conversation` | Snooze a conversation until later |
| `archive_conversation` / `unarchive_conversation` | Archive or restore a conversation |

**Account & workspace**

| Tool | What it does |
|---|---|
| `list_identities` | Your connected LinkedIn / email identities |
| `list_members` | The members of your LGM account |
| `list_workspaces` | The workspaces you can act in, when your account spans several |
| `save_identity_preference` | Save tone, language or style preferences for an identity's AI-generated content |

**LinkedIn**

| Tool | What it does |
|---|---|
| `get_linkedin_post` | Read a LinkedIn post's content and engagement from its URL |

**Analytics (BigQuery)**

| Tool | What it does |
|---|---|
| `ask_your_outbound` | Run a read-only SQL query over your outbound activity logs in BigQuery — funnels, reply times, per-step rates |
| `get_bigquery_logs_guide` | The logs schema, verified metric definitions and example queries — read it before querying |

**→ [Try La Growth Machine free](https://app.lagrowthmachine.com/register/?utm_source=github&utm_medium=readme&utm_campaign=github-gtm-skills-library&utm_content=github-gtm-skills-library-readme)**

---

## Get new skills as soon as they ship

A new outbound workflow drops every week — a skill, a playbook, or an MCP scenario. They all land on the [MCP Toolkit](https://lagrowthmachine.com/mcp-toolkit/?utm_source=github&utm_medium=readme&utm_campaign=github-gtm-skills-library&utm_content=drops-mcp-toolkit).

**→ [Subscribe](https://tally.so/r/NpRWgp)** to get each one the day it ships.

---

## License

MIT — see [LICENSE](LICENSE).

## Built by La Growth Machine

LGM is the multichannel outbound platform behind these skills. We use this exact toolkit internally.

[lagrowthmachine.com](https://app.lagrowthmachine.com/register/?utm_source=github&utm_medium=readme&utm_campaign=github-gtm-skills-library&utm_content=github-gtm-skills-library-readme)
