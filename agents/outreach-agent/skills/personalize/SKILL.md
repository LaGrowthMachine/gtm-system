---
name: personalize
description: "Shared sub-skill, personalised mode only. Writes the whole message of each step for each lead, in natural words, from the frame of the outline and what is known about the lead, stores each in its custom attribute, and says which branch or fallback was used. Pushes nothing."
---

# Write the messages per lead

In these campaigns the message is no longer an attribute of the campaign, it is an attribute of the lead. The
campaign file holds the outline and its branches. This skill picks the branch of each lead, then writes each message
for that lead and checks it.

## What is fixed and what is yours

The outline of the campaign file is a frame, not a text to fill in.

| Fixed by the outline | Yours to write |
|---|---|
| What each message says: the reason, the offer, the proof | The wording of each sentence |
| The order of the messages and their channel | How the role and the mission are named |
| The question each message ends on, in its intent | The exact words of the question, when the lead's case calls for it |
| The rules and the claims allowed | Dropping a clause that is not true for this lead |

A message that reads as a filled template has failed, even when every fact in it is right.

## How to say what the source says

The source is what the signal gave: a job post, a website, a reply.

- **Say it the way a person would after reading it.** "Saw you're hiring a GTM Engineer to turn your GTM strategy into
  signal-based playbooks", not a sentence lifted from the post.
- **Talk to the lead.** "You're hiring", "your reps", "your stack". Not "[company] is hiring".
- **Name the role in its short spoken form.** "A founding RevOps", not "Founding RevOps Lead". After the first
  message, "your new hire" or "they" is enough.
- **Never copy a sentence of the source and never write "the post mentions".** Say the thing itself: "Looks like
  Clay is already in your stack."
- **Stay true to the source.** A plain rewording is fine. A tool, a number, a mission or a priority the source does
  not state is not. If a clause of the outline claims something the source does not say ("sounds like outbound will
  be a big part of the job"), drop the clause or say what the source does say.
- **Keep it short.** One idea per sentence. The mission in 12 words at most.
- **Use our words for the offer.** "To own the pipeline marketing is accountable for" is a sentence of a post. Say "to
  own your marketing pipeline".
- **Name who already does the work.** When the post names SDRs, an agency or a GTM engineer, the question names them
  ("Is your SDR team covering this until then…").
- **Read the first word again when a sentence moves** into another message: a name or an acronym keeps its capitals
  ("ABM is one of…", never "aBM").

## Input

- The leads kept, each with what the signal says about its company (for a job post: the role, the mission, the
  tools named, the date), what the source file or audience says about the lead, and the company website when the
  client can read web pages.
- The campaign file and the outline it points to: the branches and when each applies, the messages, the custom attributes, the rules, the claims
  allowed.
- The `copywriting` skill.
- When another agent did the search: its handover. It names people and is never saved in a shared file.

## Steps

1. **Read the campaign file and its outline**, in full. Every custom attribute must have an outline for every branch, including
   the fallback branch. If one is missing, stop: ask in a session, say it in the recap in a routine.
2. **Leave out the leads the campaign cannot write to**: another language than the campaign. Also a lead already in
   another campaign of the workspace (its custom attributes would be overwritten). Count them.
3. **Pick the branch of each lead**, with the rule of the campaign file, from facts only. Take the first branch that
   applies. When no branch applies, take the fallback.
4. **Gather the facts of the lead**: what the frame of each message needs, from the source. Note where each comes
   from.
   **Then check the cases of the outline** (its section "Cases", when it has one). For a job post: look in the post and on the
   website for an outbound tool in place, then for who runs outbound today. A case that applies changes the
   sentence or the question it names, nothing else. A tool given as an example is not a tool in place.
5. **Judge the facts: usable or not, with the reason.** A fact is not usable when:
   - the line it gives would stay true for any other company (the stranger test);
   - it states something about the lead or the company that the source does not say;
   - it cannot be said in the length the campaign file sets.
   A lead with no usable fact moves to the fallback branch.
6. **Write every message** as the lead will read it, in natural words, following "How to say what the source says".
   Line breaks as `<br/>`, the format `build-campaign` uses.
7. **Read each message aloud, as the lead.** Would a person have written this sentence? Does it sound like a recital
   of the post followed by a pitch? If so, rewrite it.
8. **Check each message**: one question at most, the length of the channel, no forbidden phrase, no raw slot left
   (`[`, `{{`, `<var`), only the claims the campaign file allows, the rules of the campaign, the house style of
   `copywriting`.
9. **If a message fails**: rewrite it twice at most with the reason, then take the fallback branch. Never leave an
   attribute empty.
10. **Write the review attribute**: the branch, the source and its date, the facts used. It is never shown in a
    message. It is what tells, in La Growth Machine, why this lead got this message.
11. **Fill every custom attribute of the campaign for every lead**, even those a lead will not use. An attribute
    left empty can keep a value from another campaign.

## Output

- The table: one row per lead, one column per custom attribute.
- The count per branch, the share of fallbacks, the leads left out and why.
- What was adjusted against the outline, lead by lead, when it is more than wording: a clause dropped, a question
  changed.
- The reframings the human made during the run, each as a proposed case for the outline: when it applies, what
  changes, the company it came from. A reframing stays on its lead until the human has it written in the outline.
- In a session, the human reviews the table. In a routine, it goes to `push-leads` as it is.

If more than half of the leads end on the fallback, say so: the problem is in the target or in the branches, not in
the writing.

## Never

- Never change what a message offers, add a claim or invent a branch. Report what is missing instead.
- Never write into La Growth Machine or into a file. `push-leads` does the push.
- Never cite something the lead did not make public.

## To verify on a real account

- How a value with an apostrophe, an ampersand or an angle bracket renders in a message.
- Whether `<br>` in a custom attribute renders as a line break in an email and in a LinkedIn message.

