# LGM GTM Skills — Claude setup

You are looking at the **GTM System repo** maintained by [La Growth Machine](https://lagrowthmachine.com). It bundles a library of public Claude skills (sourcing, list building, campaigns, copywriting, analytics) and an MCP server that lets Claude act directly inside the user's LGM workspace.

## First-time setup

Check if the LGM MCP is already configured by running `claude mcp list` (look for a line starting with `LaGrowthMachine:`). The installer registers the MCP via `claude mcp add --scope user --transport http`, which stores the config in `~/.claude.json` at user scope (available in every project) — not in `settings.json` directly. If the `claude` CLI isn't available, ask the user whether they've already run `sh install.sh`.

**If it is NOT configured**, proactively tell the user:

> "I can see this is the LGM GTM Skills repo. Would you like me to install the LGM MCP and skills? It takes ~1 minute — I'll run `sh install.sh` for you. The installer is interactive: it'll ask whether you have an LGM account and prompt for your API key (hidden) to wire the MCP."

If they say yes, run `sh install.sh` and confirm when done.

**If it IS configured**, present the onboarding to the user:

1. Confirm MCP is connected and list the available MCP tools grouped by category (Audiences, Campaigns, Conversations & leads, Workspace).
2. List the available GTM Skills grouped by category.
3. Show the suggested first-steps table.
4. Ask: *"What would you like to do?"*

---

## What LGM gives you

Once the MCP is connected and skills are installed, two layers work together.

---

### Layer 1 — LGM MCP (Claude acts inside La Growth Machine)

The MCP gives Claude direct access to the user's LGM workspace. No copy-paste, no tab switching.

**Audiences**
- `create_audience_from_linkedin_url` — create an audience directly from a Sales Navigator search URL
- `get_audience` — fetch an existing audience by ID
- `get_audience_leads` — list all leads in an audience

**Campaigns**
- `list_campaigns` — list all campaigns in the workspace
- `get_campaign_messages` — fetch the message sequence of a campaign
- `get_campaign_stats` — get open rates, reply rates, and performance data

**Conversations & leads**
- `get_lead_conversations` — fetch all conversations for a specific lead
- `get_conversation_messages` — read the full message thread of a conversation
- `get_lead_logs` — get the activity log for a lead (visits, clicks, replies)

**Workspace**
- `list_identities` — list all identities (LinkedIn accounts, email accounts) in the workspace
- `save_identity_preference` — set a preferred identity for outreach

Tools are exposed under the namespace `mcp__LaGrowthMachine__*`.

---

### Layer 2 — GTM Skills (published in this repo)

Skills guide Claude through complex GTM workflows. Just describe what you want. Skills are categorized into 4 outcomes mirroring the GTM motion:

**Fuel my pipeline** — sourcing, list building, ICP

- `sales-nav-search-builder` — turn a natural-language ICP into a precise LinkedIn Sales Navigator search URL, ready to import as an LGM audience
- `won-deal-icp-finder` — audit your biggest closed-won deals to find your proven ICP and a look-alike target list

**Get qualified meetings** — campaigns, copywriting, sequences

- `multichannel-campaign-builder` — generate a complete LinkedIn + email sequence from a natural-language brief
- `campaign-challenger` — benchmark a campaign copy against your existing campaigns and return prioritized fixes before launch
- `campaign-impact-analyzer` — rank campaigns by real revenue impact by cross-referencing LGM campaigns with HubSpot deals
- `weekly-performance-advisor` — build a two-tab weekly cockpit from your LGM data: replies to handle, campaigns to fix, and reply-volume trends

**Catch opportunities** — reply handling, intent detection

- `reply-draft-assistant` — triage your inbox or a campaign's replies, draft the right answer from the full thread, and send it in LGM on your approval

**Secure my channels** — channel health, deliverability, identities — *coming soon*

---

## Suggested first steps

Suggest one of these depending on what the user wants to do:

| They want to… | Suggest |
|---|---|
| Build a prospect list | Use `sales-nav-search-builder` |
| Find their proven ICP from deals | Use `won-deal-icp-finder` |
| Write a campaign from scratch | Use `multichannel-campaign-builder` |
| Pressure-test a campaign before launch | Use `campaign-challenger` |
| See which campaigns drive pipeline | Use `campaign-impact-analyzer` |
| See what to do this week / campaign health | Use `weekly-performance-advisor` |
| Handle or draft replies to their inbox | Use `reply-draft-assistant` |
| Pull live campaign data | Call the MCP directly (e.g. `list_campaigns`, `get_campaign_stats`) |

---

## Tone

Be direct and outcome-focused. LGM users are GTM and growth professionals — they want pipeline results, not feature explanations. Lead with what they can accomplish, not how the tools work.
