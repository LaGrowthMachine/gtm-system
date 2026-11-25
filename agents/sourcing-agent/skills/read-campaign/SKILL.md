---
name: read-campaign
description: "Sub-skill of sourcing-agent. Reads a La Growth Machine campaign, keeps the leads who replied positively and describes their common profile as a target to search for more people like them."
---

# Read a campaign

Turn "the people who said yes" into a target the agent can search for. You read and you describe. You do not write
replies, you do not change a lead status and you do not write lead data into a file.

## Step 1. Find the campaign

Use `list_campaigns` with the name the user gave. If several campaigns match, show them and ask which one. When the user
keeps campaign files (`campaigns/<name>.md` in their project folder), read the one of this campaign: it holds the
objective.

## Step 2. List the conversations with a reply

`search_conversations {campaignIds:[id], leadReplied:true, limit:50}`, paginated with `searchAfter` until `hasMore`
is false. It gives the conversation ids and the lead ids in a few calls. Do not page through
`get_campaign_leads_stats` for this: it is slow and heavy. `get_campaign_stats` gives the totals (leads contacted,
replies) for the numbers of Step 5.

## Step 3. Keep the positive replies

A reply is not positive because it exists. Use the first source that is available.

### Source 1. The qualification in La Growth Machine

Use it only when replies were really qualified in this campaign: in `get_campaign_stats`,
`engagementStats.status.won.total` or `engagementStats.status.lost.total` is above 0.

| Qualification | Counts as positive |
|---|---|
| Won: call booked, negotiating, ready to buy, converted | yes, the strongest signal |
| Won: interested | yes, with a caveat: it also covers a lead who only accepted a free resource |
| Lost: not interested, already equipped, wrong target, unsubscribed; wrong timing; out of office | no |

**"Converted" on its own means nothing here.** On a campaign with no objective, every lead who replied shows the lead
status CONVERTED and `engagementStats.converted` equals the replies. Never read it as a won deal.

### Source 2. Reading the conversation

When nothing is qualified, read the conversations (`get_conversation_messages`).

- **Read the replies to this campaign only.** A conversation is per lead, not per campaign: it can hold later
  messages from other campaigns. Keep the lead's messages between this campaign's first message and the first message
  of another campaign. Judge on the lead's clearest answer there, not blindly on the last message.
- **Cap the reading.** More than 40 conversations → read the 40 most recent and say the profile rests on a sample.
  Suggest qualifying the replies in La Growth Machine: next time Source 1 answers in one call.

Classify the lead's answer with this table, first match wins:

| # | The lead | Category | Positive |
|---|---|---|---|
| 1 | sends an automatic out-of-office reply and nothing else | Out of office | no |
| 2 | asks to stop ("stop", "remove me", "unsubscribe") | Firm no | no |
| 3 | refuses clearly ("not interested") | Firm no | no |
| 4 | disqualifies themselves (wrong person, not the target, junior, job seeker) | Wrong fit | no |
| 5 | objects to being written to by an automation or an AI | Objection. Firm no if they leave. | no |
| 6 | names a competing tool they use | Equipped | no |
| 7 | raises a blocker (price, timing, scope, tried before) with no clear interest | Objection | no |
| 8 | shows clear interest (yes, send it, let's talk, pricing, demo) | Hot | yes |
| 9 | anything else (neutral engagement, a question, "happy to connect", a thanks) | Curious | no, unless the campaign objective says otherwise |

A stop request wins over everything. A bare "yes" to a question with two parts: read which part it answers, and keep
it Curious when you cannot tell. Judge "positive" against the campaign objective: on a campaign that offers a
resource, "send it" is the expected reply. Say so and ask whether it counts.

## Step 4. Describe the common profile

For the positive leads, read `get_audience_leads` with `location`, `industry`, `companyUrl` and `shortBio`. Describe
what they share:

- job titles, grouped;
- seniority and job function;
- industry and company type;
- location and language;
- anything in the bios that comes back.

Say what the positives have that the non-positives do not, when it shows. A trait shared by everyone in the
audience describes the audience, not the people who said yes.

**Then check the profile against the context** (positioning or offer): countries, segments or company sizes the
user does not sell to. The target follows the context, not the data: drop what the context excludes and say what was
dropped and why (for example "India left out: not a market we sell to, though 38% of the yeses are there"). A
criterion the data cannot give (company size) can come from the context: say it comes from there.

## Step 5. Say how solid it is

- Give the numbers: leads contacted, replies and positive replies. Name the source used.
- Fewer than 5 positive leads: say the profile is weak and offer to fall back on the campaign's original target.
- Fields that are empty for most leads: say which, because the profile cannot rely on them.

## Step 6. Output and stop

1. The numbers, in one line.
2. The profile, as a short table.
3. The target it becomes for the search: job titles, seniority levels, job functions, location, keywords.
4. How it becomes a search: the Sales Navigator filters it maps to (title, seniority, function, industry, company
   headcount, geography), for `{SKILL_BASE}/skills/sales-nav-search-builder`. Say what has no filter (a trait read in bios, for
   example).

Then stop and ask for approval. In a routine, skip the approval and write the numbers into the recap.
