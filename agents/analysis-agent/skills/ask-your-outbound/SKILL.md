---
name: ask-your-outbound
description: "Sub-skill of analysis-agent. Turns a question about outreach into a read-only BigQuery query on the La Growth Machine activity logs (ask_your_outbound), runs it, names the ids it returns and answers with the numbers and their limits."
---

# Ask your outbound

The method behind every answer of the Analysis Agent. One question, one or a few queries, one answer in the user's
numbers. Read only.

## Step 1. Read the guide (once per conversation)

Call `get_bigquery_logs_guide`. It is the reference: the table, the action types, the verified metric definitions,
the ready-made queries. The rules below summarise it and add what the tests on a real workspace showed.

## Step 2. Turn the question into a query

1. **Find the closest query** in `references/queries.md` (tested queries: the main campaigns, messages, steps,
   invitation note, CRM, identities, time to reply) or in the guide. Adapt it, keep its
   structure. Write from scratch only when nothing is close.
2. **Set the scope.** The workspace, one identity, some campaigns: filter on `identityId` or `campaignId`. Names come
   from the user: find the ids first (`list_campaigns {search}`, `list_identities`).
3. **Set the window.** The user's period when they give one. Otherwise 90 days, and say it. A query is refused above
   20 GB scanned: on a busy workspace, multi-step queries hold about 180 days ("this year" can be refused). When
   refused, move the start date forward one month at a time until it passes, or filter on campaigns, and say the
   period you could read.

The rules a query must follow (the server enforces some of them, the others keep the numbers right):

| Rule | How |
|---|---|
| The table | `FROM logs`, no project or dataset, no backticks |
| Read only | `SELECT` only, never `*` |
| The window | `WHERE date >= ...` in every `FROM logs`, subqueries included |
| People, not rows | `COUNT(DISTINCT leadId)` for any business number |
| Rates | `SAFE_DIVIDE(...)`, and `HAVING contacted_leads >= 30` (or the volume that fits) to drop tiny groups |
| Sent means sent | `status = 'SUCCESS'` on outbound actions |
| Contacted | an invitation counts only with a note (`templateId IS NOT NULL`) |
| Opens | `GOOGLE_OPENED` or `GOOGLE_HAS_CLICKED`; never the `_ON_` types; opens are noisy (Apple Mail): say it |
| Acceptance | `LINKEDIN_NEW_RELATION_ADDED`, after the invitation date |
| The `message` column | never select it: it can hold the sender's email address |

## Step 3. Run it

`ask_your_outbound` with the query. On an error:

| The error says | Do |
|---|---|
| It would scan more than the limit | Narrow the window or add a campaign filter, run again |
| A rule is broken (no date filter, `*`, a table path) | Fix the query, run again |
| The tool is missing, or access is refused | Stop. Say that this analysis needs the La Growth Machine Ultimate plan or a free trial, and that the team opens the access on the workspace. Offer what `get_campaign_stats` can answer instead (per campaign, since launch). |

Two failures in a row on the same question: show the query and the error, and ask how to narrow the question.

## Step 4. Name what comes back

The logs return ids. Never show a bare id to the user.

| Id | Name it with |
|---|---|
| `campaignId` | `get_campaign` with the id: `name`, `objective`, `status`. One call per campaign shown (a workspace can hold hundreds of campaigns: paging `list_campaigns` is slower). |
| `identityId` | `list_identities`: `name`. Two identities can share a name: add the last 4 characters of the id. |
| `templateId` | `get_campaign_stats` of its campaign: `templates[]` gives `name`, `position`, `channel` and the text (`newHtml`, `subjectNewHtml`). Step names repeat ("LinkedIn BreakUp #1" three times): show the name with its position. The payload is large: call it only for the campaigns you show. |
| `leadId` | `search_lead`, only when the user asks for names |

A template that is only `<var name="customAttributeN"/>` was written per lead: there is no single text to show. Say it,
and show one sent example only if the user asks (`search_conversations {campaignIds}` then
`get_conversation_messages`).

## Step 5. Answer

1. **The answer first**, in one or two sentences, with the number: "Your best message gets 34% replies, your weakest
   13%." A ranking names both ends: run the query in both orders when it returns only one.
2. **The table** behind it, names instead of ids, rates rounded, volumes next to the rates. 10 rows at most; say how
   many there are.
3. **What it does not say**: the window, the groups dropped for low volume, the biases that matter (warm campaigns
   next to cold ones, different targets, recent campaigns that have not had time to get replies, noisy opens, CRM
   syncs outside the logs). A number that looks off (an email reply rate near 0 on hundreds of emails, a 100% rate)
   can be a logging gap: say so rather than build a conclusion on it.
4. **The next step**: one concrete move, from the numbers ("Rewrite the weakest message, starting from the best
   one"). If it means changing a campaign, it is only a suggestion: say which agent or step does it.
5. **One follow-up question** the user may want next ("Same ranking for founders only, on LinkedIn?").

Offer the query when the user wants to check it. Show a chart only when the client can draw one and the question is
about a trend or a ranking.
