# Outline · Hiring signal

> The frame of every campaign that starts from a job post. It was written and corrected on real campaigns of La
> Growth Machine (13 leads), then made general: the structure, the rules and the sequence stay, the offer is yours.
> At the creation of a campaign (step 0b of the agent), the agent fills the parts marked **[your offer ...]** from
> `context/offer.md` and 5 real posts, with you. A campaign file sets the roles, the place and the size, and points
> here for everything else.

## The idea

| | |
|---|---|
| Signal | The company has an open job post for a role whose work your offer helps with |
| Why now | The seat is empty. The work the post describes is waiting, the targets of the role are not. |
| Who we write to | The person the role reports to, never HR. The rule by company size is in the `find-contacts` skill. |
| What we bring | **[your offer, in one line: what it does today for the work the hire will do]** |
| What happens when the hire starts | They take over, with something already running. They can focus on the rest of their list. |
| Why they reply | It is their own job post and one mission of it can start now. The question takes one line to answer. |
| What we want | **[the first step you want: a reply, then a trial, a call, a resource]** |
| The tone | Positive: we help them move forward until the hire starts. We never replace the hire. Never "miss", "lose" or "fall behind". |

We only talk about the part of the job our offer covers. A job post covers much more: we take that part off their list
so the hire can focus on the rest.

## Set up the outline for your offer (once, at the first campaign)

The agent does this with you, from `context/offer.md` and 5 real posts of the role:

1. **The missions you cover.** Which missions of a job post your offer does today. They make the "Strong" and
   "Partial" fits below.
2. **The families.** Group the missions that call for the same offer (2 to 5 families). For each, one sentence of
   offer: what you do for that mission. They go in `{SKILL_BASE}/skills/find-job-posts/mission-families.md`.
3. **The proof and the claims allowed**: what you may say (customers, integrations, numbers you can cite) and what
   you never say.
4. **What you send to test**: the low-friction thing the last message offers (a trial, a demo video, a template, a
   short audit).
5. **The signature**: the sender first name and the company name.

Write them in the campaign file, section "Adjustments", until you have run a few campaigns. Then they can move into
this file.

## What a campaign sets

The campaign file holds only what differs from one campaign to the next:

| Setting | Example (never a default: each campaign sets its own) |
|---|---|
| Roles to watch | Head of Growth, RevOps Manager. Or SDR, for another campaign. |
| Location and period | San Francisco Bay Area, posts of the last 30 days |
| Company size | For example 200 people at most. Asked at every new campaign: a limit can leave out most real posts of a region. |
| Sender, language | The sender identity of the campaign, EN |
| La Growth Machine campaign and audience | The id and the audience name |
| Matches wanted per run, routine, push while it runs | 10, no, no |
| Adjustments | The setup above, and what this campaign changes in the outline, decided with the human |

**One campaign per set of roles, not per place.** The messages do not change with the city. A brief on another city of
the same country feeds the campaign that lists the role. Another language or another outline is a reason for a new
campaign. Another city is not.

## How a post is scored

The title is not enough. The agent reads every post and keeps the ones with a mission your offer covers.

| Fit | When | What to do |
|---|---|---|
| Strong | A mission of the post is one your offer does today | Write. Say that mission. |
| Partial | The post carries that work without making it the main mission | Write. Say the closest mission. |
| None | Nothing your offer covers. Also a consumer business when you sell to businesses, a recruiting firm posting for a client, a post with no real text. | Leave out, with the reason |

**When the headcounts disagree.** The number of members on the LinkedIn page of the company ("View all N employees")
wins over the size band of that page and over an aggregator. If that number is above the size of the campaign, the
company is left out. If it cannot be read and the other sources fall on each side of the limit: ask in a session,
leave out in a routine. Also note, when the post says it: a deadline, the tools in place, who already does the work.

## The layers of personalization

Each message takes its layer.

**Layer 1, the mission family**, from the post. It sets email 1 and the first LinkedIn message. The families live in
`{SKILL_BASE}/skills/find-job-posts/mission-families.md`, a file that grows with every post read. Take the first family that
applies. No family: the post is not a fit, do not write.

**Layer 2, who the company sells to**, read on its website with the `read-company` skill. It fills `[target]` when your
offer is about their customers, or another slot your offer needs (their product, their market).

**Layer 3, the milestones of the post.** It sets email 2. When the post gives a deadline or a milestone for the role
("in 60 days", "in the first 90 days"), we use it: results can come before that date.

**Layer 4, the size of the team**, from the headcount. It adds one line to email 2. If the post contradicts the tier,
the post wins.

