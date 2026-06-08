# Classification Rules

How to classify an inbound reply to a cold outreach message (LinkedIn or email). Every reply gets exactly **one** category. The category drives the reply strategy (see `draft-rules.md`).

This is a best-practice taxonomy for B2B reply handling — it is tool-agnostic and works on any reply, pasted or pulled from a CRM.

## The 8 categories

| Category | What it is | Draft a reply? |
|---|---|---|
| **Interested** | Clear positive signal — wants the next step | ✅ |
| **Curious** | Soft interest — engages, asks a question, agrees with the topic, but no direct commitment | ✅ |
| **Objection** | Engages but raises a specific blocker (see sub-types) | ✅ |
| **Question** | Factual ask — pricing, feature, proof, how-it-works | ✅ |
| **Wrong fit** | Wrong person, not the ICP, junior, job-seeker | ✅ (short) |
| **Not interested** | Clear refusal — "not interested", "remove me", "stop" | ✅ (graceful exit) |
| **Auto / OOO** | Auto-reply, out-of-office, "I'm on leave" | ❌ no draft — note the return date if any |
| **Voice message** | The reply is a voice note (content not readable) | ❌ no draft — flag for manual review |

## Decision tree (top-down, first match wins)

Read the reply and walk down — stop at the first match. When in doubt between two categories, pick the more charitable one (**Curious** over **Not interested**).

```
1. Is it an automated message (OOO, auto-reply, "I'm away until…") ?
   → Auto / OOO   (no draft; capture return date if present)

2. Is the reply a voice note / "sent you a voice message" with no readable text ?
   → Voice message   (no draft; flag manual review)

3. Is there a clear, unequivocal refusal ?
   ("not interested" / "remove me" / "stop" / "don't contact me")
   → Not interested

4. Does the person disqualify themselves ?
   (wrong contact / not my area / "I'm a student/intern" / job-seeker / clearly out of ICP)
   → Wrong fit

5. Do they raise a specific blocker while still engaging ?
   (price / competitor in use / timing / tried-before / out of scope)
   → Objection   (then tag the sub-type below)

6. Is it a factual question ?
   ("what's the pricing?" / "how does X work?" / "do you have a case study?")
   → Question

7. Is there a clear positive signal ?
   ("interested" / "yes let's chat" / "send it" / "happy to talk")
   → Interested

8. Otherwise — neutral engagement, a strategic question, "happy to connect",
   agreement with the topic, soft curiosity :
   → Curious
```

## Objection sub-types

When the category is **Objection**, tag the sub-type — it changes the reply angle (see `draft-rules.md`).

| Sub-type | Signals |
|---|---|
| **competitor** | "we already use [tool]", names a competing product |
| **price** | "too expensive", "out of budget", "[competitor] is cheaper" |
| **timing** | "not a priority right now", "maybe next quarter", "revisit later" |
| **tried-before** | "we tried this 2 years ago", "didn't work for us" |
| **scope** | "we don't do that anymore", "we focus on inbound", "outsourced this" |

For the **competitor** sub-type, also note whether they ask a question back ("what do you use?") — that's a signal of genuine openness, flag it.

## Wrong-fit sub-types

| Sub-type | Signals |
|---|---|
| **wrong-person** | "I'm not the right contact", "talk to [name]", "not my area" |
| **not-icp-junior** | "I'm a student / intern / junior / still learning" |
| **not-icp-segment** | "we're [industry/size clearly outside the target]" |
| **job-seeker** | "I'm looking for a role", "currently between jobs" |

## Metadata to extract (every category)

Alongside the category, extract these — they calibrate the draft:

- **Tone** — `formal` / `casual` / `enthusiastic` / `terse` / `dismissive` / `suspicious`. Read from greetings, sentence length, contractions, punctuation, language.
- **Language** — the language the reply is written in (the draft must match it).
- **Urgency** — 1 (no action expected) to 5 (explicit immediate ask, "can we talk this week?").
- **Channel** — where the last received message came from (`LinkedIn` / `email`). The reply goes back on the **same channel**.
- **Key points** — 2-4 bullets of what they actually said, condensed, no interpretation.
- **Hidden meaning** (optional) — only when there's a clear read between the lines (e.g. "already using X" → happy-and-set vs. frustrated-and-open; "not right now" → real interest postponed vs. polite brush-off).

## Ambiguous cases — how to handle

**One-word / very short replies** ("Yes", "OK", "Sure", "Thanks")
A short polite reply with no clear direction → classify **Curious** with a `needs_clarification` flag. The draft is then a short clarifying question, **not** a pitch.

**Short but directional** ("send it", "yes please", "how much?")
These are decisive despite being short → classify on the intent (**Interested** / **Question**), not on the length.

**Mixed signals** (interest + a constraint in the same message)
Lead the classification on the **constraint** (→ **Objection**) but note the interest in the key points — the draft acknowledges both.

**Multi-message** (the person sent 2+ messages in a row before you replied)
Classify on the **last** message, but make the draft address the earlier ones too (e.g. a "thank you" followed by a "no" → classify **Not interested**, acknowledge the thanks).

**Late reply** (the person replied more than ~3 days after the last touch)
No category change — but the draft may open with a light "sorry for the delay" if you're the one who went quiet, or simply pick the thread back up naturally.

## Output of this step

For each reply, produce a compact record:

```
{ name, category, sub_type?, tone, language, urgency, channel, key_points[], hidden_meaning?, needs_clarification? }
```

`Auto / OOO` and `Voice message` get the record but **no draft** in the next step. All other categories proceed to drafting.
