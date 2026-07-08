---
name: weekly-performance-advisor
category: get-qualified-meetings
type: use-case
tags: [analysis]
description: "Generate your Weekly Performance Advisor dashboard from your La Growth Machine data: a two-tab cockpit (To do + Weekly performance) that flags campaigns to fix, sorts replies by urgency, and tracks reply volume week over week. It pulls only YOUR live LGM data, scores each running campaign against baked 3-zone benchmarks, classifies your untagged replies, and renders a live artifact you can re-open every Monday. Use when the user wants a weekly outbound performance dashboard, a Monday cockpit, campaign health at a glance, \"how are my campaigns doing this week\", \"who do I need to reply to\", or a reply-triage + campaign-health view. Triggers on: 'weekly performance dashboard', 'my outbound cockpit', 'weekly performance advisor', 'campaign health this week', 'how are my campaigns doing this week', 'my Monday cockpit'. First run does a short setup (detect + connect LGM, pick the identity, optional deal layer); every run after that just rebuilds the dashboard. Maintained by La Growth Machine."
---

# Weekly Performance Advisor

Generate the user's **own** Weekly Performance Advisor: a two-tab live artifact built from **their**
La Growth Machine (LGM) data. This skill is **fully self-contained** — every rule needed to detect
the environment, score campaigns, classify replies, and fill the dashboard is written below. It
references no other document.

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
- **`campaign-impact-analyzer` skill available?** (used to build the optional deal/€ layer.)

Record these three booleans and move on. Do not announce the detection.

---

## Phase 1 — LGM MCP gate

**If the LGM MCP is present:** say "LGM connected ✓" in one line and go to Phase 2.

