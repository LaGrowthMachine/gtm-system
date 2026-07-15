# Copywriting Rules (base set)

The base rules for writing the outreach sequence off a post. This is the standalone rule set. For the full angle, CTA and channel frameworks, install the `multichannel-campaign-builder` skill and defer to it; these rules cover the common case well on their own.

The sequence is written in the **language of the post** (confirmed with the user), not the language of the questions.

## The one framing rule for post engagers

Someone liked or commented on a post. That is a **warm topical signal**, not permission to mention their action. Reference the **topic or idea** of the post, never the individual's like or comment.

- Good: "The point about outbound reply rates in that post is a real tension for teams at [stage] right now."
- Bad: "Saw you liked / commented on the post." (reads as surveillance)

One exception: **employee advocacy.** If the sender is a *colleague* of the post's author, the relationship can be named openly ("[Author] is our [role], and their post on [topic] clearly landed with you"), because it is a real professional relationship, not monitoring. Never frame it as "I noticed you engaged".

## Sequence shape

Post engagement is warm, so keep it light and topical. A solid default:

| Touch | Day | Channel | Role |
|---|---|---|---|
| T1 | 0 | LinkedIn invite | Speak to the post's idea, no pitch, no link, 200 chars max |
| T2 | 2 | LinkedIn DM (or email if multichannel) | Peer opener + one concrete pain, fresh angle |
| T3 | 5 | Email (multichannel) or LinkedIn DM | Deepen, a new angle, still no hard sell |
| T4 | 12 | LinkedIn DM or email | The CTA, driven by the objective |
| T5 | 18 | LinkedIn DM or email | Re-engagement, a different angle, door left open |

LinkedIn-only collapses the email touches into DMs. Each follow-up moves to a **fresh angle**; never repeat the same point twice.

## Length per channel

| Channel | Target | Hard limit |
|---|---|---|
| Email body | 50 to 100 words | 120 words |
| Email subject | 3 to 5 words | 6 words |
| LinkedIn invite note | 150 to 200 chars | 200 chars, no exception |
| LinkedIn DM | 40 to 70 words | 90 words |

Shorter beats longer. Cut before sending.

## Opening rules

Required: 10 to 20 words, names a specific tension or idea the reader recognizes instantly, peer to peer.

Forbidden openers: starting with a question, starting with "I", starting with a compliment, "I came across your profile", "I hope this finds you well", naming your product in the first line, or corporate buzzwords.

## Body and CTA

- One problem per message, never two.
- Short sentences, active voice, "you / your team" not "I".
- No feature dumping in a first touch. Talk in problems and outcomes.
- One ask per message. Value-framed, low friction.
- Never ask for a meeting in touch 1. Value first, ask later.
- Never the same CTA type twice in a row.

## Anti-AI tells (rewrite on sight)

| Tell | Why it breaks |
|---|---|
| Em-dash or en-dash in the body | The most obvious machine signature |
| "Furthermore", "Moreover", "Additionally" | Corporate connectors |
| "Thus", "Hence", "Therefore" | Academic tone |
| "It is worth noting that" | Filler hedging |
| "Imagine a world where" | Generative cliche |
| 2+ exclamation marks, or ALL CAPS | Machine over-emphasis |
| Long sentences with stacked clauses | Over-formulation |

## Forbidden phrases

- Openers: "I hope this finds you well", "I came across your profile", "I noticed you", "I wanted to reach out", "Quick question:".
- Follow-ups: "Just checking in", "Following up on", "Circling back", "Bumping this", "Did you have a chance to".
- CTAs: "Would you be open to a 30-min call?", "Can we jump on a quick call?", "Let me know if interested!", "Click here", "Book a slot", "When works for you?".
- Filler verbs: leverage, utilize, optimize, streamline, facilitate, enable, empower, unlock, robust, synergies, best-in-class, cutting-edge. Use a specific action verb instead.
- Creepy: "Saw you engaged with", "I noticed you visited our website", "I see you opened my email".

## Personalization variables (V1)

Use only standard scraped fields the audience import provides: `firstname`, `lastname`, `company`, `jobTitle`. Do not invent custom-attribute variables in V1. The copy adapts to the post's idea in the plain text, not through per-lead custom attributes.

When writing to LGM, these become `<var name="firstname"/>` etc. (see `lgm-campaign-create.md` for the `newHtml` format).

## Self-check before output

Run every message against this list and rewrite any failure:

- [ ] No em-dash or en-dash anywhere.
- [ ] One ask per message, zero for a re-engagement exit.
- [ ] No banned phrase present.
- [ ] Length within the per-channel hard limit.
- [ ] Opener does not start with a question, "I", or a compliment.
- [ ] References the post's topic, never the individual's like or comment.
- [ ] Email subjects are all distinct.
- [ ] CTA type does not repeat two touches in a row; no meeting ask in touch 1.
