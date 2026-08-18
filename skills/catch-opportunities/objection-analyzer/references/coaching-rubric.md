# Coaching rubric — scoring how a reply handled an objection

Nine dimensions, 0-3 each, 27 total. This is the half of the skill that looks at **our own
messages** rather than the prospect's. It answers "are we good at this", which is a
different question from "what do we get", and it is the one that produces coaching
material.

The nine dimensions are the same nine the `team-performance-dashboard` skill scores, in
the same order, so a reply's dimension breakdown transfers between the two. The anchors
below belong to this skill: the dashboard names the dimensions and applies the 22
threshold, it does not define what a 1 or a 2 looks like. If you change an anchor here,
nothing breaks there, but the two stop agreeing on the integers.

**You score. The script counts.** Emit the nine integers per handled objection and let
`analyze.py` do the medians, the promotion of the best reply, and everything else. Do not
compute a total yourself and do not describe a reply as "good" without the number.

## The nine dimensions

Score each 0-3. When you hesitate between two scores, take the lower one: an inflated
rubric produces a playbook that congratulates the team instead of coaching it.

The JSON key is given with each dimension: the script refuses a rubric whose keys are not
exactly these nine, so emit the key, not the label.

| # | Dimension (JSON key) | 0 | 3 |
|---|---|---|---|
| 1 | **Tone match** (`tone_match`) | Corporate reply to a casual message, or the reverse | Reads like the same conversation the prospect started |
| 2 | **Addresses the message** (`addresses_message`) | Answers a different objection, or ignores it and pitches | Engages the specific blocker they raised, and the acknowledgment does not open on "but" |
| 3 | **Length mirrors** (`length_mirrors`) | Six lines back to a six-word message | Inside the band their last message sets |
| 4 | **One question max** (`one_question_max`) | Three questions stacked, or a question on an exit | Exactly one, it is open, and it is the last thing in the message |
| 5 | **No forbidden phrases** (`no_forbidden_phrases`) | "Just circling back", "hope this finds you well", "game-changer", "leverage" | None of it |
| 6 | **Not pushy** (`not_pushy`) | Fake urgency, guilt, "but wait", a meeting ask they did not invite | Zero pressure, the next step is theirs to take |
| 7 | **Resource priority** (`resource_priority`) | Three links dumped, or a link in a first reply | The one hook that fits what they asked for, chaining to the goal's destination |
| 8 | **Not creepy** (`not_creepy`) | Personalization that reveals scraping, or a claimed connection that is not real | Context they would expect a human to have |
| 9 | **Process compliant** (`process_compliant`) | Wrong channel, ignores an opt-out, sends after a no | Respects the channel, the no, and the opt-out |

**Thresholds the engine applies.** Three numbers, and 18 does two jobs, so keep them apart.

- **22 or above, single reply** — promoted as the "clone this" exemplar for its objection
  type. Never fabricate one: if nothing clears 22, the card says so, and that empty state
  is itself the finding.
- **18 or above, median of a type** — counts as "we answer this well", which is what lets
  the diagnosis separate a handling problem from a genuine product wall.
- **Below 18, single reply** — do not clone it and do not quote it as an example. A reply
  under 18 has something structurally wrong with it, not something stylistically weak.

## Real or smokescreen

A per-instance flag, not a type. Mark three booleans and let the script apply the
2-of-3 rule: `pre_information` (the objection lands on the **first** received message,
before anything substantive), `no_specifics` (no figure, no tool, no date, no stated
constraint), `immediate_drop` (the thread died even though the reply scored 22+).

It changes the play. A real objection gets dig-then-reframe. A smokescreen gets one
de-escalating question that offers an honest out.

## Score against the goal, not against a generic idea of a good reply

Before scoring anything, name the conversation's goal in one word. Every campaign has one
and most teams never write it down: a booked meeting, a self-serve signup, a resource
downloaded, a partnership, or a nurture with no ask this quarter.

The goal leaves eight of the nine dimensions alone. It changes dimension 7 completely, and
it is why two reviewers score the same reply 3 and 1 without either being wrong.

**Hook and destination.** What you send is a hook. What you steer toward is the
destination. The hook varies with the thread: whatever fits what they just said. The
destination is fixed by the goal and does not move. A reply that sends a perfect hook and
never chains to the destination scores 1 on dimension 7, not 3, because the thread now ends
on an asset instead of a next step.

