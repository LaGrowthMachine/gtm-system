# Baseline playbook — the nine cards

The shipped best-practice body for each objection type. `scripts/analyze.py render`
splices the block between the `BASELINE:` markers into `cards/<type>.md`, under the
numbers pulled from the user's own data.

**This file is read-only.** Nothing writes to it, so a skill reinstall can only ever
cost the accumulated half of a card, never the useful-on-day-1 half. If a team wants
to change the house angle for an objection, they edit the rendered card in their
playbook directory, and `render` will detect the hand edit and refuse to clobber it.

Two rules run through every card:

1. **Dig before you reframe.** Almost every objection is a summary of something more
   specific. The question that gets the specific version is worth more than the best
   rebuttal to the summary.
2. **The exit is part of the play.** A clean, useful "no" keeps the door open and
   costs nothing. Reps who cannot exit gracefully create the objections they get next
   quarter.

Example lines are written to be sent as-is: no em-dashes, no marketing-speak, one
question maximum.

---

<!-- BASELINE:competitor_in_place -->
**What it usually means.** Rarely "we are happy". Usually one of three things: they
are genuinely well served, they bought a tool and never onboarded it, or they are
using the incumbent's name as a polite exit. The three need opposite replies, and you
cannot tell which one you have from the objection itself.

**Dig first.**
> How are you using [tool] today, on which part of the funnel? Asking because [the
> specific job] is the part most teams still end up doing by hand.

Do not open with a compliment to the incumbent. "Nice, [tool] is solid" reads as fake and
buys you nothing, and praising a tool you are about to be compared to makes them defend it
harder. Ask how they use it instead. Naming a specific job rather than a feature is what
separates a real answer from "yeah it's fine": you are looking for the gap between what
they bought and what they actually run.

**Reframe.** Only once they have named a gap. Anchor on the gap, never on a feature
comparison: they own the decision to buy the incumbent and defending against it makes
them defend it harder. If they are genuinely happy, say so out loud and leave.

**Exit with value.** A benchmark, a teardown, one number about how peers run it. You
want to be the person they message when the incumbent renewal comes up.

**Smokescreen branch** (named no tool, no specifics, arrived at first touch): give
them the honest out. "Sounds like you are set. If that changes, I'm around." A clean
exit here converts more often six months later than any second attempt now.

**What NOT to say**
- Anything negative about the incumbent. It reads as an attack on their judgment.
- A feature-by-feature comparison table they did not ask for.
- "What made you choose them?" as an opener. It sounds like an audit.
<!-- /BASELINE:competitor_in_place -->

<!-- BASELINE:feature_gap -->
**What it usually means.** The most honest objection you get, and the most often
mishandled. A named missing capability is a buying signal wearing a blocker's coat:
they evaluated enough to know what they need. The mistake is answering the feature
question instead of the job behind it.

**Dig first.**
> Good to know. What would [the capability] need to do for you day to day? Asking
> because teams mean quite different things by it.

**Reframe.** Three honest branches, and only three. You have it: show it in one line,
no demo pitch. You do not have it but the job is covered another way: say exactly how,
and say plainly that it is not the same thing. You do not have it and cannot cover it:
say so, and say when or whether it is coming. Never say "it's on the roadmap" unless
you can name a quarter.

**Exit with value.** Point them at what actually solves it, even if that is a
competitor. This is the single highest-trust move available to a seller, and reps who
make it get referrals.

**Smokescreen branch** (the requirement keeps moving, or each answer produces a new
one): stop answering. "Feels like I'm not hitting the real blocker. What would have to
be true for this to be worth your time?"

**What NOT to say**
- "It's on the roadmap" with no date. It reads as a no with extra steps.
- Reframing their requirement as unnecessary. They know their stack.
- Burying the gap under three things you do have.
<!-- /BASELINE:feature_gap -->

<!-- BASELINE:tried_before -->
**What it usually means.** They are not objecting to your product, they are objecting
to a memory. Someone spent budget, it failed, and it was probably visible internally.
The blocker is reputational as much as technical. Treat it that way.

**Dig first.**
> That is worth knowing. What went wrong, was it the tool or everything around it?

