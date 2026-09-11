# Nurture situations

Which replies belong in a nurture wave, and which do not. Read the **whole thread**; the label describes where the conversation stands, not the last message alone.

## The four situations

| Situation | What it looks like | Who labels it |
|---|---|---|
| `not_now` | The lead is open but defers: "come back in October", "after our fundraise", "not a priority this quarter", "ping me next year". A date or an event is often given: capture it as `return_condition`. | you |
| `vague` | Polite engagement without commitment: "happy to connect", "thanks for the invite", a thumbs-up or a smiley, "interesting, send me something", "we'll see". The lead left the sequence and nobody followed up. | you |
| `ghosted` | The lead replied, you answered, then silence for `--ghost-days` (default 10). Not a reply waiting on you; a conversation that died after an exchange. | the engine, from `last_received_at` / `last_sent_at` |
| `in_nurture` | Already in a previous wave (a member of a nurture audience, or custom attributes already filled). Eligible for a new content that fits, never for one already sent. | you, from the audience or the attributes |

## Not nurture (route elsewhere)

| Case | Route |
|---|---|
| The lead spoke last and awaits an answer (a question, an objection, an "interested") | `reply-draft-assistant`. The engine excludes these as `awaiting_reply` when dates show the lead spoke last. |
| Firm refusal: "not interested", "remove me", "stop", unsubscribe | Nothing. Respect it. |
| Out of office, auto-reply | Nothing now; the thread stays in the inbox. |
| Wrong person who names the right one, or who forwarded your content to a colleague | Not nurture: a referral. Ask who the right contact is (reply-draft-assistant), then a new campaign for that person. Note them in the review under "referrals" so they are not lost. |
| An open ask from you is pending (an intro, a call invitation) | Not nurture yet: a nurture touch would collide with the ask. Note them under "open asks". |
| Meeting booked or in progress | The sales process, not the skill. |

## Triage tree (top-down, first match wins)

```
1. Unsubscribed / firm refusal / auto-reply            → out
2. The lead spoke last (question, objection, yes)      → out, reply-draft-assistant
3. Explicit deferral with or without a date            → not_now
4. Polite, non-committal, no question, no next step    → vague
5. You spoke last, N+ days of silence after a reply    → ghosted (engine)
6. Already in a nurture audience                       → in_nurture
```

Two sellers can disagree on step 3: some read "in three months" as a no in disguise, others nurture it for months and close it. Do not decide for the user: keep the lead, and let the first-run question ("anyone to exclude?") apply their rule.

## The nurture profile (what you extract per lead)

| Field | Source | Notes |
|---|---|---|
| `lead_id` | MCP or export | required, the write key |
| `name` | thread or audience | for the review table only |
| `situation` | triage above | `not_now`, `vague`, `in_nurture`; leave empty for the engine to decide `ghosted` |
| `pains[]` | the lead's own words | 1 to 3 short phrases: "reply handling", "no time for follow-ups", "AI visibility". Keep their vocabulary; the library is tagged the same way. |
| `persona` | job title | normalized function: founder, sales, marketing, ops, revops, growth, recruiting… |
| `industry` | lead record | plain words: "marketing agency", "saas", "logistics" |
| `company_size` | lead record | one of `1-10`, `11-50`, `51-200`, `201-1000`, `1000+`, or empty |
| `language` | thread | `en`, `fr`, `de`… the wave's messages follow it |
| `return_condition` | thread | "October", "after the fundraise": goes into the first sentence when present |
| `already_sent[]` | thread + attributes | every URL already shared with this lead, short links resolved to the final URL (the engine dedups on the exact URL) |
| `last_received_at`, `last_sent_at` | thread | ISO dates; the engine uses them for `ghosted` and `awaiting_reply` |

Keep it factual. A pain you infer is worth less than a pain they wrote.
