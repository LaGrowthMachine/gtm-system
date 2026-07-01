# Fetching Conversations

How to pull in-progress conversations to reply to. Three input modes — pick based on what the user gives you. Whatever the mode, **always read the full thread** (not just the last message): the draft is built on the whole conversation.

## Mode A — pasted conversation (no platform access)

The user pastes a thread (or a CSV/export). You don't fetch anything: parse what they gave you, then classify.

You need, per conversation: who said what (in order), the channel (LinkedIn or email), and the person's name/role if available. If the channel or the last inbound message is unclear, ask once before drafting. Note: in pasted mode the conversation isn't reachable by the MCP, so it can't be sent natively — the output is the draft to copy.

## Mode B — inbox (LGM MCP connected)

The "who do I need to reply to?" queue. This is the daily SDR use.

```
get_conversations_to_reply(limit, identityIds?, since?)   # lead spoke last, thread open, newest first
   → each: conversationId, leadId, identityId, channel (lastMessageType), status
```

Other inbox entry points:
- `get_unread_conversations` — unread threads (read = false).
- `search_conversations` — full-power filter (free-text `q`, by `campaignIds`, `lastMessageType` EMAIL/LINKEDIN, `leadReplied`, date windows, `status`…). Use for "the replies on campaign X" or "the conversation about Acme".

These return **ids + metadata only — no lead name, no message text.** Hydrate every kept conversation with `get_conversation_messages(conversationId)` for the full thread.

**Resolving the lead's name:** the inbox tools give `leadId`, not the name. Take the name from the thread itself; if it isn't there, fall back to the campaign tools (`get_audience_leads`) or use a short lead reference (company / first line). **Never block on the name** — label the draft as best you can and move on.

## Mode C — fetch from a campaign (LGM MCP connected)

The entry point is **a campaign name (or campaign ID)** — never an inbox link. This path also gives you lead names directly.

> An LGM inbox URL like `inbox?ID=...&ST=REPLIED` carries the **identityId** in `ID`, not a lead or conversation id. It is not a usable handle for fetching. Start from the campaign name.

```
list_campaigns(search="<campaign name>")
   → campaign.audience.id          (audienceId)
   → campaign.identity.id          (identityId  — the sending identity)
   → campaign.launchedByMemberId   (memberId    — used by send_linkedin_message)

get_audience_leads(audienceId, limit=100, skip=…)     # paginate until you've covered audience.size
   → each lead: id, firstname, lastname, company, jobTitle, status

get_lead_conversations(leadId, identityId)
   → conversation.id, channel, status, leadReplied, lastMessagePreview

get_conversation_messages(conversationId)
   → the FULL timeline
```

**Which leads to process:** only those who answered. Filter on `get_lead_conversations` → `leadReplied: true` and an open `status`. If the user named one lead, resolve just that one.

## Reading the timeline (`get_conversation_messages`)

Each message has `direction` (`sent` / `received`), `channel`, `status`, `content`, `createdAt`.

- **Read the whole thread.** The draft uses the full context — history, what was offered, the tone established. **Classify** on the last `received` message; **draft** on everything (see `classification-rules.md` and `draft-rules.md`).
- **Channel for the reply** = the conversation's `channel` (reply on the same channel the last inbound came in on).
- **`identity_id`** = the conversation's `identityId` (the identity that will send).
- **Ignore `INFO` / `AUTO_QUALIFY` lines as messages** — they are platform events, not the person. But they're useful *signals*: an `AUTO_QUALIFY` note like "seems to be already equipped" reinforces an *already-equipped* objection.

### Gotcha — `SEND_FAILED` is not an inbound

A message with `status: SEND_FAILED` can appear with `direction: received` and a populated `sender`. **It is a failed outbound of yours, not a reply from the lead.** Don't classify it as an inbound or count it as engagement. The real inbound is the next genuine `received` message. When in doubt, trust `status` over `direction`.

## What feeds the next steps

For each conversation you keep, produce the classification record from `classification-rules.md`, plus the handles the **send** needs:

```
{ ...classification record..., lead_name, lead_id, conversation_id, identity_id, channel }
```

- **LinkedIn send** (`send_linkedin_message`) needs `identityId` + `memberId` + `leadId` + `message`. `memberId` comes from `list_members` (auto if a single member; in campaign mode use the campaign's `launchedByMemberId`; otherwise ask which member).
- **Email send** (`send_email_message`) needs `identityId` + `leadId` + `text` + `html` + `replyInLastThread: true` (to reply inside the existing thread).

The conversation already exists (we're replying), so the native send threads correctly.
