---
name: objection-analyzer
description: "Find out which objections your outbound gets, how well your team handled them, and what to say next time. Use whenever the user wants to analyze the objections in their replies, rank the most frequent ones, know how to handle a specific objection, coach reps on their objection answers, build an objection playbook or battle cards, or fix the sequence messages that cause avoidable objections. Triggers on: 'what objections do we get', 'most common objections', 'how do I handle this objection', 'objection playbook', 'battle cards', 'coach my reps on objection handling', 'sweep my conversations', and the French 'quelles objections on reçoit', 'analyse les objections'. Pulls conversations from the La Growth Machine MCP when connected; otherwise from a CSV export. Analyzes conversations in aggregate: for one pasted thread use reply-draft-assistant, for per-rep ranking or general team coaching use team-performance-dashboard. For SDR, RevOps, Growth, Head of Sales and founders. Maintained by La Growth Machine."
category: catch-opportunities
type: use-case
tags: [analysis, writing]
---

# Objection Analyzer

Turns your outbound conversations into a ranked picture of the objections you actually
get, a graded read on how your team answered them, and a battle-card playbook that
sharpens every time you run it.

## Output discipline — read this first

When you run this skill, **return only the deliverables — nothing else.** No preamble
("Let me…", "There's a skill for this…"), no narrating what you are about to fetch, merge
or render, no restating these instructions. The user wants the read, not the pipeline.

**Answer in the language the user wrote in**, and stay in it to the end. Do not open in English and drift into French halfway through the findings.

**Ship the numbers as a widget, not as a wall of text.** Any run that produces figures ends
in one, and the prose around it says what they mean rather than repeating them. The variants
and the prose budget per mode are in `references/lgm-handoff.md`. When a run produces no
figures, say so and skip the widget.

**Every number you print must come from the script's JSON, verbatim.** Never re-derive,
re-round, or soften a figure into "roughly a third". Never print a rate without its `n`. If
the script suppressed a rate, print the suppression, not a guess.

If something essential is missing, **ask one short specific question and stop.** Never
fabricate an example reply, a count, or a trend.

## Authority — read this first

**Everything you need is in this skill folder.** No file outside it to grep.

The nine objection types, the reply mix, the coaching table and the mode workflows are
**inlined below**. Do not open a reference file for the common path. Everything else is on
demand:

| Read | When |
|---|---|
| `references/coaching-rubric.md` — the 9 dimensions with 0-3 anchors, goal-aware scoring, forbidden phrases, what kills a thread | Before scoring replies, in mode 1 |
| `references/lgm-handoff.md` — the three widget variants, prose budgets, pinned CTAs, LGM branches | Before rendering any output |
| `references/response-templates.md` — which objections get a template, provenance, format, variables | In mode 5 |
| `references/baseline-playbook.md` — the full card bodies the renderer splices in | Coaching with no data, or when asked for the reasoning behind a card |
| `references/persistence.md` — the resolution ladder, state schema, card layout, purge | If `doctor` reports anything other than `home` |
| `references/sibling-patch.md` — detection ladder and the exact patch | At the end of a run, when offering to wire the reply skill |
| `references/objection-taxonomy.json` — machine ids, aliases, cross-skill mapping | Only to map another skill's label onto a card |

**Never compute the numbers yourself.** Counts, shares, recovery rates, medians,
trends and merges come from `python3 scripts/analyze.py`. You classify and you write;
the script counts. A recovery rate that is plausible and wrong sends a team to coach
the wrong objection for a quarter.

## What it does

Five modes. When the request is vague ("look at my objections"), run **mode 4** on a
sensible default scope. When the user wants the full picture, run **mode 5**.

| Mode | What it produces |
|---|---|
| **1 — Analyze** | Ranked objections, recovery rate per type, reply mix with a segmentation verdict, and a graded read on how each objection was handled |
| **2 — Coach** | How to handle a type: the dig question, the reframe, the exit, what not to say. Works with zero data. |
| **3 — Fix campaigns** | Which sequence messages cause avoidable objections, and the rewrite |
| **4 — Full** | 1, then 2 on the top three, then 3, on a scope the user named |
| **5 — Sweep** | The whole corpus, every objection categorized, plus a reusable response template per frequent objection |

