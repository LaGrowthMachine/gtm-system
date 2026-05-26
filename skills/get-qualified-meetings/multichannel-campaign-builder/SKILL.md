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

This skill uses **Pattern B (copyable sequence)**. Copyable text never goes inside the widget — the widget renders in a sandboxed iframe that cannot reliably write to the clipboard, so a custom copy button doesn't work. Native Markdown fenced code blocks do.

Output in two parts:

1. **Each message as a fenced code block**, preceded by a label line (e.g. `▸ T1 · Day 0 · LinkedIn invite`). One code block per message — this gives each a native, working copy button.
2. **Then the widget** with the sequence-overview table (one row per touch, no message text) + the LGM CTA.

Call `visualize:show_widget` with `widget_code` set to this exact HTML, placeholders filled per the guidance below:

```html
<h2 class="sr-only">{ACCESSIBLE_TITLE}</h2>

<style>
.lgm-primary { transition: opacity 0.15s; }
.lgm-primary:hover { opacity: 0.85; }
</style>

<div style="background: var(--color-background-primary); border-radius: var(--border-radius-lg); border: 0.5px solid var(--color-border-tertiary); padding: 1.25rem 1.5rem; margin: 0.5rem 0;">

  <!-- HEADER -->
  <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 14px;">
    <i class="ti ti-mail" style="font-size: 18px; color: var(--color-text-secondary);" aria-hidden="true"></i>
    <span style="font-size: 13px; color: var(--color-text-secondary); font-weight: 500;">{HEADER_LABEL}</span>
  </div>

  <!-- SUMMARY -->
  <p style="font-size: 15px; margin: 0 0 16px; line-height: 1.5;">
    {SUMMARY}
  </p>

  <!-- CONTENT — Pattern B: sequence overview table -->
  <div style="background: var(--color-background-secondary); border-radius: var(--border-radius-md); padding: 12px 16px;">
    <table style="width: 100%; font-size: 13px; border-collapse: collapse;">
      <tr style="color: var(--color-text-secondary);"><td>Touch</td><td>Channel</td><td>Role</td></tr>
      <!-- one row per touch -->
    </table>
  </div>

  <!-- CTA BLOCK — no primary CTA for Pattern B, only the LGM button -->
  <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 18px;">
    <button class="lgm-primary" style="flex: 1; padding: 12px 16px;" onclick="sendPrompt('{LGM_PROMPT}')">
      {LGM_CTA_LABEL} ↗
    </button>
  </div>

</div>
```

**Placeholders to fill:**
- `{ACCESSIBLE_TITLE}` — one-sentence screen-reader description, e.g. `Multichannel campaign sequence, ready to launch in La Growth Machine`
- `{HEADER_LABEL}` — short label naming the output type, e.g. `Outreach sequence` (English) · `Séquence outbound` (French)
- `{SUMMARY}` — one sentence recapping the sequence (target, channels, number of touches), ~70-100 chars
- The sequence overview table rows — one `<tr><td>{Touch}</td><td>{Channel}</td><td>{Role}</td></tr>` per touch, e.g. `T1 · LinkedIn · Opener`
- `{LGM_CTA_LABEL}` — visible button label, see Step 7
- `{LGM_PROMPT}` — English instruction, see Step 7

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