Most "we tried this" failures are process failures: nobody owned it, the data was bad,
the team never adopted it. If they name the surrounding process, you are in good shape.
If they name a hard product limit, believe them.

**Reframe.** Acknowledge the scar before anything else, and be specific about what is
different now. Vague "things have changed" makes it worse. If nothing meaningful has
changed, say so and leave.

**Exit with value.** Whatever they learned is worth naming back to them. "Sounds like
the blocker was ownership rather than tooling" is a more useful sentence than any pitch.

**Smokescreen branch** (cannot say what was tried or when): they are using a past
attempt as a shield. One light question, then out.

**What NOT to say**
- "It's completely different now." Unfalsifiable, so it reads as a sales line.
- Anything implying they ran it wrong, even gently.
- Asking them to re-litigate a decision their boss made.
<!-- /BASELINE:tried_before -->

<!-- BASELINE:price_budget -->
**What it usually means.** "Too expensive" is a comparison you cannot see. Expensive
against what: another tool, an internal hire, doing nothing, or last year's budget
that is already spent. Discounting before you know which one is the most expensive
mistake in this playbook, because it prices the deal against the wrong anchor and you
never get the anchor back.

**Dig first.**
> Fair. Expensive compared to what, out of curiosity? Helps me tell you straight
> whether it is worth your time.

**Reframe.** Anchor against whatever they name, and only that. Against another tool:
compare on the job, not the line item. Against a hire: compare on ramp and fixed cost.
Against doing nothing: put a number on the current cost, using their numbers, not
yours. If there is genuinely no budget this year, that is a timing objection wearing a
price coat, and it gets the timing play.

**Exit with value.** "Not at that price" is real information. Leave them something
they can use for free, and note the budget cycle.

**Smokescreen branch** (price raised at first touch, before any scope exists): nobody
can evaluate price from a cold message. This is a polite exit most of the time. One
de-escalating line: "Totally fair, you have no reason to care about the price yet.
Was it the [topic] itself that missed?"

**What NOT to say**
- A discount. Not in the first reply, not as a question, not as a hint.
- "It pays for itself" without their numbers in the sentence.
- Defending the price. You cannot win an argument about a number they have not
  scoped yet.
<!-- /BASELINE:price_budget -->

<!-- BASELINE:timing -->
**What it usually means.** The most common objection and the least informative. It
covers real sequencing ("we are mid-migration"), soft rejection, and no-budget. The
job of the reply is to convert a vague later into either a real date or an honest no,
because a vague later costs you a follow-up every quarter forever.

**Dig first.**
> Understood. What is taking the priority right now? Might be more useful to talk
> about that instead.

This is a genuinely useful question and not a technique. Often what they name is
something you can help with, and that conversation converts better than the one you
opened with.

**Reframe.** Do not argue with the timing. Attach to the priority they named, and set
a specific reconnect anchored to their calendar, not yours: after their migration,
after the fiscal year, after the hire lands. "Q3" is not a date, "after your Workday
migration wraps" is.

**Exit with value.** One thing useful for the priority they named. That is what makes
the reconnect welcome rather than tolerated.

**Smokescreen branch** (no reason given, no date, first touch): "Sounds like the
timing is a no rather than a later, which is completely fine. Want me to close the
loop, or ping you once things settle?" Giving permission to say no gets you a truthful
answer, and truthful answers are what keep the pipeline honest.

**What NOT to say**
- "When would be a good time?" You will get a date they invented to end the exchange.
- Manufactured urgency. Any version of "prices go up".
- "I'll circle back in Q3" with no reason to.
<!-- /BASELINE:timing -->

<!-- BASELINE:value_doubt -->
**What it usually means.** They believe the category works, they do not believe your
claim. Almost always caused by our own copy: a number too round, an outcome too big,
a promise with no mechanism attached. This is the one objection where the fix is
usually upstream, in the message that produced it.

**Dig first.**
> Fair enough, it does sound like a lot. What would you need to see to believe it,
> a number from someone like you or the mechanics of how it works?

The two answers need different proof, and guessing wrong wastes your one shot.

**Reframe.** Replace the claim with the mechanism. People disbelieve outcomes and
believe processes. Shrink the claim to the part you can evidence, and name the
conditions where it does not hold. A caveat is the cheapest credibility available.