| Tier | Headcount | The line |
|---|---|---|
| XS | 10 or fewer | **[how a founder can run it alone]** |
| S | 11 to 50 | **[how fast it starts and who approves]** |
| M | 51 to 200 | Meanwhile they can focus on the rest of their list |
| L | Over 200 | One team can start with it and the others follow |

## Claims allowed

Only what `context/offer.md` and the setup above allow. Never a price, never a result promised with a number unless
the offer gives it as a public proof. Never the name of an integration you do not have.

## Custom attributes

One message = one custom attribute.

| Attribute | Content |
|---|---|
| customAttribute1 | Email 1 |
| customAttribute2 | Email 2 |
| customAttribute3 | Email 3 |
| customAttribute4 | Invitation note (leads with no email) |
| customAttribute5 | Not used. Write "Not used in this campaign." so no value from another campaign stays in it. |
| customAttribute6 | LinkedIn message 1 |
| customAttribute7 | LinkedIn message 2 |
| customAttribute8 | LinkedIn message 3 |
| customAttribute9 | Subject of email 1 |
| customAttribute10 | For review only, never in a message: the fit, the family, the tier, the post and its date, the mission quoted, the target and the milestone used |

Emails are written in HTML, with `<br>` for line breaks.

How the 10 steps of the model campaign map to the attributes:

| Step in La Growth Machine | Branch | Attribute |
|---|---|---|
| Email #1 | Lead with an email | 1, subject 9 |
| Email #2, two steps at the same position | Lead with an email | 2 |
| Email #2 at the last email position | Lead with an email, invitation not accepted | 3 |
| LK #1 and LK #2 after the emails | Lead with an email, invitation accepted | 6 and 7 |
| LinkedIn Contact Request #1 | Lead with no email | 4 |
| LK #1, LK #2, LK #3 | Lead with no email | 6, 7 and 8 |

The model campaign to duplicate is shared by La Growth Machine: « Template Hiring Signal | Apify x La Growth Machine »,
https://app.lagrowthmachine.com/campaigns_shared/6afd83a77b678cc317a833c6 (id `6afd83a77b678cc317a833c6`, no lead in
its audience). Its 10 steps already hold these variables, so a copy needs no message edit. A copy keeps the audience,
the sender, the language and the CRM sync of its source: set them right after (`{SKILL_BASE}/skills/build-campaign`).

## The sequence

```
With an email:  Day 0 Email 1 → Day 1 invitation, no note → Day 3 Email 2
                → invitation accepted: LinkedIn 1 then LinkedIn 2
                → not accepted: Email 3
No email:       Day 0 invitation with a note → accepted: LinkedIn 1 → LinkedIn 2 → LinkedIn 3
```

No link in the sequence and none in a custom attribute. The last message offers to send **[what you send to test]**.
The link is sent in the reply.

## The outline

The outline is a frame. It fixes what each message says, the order of the messages and the question each ends on.
The agent writes every message in natural words for its lead (`personalize` skill): it may reword a sentence, name
the role in its short form or drop a clause that is not true for this lead. It never changes the offer and never
adds a claim. A message that reads as a filled template has failed.

`[firstname]` comes from the lead, as the person writes it on their profile. Every email opens with "Hi
[firstname],". The other slots are written per lead:

| Slot | What it is | Where it comes from | If it cannot be filled |
|---|---|---|---|
| `[role]` | The role in its short spoken form: "a head of growth", "a founding RevOps". After email 1, "your new hire" or "they". | The post | The post is not a fit |
| `[mission]` | What the hire will do, in plain words, 12 words at most. True to the post, never copied from it. | The post | Pick another mission of the post. None: not a fit. |
| `[target]` | Who the company sells to, 8 words at most (when your offer is about their customers) | The `read-company` skill | "the right people" |
| `[milestone]` | The deadline or the milestone the post gives for the role | The post | Use the version of email 2 with no milestone |
| `[tool]` | A tool the post names that matters for your offer. A tool given as an example does not count. | The post | The family that needs it does not apply |
| `[colleague]` | The person who may own the topic: a first name found by `find-contacts`. Otherwise the role the post names. | `find-contacts`, the post | The default question of email 3 |

`[your offer for this family]` is the sentence of offer of the family, from `mission-families.md`.

### Email 1 · Day 0

Subject: `your [role] hire`, in lower case, with the short form of the role: "your head of growth hire".

```
Hi [firstname],

Saw you're hiring a [role] to [mission].

To help before they start, [your offer for this family].

Is someone on this until then or is it waiting for them?

[sender first name]
[your company]
```

**The question of a message names the work and who does it.** "Is someone on this until then or is it waiting for
them?" is the default. When the post says who already does the work (a team, an agency, the founder), name them:
"Is your team covering this until then or is it waiting for them?". In the invitation note and in LinkedIn 1, "until
then" becomes "until they start".

### Email 2 · Day 3, same thread

