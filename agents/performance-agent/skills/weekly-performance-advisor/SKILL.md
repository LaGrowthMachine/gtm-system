---
name: weekly-performance-advisor
category: get-qualified-meetings
type: use-case
tags: [analysis]
description: "Step 1 of performance-agent. Builds the weekly cockpit from the user's La Growth Machine data: campaign status (On target, Watch, To fix), replies sorted by urgency, Fix #1 with the flagged step rewritten. Called by the master skill, not alone."
---

# Weekly Performance Advisor

> Sub-skill of `performance-agent`. Paths are relative to `SKILL_BASE`, the folder of the master `SKILL.md`. The
> master skill already checked the La Growth Machine MCP and the context before calling this file.

Generate the user's **own** Weekly Performance Advisor: a two-tab live artifact built from **their**
La Growth Machine (LGM) data. Every rule to score campaigns, classify replies and fill the dashboard is written below. The
rewrite of E6b also reads `{SKILL_BASE}/skills/campaign-challenger/references/`.

**Two hard rules, always:**

1. **Only ever show the downloading user's data.** Pull exclusively from *their* connected MCPs.
   Never inject numbers, campaign names, replies, or examples from anyone else. The template ships
   **empty**; it is filled at runtime with their live values. If you cannot pull a value, render the
   documented empty state — never a placeholder number and never a value borrowed from somewhere else.
2. **The output is a LIVE ARTIFACT, not a saved HTML file.** In Generate mode you fill the template
   in memory and render it as a live artifact **using the available artifact tool** (whatever the
   current Cowork build exposes for creating/updating an artifact — do not hard-code a tool name).
   On a refresh, **update the existing artifact** rather than creating a new one. The
   `assets/dashboard-template.html` file is the **build source only**.

---

## Two modes

- **Setup mode** (first run, or when LGM isn't connected / no identity chosen yet): interactive.
  Detect the environment, guide install if needed, ask the scoping questions. Conversational.
- **Generate mode** (every run once setup is done): run the engine, fill the template, emit the
  artifact + a short handoff. Apply output discipline here — return the artifact and a few lines of
  handoff, **no step-by-step narration**.

If setup was already done in this project (a `./.lgm-wpa/` snapshot exists and LGM is connected),
skip straight to Generate mode; only re-ask a question if something is missing.

---

## Phase 0 — Detect (silent, no questions)

Check your **own tool list** — do not ask the user what they have installed.

- **LGM MCP present?** True if tools named `mcp__*` for La Growth Machine are available, i.e. any of
  `list_identities`, `list_campaigns`, `get_campaign_stats`, `get_conversations_to_reply`,
  `get_conversation_messages`, `search_conversations`. (In a terminal you could also confirm with
  `claude mcp list` showing an LGM server, but tool presence is enough — never ask the user.)
- **CRM / deal MCP present?** Is a HubSpot MCP available (deal/company/contact tools)?
- The deal/€ layer (`campaign-impact-analyzer`) is **not part of this pack**: treat it as unavailable.

Record these two booleans and move on. Do not announce the detection.

---

## Phase 1 — LGM MCP gate

**If the LGM MCP is present:** say "LGM connected ✓" in one line and go to Phase 2.

**If the LGM MCP is absent:** the dashboard is built entirely from LGM data, so it can't run yet.
Say it in one sentence and give the "Connect" steps of `{SKILL_BASE}/README.md`. Auth is a browser sign-in: there
is **no API key to paste**. No La Growth Machine account yet → https://app.lagrowthmachine.com/register. After they
connect, re-detect (Phase 0) and continue.

Keep this friendly and short; it's a gate, not a lecture.

---

## Phase 2 — Scope (a real question, asked once)

The scope is set by the master skill (Setup, "Scope"). If it is already set in this conversation or in the latest
snapshot (`identities`), use it and do not ask again. Otherwise:

Call `list_identities`, then `list_campaigns {status:"RUNNING"}` (paginate) and count RUNNING campaigns per
`identity.id`. Keep only the identities with at least one running campaign.

- **One identity** → that is the scope, no question.
- **Several** → ask once, with three options, and show the identities with their running campaigns
  (e.g. "Alex Martin · 12 running"):
  1. **My campaigns only** → "Which identity is yours?" (default: the one with the most running campaigns). The MCP
     cannot tell which identity belongs to the person asking.
  2. **Some identities** → the user picks them (a team view: their campaigns and replies are merged).
  3. **The whole workspace** → every identity with a running campaign.

Store the selected identity id(s) and display name(s) in the snapshot (`identities`); every LGM pull below is scoped
to them. The user can change the scope any time ("track the whole workspace").

---

## Phase 3 — Deal layer (optional, additive — never blocks)

The dashboard ships a **"Deals from campaigns"** box. Without a CRM it shows `—` and the note
*"connect HubSpot to pull deal data"*. Offer the richer layer, but **never block the build on it.**

- **CRM/deal MCP present** → offer now: "Want me to add the deals/€ layer (which campaigns actually
  drove pipeline), or ship the dashboard first and add it later?"
- **No CRM MCP** → ask "What do you track deals in?" (HubSpot / Salesforce / Sheets / other / none).
  - HubSpot but not connected → offer to connect it (then it becomes "present").
  - Salesforce / Sheets / other / complex → **dashboard-first**; add the deal layer later.

