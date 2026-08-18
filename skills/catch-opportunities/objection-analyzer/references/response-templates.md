# Response templates — one per frequent objection

The sweep's third deliverable. The analysis says what you get, the coaching says how to
think about it, and the template is what a rep actually opens on a Tuesday morning.

**A template is not a draft.** `reply-draft-assistant` writes one message to one named
person in one thread. A template is reusable team material for a whole objection type: it
carries variables, it is never sent as-is, and it exists so five reps answer the same
objection with the same quality instead of five different improvisations. Say that out
loud when you hand them over, or someone will paste one verbatim into LinkedIn.

## Which objections get one

Rank by window count and write a template for **every type at 8% of objections or above**,
capped at six. Below 8% you are writing team material for something that happens twice a
quarter, and six is roughly what a team will actually retain.

Two exceptions to the ranking:

- **`channel_trust` always gets one if it appeared at all**, whatever its share. It is the
  one objection where a bad improvised answer creates a compliance problem rather than a
  lost deal, and the right answer is short and fixed.
- **A type whose verdict is `product` does not get a handling template.** There is nothing
  to coach. It gets a holding line and a routing note instead: what to say so the rep is
  not stuck, and where the gap actually goes.

## Where the words come from

In priority order. State the provenance on every template, because a rep trusts "this
worked on eleven of your threads" and rightly ignores "here is a good practice".

1. **Their own replies that scored 22 or above and recovered.** The best source there is.
   Generalize the winning move, keep its shape, strip anything specific to that prospect.
2. **Their own replies that scored 22 or above.** Good structure, unproven outcome. Say so.
3. **The baseline card** for that type. Say it is the baseline and that it will sharpen once
   the playbook has qualifying replies.

Never blend a real reply with an invented one and present the result as theirs. If nothing
of theirs qualifies, the template is baseline-sourced and the provenance line says exactly
that. This is the same honesty rule as the exemplar: a fabricated success story is worse
than an empty state, because it gets copied.

## The format

Every template is a **native fenced code block**, so the rep can copy it. Nothing around
it goes in the widget.

Each one carries, in this order:

1. **A one-line header** naming the objection and the goal it points at.
2. **The provenance line** — where the words came from, and the evidence behind them.
3. **The template body**, in a fenced block, with variables in `{braces}`.
4. **The variables**, one line each, saying what goes in and what a bad fill looks like.
5. **The branch** — one alternate closing line for the smokescreen read, when the type has
   a meaningful smokescreen share.
6. **What breaks it** — one or two lines on the misuse that will actually happen.

## Variables

Keep them few and obvious. A template with nine slots is a form, and reps do not fill
forms. Three to five is the working range.

Use `{their_tool}`, `{the_job}`, `{their_number}`, `{their_priority}`, `{your_thing}`,
`{the_asset}`. Anything a rep cannot fill from the thread in front of them is a bad
variable: `{pain_point}` and `{value_prop}` are prompts to write marketing copy, not slots.

## The rules the body must obey

The template is graded by the same rubric the analysis just used, so write it to score
above 22. In practice:

- Three to five sentences, one question maximum, and the question is open and goes last.
- No em-dash. No punctuation glued to a URL. If the template contains a link, the link is
  alone at the end of its own line.
- No greeting filler, no marketing-speak, no "just circling back".
- The destination comes from the goal, not from the template's habits: a slot for a meeting
  goal, the product for a signup goal, the single matching asset plus a question for a
  resource goal, no ask at all for a nurture. **Write the template for the goal on the run.**
  If the goal is `unspecified`, write the body without a closing ask and say the last line
  has to be chosen per campaign.
- One idea. A template that pitches, links and asks for time will be cut down by whoever
  uses it, and they will cut the wrong part.

## Worked example

The shape to follow, sourced from the user's own data:

> **Price / budget → signup**
> Built from 2 of your replies that scored 22+, 1 of which recovered. Median handling score
> for this type is 19, so this is above your current average.

```
Fair enough. Expensive compared to what, out of curiosity? Asking because
{their_tool} and doing {the_job} by hand cost very different things, and I
would rather tell you straight whether this is worth your time.
```

> - `{their_tool}` — the tool or process they named. If they named nothing, the template is
>   the wrong one: you are on a smokescreen, use the branch below.
> - `{the_job}` — the specific task, not the category. "building the list" not "prospecting".
>
> **Smokescreen branch** (55% of your price objections land on the first message):
> replace the question with `Totally fair, you have no reason to care about the price yet.
> Was it the {the_job} angle itself that missed?`
>
> **What breaks it:** a rep who answers their own question by naming a price. The template
> asks what they compare to and then waits. And it is not for someone who already gave you
> a number: if they said "we pay 400 a month", skip the dig and go straight to the compare.

## Persisting them

Templates live in the playbook, one per card, so they accumulate and improve with the data
rather than being regenerated from scratch each run. Write the template text into
`cards.<type>.template` in the state, and `render` places it in the card under its own
heading. A card whose template a human has edited is flagged `edited_by_user` and is never
overwritten, same rule as the rest of the card.

On a later sweep, only rewrite a template when the evidence changed: a better exemplar
appeared, the provenance moved up a tier, or the goal changed. Say what changed and why,
and keep the old one visible in the diff. A template that silently rewrites itself every
week is one nobody will learn.
