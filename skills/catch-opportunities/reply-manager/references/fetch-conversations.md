# Fetching Conversations

How to pull in-progress conversations to reply to. There are two input modes — pick based on what the user gives you.

## Mode A — pasted conversation (no platform access needed)

The user pastes a thread (or a CSV/export). You don't fetch anything: parse what they gave you, then go straight to classification.

You need, per conversation: who said what (in order), the channel (LinkedIn or email), and the person's name/role if available. If the channel or the last inbound message is unclear, ask once before drafting.

## Mode B — fetch from a campaign (LGM MCP connected)

The entry point is **a campaign name (or campaign ID)** — never an inbox link.

> An LGM inbox URL like `inbox?ID=...&ST=REPLIED` carries the **identityId** in `ID`, not a lead or conversation id. It is not a usable handle for fetching. Always start from the campaign.

### Pipeline

```
list_campaigns(search="<campaign name>")
   → campaign.audience.id          (audienceId)
   → campaign.identity.id          (identityId  — the sending identity; also used to deep-link the inbox in the handoff)

get_audience_leads(audienceId, limit=100, skip=…)     # paginate: loop skip += 100 until you've covered audience.size
   → each lead: id, firstname, lastname, company, jobTitle, status

get_lead_conversations(leadId, identityId)
   → conversation.id, channel, status, leadReplied, lastMessagePreview

get_conversation_messages(conversationId)
   → the full timeline → classify the LAST received message
```

### Which leads to process

A campaign has many leads; you only reply to those who actually answered. Filter on `get_lead_conversations` → `leadReplied: true` (and a `status` that's still open, e.g. `OPEN`). Skip leads with no inbound.

If the user named a single lead, resolve just that one: find them in `get_audience_leads`, then their conversation.

### Reading the timeline (`get_conversation_messages`)

Each message has `direction` (`sent` / `received`), `channel`, `status`, `content`, `createdAt`.

- **Classify the last `received` message.** Earlier messages are context (see `classification-rules.md` for multi-message handling).
- **Channel for the reply** = the conversation's `channel` (reply on the same channel the last inbound came in on).
- **`identity_id` for the reply** = the conversation's `identityId` (same as the campaign identity).
- **Ignore `INFO` / `AUTO_QUALIFY` lines as messages** — they are platform events, not the person talking. But they're useful *signals*: e.g. an `AUTO_QUALIFY` note like "seems to be already equipped" reinforces an *already-equipped* objection.

### Gotcha — `SEND_FAILED` is not an inbound

A message with `status: SEND_FAILED` can appear with `direction: received` and a populated `sender`. **It is a failed outbound of yours, not a reply from the lead.** Do not classify it as an inbound or count it as engagement. The real inbound is the next genuine `received` message (often the platform re-sent your message later as a normal `sent`). When in doubt, trust `status` over `direction`.

## What feeds the next step

For each conversation you keep, produce the classification record from `classification-rules.md`, plus the handles the draft + handoff need:

```
{ ...classification record..., lead_name, identity_id, channel, conversation_id }
```

`identity_id` is what builds the inbox deep-link in the handoff (`inbox?ID=<identity_id>&ST=REPLIED`); the lead name lets the user spot the right thread there.