The deal/€ join (`campaign-impact-analyzer`) is not in this pack. Ship the LGM-only dashboard: the deals box
shows `—` and its default note. Do not inline a join cascade.

---

## Phase 4 — Build

Run the engine (below) on the user's live data → fill every placeholder in
`assets/dashboard-template.html` → **render as a live artifact** (2 tabs) using the available
artifact tool (create on the first run, **update the existing artifact** on later runs) → write this
week's snapshot to `./.lgm-wpa/`.

## Phase 4.5 — Wire the weekly refresh (routine)

The dashboard has a ↻ **Refresh** button. It only works once a **weekly routine** exists to re-pull
the data and update the artifact — so offer to build it now (do it only if they say yes):

> **Ask (English, verbatim-ish):** *"To make the ↻ Refresh button live, I can set up a weekly routine
> that re-pulls your La Growth Machine data and updates this dashboard every Monday morning. Want me
> to set it up?"*

- **Yes →** create a scheduled task with the available scheduling tool, cadence **Monday morning
  (weekly)**, whose prompt re-runs THIS skill in Generate mode for the same identity/identities and
  **updates the existing artifact** (it does not create a new one). Suggested task prompt to store:
  > *"Run the performance-agent skill in Generate mode for identity/identities
  > [<ids>]: pull fresh La Growth Machine data, recompute the engine, update the existing Weekly
  > Performance Advisor artifact, and write this week's snapshot to ./.lgm-wpa/. Do not ask
  > questions; setup is already done."*
  - **Capture the task id the tool returns at runtime** and pass it into the template as
    `{{REFRESH_TASK_ID}}` so the ↻ button triggers *this user's* task. The id is resolved per user at
    creation time — **never hard-code an id in the shipped files.**
  - The button already calls `runScheduledTask(<that id>)` and shows a graceful message if it can't run.
- **No / skip →** fill `{{REFRESH_TASK_ID}}` with an empty string. The ↻ button then falls back to a
  friendly alert (nothing breaks); mention they can enable the routine anytime by re-running the skill.

## Phase 5 — Handoff

After the artifact renders, give a short handoff (no step narration):

- **To do** tab = your week: the moves to make, replies to handle (urgency-sorted), and the only-🔴
  campaigns to fix. **Weekly performance** tab = the stats: count KPIs with WoW/30-day deltas,
  volume-weighted health gauges, and the full campaign panorama.
- **Refresh weekly:** if they enabled the routine (Phase 4.5), the ↻ button and the Monday task keep
  the dashboard fresh; otherwise they can re-run this skill anytime (and enable the routine then).
  Deltas and the 30-day trend come alive after 2+ weeks of snapshots.
- **Routine status:** confirm whether the Monday auto-refresh was set up (Phase 4.5). If they skipped
  it, remind them the ↻ button stays inert until the routine exists.
- **Classify replies in LGM:** nudge them to tag replies (interested / not) in the LGM inbox — it
  makes next week's positive-reply count and trend sharper.
- **Fix-this buttons** in the artifact open a copy/paste prompt modal. The prompt asks `performance-agent` to
  apply that fix (or to draft the replies), so it works in a new conversation too. Nothing is applied without the
  user's go.

---

# THE ENGINE (inline — reproduce exactly)

All scoring is deterministic. Percentages are whole numbers. Use en-dash-free copy (plain hyphens).

## E1. Pull (scoped to the selected identity/identities)

1. `list_identities` → resolve the selected identity id(s) and name(s).
2. `list_campaigns {status:"RUNNING"}`, paginated with `skip` (25 per page, no identity filter exists) → keep the
   campaigns whose `identity.id` ∈ selected. Ignore the `language` field: it can be wrong. Read the language from the
   copy itself.