| Goal | 3 looks like | 0 looks like |
|---|---|---|
| **Meeting** | The next step is a slot, offered after the blocker was addressed, and it is a slot you can honour | Promising a meeting the process has not approved, or asking for time before answering the objection |
| **Signup or trial** | One ask, earned. Immediate if they raised their hand, after two exchanges of value otherwise | A link in a first reply, or a warm reply that ends on a resource and never mentions the product |
| **Resource** | The single asset matching what they asked for, and a question that keeps the thread alive after it | Three assets at once, or an asset with no follow-up question, which reads as a delivery receipt |
| **Nurture / partnership** | No ask at all, and something they can use. The next step is a reason to talk again | An ask. Any ask. A nurture with a CTA is a sales message wearing a nurture label |

**Two rules hold at every goal.** A raised hand never waits: if they asked to try it, buy
it, or see it, give it in that reply. And nobody gets the highest-commitment ask off a soft
signal, so "interesting" is not an invitation to the trial link.

**The goal can be abandoned mid-thread, and often should be.** A firm no, a wrong fit, or a
junior who is genuinely learning all end the goal. A reply that pursued it past that point
is being scored for pushiness, which is dimension 6, and it should cost points there too.

## The length bands for dimension 3

Read the lead's **last** message, not the average of the thread. You are mirroring their
current energy, not the conversation's history.

| Their last message | Your band | Floor |
|---|---|---|
| 1 to 3 words | 1 short sentence plus the question | Never a bare "sure" back |
| One sentence, ~15 words or fewer | 1 to 2 sentences | |
| 2 to 3 sentences | 2 to 3 sentences | |
| A paragraph, or bullets | 3 to 5 sentences, structured if theirs was | |

Mirror length, register, language and formatting. Do not mirror rudeness, typos or
aggression. When the band and the message you want to send disagree, **the band wins**:
compress the ask into a half sentence grafted onto the question rather than adding a
sentence to hold it. A reply that says everything and breaks the band gets ignored exactly
like the one before it. Length discipline also outranks the reply's category: a hot lead
who writes "yes" gets one sentence back, not four.

Structure order flips with how much they gave you. One to three words: the question comes
**first**, then a line of context. A full sentence with a question in it: acknowledge
first, then answer, then the question. A refusal: no structure at all.

An objection reply has three slots and no more. One sentence of acknowledgment, one
question that digs, and optionally one line of workaround or a clean exit.

## Dimension 4 is about placement as much as count

The one question goes last and it is open. A message ending on a closed CTA scores 0 here
even with a question earlier in it, because a closed CTA asks them to commit rather than to
speak.

Good: `what does your setup look like on your side?`
Good: `curious how you are handling that piece today`
Bad: `let me know if you are interested`
Bad: `want to book a demo?`
Bad: `Could you share more about your current outreach process?` (a survey, not a question)

Zero questions on an exit. Someone who has said no is not being interviewed.

## What to write in `should_have`

One sentence, on the weakest reply of each type. It is the coaching line a manager reads out
loud, so make it specific and aim it at the move rather than the person.

Good: `ask what the current spend is instead of defending the price`
Good: `no question at all here, they said no twice`
Bad: `could be better`
Bad: `the rep was too pushy` (names the person, not the move)

## Reading the scores

- **High score, low recovery** — the reply is not the problem. Look at targeting, or accept
  the objection is real. This is the pattern that produces a `product` verdict.
- **Low score, decent recovery** — you are getting away with it. Real upside here, and the
  easiest coaching win available.
- **High `no_reply_rate`** — nothing to score, because nobody answered. Usually the biggest
  single finding in a first run, and it is a process fix, not a copywriting one.
- **Low score concentrated on one type** — a battle card gap. Write the card, do not coach
  the individuals.
- **Low score spread across every type by one identity** — an individual coaching
  conversation. Compute per-identity only when asked, and hand the team-wide ranking to
  `team-performance-dashboard` rather than rebuilding it here.

## The phrases that cost a point on dimension 5

Openers: "I hope this email finds you well", "Hope you're doing great", "I wanted to reach
out", "I'm reaching out because".
Follow-ups: "just circling back", "just following up", "checking in", "did you see my last
message".
Marketing: "game-changer", "leverage", "synergy", "best-in-class", "revolutionize",
"unlock", "supercharge", "seamless".
Pressure: "before it's too late", "prices go up", "last chance".
Fake empathy: "Totally understand!", "Perfect timing!", "Absolutely!".

Structural tells, which cost a point for the same reason: a colon in the opening sentence,
which is how an article announces itself and not how a person talks; a breathing comma
before a short conjunction, `, or` and `, and` where the sentence holds without it; a number
spelled out where digits would do, so `2/3` not "two thirds" and `40` not "forty".

