# LGM GTM Skills — Claude setup

You are looking at the **GTM System repo** maintained by [La Growth Machine](https://lagrowthmachine.com). It bundles a library of public Claude skills (sourcing, list building, campaigns, copywriting, analytics, reply handling) and an MCP server that lets Claude act directly inside the user's LGM workspace.

## First-time setup

Check if the LGM MCP is already configured by running `claude mcp list` (look for a line starting with `LaGrowthMachine:`). The installer registers the MCP via `claude mcp add --scope user --transport http`, which stores the config in `~/.claude.json` at user scope (available in every project). If the `claude` CLI isn't available, ask the user whether they've already run `sh install.sh`.

**If it is NOT configured**, proactively tell the user:

> "I can see this is the LGM GTM Skills repo. Would you like me to install the LGM MCP and skills? It takes ~1 minute — I'll run `sh install.sh` for you. On first use, a browser tab opens to sign in to La Growth Machine (OAuth) — new accounts can be created from that tab. No API key to copy, nothing to paste."

If they say yes, run `sh install.sh` and confirm when done.

**If it IS configured**, present the onboarding to the user:

1. Confirm MCP is connected and list the available MCP tools grouped by category (Audiences, Campaigns, Inbox, Send, Workspace, LinkedIn, BigQuery).
2. List the available GTM Skills grouped by category.
3. Show the suggested first-steps table.
4. Ask: *"What would you like to do?"*

---

## What LGM gives you

Once the MCP is connected and skills are installed, two layers work together.

---

### Layer 1 — LGM MCP (Claude acts inside La Growth Machine)

The MCP gives Claude direct access to the user's LGM workspace. No copy-paste, no tab switching. Tools are exposed under the namespace `mcp__LaGrowthMachine__*`.

**Audiences & leads**
- `list_audiences` — list every audience with id, name and lead count; the way to resolve an audience id by name (e.g. right after `create_audience_from_linkedin_url`, which returns no id)
- `get_audience` — fetch an existing audience by ID (details, size, import status)
- `get_audience_leads` — list all leads in an audience, full record (paginated with `skip`, 100 max per page)
- `create_audience_from_linkedin_url` — create or populate an audience (by name) from a LinkedIn / Sales Navigator search URL, a post's engagers, or an event's attendees; needs an `identityId` from `list_identities`; async
- `create_lead` — create or update (upsert) a lead and attach it to an audience
- `enrich_lead` — find a lead's pro email and/or refresh LinkedIn fields; spends credits, confirm-gated
- `get_enrich_result` — poll an enrichment request started by `enrich_lead`
- `get_credits` — credit balance (`total`, `perishable`); check before enriching

**Campaigns — read**
- `list_campaigns` — list all campaigns in the workspace (filter by status, search, paginate)
- `get_campaign_stats` — acceptance rate, reply rate, conversions, performance data
- `get_campaign_messages` — fetch the messages of a campaign's sequence (rendered HTML + editable `newHtml` source)
- `get_campaign_steps` — fetch the sequence structure (steps, channel, order, whether a message is attached)

**Campaigns — build / edit**
- `duplicate_campaign` — clone an existing campaign into a draft as the starting point for a new one
- `add_campaign_step_message` — add a message to an empty step of a draft campaign
- `edit_campaign_message` — edit an existing message in a campaign
- `rename_campaign` — rename a campaign (unique name)
- `set_campaign_audience` — assign or change the audience of a campaign that has not started yet (`audienceId` from `list_audiences`)
- `set_campaign_auto_enrich` — toggle auto-enrichment of the campaign's leads
- `set_campaign_out_of_office` — toggle out-of-office auto-rescheduling
- `set_campaign_crm_sync` — toggle HubSpot / Pipedrive sync (campaign must be paused, CRM plan required)
- `set_campaign_skip_rules` — toggle "skip already contacted" (campaign READY or PAUSED)

**Inbox / conversations — read**
- `get_lead_conversations` — all conversations for a specific lead
- `get_conversation_messages` — the full message thread of a conversation
- `get_lead_logs` — the activity log for a lead (sent, accepted, replied…)
- `get_unread_conversations` — inbox: unread conversations
- `get_conversations_to_reply` — inbox: conversations waiting for a reply
- `get_favourite_conversations` — inbox: starred conversations
- `search_conversations` — search the inbox by keyword, lead, campaign, audience, channel, status, dates

**Inbox / conversations — actions**
- `send_email_message` — send an email (new thread or reply); actually sends, confirm first
- `send_linkedin_message` — send a LinkedIn text or voice message (needs `identityId` + `memberId`); actually sends, confirm first
- `snooze_conversation` / `unsnooze_conversation` — snooze a thread for later
- `archive_conversation` / `unarchive_conversation` — archive / restore a thread

**Workspace**
- `list_workspaces` — list the workspaces the user can act in; only pass `workspaceId` when `multiWorkspace` is true
- `list_members` — list the members of the current workspace (source of `memberId`)
- `list_identities` — list all identities (LinkedIn accounts, email accounts) (source of `identityId`)
- `save_identity_preference` — save tone / language / style preferences for an identity's AI-generated content

**LinkedIn**
- `get_linkedin_post` — fetch a LinkedIn post's content, author and reactions from its URL

**BigQuery**
- `ask_your_outbound` — run a read-only BigQuery SELECT over the workspace's activity logs (one row = one campaign action per lead); always filter on the `date` partition
- `get_bigquery_logs_guide` — the logs schema, verified metric definitions and example queries; read before any non-trivial query

---

### Layer 2 — GTM Skills (published in this repo)

Skills guide Claude through complex GTM workflows. Just describe what you want. Skills are categorized into 4 outcomes mirroring the GTM motion:

**Fuel my pipeline** — sourcing, list building, ICP

- `sales-nav-search-builder` — turn a natural-language ICP into a precise LinkedIn Sales Navigator search URL, ready to import as an LGM audience
- `post-to-campaign` — turn a LinkedIn post into a ready-to-launch campaign: scrape the post's likers and commenters into an audience and fill a draft sequence
- `audience-icp-filter` — filter an existing audience against an ICP; sorts every lead into match / needs review / no match, strips your team and competitors, never silently drops anyone
- `won-deal-icp-finder` — audit your biggest closed-won deals to find your proven ICP and a look-alike target list
- `outreach-icp-finder` — find your proven ICP from the outreach you already ran (who replies and shows interest, who to stop contacting), from LGM data or any outreach tool's CSV export

**Get qualified meetings** — campaigns, copywriting, sequences

- `multichannel-campaign-builder` — generate a complete LinkedIn + email sequence from a natural-language brief, and create it as a draft campaign in LGM
- `campaign-challenger` — benchmark a campaign copy against your existing campaigns, return prioritized fixes, and apply them back into the campaign
- `campaign-impact-analyzer` — rank campaigns by real revenue impact by cross-referencing LGM campaigns with HubSpot deals
- `weekly-performance-advisor` — build a two-tab weekly cockpit from your LGM data: replies to handle, campaigns to fix, and reply-volume trends
- `team-performance-dashboard` — rank each sender on reply rate, your success event and conversion, surface hot leads going cold, and clone your best reps' campaigns across the team

**Catch opportunities** — reply handling, intent detection

- `reply-draft-assistant` — triage your inbox or a campaign's replies, draft the right answer from the full thread, and send it in LGM on your approval
- `objection-analyzer` — rank the objections your outbound actually gets, grade how your team handled each one, and build a battle-card playbook that sharpens every run

**Secure my channels** — channel health, deliverability, identities — *coming soon*

---

## Suggested first steps

Suggest one of these depending on what the user wants to do:

| They want to… | Suggest |
|---|---|
| Build a prospect list | Use `sales-nav-search-builder` |
| Sequence people who engaged with a LinkedIn post | Use `post-to-campaign` |
| Filter or segment an existing audience against an ICP | Use `audience-icp-filter` |
| Find their proven ICP from deals | Use `won-deal-icp-finder` |
| Find their proven ICP from replies / engagement | Use `outreach-icp-finder` |
| Write a campaign from scratch | Use `multichannel-campaign-builder` |
| Pressure-test a campaign before launch | Use `campaign-challenger` |
| See which campaigns drive pipeline | Use `campaign-impact-analyzer` |
| See what to do this week / campaign health | Use `weekly-performance-advisor` |
| See per-rep team performance / who converts best | Use `team-performance-dashboard` |
| Handle or draft replies to their inbox | Use `reply-draft-assistant` |
| Know which objections the team gets, and how to handle them | Use `objection-analyzer` |
| Pull live campaign data ad hoc | Call the MCP directly (e.g. `list_campaigns`, `get_campaign_stats`) |
| Run a custom analytics query | Call the BigQuery tools (`ask_your_outbound`, `get_bigquery_logs_guide`) |

---

## Tone

Be direct and outcome-focused. LGM users are GTM and growth professionals — they want pipeline results, not feature explanations. Lead with what they can accomplish, not how the tools work.
