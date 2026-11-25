---
name: write-sequence
description: "Shared sub-skill. Writes the outline of the sequence: 3 angles to choose from, then every message. In personalised mode each message is a frame the agent rewrites for each lead; in template mode each message is the final text, with {{firstname}} as the only variable."
---

# Write the sequence

Produce the outline the human approves once. You write copy here. You do not search leads and you do not touch La
Growth Machine.

## Two modes, set by the brief

| Mode | When | What each step of the campaign holds |
|---|---|---|
| **Personalised** (the default of the agent) | The agent writes for each lead: there is a signal or facts per lead worth using | `{{customAttributeN}}` only. The attribute holds the whole message of that lead, written at step 7 from this outline. |
| **Template** | The user does not want per-lead messages, or the leads carry no usable fact | The final text, the same for everyone. `{{firstname}}` is the only variable. |

Ask when the brief does not say it: "One message written for each lead, or the same message for everyone with their
first name?" In both modes the outline below is written the same way. Only its use changes.

## Output discipline

Return the deliverables and nothing else: the 3 angles, the outline, the attribute table. No preamble, no narration of
the steps. If something essential is missing, ask one short question and stop.

## Step 1. Gather the brief

Read the context loaded at Setup first (what we sell, to whom, how we write). Take the rest from the request. Ask only for what is missing, in one message.

- **What we sell** and the problem it solves: from the context.
- **The target**: persona, company type, size, industry, location. From the request.
- **The signal**: the reason to write to these people now. If there is none, say so: the campaign is cold.
- **The campaign type**: `cold-outbound` (no signal), `social-selling` (a social intent signal exists) or
  `employee-advocacy` (engagers of a colleague's posts).
- **The channel mix**: LinkedIn + email (default), email only, LinkedIn only.
- **The language** of the leads.

## Step 2. Load the rules

Read `{SKILL_BASE}/skills/copywriting/SKILL.md`, then the files it lists. Load only the campaign-type playbook that applies.

## Step 3. Build 3 angles

Follow `{SKILL_BASE}/skills/copywriting/angle-framework.md`. Produce exactly 3 distinct angles and recommend the one to lead with. If a
signal exists, angle 1 is built on it.

If the user already gave the angle, skip this step and write on it.

Otherwise show the 3 angles as a choice, each in 2 lines (the tension it opens, the first line it would give), and
ask: "Which one do you want to go with? Or should I dig other angles?" Recommend one and say why. If the user wants
others, give 3 new ones, different from the first three. Write nothing more until an angle is picked.

## Step 4. Set the shape

The copy comes first. Take the channel mix from the brief and the cadence from the campaign-type playbook: the
number of touches, their channel, their order, the days between them. `build-campaign` then finds the structure
that fits this outline and adapts with the human where they differ.

If the user already named a campaign or a template to start from, write on its shape instead.

## Step 5. Write every message

For each step of the template:

The files below are in `{SKILL_BASE}/skills/copywriting/`.

- Follow `base-copywriting-rules.md`, then the channel file (`linkedin-rules.md` or `email-rules.md`).
- Pick the CTA with `cta-framework.md`: never the same type twice in a row, never a meeting ask in step 1.
- Give each follow-up a fresh angle from the Angle Bank in `angle-framework.md`.
- Email follow-ups go in the same thread, with no new subject.

Then, in personalised mode, give each message its frame for step 7:

- **What it says**: the reason, the offer, the proof, the question it ends on. This is fixed for every lead.
- **What changes per lead**: which fact of the lead or of the signal it opens on, and how the tension ties to their
  case. Never a sentence to fill in: the whole message is rewritten per lead in natural words.
- **The custom attribute** of the step (one per message step, plus one for the email subject when it changes per
  lead, plus one review attribute that is never shown) and its maximum length.
- **The fallback version**: the full message for a lead with no usable fact. It must stand on its own.
- **Branches** when the target mixes profiles that do not read the same message (a seller and a builder, two
  industries): one frame per branch, and the rule that picks the branch of a lead.

In template mode, the message written here is the final text: `{{firstname}}` is its only variable.

## Step 6. Self-check

Run `{SKILL_BASE}/skills/copywriting/quality-check.md` on every message (in personalised mode, on its fallback version). Rewrite any message scoring
below 7 out of 10 before showing it. Check in particular:

- no em dash, no punctuation glued to a URL;
- one question per message at most;
- no forbidden phrase;
- the CTA order respects the framework;
- the best message is the first touch.

## Step 7. Output and stop

In the language of the leads. One line of framing, then:

1. The 3 angles, the chosen one marked.
2. Each message in its own code block, with a one-line label above it (step, channel). In personalised mode: the
   fallback version, then under it what changes per lead.
3. In personalised mode, the attribute table: custom attribute, step, role, maximum length, the branch rule.
4. The sequence overview: one line per step with its channel, its angle and its CTA type.

Then stop and ask for approval. Nothing else happens until the outline is approved.

Once approved, the outline and the attribute table go into the campaign file, written by `build-campaign`.