Openers to avoid: a question as the first sentence, "I" as the subject of the first
sentence, and any P.S. If it matters enough for a P.S. it belongs in the message.

Three formatting faults break the message in the client rather than just reading badly. An
em-dash anywhere, the most reliable "written by AI" tell there is. Punctuation glued to a
URL, which gets swallowed into the link and 404s. And a link that is not alone at the end of
its line: put it on its own line and let nothing follow it. If a broken link already went
out, send the fix on its own and say nothing else about it.

## Voice notes that separate a 2 from a 3

- **Peer, not vendor.** `on my side at [company], mostly around [X]` beats `at [company] we
  help teams do [X]`. The second is a brochure sentence in a DM.
- **A resource is a parenthetical, not a paragraph.** `(btw we ran something on this exact
  topic last month, want the replay?)` beats `We have a webinar on this topic. Would you
  like me to send you the link?` The same offer as its own formal sentence reads as a
  handoff to marketing.
- **Short acknowledgments.** "Cool", "Got it", "Nice". Not "I'm so glad to hear that".
- **One idea per message.** Do not stack a pitch, a resource, a question and a meeting ask.
- **Never invent a product fact.** If you are unsure, say you will check. "I don't know, let
  me ask and come back with a real answer" outperforms a confident guess and survives being
  wrong.
- **Never reference the mechanism that captured them.** You may reference the substance they
  opted into, never the channel that gave you their name, and never a silent behavioural
  signal. "Saw you engaged with that post" is the clearest version of dimension 8 scoring 0.

## What kills a thread

Five moves end a conversation that was still alive. None of them are rude, which is why they
survive review. Score them under dimension 6 and name them in `should_have`.

**Repeating yourself.** A follow-up carrying nothing new is noise. Repeating does not revive
a thread, it buries it, and it teaches them that ignoring you works.

**Recapping the thread to the person who was in it.** Never tell them what they said. Nobody
summarizes a conversation back to the person who had it, so it reads as a machine proving it
read the transcript. Open on the substance instead. The test: does the sentence tell them
what they did, or does it say what brings you back today? Do not overcorrect into a bare
statistic either, which reads as a mass send. Keep half a sentence of reason for writing now.

**The apology opener.** "That's on me", "my question was badly framed". An old reflex, and at
any scale it reads as a template. If you owe them an answer, the repair is the answer, not
the confession.

**A constant interval.** The same gap between every follow-up is the signature of a machine.

**A third follow-up.** Two is the limit. Past that you do not recover a lead, you manufacture
a firm no and you burn the account that sent it.

## Scoring an exit

An exit is a reply and it gets scored. Most exits lose points on dimensions 6 and 7 rather
than on tone.

- One asynchronous thing, or nothing. Never the high-commitment ask.
- Zero questions.
- No scheduled follow-up. A clean exit forecloses the follow-up, it does not defer it.
- Offering a different channel is an escalation, not a courtesy. "Can I email you instead?"
  scores 0 on dimension 6.
- Thank them properly and specifically. Most people ghost. Someone who took the time to say
  no did you a favour, and "have a great day" does not acknowledge it.
- If they handed you a name, thank the handoff and route it to a person. A referral is a new
  lead, not a reply you can answer.

## Anchors when you score a follow-up

Dimensions 2, 3 and 7 all assume a recent inbound message. A follow-up has none: the last
message in the thread is yours. Do not add a tenth dimension for this, because the 22
threshold is wired into the script. Re-anchor the three instead.

- **Dimension 2** reads against their last received message, however old. 3 means the
  follow-up picks up a specific point they raised. 0 means it would work on any lead.
- **Dimension 3** mirrors that same old message, one band lower. A follow-up is shorter than
  the reply it chases, because you are reopening, not re-delivering.
- **Dimension 7** reads against what already left the thread. If a link has gone, the correct
  move is to ask what happened to it, not to send another. A link in a first follow-up is 0
  whatever the category.

Triage a follow-up on **why** they went quiet, not on how long it has been. Four reasons
cover almost all of it: you delivered value then asked a question that cost them something to
answer, so drop the question and put the ask in its place; they said not now, so re-enter on
the date; they are already equipped, so lead with the fact that you are not trying to move
them; or they asked you something and never got an answer. Check that last one first. In any
pile of threads labelled "waiting on them", some fraction is waiting on you, and it is the
fastest recovery available.

The second follow-up is the one that offers the way out, because that is also what makes
people answer. A clean no beats a silence and it releases the lead.