**If the LGM MCP is absent:** the dashboard is built entirely from LGM data, so it can't run yet.
Explain that in one sentence, then guide the install (do not ask "is it installed?" — you already
know it isn't):

1. From the `gtm-system` repo, run the installer and complete browser sign-in:
   ```bash
   sh install.sh
   ```
   (or the curl one-liner the repo's README provides). Auth is **browser OAuth** — there is **no API
   key to paste**.
2. No LGM account yet → point them to register at https://app.lagrowthmachine.com and then re-run
   the installer.
3. After they've run it, **re-detect** (Phase 0). Loop until the LGM tools appear, then continue.

Keep this friendly and short; it's a gate, not a lecture.

---

## Phase 2 — Identity scope (a real question)

Call `list_identities`. Then, to pick a sensible default, get each identity's campaign load: call
`list_campaigns {status:"RUNNING"}` (paginate) and count RUNNING campaigns per `identity.id`.

Ask which identity to track, **defaulting to the identity running the most RUNNING campaigns**
(name it, and ask them to confirm or switch). Mention they can add more identities later for a
team-wide view (the dashboard supports multiple identities — union their campaigns and replies).

Store the selected identity id(s) and display name(s); every LGM pull below is scoped to them.

---

## Phase 3 — Deal layer (optional, additive — never blocks)

The dashboard ships a **"Deals from campaigns"** box. Without a CRM it shows `—` and the note
*"connect HubSpot to pull deal data"*. Offer the richer layer, but **never block the build on it.**

- **CRM/deal MCP present** → offer now: "Want me to add the deals/€ layer (which campaigns actually
  drove pipeline), or ship the dashboard first and add it later?"
- **No CRM MCP** → ask "What do you track deals in?" (HubSpot / Salesforce / Sheets / other / none).
  - HubSpot but not connected → offer to connect it (then it becomes "present").
  - Salesforce / Sheets / other / complex → **dashboard-first**; add the deal layer later.

**Delegation (do not re-implement the join here):**

- If `campaign-impact-analyzer` **is available** → delegate the LGM×CRM cross-reference to it to
  populate the "Deals from campaigns" box (deal count + €, this week, portfolio-wide). Use its output
  to fill `{{DEALS_VALUE}}` / `{{DEALS_NOTE}}`.
- If `campaign-impact-analyzer` **is not available** → do **not** block and do **not** inline a join
  cascade. Ship the LGM-only dashboard (deals box shows `—`) and, in the handoff, add the pointer:
  *"For the deals/€ layer, install `campaign-impact-analyzer` from gtm-system, then re-run."*

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
  > *"Re-run the weekly-performance-advisor skill in Generate mode for identity/identities
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
- **Fix-this buttons** in the artifact open a copy/paste prompt modal (the ready-made prompt targets
  the matching gtm-system skill — `/reply-draft-assistant`, `/campaign-challenger`, `/sales-nav-search-builder`,
  `/won-deal-icp-finder`) to paste into a new conversation.

---

# THE ENGINE (inline — reproduce exactly)

All scoring is deterministic. Percentages are whole numbers. Use en-dash-free copy (plain hyphens).

## E1. Pull (scoped to the selected identity/identities)

1. `list_identities` → resolve the selected identity id(s) and name(s).
2. `list_campaigns {status:"RUNNING"}` (paginate) → keep campaigns whose `identity.id` ∈ selected.
3. `get_campaign_stats` per kept campaign → per-channel counters.
4. Replies — two distinct pulls (do not conflate them):
   - **Actionable "to handle" list** → `get_conversations_to_reply {identityIds:[...selected]}`:
     threads currently awaiting *your* reply. Drives E8 (the rows shown on the To do tab).
   - **This-week count set** → `search_conversations` filtered to **RECEIVED this week** (the lead
     replied since Monday), scoped to the selected identities — **regardless of whether you've
     already answered**. Drives the E9 count KPIs. This is what makes the hero count accurate: an
     "interested" lead you already replied to has left the *to-handle* queue but must still be
     counted this week.
   - For any thread in either set not yet in the latest snapshot's `classifiedReplyIds`, read
     `get_conversation_messages` and classify (incremental — don't re-classify known ids).

## E2. Normalize each campaign

```
campaign = {
  id, name, contacted,
  li: {accept, reply, csent, msent} | null,     // % values; csent = connection-request sends, msent = message sends
  em: {sent, deliv, open, reply, click, bounce, atag, eng} | null
}
```
- `atag` = the email step contains a tracked `<a href>` link (only then is click a real KPI).
- `eng` = email had any engagement to score = (email reply > 0) OR (email click > 0).
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

## E4. Per-campaign KPI set (`kpis_for`)

Emit ordered `(kpi, value, state, driving)`:
- If `li`: `linkedin_acceptance` (scored if `csent≥10` else insuf), `linkedin_reply` (scored if
  `msent≥10` else insuf).
- If `em` and `em.sent≥10` and `em.eng`: `email_open`, `email_reply`, then `email_click` **only if
  `em.atag`** (non-driving), then `email_bounce`.
- If `em` and `em.sent≥10` and **not** `em.eng`: no email KPIs scored → render the line
  *"Email: {sent} sent · {open}% open · 0 replies · 0 clicks - delivered, no engagement to score"*.

## E5. Primary-channel weighting → status

- `li_sends = li.msent (or 0)`, `em_raw = em.sent (or 0)`, `total = li_sends + em_raw`.
- `primary = 'li' if li_sends ≥ em_raw else 'email'`. `SEC_MIN = 0.30`.
- `balanced = li_sends>0 AND em scored AND min(li_share, em_share) ≥ 0.30`.
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

## E6. Fix #1 (diagnosis) for To-fix campaigns

- Among `driving_reds`, pick the weakest step in **funnel order**, EXCLUDING the terminal breakup step:
  `FUNNEL = [email_bounce, linkedin_acceptance, email_open, linkedin_reply, email_reply]` → take the
  first in this order that is red.
- `s = sev(k, v)`; `conf = high if s≥0.4 else medium`. **Cap conf to medium** when the flagged step
  has `<20` sends (driving evidence is thin). When you show verbatim "current copy", annotate the
  step type (Intro / Follow-up / BreakUp); the flagged step must not be the breakup.
- **Cause + routing skill** per KPI:
  ```
  linkedin_acceptance -> "targeting or connection note" -> sales-nav-search-builder
  linkedin_reply      -> "message copy"                 -> campaign-challenger
  email_open          -> "subject line or setup"        -> campaign-challenger
  email_reply         -> "message copy"                 -> campaign-challenger
  email_bounce        -> "list quality / warm-up"       -> won-deal-icp-finder   (also flag list hygiene / email verification)
  ```
- **Channel tip** (`reco`): if both LinkedIn reply and email reply are scored and one is red while the
  other is green/yellow, recommend favoring the stronger channel and reworking/dropping the weaker leg.
- **Ranking:** `prio = maxsev(driving_reds) × contacted`. To-fix cards sorted by `prio` desc.

## E7. Volume-weighted portfolio gauges

For each of the five gauge KPIs, aggregate **Σnumerator / Σdenominator** across channel-active,
scored campaigns (not a mean of percentages). Round to whole %. `N_LI` = # campaigns feeding the
LinkedIn gauges; `N_EM` = # feeding the email gauges. Gauge zone = `zone(k, weightedValue)`.

## E8. Reply classification + urgency sort

- Classify each new RECEIVED reply into `interested / neutral / not_interested / wrong_fit` from the
  thread. `hot` = explicit call/meeting request. `corr` = LGM auto-qualify said interested but you
  corrected it here. `chan` ∈ {LINKEDIN, EMAIL}. `act` (actionable) = `cls ∈ {interested, neutral}`.
- **waited days** = `floor((asOf − lastMessageAt)/86400000)`, min 0; `urgent` = actionable AND waited > 3.
- **Urgency sort** (actionable only): group 0 = call requests (`hot`), 1 = interested, 2 = neutral;
  within a group, longest-waiting first. Show a **"waited Xd"** badge per row (urgent → red marker).
- **Only interested + neutral are listed as rows.** `not_interested` / `wrong_fit` are collapsed to a
  count behind an *"open in LGM inbox ↗"* link; keep a small **"N corrected"** tally visible there so
  auto-qualify corrections stay surfaced. **No write-back to LGM** (the user validates in LGM).

## E9. Count KPIs (North Star, portfolio-wide, this week) — refresh-safe

Source the counts from the **this-week RECEIVED set** (E1 step 4b, `search_conversations`), **not**
from the to-handle queue, so leads you've already answered still count.

- `TOTAL_POSITIVE_REPLIES` (hero) = count of this-week received threads classified `interested`
  (incl. call requests), portfolio-wide.
- `TOTAL_REPLIES` (secondary) = count of this-week received threads (any lead reply this week).
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
Use the /reply-draft-assistant skill. Handle my {nAct} actionable replies across all running campaigns, most urgent first: {nHot} call requests ({callNames}) first, then {nInterested} interested and {nNeutral} warm neutrals to nudge (some have waited over a week). Draft each in the thread language for my approval. If the /reply-draft-assistant skill is not installed, download it from https://github.com/LaGrowthMachine/gtm-system first, then run it.
```

### Snippet C — to-fix card
Card with `card-name`, a `badge tofix` + `contacted N` meta, and a **Fix-this button** whose
`data-prompt` (escaped) is built per the routing skill:
- `campaign-challenger`: `Use the /campaign-challenger skill. Challenge campaign "{name}" ({label} {value}%, below the {floor}% floor, likely {cause}): rewrite the current copy of the flagged step. If the /campaign-challenger skill is not installed, download it from https://github.com/LaGrowthMachine/gtm-system first, then run it.`
- `sales-nav-search-builder`: `... Rebuild the targeting for campaign "{name}" ({label} {value}%, below the {floor}% floor): draft a tighter Sales Navigator search and connection note. ...`
- `won-deal-icp-finder`: `... Clean the audience for campaign "{name}" ({label} {value}%, below the {floor}% floor): rebuild it from a verified ICP list. ...`

Then the `fix1` block (Fix #1 tag, KPI label, `{conf} confidence`, `{value}% now · target ≥{good}% ·
floor {floor}% · {gap} pt(s) under target`, `Likely cause: {cause}`), optional channel-tip `reco`
box and watch/leg chips, an optional `diag-out` diagnosis line + `focus` "Current copy to rewrite"
block (verbatim step copy, channel + step type), and a `<details>` with the full-funnel gauges. Use
the exact class names from the template's CSS.

### Snippet PANO / LOW — panorama rows
`prow` (clickable) + hidden `drow` detail per scored campaign: columns Campaign, Contacted, Accept,
LI reply, Email open, Email reply, Status badge, Fix #1. Missing KPI → `—`; insufficient/no-engagement
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
- HubSpot + `campaign-impact-analyzer` present → deal layer offered and delegated.
- `campaign-impact-analyzer` absent → dashboard shipped anyway + install pointer in the handoff.
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