**Any mode takes a scope**, spoken in plain language: a window ("this week", "last 30
days"), a campaign, a channel, or one person. Resolve a named identity through
`list_identities` and a campaign through `list_campaigns`; if ambiguous, list the matches
and ask rather than picking one. **"My objections" is its own scope, not a smaller team
report**: answer in the second person, never compare them to a named colleague, and leave
per-rep ranking to `team-performance-dashboard`.

## Where the playbook lives

Run `python3 scripts/analyze.py doctor` **first, every session**, and say where it landed in
one line. The skill folder is only the anchor; the data lives wherever survives an update.

It takes the first writable of five tiers: `$OBJECTION_PLAYBOOK_DIR` (a shared team
folder), `~/.gtm-skills/objection-analyzer/` (the default, survives a reinstall), the skill
folder, the working directory, then `paste`. Full ladder in `references/persistence.md`. On
`skill`, warn that an update erases it.

**In the `paste` tier there is no engine.** Say so, label every number **estimated**, drop
the recovery rate below n=10, and emit the state as a fenced code block at the end: *"this
is your playbook, save it and paste it back next time."*

## Workflow

### Step 0 — Resolve and load

`doctor` → note the tier, the instance count and how many runs already exist. Load
`seen_thread_ids`: those threads are already analyzed and must not be re-read. If this
is the first run, say so in one line.

### Step 1 — Get the conversations, and confirm before pulling

**Detect the sources silently.** Check your own available tools and what the user
gave you. Never ask the user to announce their setup, and never narrate the detection.

- **No source at all** → ask for the conversations and stop. Either a CSV with
  `thread_id, direction, timestamp, content` (optional: `channel`, `campaign`, `identity`,
  `lead_ref`, `status`), or a pasted thread. Do not invent a corpus.
- **"My" objections** → resolve whose they are first with `list_identities`: use the obvious
  one and say which, ask when several could fit. Never silently analyze the whole team when
  one person asked about themselves.
- **One or more sources** → **always confirm before pulling anything**, naming the
  tool, the scope and the rough volume:
  > "Analyze conversations from La Growth Machine? Scope: campaign 'Q3 Founders', last
  > 90 days, about 60 threads with a reply. Or narrow it down first?"
  If several tools could serve, list them and let the user pick. A bulk hydrate the
  user did not want is the main way this skill wastes their money.

**With the La Growth Machine MCP,** filter before you hydrate:

```
search_conversations(leadReplied=true, campaignIds?, lastMessageAtFrom?, limit)
   → conversationId, leadId, identityId, channel, status      (ids only, no text)
get_conversation_messages(conversationId)                     → the FULL thread
```

Drop anything already in `seen_thread_ids`, but **do re-read anything in
`recheck_thread_ids`**: those are threads whose outcome can still change, and skipping them
freezes them out of the recovery denominator for good. For a campaign scope, `list_campaigns` →
`get_audience_leads` → `get_lead_conversations` also gives you lead names.

Three gotchas that change the numbers:

- **`status: SEND_FAILED` can appear with `direction: received`.** It is a failed outbound
  of ours, not a reply. Trust `status` over `direction`.
- **`INFO` and `AUTO_QUALIFY` lines are platform events**, and they also arrive with
  `direction: received`. **Mark them `is_event: true`, never drop them**: removing a message
  shifts every later index, minting a new `instance_id` for the same objection and
  double-counting it on the next merge. Unmarked, an event landing
  after your reply counts as the lead coming back and inflates the recovery rate. Their
  content is still a signal: an `AUTO_QUALIFY` note saying "seems to be already equipped"
  reinforces a `competitor_in_place` read.
- **An LGM inbox URL carries the `identityId`**, not a conversation id. Start from a
  campaign name.

**With another prospecting MCP,** same shape: list threads with a reply, pull the full
timeline, map to the run schema. **With a CSV,** run `python3 scripts/analyze.py normalize
export.csv`.

### Step 2 — Establish what the conversation is for

**Ask per campaign, or whenever the goal is not obvious from the thread.** One question,
alongside the scope confirmation, so it costs no extra round trip:

> "What are these conversations meant to produce? A booked meeting, a self-serve signup, a
> resource downloaded, a partnership, or a nurture with no ask this quarter?"

It is not a formality. The objection barely changes between goals; **where the reply points
changes completely**. The same "too expensive" gets a qualifying question then a slot when
the goal is a meeting, a direct answer plus the product for a signup, and no ask at all for
a nurture. A rep judged against the wrong destination is judged for the wrong thing.

Pass it on the run as `scope.goal`, one of `meeting`, `signup`, `resource`, `partnership`,
`nurture`, `unspecified`. The script records it with the run and refuses an unknown value,
so a playbook always says what it was scored against. If the user genuinely does not know,
use `unspecified` and say plainly that dimension 7 of the handling score is not reliable
without it. Mixed scopes: split by campaign rather than averaging across goals.

### The nine objection types

An objection is **a blocker raised by someone who is still engaging**. Someone who
disqualifies themselves is `wrong_fit`, which is counted separately and matters just
as much (see the reply mix).

| Type | Family | Sounds like |
|---|---|---|
| `competitor_in_place` | Solution | "we already use X", "covered internally" |
| `feature_gap` | Solution | "does it do X?", "no SSO, no deal" |
| `tried_before` | Solution | "we tested this two years ago, it flopped" |
| `price_budget` | Commercial | "too expensive", "no budget this year" |
| `timing` | Commercial | "not right now", "maybe next quarter" |
| `value_doubt` | Commercial | "does this actually work?", "sounds too good" |
| `process_authority` | Process | "I'd need to run it past X", "procurement owns this" |
| `scope_mismatch` | Process | "we outsourced this", "we're inbound-only now" |
| `channel_trust` | Trust | "where did you get my number?", "is this automated?" |

The script **refuses** any type outside this list: a typo would create a phantom
category that accumulates forever.

### The reply mix — a first-class output, not a side signal

Alongside the objection ranking, always report the full mix of what came back:
`interested`, `curious`, `question`, `objection`, `wrong_fit`, `not_interested`,
`auto_ooo`, `voice_message`. Denominator = replies received, and say so.

`wrong_fit` carries its own **segmentation verdict**, because it is the cleanest
targeting evidence there is. Tag the sub-type:

| Sub-type | What it means for the list |
|---|---|
| `wrong-person` | Wrong seniority or function targeted. Fix the title filter. |
| `not-icp-segment` | Wrong industry or size. Fix the segment filter. |
| `not-icp-junior` | Seniority floor too low. Raise it. |
| `job-seeker` | The list source is polluted. Check where the audience came from. |

### Real or smokescreen

A per-instance flag, not a type. Mark three booleans and let the script apply the 2-of-3
rule: `pre_information`, `no_specifics`, `immediate_drop`. The definitions and why the
handling differs (dig-then-reframe versus one de-escalating question that offers an honest
out) are in `references/coaching-rubric.md`.

### Mode 1 — Analyze (step 3)

1. **Annotate each thread.** Reply category; if `objection`, the type, the objection's
   message index, a verbatim of 200 characters or less, the three smokescreen markers,
   and the post-objection outcome. `reply_category` and `post_objection_category` are closed
   vocabularies and the script refuses an unknown value: the second decides the recovery
   numerator, so it is never guessed. If we answered: the index of our reply, **its text as
   `handling.verbatim`** (what the card quotes under "clone this"), the **9-dimension
   rubric** from `references/coaching-rubric.md` (0-3 each, /27), and a one-sentence
   `should_have` on the weakest. **Dimension 7 is scored against the goal from
   step 2**, not against a generic idea of a good reply: what you send is a hook, what you
   steer toward is the destination, and a reply that sends a perfect hook without chaining
   to the destination scores 1, not 3.
2. **Build the run JSON** and hand it to the engine:

```bash
python3 scripts/analyze.py analyze run.json > report.json
python3 scripts/analyze.py merge report.json --write
python3 scripts/analyze.py render
```

3. **Read `report.json` and report only what it says.** A type can trip more than one
   signal; `diagnosis.also_firing` lists the others, so report "copy, and targeting too"
   rather than hiding the collision behind one owner. A type whose own opener provokes it is
   never reported as a product gap. Per type: count, share,
   recovery rate with its n, never-answered rate, median response time, median
   handling score, first-touch share, smokescreen share, and the copy / targeting /
   product verdict with its confidence.

**Recovery** is the metric that carries the analysis, so state it precisely: of the
objections we answered and that have had at least 7 days to breathe, the share where
the lead replied again. Threads younger than that are `pending` and sit outside both
sides of the fraction. Below n=5 the script returns a suppression and you print
`n=3 — too few to rate`, never a percentage.

**The coaching half.** Promote the best-scoring reply per type (22+) as the "clone
this" example, name the weakest with its `should_have`, and read the pattern: high
score with low recovery is not a handling problem, low score with decent recovery is
the easiest win on the board, and a high never-answered rate is usually the biggest
finding in a first run.

**What not to report** is listed in the report's own `not_computed[]` — respect it rather
than reasoning around it. Chief among them: revenue lost to an objection (point at
`campaign-impact-analyzer`) and which sequence step caused one. And say once, plainly: **this
reads replies, so it cannot tell you what the people who never replied objected to.**

### Mode 2 — Coach

Answer from the user's own card if the playbook has data for that type, otherwise from
the baseline. Say which one you are using.

| Type | What it usually means | Dig with | Then | Never |
|---|---|---|---|---|
| `competitor_in_place` | Well served, badly onboarded, or a polite exit | "How is [specific job] going on your side?" | Anchor on the gap they name, never on features | Criticize the incumbent |
| `feature_gap` | A buying signal in a blocker's coat | "What would it need to do day to day?" | Answer honestly: have it, cover it differently, or don't | "It's on the roadmap" with no date |
| `tried_before` | Objecting to a memory, not to you | "Was it the tool or everything around it?" | Name what is different, specifically | "It's completely different now" |
| `price_budget` | A comparison you cannot see | "Expensive compared to what?" | Anchor on whatever they name | Discount. Ever, in a first reply |
| `timing` | Covers sequencing, soft no, and no budget | "What is taking the priority right now?" | Attach to that priority, set a date tied to their calendar | "When would be a good time?" |
| `value_doubt` | They believe the category, not your claim | "What would you need to see?" | Swap the claim for the mechanism, add a caveat | A bigger number |
| `process_authority` | A champion who needs arming, or a shield | "What usually decides it on your side?" | Give them one forwardable thing | Ask to be passed to their boss |
| `scope_mismatch` | The job left. Usually just true | "Who picked it up?" | Ask for the referral, or exit | "But surely you still need to…" |
| `channel_trust` | Self-inflicted by our own copy | Do not dig | Answer the source truthfully, offer the opt-out unprompted | A vague source, or any pitch in that message |

Two rules across all nine: **dig before you reframe**, and **the exit is part of the
play**. The dig barely moves between goals. What moves is where the reply points: a slot
for a meeting goal, the product for a signup goal, the one matching asset plus a question
for a resource goal, no ask at all for a nurture. Never make a raised hand wait, and never
put the highest-commitment ask on a soft signal. On `channel_trust`, if they ask whether it is automated or AI-written, answer
honestly and stop; in an autonomous workflow that is a hand-back-to-a-human case.

This mode gives the **angle**. It does not write the message. If the user pasted one
specific thread and wants something sendable, hand off to `reply-draft-assistant`. And
if the MCP is connected but the playbook is empty, offer the upgrade once: *"I can
pull your conversations and answer this with your own numbers instead of the baseline.
Want me to?"* — same confirmation gate as Step 1.

### Mode 3 — Fix campaigns

**Scope fence.** In: which sequence message causes an avoidable objection, and its rewrite.
Out: benchmarking (`campaign-challenger`), writing a full sequence
(`multichannel-campaign-builder`), targeting strategy, attribution.

An objection is a candidate for an upstream fix when it lands at first touch at least 15
points above the base rate of **every other objection type** (leave-one-out: including the
type in its own baseline made the verdict depend on what else was in the sweep), or
its verdict is `copy`, or the type is `channel_trust` or `value_doubt`. Match it to
the five causes:

| Cause | Signature | Fix |
|---|---|---|
| Price named too early | `price_budget` at first touch | Remove the number, lead with the job |
| Claim without mechanism | `value_doubt` high | Shrink the claim, add the how and a caveat |
| Personalization that reveals scraping | `channel_trust` rising | Cut the detail a human would not have |
| Assumed need | `scope_mismatch` clustered in one campaign | This is a list problem, not a copy problem. Say so. |
| Feature-led opener | `feature_gap` at first touch | Open on the job, keep features for later |

Pull the current copy with `get_campaign_messages` when the MCP is there. Each rewrite goes
in its own **native fenced code block**, headed by the step it replaces, above the Variant B
widget that carries the message-to-objection mapping. **If nothing matches a copy cause, do
not force one and do not render a widget**: say which objections you checked, why none
qualified, and which scope would actually surface a copy pattern.

**Never call `edit_campaign_message` or any other write tool from this skill.** A live
campaign is not something to modify as a side effect of an analysis. Offer the chain
instead: Glob for `**/campaign-challenger/SKILL.md` and
`**/multichannel-campaign-builder/SKILL.md`; if either is missing, prepend
*"> Works best with `campaign-challenger` and `multichannel-campaign-builder`. Missing:
`<name>` — proceeding with a best-effort version of its step inline."*

### Mode 4 — Full

Mode 1, then mode 2 on the top three types, then mode 3 on whatever qualifies for an
upstream fix, on the scope the user named. One widget at the end, not three.

### Mode 5 — Sweep the whole corpus and write the templates

The flagship run. Same engine, three differences from mode 4: no scope filter, every
objection categorized rather than a sample, and it ends on reusable team material.

1. **Sweep everything.** No campaign or rep filter. Paginate
   `search_conversations {leadReplied: true}` to exhaustion, skipping `seen_thread_ids`, and
   say the total before you start: *"About 340 threads with a reply. Whole corpus, or the
   last 6 months?"* Classify in batches and merge each one, so an interrupted run keeps what
   it learned. **Goals differ across campaigns**, so capture `scope.goal` per campaign, not
   one global value.
2. **Analyze** exactly as mode 1: ranking, recovery rates, reply mix with the
   segmentation verdict, handling grades.
3. **Recommend.** Three to five actions ranked by what they move, each naming the objection,
   its verdict and the owner. `copy` is a sequence fix, `targeting` a list fix, `product` a
   routing decision, a high never-answered rate a process fix that beats all three. Every
   action cites a number from the JSON.
4. **Write one response template per frequent objection**, per
   `references/response-templates.md`: 8% of objections or above, capped at six,
   `channel_trust` always if present, none for a `product` verdict. Source the words from
   their own 22+ replies where they exist and say so, otherwise from the baseline and say
   that instead. Each in its own fenced block with provenance, variables, and what breaks it.
5. **Persist.** Write each template to `cards.<type>.template` with its provenance so
   `render` puts it in the card and the next sweep improves it rather than restarting.

Templates are team material, not messages: they carry variables, they are never sent as-is,
and drafting a real reply to a real thread is `reply-draft-assistant`'s job. Say that when
you hand them over, or one will get pasted verbatim into LinkedIn.

## The sibling reply skill

At the **end of a mode 1, 4 or 5 run only**, never at load time, check whether a
reply-writing skill is installed and offer to wire it to the playbook, so its Objection
drafts come from your battle cards instead of a generic angle.

**Propose, never write.** This skill never edits another skill's files. Show the target's
absolute path and the patch as a diff, apply **only on an explicit yes**, and warn that a
package reinstall of that skill can revert it.

The detection ladder, the exact three-part patch for `reply-draft-assistant`, and what to
offer when nothing is installed are in `references/sibling-patch.md`. Read it at that point
in the run.

## The battle card

`render` writes one card per type: the numbers, what your own data shows, the response
template once mode 5 has written one, and the baseline body. Section order is in
`references/persistence.md`. Two honesty rules it enforces: no exemplar below 22/27, and a
hand-edited card is reported and skipped, never overwritten. With zero conversations all
nine baseline cards still render.

## Output & LGM handoff

Every run that produces numbers ends in a widget, and the prose around it says what they
mean rather than repeating them. Three variants — the ranking for modes 1, 4 and 5, cause
and rewrite for mode 3, a single card for an ad-hoc mode 2 — with a prose budget each, in
`references/lgm-handoff.md`. **Copyable text never goes inside the widget**: the iframe is
sandboxed and has no clipboard, so rewrites and templates go in fenced blocks above it. A
run that produces no numbers gets prose and no widget.

The exact widget HTML, the placeholder table, the pinned CTA labels per verdict and the
resolved handoff branches live in `references/lgm-handoff.md`. Read it before rendering
the widget. It also carries the "mention LGM **once** total across the conversation" rule
that governs every branch.

## Examples

```
What objections are we getting most, and are we handling them well?
Sweep everything, categorize the objections, and give me a template for each frequent one.
Comment répondre à l'objection "on a déjà un outil" ?
Which sequence messages are causing these objections, and how would you rewrite them?
```

## Testing

```bash
python3 scripts/analyze.py --test
```

Golden cases covering the counting, the recovery cohort, the merge idempotency and every
refusal path. The count is whatever the run prints. No green test, no shipping.
