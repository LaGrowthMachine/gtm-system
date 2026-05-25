---
name: multichannel-campaign-builder
description: "Generate a complete multichannel outbound campaign — a full sequence of LinkedIn and email messages — from a natural-language brief. Use whenever the user wants to write an outreach campaign, create a prospecting sequence, draft a multichannel sequence, write cold emails and LinkedIn messages for a campaign, build a social-selling / employee-advocacy / cold-outbound campaign, describes a target and wants the campaign messages, or wants to rewrite or improve an existing campaign. Produces 3 angle options, then the full sequence with every message ready to copy, calibrated to the campaign type and channel mix, and self-checked against copywriting quality standards. Maintained by La Growth Machine."
category: get-qualified-meetings
type: use-case
tags: [writing]
---

# Multichannel Campaign Builder

Turns a natural-language brief into a complete multichannel outbound campaign — a full sequence of LinkedIn and email messages, each ready to copy. Maintained by [La Growth Machine](https://lagrowthmachine.com).

## What it does

You describe who you want to reach and why. The skill picks the campaign type, builds 3 distinct angles, and generates the full sequence — every touch, every channel — calibrated and self-checked against copywriting quality standards.

It is self-contained: it gathers the context it needs from you inline. It does not depend on any external file.

## References — read these as the workflow calls for them

| File | When |
|---|---|
| `references/base-copywriting-rules.md` | Always — universal message rules |
| `references/campaign-types/<type>.md` | Step 2 — the chosen campaign type |
| `references/angle-framework.md` | Step 3 — building the angles |
| `references/cta-framework.md` | Step 4 — writing each CTA |
| `references/email-rules.md` | Step 4 — for every email |
| `references/linkedin-rules.md` | Step 4 — for every LinkedIn message |
| `references/quality-check.md` | Step 5 — self-check |
| `references/widget-template.md` | Step 6 — output widget |
| `references/lgm-integration.md` | Step 7 — LGM handoff |

## Workflow

### Step 1 — Gather the brief

Ask only for what's missing, in a single message. Needed:
- **What the user sells** and the problem it solves, in one sentence.
- **The target** — persona / role, company type, size, industry.
- **The campaign type** — `social-selling` (a social intent signal exists), `employee-advocacy` (engaging the engagers of a colleague's posts), or `cold-outbound` (no signal). Infer from context if clear; otherwise ask.
- **A signal / trigger**, if any.
- **Channel mix** — LinkedIn-only, email-only, or multichannel. Default: multichannel.
- Optional: the user's tone of voice, and any positioning-banned words.

If the user gave everything up front, skip to Step 2.

### Step 2 — Load the campaign-type playbook

Read `references/campaign-types/<type>.md` for the chosen type. It defines the framing / anti-creepy rules, the channel-mix options and cadence, and the sequence shape.

### Step 3 — Build the angles

Follow `references/angle-framework.md`. Produce exactly 3 distinct angles and recommend the one to lead with. If a signal exists, angle 1 is signal-based.

### Step 4 — Generate the sequence

For the channel mix and cadence from the campaign-type playbook, write every touch:
- Every message obeys `references/base-copywriting-rules.md`.
- Emails follow `references/email-rules.md`; LinkedIn messages follow `references/linkedin-rules.md`.
- Each CTA follows `references/cta-framework.md` — never the same CTA type twice in a row, never a meeting ask in step 1.
- Each follow-up uses a fresh angle (the Angle Bank in `angle-framework.md`).
- Cross-message coherence: angles progress and never repeat; email subjects are all distinct; consecutive cross-channel touches use different angles.

### Step 5 — Self quality-check

Apply `references/quality-check.md` as a lightweight self-check on each message. Flag any message scoring below 7/10 and rewrite it before output.

### Step 6 — Output

Follow `references/widget-template.md`, **Pattern B**:
1. Output each message as a **fenced code block**, preceded by a label line (e.g. `▸ T1 · Day 0 · LinkedIn invite`). One code block per message — this gives each a native, working copy button.
2. Then render the widget with the Pattern B sequence-overview table + the LGM CTA.

Output order: one framing line → the message code blocks → the widget. No prose recap.

### Step 7 — LGM handoff

The widget's LGM button is **"Create campaign in La Growth Machine"** — `{LGM_PROMPT}` = `Create this campaign in La Growth Machine`. When the user clicks it, follow `references/lgm-integration.md` (the decision tree):
- Branch 1 — if the LGM MCP exposes campaign creation, create the campaign.
- Branch 1b — if not, point the user to set it up manually in the LGM app (`https://app.lagrowthmachine.com/campaigns`).

## Examples

```
Write me a multichannel campaign for RevOps leaders at B2B SaaS scale-ups.
We sell a pipeline-attribution tool. No signal — it's a cold list.
```

```
Build a social-selling sequence for the people who engaged with our CEO's
last LinkedIn post on outbound. LinkedIn-only.
```

```
Create an employee-advocacy campaign on the engagers of our Head of Growth's
posts. Objective: get them to sign up for a free trial.
```