3. `get_campaign_stats` per kept campaign → the counters of E2 and the per-step `templates` (E6).
4. Replies — two distinct pulls (do not conflate them):
   - **Actionable "to handle" list** → `search_conversations {identityIds:[...selected], lastMessageStatus:["RECEIVED"],
     status:["OPEN"], sortField:"lastMessageAt", sortDirection:-1}`, paginated with `searchAfter`. This is the list
     where the lead spoke last and the thread is open. Do **not** use `get_conversations_to_reply` for it: it returns
     threads where you spoke last too. Drives E8 (the rows of the To do tab).
   - **This-week count set** → `search_conversations {identityIds:[...selected], leadReplied:true,
     lastMessageAtFrom:<Monday 00:00 local, in ms>}`. There is no "received since" filter: keep a thread only if, once
     read, it holds a **lead** message dated this week. Drives the E9 counts, **whether or not you already answered**.
   - For any thread in either set not yet in the latest snapshot's `classifiedReplyIds`, read
     `get_conversation_messages` and classify (incremental — don't re-classify known ids). It returns 25 messages at
     most: classify on the last messages, they are the ones that matter.
   - Conversations carry no campaign id: a reply row shows no campaign. They carry a `leadId`: get the lead's name with
     `search_lead` only for the rows you show (actionable replies), never for the counts.
5. **Cap the work.** Take the union of both pulls, minus the ids already in `classifiedReplyIds`. More than 40 left →
   classify the this-week set first (it feeds the counts), then the to-handle list newest first, 40 threads in all.
   Say how many were left in the handoff. The next run starts from the same union minus the ids it now knows, so the
   backlog empties over a few runs. Do not rely on `total` of `search_conversations` after page 1 (it comes back
   null): page until `hasMore` is false.
6. **Lead names.** The thread carries no `leadId`: take it from the search result of that thread. `search_lead`
   returns the name as stored: trim it and show first name + last name, no title.

## E2. Normalize each campaign (exact fields of `get_campaign_stats`)

All rates are **since launch**: the stats have no date window. Say "since launch" in the panorama header, never "this
week", for campaign rates. Only the reply counts of E9 are "this week".

| Value | Field of `engagementStats` |
|---|---|
| `contacted` | `replies.contacted` |
| `li.csent` (connection requests sent) | `channel.linkedin.contactRequest.sent` |
| `li.accept` | `channel.linkedin.contactRequest.newRelations / channel.linkedin.contactRequest.sent` |
| `li.msent` (leads reached by LinkedIn message) | `replies.linkedinContacted` |
| `li.reply` | `replies.linkedinReplied / replies.linkedinContacted` |
| `em.sent` | `channel.email.sent` |
| `em.contacted` (leads reached by email) | `replies.emailContacted` |
| `em.open` | `channel.email.opened / channel.email.sent` |
| `em.reply` | `replies.emailReplied / replies.emailContacted` |
| `em.click` | `channel.email.clicked / channel.email.sent` |
| `em.bounce` | `channel.email.bounced / channel.email.sent` |
| per step | `templates[]`: `templateId`, `name`, `channel` (`GOOGLE` = email), `position`, `newHtml`, `subjectNewHtml`, `sent`, `opened`, `replied`, `bounced` |

- Compute the rates from the counts, not from the `*Percent` fields (they use other denominators). Keep the raw value
  (two decimals) for scoring, round only for display.
- `li` is `null` when `channel.linkedin.activated` is false; `em` is `null` when `channel.email.activated` is false.
- `em.atag` = an email step's `newHtml` holds an `<a href` without `track="false"` (only then is click a real KPI).
- `em.tracked_open` = `channel.email.opened > 0` (opens are tracked).
- A campaign with `contacted < 20` is **low-sample**: list it, do **not** score or rank it.

## E3. Benchmark constants (BAKED — never cited, no source/brand name in the artifact)

3 zones per KPI: **🟢 on target / 🟡 watch / 🔴 to fix**. `(good, floor, direction)`:

```
linkedin_acceptance = (30, 20, up)
linkedin_reply      = (25, 15, up)
email_open          = (60, 45, up)
email_reply         = (6,  3,  up)      # cold-email calibration
email_click         = (8,  4,  up)      # shown, NOT status-driving
email_bounce        = (15, 25, down)    # lower is better
email_deliverability= (90, 80, up)      # not shown as a gauge (see note)
```
- **No deliverability gauge.** In LGM `Delivered = Sent − Bounced`, so "deliverability" is just
  `100 − bounce` — not a true inbox-placement signal. We track **bounce** instead (the actionable
  email technical-health metric). The five portfolio gauges are: LinkedIn acceptance, LinkedIn reply,
  **email bounce**, email open, email reply.
- `MIN_SEND = 10`: a KPI or step needs **≥10 sends** to be scored, else "insufficient volume".

**zone(k, v):** up → `g if v≥good else y if v≥floor else r`. down → `g if v<good else y if v≤floor else r`.
**sev(k, v)** (how far below floor, ≥0): up → `max(0,(floor−v)/floor)`; down → `max(0,(v−floor)/floor)`; round 3.
Zones and severities use the **raw** value (2.68% email reply is under the 3% floor), the display rounds.

## E4. Per-campaign KPI set (`kpis_for`)

Emit ordered `(kpi, value, state, driving)`:
- If `li`: `linkedin_acceptance` (scored if `csent≥10` else insuf), `linkedin_reply` (scored if `msent≥10` else
  insuf).
- If `em` and `em.sent≥10`: `email_reply` (scored on `em.contacted≥10`), `email_bounce`, then `email_open` **only if
  `em.tracked_open`**, then `email_click` **only if `em.atag`** (non-driving). A reply is always measurable: 0 replies on
  38 emails is a real 0%, scored red.

## E5. Primary-channel weighting → status

- `li_reach = li.msent (or 0)`, `em_reach = em.contacted (or 0)`: leads reached on each channel.
- `primary = 'li' if li_reach ≥ em_reach else 'email'`. `SEC_MIN = 0.30`.
- A channel is **scored** when its reply KPI is scored (`li.msent ≥ 10`, `em.contacted ≥ 10`).
- `balanced = both channels scored AND min(li_share, em_share) ≥ 0.30`.
- **is_driving(k):**
  - `email_click` → never driving.
  - `linkedin_*` → `li present AND li.msent≥10 AND (primary=='li' OR balanced)`.
  - `email_bounce` → driving whenever email is scored (technical health always counts).
  - `email_open` / `email_reply` → `email scored AND (primary=='email' OR balanced)`.
- `driving_reds` / `driving_yellows` = driving KPIs at 🔴 / 🟡.
- **status** = `To fix` if any driving_reds, else `Watch` if any driving_yellows, else `On target`.
  *(Internally "On target" is the healthy state; never print the words "Healthy" or "needs work".)*
- **Secondary-channel red** (a 🔴 KPI that is NOT driving, on linkedin_acceptance/linkedin_reply/
  email_open/email_reply) → don't flip the whole campaign; attach a **"email leg to fix"** or
  **"LinkedIn leg to fix"** chip instead.
- **Silent campaign:** `contacted ≥ 30` and 0 replies on every channel → never `On target`: at least `Watch`, with the
  chip "no reply yet".

## E6. Fix #1 (diagnosis) for To-fix campaigns

- **The KPI:** among `driving_reds`, the one with the highest `sev`. When two are within 0.10 of each other, take the
  first in funnel order `[email_bounce, linkedin_acceptance, email_open, linkedin_reply, email_reply]` (fix upstream
  first).
- `s = sev(k, v)`; `conf = high if s≥0.4 else medium`. **Cap conf to medium** when the flagged step has `<20` sends.
- **The step** (from `templates[]` of the stats, never from `get_campaign_messages`, which has no names nor stats):

  | Flagged KPI | Step |
  |---|---|
  | `linkedin_acceptance` | The LinkedIn connection request step(s) (name like "Contact Request", or the LinkedIn template sent first) |
  | `linkedin_reply` | Among LinkedIn **message** steps with `sent ≥ 10` (never a connection request: a name like "Contact Request", or the step whose sends match `contactRequest.sent`), the lowest `replied/sent`. Tie → more sends, then the earliest `position`. |
  | `email_open` | The first email (lowest `position` on `GOOGLE`): its subject and first line |
  | `email_reply` | Among email steps with `sent ≥ 10`, the lowest `replied/sent`. Tie → more sends, then the earliest `position`. |
  | `email_bounce` | No step: the list |

  **Never pick a breakup step.** A breakup is the last step of its channel by `position`, or a step whose copy reads as a
  farewell ("last one from me", "closing the loop"); for a per-lead step, judge on its sent examples. Do not trust the step name: some campaigns name mid-sequence
  follow-ups "BreakUp". Annotate the step type (Intro / Follow-up) in the card.
- **Cause** per KPI:
  ```
  linkedin_acceptance -> "targeting or connection note"
  linkedin_reply      -> "message copy"
  email_open          -> "subject line or setup"
  email_reply         -> "message copy"
  email_bounce        -> "list quality: verify the emails before the next push"
  ```
  Targeting and list problems are rebuilt with another La Growth Machine agent: the Sourcing Agent. Say it in the
  card, do not run it from here.
- **Channel tip** (`reco`): only when both reply KPIs are scored, one is red, and the other is **On target or Watch**
  (never recommend a red channel, and never the channel of Fix #1). Then recommend favoring the stronger channel and
  reworking or dropping the weaker leg. Both at 0% → no tip.
- **Ranking:** `prio = maxsev(driving_reds) × contacted`. To-fix cards sorted by `prio` desc.

## E6b. The rewrite of the flagged step (Fix #1 ready to apply)

For the **top 3** To-fix cards by `prio` (the others keep the diagnosis only), when the cause is copy:

| Flagged KPI | What to rewrite |
|---|---|
| `linkedin_reply`, `email_reply` | The step picked in E6 |
| `email_open` | The subject of the first email, and its first line |
| `linkedin_acceptance` | The connection note if the step has one. An empty note → no rewrite: the cause is targeting. |
| `email_bounce` | No rewrite: the cause is the list |

1. **Get the copy.** The step's `newHtml` (and `subjectNewHtml`) is in `templates[]` of the stats.
   - **Per-lead copy.** When the step is only a variable (`<p><var name="customAttributeN"/></p>`), the text was
     written upstream and stored per lead. Read 2 or 3 sent examples (`search_conversations {campaignIds:[id],
     limit:5}` then `get_conversation_messages`; skip out-of-office replies; match the step by its order in the
     thread). Then:
     - **The examples differ beyond the variables** (truly per lead): rewrite **one** example to show the direction
       and label the card "Per-lead copy: change the brief that writes `customAttributeN`, not the step". Never
       offer to apply it with `edit_campaign_message`: one fixed text would erase the personalisation.
     - **They are the same text except names or companies**: it is one fixed text stored per lead. Rewrite it as a
       normal step, with the variables put back (`{{firstname}}`, `{{companyName}}`), and say in the card that
       applying it replaces `customAttributeN` by this text for the leads still to come.
2. **Rewrite it**, with these rules:
   - Start from what works for this user: their scored campaign with the best reply rate on the same channel and at
     least 30 leads contacted (meetings booked are not in the stats, do not rank on them). If its copy is per lead and
     unreadable, take the next one with readable copy. Name what it does that the
     flagged step does not (opening, length, question, call to action).
   - Keep every `<var .../>` of the original, the language of the original copy and its channel.
   - Lengths: connection note 200 characters max; LinkedIn message 40 to 70 words; email 50 to 100 words, subject 2
     to 5 words.
   - Never open on a question (the prospecting doctrine): open on the observation, ask the one question at the end.
   - One problem, one question. The call to action follows `{SKILL_BASE}/skills/campaign-challenger/references/cta-framework.md`.
   - Only claims the context supports (the product context or the offer). No invented number.
3. **Score it** with `{SKILL_BASE}/skills/campaign-challenger/references/quality-check.md`: the 12 dimensions, then **overall = the
   mean of the 12, one decimal**. Below 7.0 → rewrite once more. Still below → show it with its score and the weakest
   dimensions. You score your own rewrite: be strict, and cite the excerpt behind each low dimension.
4. **Show both** in the card (snippet C): "Current copy" then "Proposed rewrite" with its score. Do not render the
   widgets of `campaign-challenger` and do not narrate. **Never write it into La Growth Machine from the Monday run.**
   It is applied only when the user asks, with `{SKILL_BASE}/skills/campaign-challenger/references/lgm-apply-fixes.md`
   (duplicate first when the campaign is running).
5. Store the rewrite in the snapshot (`campaigns[].fix1.rewrite`, `fix1.score`, `fix1.templateId`) so a refresh in the
   same week reuses it instead of writing a new one.

## E7. Volume-weighted portfolio gauges

For each of the five gauge KPIs, aggregate **Σnumerator / Σdenominator** across channel-active,
scored campaigns (not a mean of percentages). Round to whole %. `N_LI` = # campaigns feeding the
LinkedIn gauges; `N_EM` = # feeding the email gauges. Gauge zone = `zone(k, weightedValue)`.

## E8. Reply classification + urgency sort

- **Read only the lead's words.** `get_conversation_messages` also returns platform lines (status changes,
  auto-qualify notes) as received messages, and sometimes a message without `content`. Skip those. Email bodies hold
  signatures with phone numbers: never copy them anywhere.
- Classify each new RECEIVED reply with the 8 categories of
  `{SKILL_BASE}/skills/reply-draft-assistant/references/classification-rules.md` (one classification for the whole pack), then map:

  | Category of classification-rules.md | Class here |
  |---|---|
  | Interested | `interested` (`hot` if it asks for a call or a meeting) |
  | Curious, Question, Objection | `neutral` |
  | Not interested | `not_interested` |
  | Wrong fit | `wrong_fit` |
  | Auto / OOO, Voice message, and a greeting with no content (birthday, "thanks for connecting") | `auto`: not a reply. Out of every count and every list. A voice message is listed apart: "N voice messages to listen to in the LGM inbox". |

- **Judge on the lead's last real message.** A thumbs-up, "ok", "thanks" or an empty message sent after our closing
  message does not make a thread `interested` or `neutral`: it keeps the class of the lead's previous real message
  and goes to **To decide** (below). "Waited" is counted from the last real message.
- **A human already decided.** When the LGM lead status is a lost or won one (not interested, wrong target, already
  equipped, interested, call booked) and the lead wrote nothing new since, the thread is neither a reply to handle
  nor a thread to decide.
- **To decide** (`decide`): the threads where the user must make a call, so the lead gets qualified in La Growth
  Machine. They are not counted as positive replies. A thread goes here when:
  - the lead acknowledged our closing message (thumbs-up, "ok", "thanks") without a real answer;
  - the last real lead message is older than 45 days and nobody qualified the lead;
  - the lead closed the door ("we chose X", "we signed with X"): suggested decision "close as lost";
  - the lead left it open long ago ("not now", "next quarter") and the date has come or passed.
  For each, suggest one decision: **follow up** (a reason to write again exists), **close as lost** (not interested
  or wrong target), **mark as won** (interested, call booked), or **keep open** (wait, ask again next week). The
  decision itself is taken with the user, by the master skill (step 3 of `performance-agent`), never here.
- An Objection that leaves the door open and is recent ("not now", "how is it different from X?") is `neutral`.
- Mass event invitations, off-topic messages and goodbyes with nothing to answer are `auto`.
- `corr` = LGM auto-qualify said interested but you classified otherwise here (the auto-qualify note is not tied to a
  message: judge on the lead's last words). `chan` ∈ {LINKEDIN, EMAIL}. `act` (actionable) = `cls ∈ {interested,
  neutral}`.
- **waited days** = `floor((asOf − lastMessageAt)/86400000)`, min 0; `urgent` = actionable AND waited > 3.
- **Urgency sort** (actionable only): group 0 = call requests (`hot`), 1 = interested, 2 = neutral;
  within a group, longest-waiting first. Show a **"waited Xd"** badge per row (urgent → red marker).
- **Only interested + neutral are listed as rows**, with the lead's name (`search_lead`) and a short reason, never a
  quote of their message. `not_interested` / `wrong_fit` are collapsed to a count behind an *"open in LGM inbox ↗"*
  link; keep a small **"N corrected"** tally visible there so auto-qualify corrections stay surfaced. **No
  write-back to LGM** (the user validates in LGM).

## E9. Count KPIs (North Star, portfolio-wide, this week) — refresh-safe

Source the counts from the **this-week RECEIVED set** (E1 step 4b, `search_conversations`), **not**
from the to-handle queue, so leads you've already answered still count.

- `TOTAL_POSITIVE_REPLIES` (hero) = count of this-week received threads classified `interested`
  (incl. call requests), portfolio-wide.
- `TOTAL_REPLIES` (secondary) = count of this-week received threads (any lead reply this week), `auto` excluded.
- **Week-cumulative + refresh-safe:** persist this week's positive and total counts (and the
  `classifiedReplyIds`) in the snapshot. On a re-run **within the same ISO week**, take the **union**
  of already-counted ids and the fresh set — a refresh may only **add**, never drop, a reply already
  counted this week. (Across weeks the count resets per week, as expected.)
- Never render a "0 positive leads" hero; if zero, show `0` plainly with the delta caveat.

## E10. Period comparison (deltas)

From the rolling snapshot history in `./.lgm-wpa/` (keep ≥5 weeks):
- For each count KPI and each gauge, show **vs last week** and **vs trailing-30-day weekly average**
  (last ≤4 prior weeks). Arrow ▲/▼; **up = green, down = red — inverted for bounce** (down is good).
- Units: counts have no unit; gauges use `pt`. Zero delta → `+0`.
- **No history yet** → render `— · trend starts after 2+ weeks` and caption *"Baseline week - trends
  start after 2+ weeks of history."* With history, caption is *"Deltas compare this week vs last week
  and vs the trailing 30-day weekly average."*

## E11. Health cards (under the gauges, Weekly performance tab)

Replace any single-sentence "verdict" with two cards:
- **🟢 On target** — lists the gauges currently green (`"LinkedIn acceptance 53%, email bounce 7% ...
  - all on target."`).
- **🟡 Watch** — for each non-green gauge, `"<KPI> <v>% - <gap>pt under/over the <good>% target,
  <note>"` where note = `just optimization, not urgent` if gap ≤ 3, else `worth a pass` (or, if that
  gauge is red, `needs work`). Add the pill `N campaign(s) to fix`. Then a **red line**:
  `"Real fix: N campaign(s) to fix on their main channel - <name> (<KPI> <v>%); ... Rewrite that copy
  first."` — so 🔴 campaigns stay visible on this tab and point to the To do tab.
- **Empty state:** no 🔴 campaigns → the To-fix cards region shows
  *"No 🔴 campaigns this week - every running campaign is On target or Watch on its primary channel."*

## E12. Status lexicon (use these three words everywhere)

**🟢 On target · 🟡 Watch · 🔴 To fix** — identical on the gauge legend, the two health cards, the
panorama badges, and the campaign cards. Do **not** print "Healthy", "needs work", or "To improve".

---

# FILL CONTRACT — placeholders in `assets/dashboard-template.html`

Read `assets/dashboard-template.html`, compute the values below, replace every `{{...}}`, and render
the result as a live artifact. **Escape** all user-supplied text (campaign names, reply notes, lead
names) for HTML. **Gauge colored bands and the target tick are derived from the E3 constants at
fill-time** (see the gauge snippet) — never hardcode band widths; change a threshold and the bands move.

| Placeholder | Source / value |
|---|---|
| `{{WEEK_LABEL}}` | Monday of the current week, e.g. `Jul 6, 2026` (title only). |
| `{{LAST_UPDATE}}` | Date the pull ran, e.g. `Jul 7, 2026`. |
| `{{REFRESH_TASK_ID}}` | The scheduled-task id captured at runtime in Phase 4.5 (this user's own task). If no routine was created, fill with an **empty string** — the ↻ button then falls back to a friendly alert. **Never** ship a real id in the template file. |
| `{{SR_SUMMARY}}` | One-line screen-reader summary: `Weekly Performance Advisor, week of {WEEK_LABEL}: {posReplies} positive replies of {totalReplies}; {tofixCount} campaigns to fix; {nAct} actionable replies including {nHot} call requests.` |
| `{{TODO_COUNT}}` | `nAct` (actionable replies) — the To-do tab pill count. |
| `{{MOVES}}` | 2-3 `<li>...</li>` items (see snippet M). Built from calls, interested, neutrals, and the to-fix count. |
| `{{N_ACT}}` | actionable reply count (used in 3 spots). |
| `{{N_HOT}}` | call-request count. |
| `{{REPLY_PROMPT}}` | escaped reply-triage prompt (snippet P). |
| `{{REPLY_ROWS}}` | one `<tr>` per **actionable** reply, urgency-sorted (snippet R). |
| `{{INBOX_LINK}}` | if any non-actionable replies: the inbox link with the corrected tally (snippet I); else empty string. |
| `{{N_DECIDE}}` | count of `decide` threads. |
| `{{DECIDE_ROWS}}` | one `<tr>` per `decide` thread, oldest first: lead name, age of the last real message ("62 days ago"), channel chip, where it stands in a few words (never a quote), suggested decision. No thread → one row "Nothing to decide this week". |
| `{{DECIDE_PROMPT}}` | `Use the performance-agent skill. Go through my {N_DECIDE} threads to decide one by one: follow up, close as lost, mark as won or keep open, then qualify each lead in La Growth Machine after my answer.` (escaped) |
| `{{TOFIX_CARDS}}` | To-fix cards sorted by `prio` (snippet C); or the empty-state card (E11). |
| `{{TOTAL_POSITIVE_REPLIES}}` | `posReplies` (E9). |
| `{{TOTAL_REPLIES}}` | `totalReplies` (E9). |
| `{{POS_REPLIES_DELTA}}` / `{{TOTAL_REPLIES_DELTA}}` | delta span for each count KPI (snippet D). |
| `{{DEALS_VALUE}}` | `—` by default; deal count/€ if the deal layer ran (Phase 3). |
| `{{DEALS_NOTE}}` | `connect HubSpot to pull deal data` by default; else a short deals note. |
| `{{DELTA_CAPTION}}` | E10 caption (history vs baseline). |
| `{{N_LI}}` / `{{N_EM}}` | gauge feed counts (E7). |
| `{{GAUGES}}` | the five portfolio gauges in order: linkedin_acceptance, linkedin_reply, email_bounce, email_open, email_reply (snippet G, each wrapped in `.stat` with a delta). |
| `{{HEALTH_CARDS}}` | the `.hcards` block (E11, snippet H). |
| `{{PANORAMA_ROWS}}` | one `prow`+`drow` pair per scored campaign, To-fix first then Watch/On-target by contacted desc (snippet PANO). |
| `{{LOW_SAMPLE_ROWS}}` | the low-sample header row + one row per low-sample campaign (snippet LOW); empty string if none. |

### Snippet G — gauge (bands derived from constants)

For an "up" KPI with `(good, floor)`; needle left = `clamp(value,0,100)%`; `z = zone(k,value)`:
```
<div class="stat"><div class="k">{LABEL}</div>
 <div class="gauge"><span class="gbands">
  <span class="gb r" style="left:0;width:{floor}%"></span>
  <span class="gb y" style="left:{floor}%;width:{good-floor}%"></span>
  <span class="gb g" style="left:{good}%;width:{100-good}%"></span>
  <span class="gtick" style="left:{good}%"></span>
  <span class="gneedle {z}" style="left:{value}%"></span></span>
  <span class="gval {z}">{value}%</span><span class="gtgt">target ≥{good}%</span></div>
 <div class="dwrap">{DELTA}</div></div>
```
For a **"down"** KPI (email_bounce): bands are `g` (0→good), `y` (good→floor), `r` (floor→100), tick
at `good`, target text `target &lt;{good}%`. Labels: `LinkedIn acceptance`, `LinkedIn reply`,
`Email bounce`, `Email open`, `Email reply`. The same gauge markup (row layout via `.dg`) is reused
inside campaign detail rows — there without the `.stat`/delta wrapper.

### Snippet D — delta span
```
<span class="delta"><span class="dl">vs last wk</span> <b class="d {cls}">{▲/▼ ±d}{unit}</b><span class="dl">· vs 30d</span> <b class="d {cls}">{▲/▼ ±d}{unit}</b></span>
```
`cls` ∈ up/down/flat. No history → `<span class="delta none">- · trend starts after 2+ weeks</span>`.

### Snippet M — moves list (example shape; adapt to the data)
```
<li><b>Answer the {nHot} call requests</b> ({callNames}){ - firstCall waited Xd if urgent}. Then reply to {firstInterested} and nudge the {nNeutral} warm neutrals.</li>
<li><b>Rewrite the flagged copy</b> on the {N} campaign(s) leaking their main-channel reply rate.</li>
<li><b>Keep classifying replies in LGM</b> so next week's trend stays live.</li>
```
Drop line 1 if no replies, line 2 if no to-fix campaigns. Never fabricate; only mention names/counts present.

### Snippet R — reply row (actionable only, urgency-sorted)
```
<tr><td class="cname">{lead}{ <span class="hotpill">CALL</span> if hot}{ <span class="corrpill" title="LGM auto-qualify said interested; corrected">corrected</span> if corr}</td>
<td><span class="wbadge{ urgent}">waited {X}d</span></td>
<td><span class="chan {li|em}">{LINKEDIN|EMAIL}</span></td>
<td><span class="rcls {good|neu}">{interested|neutral}</span></td>
<td class="rnote">{why}</td></tr>
```

### Snippet I — inbox link (with corrected tally)
```
<a class="inboxlink" href="https://app.lagrowthmachine.com/" target="_blank" rel="noopener">{N} more replies (not interested / wrong fit){, M corrected} - open in LGM inbox ↗</a>
```

### Snippet P — reply-triage prompt (goes in the button's data-prompt, escaped)
```
Use the performance-agent skill to draft my replies. Handle my {nAct} actionable replies across all running campaigns, most urgent first: {nHot} call requests ({callNames}) first, then {nInterested} interested and {nNeutral} warm neutrals to nudge (some have waited over a week). Draft each in the thread language for my approval. Send nothing without my go.
```

### Snippet C — to-fix card
Card with `card-name`, a `badge tofix` + `contacted N` meta, and a **Fix-this button** whose
`data-prompt` (escaped) is built per the routing skill:
- a card with no rewrite (rank 4 and below): `Use the performance-agent skill. Campaign "{name}" is to fix ({label} {value}%, below the {floor}% floor, likely {cause}): rewrite its {step} and show me the result before anything is written.`
- copy causes with a rewrite shown (reply, open, and acceptance when the step has a note): `Use the performance-agent skill. Apply Fix #1 on campaign "{name}" ({label} {value}%, below the {floor}% floor): show me the proposed rewrite of the flagged step again, then write it into La Growth Machine only after my go (duplicate the campaign first if it is running).`
- per-lead copy (E6b step 1): `Use the performance-agent skill. Campaign "{name}" ({label} {value}%): its {step} is written per lead in {customAttributeN}. Show me the proposed direction again and help me change the brief that writes it.`
- `linkedin_acceptance` without a note: `Use the performance-agent skill. Campaign "{name}" has a {value}% acceptance rate, below the {floor}% floor: tell me what is wrong with its targeting and what search to rebuild.`
- `email_bounce`: `Use the performance-agent skill. Campaign "{name}" bounces at {value}%, over the {floor}% limit: tell me how to clean its list before the next push.`

Then the `fix1` block (Fix #1 tag, KPI label, `{conf} confidence`, `{value}% now · target ≥{good}% ·
floor {floor}% · {gap} pt(s) under target`, `Likely cause: {cause}`), optional channel-tip `reco`
box and watch/leg chips, an optional `diag-out` diagnosis line + `focus` "Current copy to rewrite"
block (verbatim step copy, channel + step type). When E6b wrote a rewrite, add right under the quote:
`<div class="focus-h"><span class="newlabel">Proposed rewrite</span><span class="score">{score}/10</span></div>
<div class="rewrite">{rewrite, escaped}</div>`. Then a `<details>` with the full-funnel gauges. Use
the exact class names from the template's CSS.

### Snippet PANO / LOW — panorama rows
`prow` (clickable) + hidden `drow` detail per scored campaign: columns Campaign, Contacted, Accept,
LI reply, Email open, Email reply, Status badge, Fix #1. Missing KPI → `—`; insufficient volume or untracked opens
→ `n/a` (class `zi`). Low-sample block: a `lowhead` row `Below sample floor - listed for
completeness, not scored`, then one `prow low` per low-sample campaign whose detail says
`{contacted} contacted · ... - not scored (below the 20-contact floor; rates on so few sends aren't
reliable).`

---

# SNAPSHOT PERSISTENCE (in the current project)

Create `./.lgm-wpa/` in the project where the skill runs and write
`./.lgm-wpa/snapshot-<YYYY>-W<ww>.json` for the current ISO week. Store:

```
{
  "week": "2026-W28",
  "identities": ["<id>", ...],
  "counts": { "posReplies": N, "totalReplies": N },
  "positiveReplyIds": ["<conversationId>", ...],   // this-week ids classified interested (for the union)
  "weekReplyIds": ["<conversationId>", ...],        // this-week ids that received a lead reply
  "gauges": { "linkedin_acceptance": %, "linkedin_reply": %, "email_bounce": %, "email_open": %, "email_reply": % },
  "campaigns": [ { "id", "name", "contacted", "status", "fix1": {...}|null, "kpis": {...} } ],
  "classifiedReplyIds": ["<conversationId>", ...]   // every id already classified (skip-list, incremental)
}
```

- **First run = baseline:** no prior snapshot → all deltas render `—` and the baseline caption.
- Before overwriting, load the latest prior snapshot to compute WoW + 30-day deltas and to skip
  already-classified reply ids. **Keep ≥5 weeks** (prune older) so the ~4-week average is computable.
- **One snapshot per ISO week.** Re-running in the same week **updates** that week's file: union
  `positiveReplyIds` / `weekReplyIds` with the fresh pull, recompute `counts` from the unions (so the
  hero count is refresh-safe and only grows within the week), then persist. Deltas always compare
  against *prior* weeks' snapshots, never the current week's earlier run.

---

# ACCEPTANCE (self-check before finishing)

- Fresh env, LGM absent → skill guided install, waited, re-detected, then proceeded.
- LGM present → detected silently, asked identity, (optionally) deals, built the artifact from the
  user's **live** data. No data from anyone but the user appears anywhere.
- Deal layer not in this pack → deals box shows `—`, nothing blocks.
- Top 3 To-fix cards with a copy cause show the current copy and a proposed rewrite scored /10 (E6b). Nothing was
  written into La Growth Machine.
- Output is a **live artifact** (2 tabs) rendered with the available artifact tool (no hard-coded
  tool name); a snapshot was written to `./.lgm-wpa/`.
- **Refresh routine offered (Phase 4.5):** on yes → Monday task created, its runtime id injected as
  `{{REFRESH_TASK_ID}}`, ↻ button live; on skip → empty id, button falls back gracefully. No real
  task id is embedded in the shipped files.
- **Counts are refresh-safe:** `posReplies`/`totalReplies` come from the this-week RECEIVED set
  (`search_conversations`), persisted and unioned within the week, so a mid-week refresh only adds
  and never drops an already-counted reply (fixes undercount from the to-handle queue).
- Single status lexicon (On target / Watch / To fix) everywhere; email reply uses 🟢≥6/🟡3-6/🔴<3;
  bounce gauge (not deliverability); no benchmark source/brand cited; English; self-contained.