**Exit with value.** Send the proof even if they are gone. Skeptics forward things.

**Smokescreen branch** (dismissive, no specifics, no question back): they are not
asking to be convinced. Do not send a case study. Acknowledge and leave the door open.

**What NOT to say**
- A bigger number. Escalating the claim confirms the suspicion.
- "Happy to show you on a call." Asking for time is the wrong currency with a skeptic.
- Three case studies at once. Volume reads as compensation.
<!-- /BASELINE:value_doubt -->

<!-- BASELINE:process_authority -->
**What it usually means.** Two very different situations behind one sentence. Either
they are a genuine champion who needs help selling internally, or they are using the
org chart as a shield. Tone tells you which: a champion adds detail, a shield stays
vague.

**Dig first.**
> Makes sense. What usually decides it on your side, and what would you need from me
> to make that easy?

**Reframe.** If they are a champion, your job stops being selling to them and starts
being arming them: one short thing they can forward, in their language, that survives
being read without you. Ask who else needs to be comfortable and what usually kills
these internally. If it is procurement or security, ask for the actual process rather
than trying to route around it.

**Exit with value.** A one-page version they can forward. It travels where you cannot.

**Smokescreen branch** (vague authority, no names, no process): "Sounds like this is
not a priority to push internally right now, which is fair. Want me to leave it?"

**What NOT to say**
- "Can you introduce me to your boss?" as the first move. It skips over them.
- Anything that implies they lack influence.
- A long document. Nobody forwards a long document.
<!-- /BASELINE:process_authority -->

<!-- BASELINE:scope_mismatch -->
**What it usually means.** The job left. Outsourced, cut, absorbed by another team, or
the strategy changed. This is the objection most often over-fought, because it is
frequently just true, and it is also the most reliable targeting signal you get: a
cluster of these in one campaign means the list is wrong, not the copy.

**Dig first.** One question, not a campaign.
> Good to know. Who picked it up, or did it stop being a thing entirely?

**Reframe.** Only if an adjacent need is plausible. Often the honest move is to ask
who owns it now, which turns a dead end into a referral. If they say it stopped being
a thing, believe them and leave.

**Exit with value.** Thank them properly. They spent time correcting your assumption
when ghosting was easier, and that is worth an actual thank you.

**Smokescreen branch** (rare here, because it is a costly lie to tell): treat it as
real. Take it at face value and exit.

**What NOT to say**
- "But surely you still need to..." You are telling them about their own company.
- A pivot to an unrelated product in the same message.
- Any question after they have said the job is gone. Zero questions on an exit.

**Note for the analysis.** If this type concentrates in one campaign or audience, the
fix is not the reply. It is the list.
<!-- /BASELINE:scope_mismatch -->

<!-- BASELINE:channel_trust -->
**What it usually means.** They are not objecting to the offer, they are objecting to
the approach. Almost always self-inflicted: over-personalized copy that reveals
scraping, a false claim of connection, an obviously automated message, or a channel
they never opted into. It is the highest-signal objection in the whole set, because it
points at something you control completely.

**Handle it, do not dig.** This is the one card where digging is wrong. Answer the
question directly and immediately, in one short message.
> Fair question. I found you [exact, true source]. If you'd rather I didn't reach out
> here, tell me and I'll close the loop.

Two rules, no exceptions. Be truthful about the source: a vague answer confirms the
suspicion and a false one is a compliance problem. And offer the exit unprompted.

**Reframe.** There isn't one, and reaching for one is the mistake. The only recovery
available is a straight answer plus a genuine opt-out. Take the no if it comes.

**Exit.** Immediate, complete, and honour it across every channel and every list.

**If they ask whether it is automated or AI-written:** answer honestly. Denying it
when it is true ends the relationship and, in some jurisdictions, creates a real
problem. This is a stop-and-escalate case in any automated workflow.

**What NOT to say**
- A vague source. "Your profile came up" is what a scraper says.
- Any pitch in the same message. Answer the question, nothing else.
- Anything defensive about the legality. If it needs defending, fix the process.

**Note for the analysis.** A rising rate here is a copy and compliance alarm, not a
coaching topic. Fix the sequence before you coach the replies.
<!-- /BASELINE:channel_trust -->