```
Hi [firstname],

[mission, said as one of the first things on the new hire's list]. If [your offer] already brings the first results, they will only have to scale it.

No need to wait [milestone] to see results. [tier line]

Is [the work] among the first things you expect from them?

[sender first name]
```

With no milestone in the post, the third sentence becomes "No need to wait for the hire to see results."

### Email 3 · if the invitation is not accepted, same thread

```
Hi [firstname],

I can send you [what you send to test]. [One sentence on how little it takes to try.]

Do you want it now or should I come back once your new hire has started?

[sender first name]
```

The routing question, when another person may own the topic, replaces the question above:

```
Should I send it to [colleague] or come back once your new hire has started?
```

### LinkedIn, leads with an email (after the invitation is accepted)

LinkedIn 1

```
Hi [firstname], sent you an email too, easier to answer here if you prefer. Is someone on [the work] until your new hire starts or is it waiting for them?
```

LinkedIn 2 · 4 days later

```
[firstname], I can send you [what you send to test]. Do you want it now or should I come back once your new hire has started?
```

### LinkedIn, leads with no email

Invitation note (200 characters at most)

```
Hi [firstname], saw you're hiring a [role]. Is someone on [the work] until they start or is it waiting for them?
```

LinkedIn 1 · 1 day after the invitation is accepted

```
Hi [firstname], you're hiring a [role] to [mission]. To help before they start, [your offer for this family]. Want me to show you?
```

LinkedIn 2 · 3 days later

```
[firstname], [mission, said as one of the first things on the new hire's list]. If [your offer] already brings the first results, they will only have to scale it. Is [the work] among the first things you expect from them?
```

LinkedIn 3 · 4 days later

```
[firstname], I can send you [what you send to test]. Do you want it now or should I come back once your new hire has started?
```

## Cases

A case is not a family. It adds to the family of the lead when a fact of its post or of its website calls for it. It
changes a sentence or a question. It never changes what we offer.

**How a case gets here.** In a run, the human reframes a message for one lead. The agent applies it to that lead only
and notes it in the review attribute. At the end of the run it lists the reframing as a proposed case: when it
applies, what changes, the company it came from. The human decides. Only then is it written in this section.

Two cases come from the original campaigns and hold for most offers:

### A tool that does what you do is in place

| | |
|---|---|
| When | The post or the website names a tool the company uses today for the work your offer does. A tool given as an example or as experience wanted does not count. |
| Email 1 | Names the tool once, right after the mission, with no judgment: "Looks like [tool] is already in your stack." |
| The question of email 1, of the invitation note and of LinkedIn 1 | "Will your new [role] have to keep using [tool] or are you open to testing other tools?" |
| The tool is yours | Do not write. Tell the human: the company is a customer. |

Never compare and never say what the tool lacks.

### A founder who does the work and nobody else known

| | |
|---|---|
| When | We write to a founder or a CEO, a source says they carry this work themselves and nothing says who else does it. |
| The offer of email 1 | "Until they start, [your offer] can take [the work] so you can focus on [what the source says this person does]. Your new hire will only have to scale it." |
| If no source says what the founder does | Drop "so you can focus on…". Never guess it. |

## Rules

- One question per message. No comma before "and" or "or". No long dash.
- No colon to link two clauses inside a message. Write two sentences.
- Positive words only: we help them move forward until the hire starts. Never "miss", "lose", "fall behind".
- We never replace the hire. Say "until they start", "so they start with something already running".
- Never open with "Thanks for connecting". Never "congrats on the hire".
- Say what the post says in plain words, as a person would after reading it. Never copy a sentence of the post and
  never write "the post mentions". Talk to the lead: "you're hiring", not "[company] is hiring".
- Stay true to the post: no tool, number, mission or priority it does not state.
- The role in its short spoken form, never the title pasted as it is.
- Only the work your offer covers. Never comment on the other missions of the post.
- The offer has to follow from the mission the message says. If it does not, take another family or leave the post
  out.
- The words of the offer are yours, not the post's.

## If the lead replies

- **They want what you offered**: send it, with the link, and offer to set up the first step together.
- **Nobody does the work or it is waiting**: same, with one line on how fast it starts.
- **Someone does it**: one question on what they use today, then your offer as a complement.
- **"Come back when they have started"**: thank them, note the date, come back when the role is filled.
- **They ask for a demo**: one qualifying question, then the next step you offer.

## Adapting the outline to another role

The agent does this with the human, before any lead is searched:

1. Read 5 real posts for the role and score them. If most are "None", the role is not a signal for your offer.
2. Check that the families cover what these posts say. Propose a new family when one keeps coming back.
3. Choose the question for companies that already have someone on the work.
4. Write the adjustments in the campaign file.
