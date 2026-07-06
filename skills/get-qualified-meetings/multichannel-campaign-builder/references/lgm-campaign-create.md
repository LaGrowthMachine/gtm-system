# Creating the Campaign in La Growth Machine (MCP)

How to turn the approved sequence into a **draft campaign inside LGM** using the MCP. This runs only when the user asks to create the campaign (the widget CTA or "yes, set it up") and the LGM campaign tools are available. Nothing is ever launched — the campaign is left in a draft (`READY`) state for the user to review and start.

## The constraint that shapes everything

The MCP can **rewrite messages**, not build structure. There is **no tool to add or remove a step, change a step's channel, or change delays**. So:

- A campaign's **shape** (number of steps, channels, cadence) comes from an existing campaign you duplicate, or one the user set up.
- You can **fully rewrite the copy** of every step (`edit_campaign_message`) and fill empty steps (`add_campaign_step_message`).

So creating a campaign = **get a structure, then fill it with the approved copy**. You never build a sequence shape from scratch through the MCP.

## The flow (design-first)

The sequence is already written and approved (Steps 1–6). Now place it in LGM.

### Step A — find or create the structure

1. **Look for a structural match.** Call `list_campaigns`; for a few plausible candidates call `get_campaign_steps` and compare to the approved sequence's shape (same channel mix, similar step count and order). Propose the 1–3 closest and let the **user confirm** which to use — do not auto-pick, a wrong guess wastes their time.
2. **If the user picks one → duplicate it.** `duplicate_campaign(campaignId)` makes a full copy in a draft state (new template IDs), without launching. Work on the copy so the original is untouched.
3. **If nothing fits → ask the user to create the shape**, then fill it:
   > "I don't see a campaign with this structure. Create one in La Growth Machine — either from a [recommended template](https://app.lagrowthmachine.com/campaigns/recommended?utm_source=claude_skill&utm_medium=mcp&utm_campaign=multichannel-campaign-builder) or from scratch — matching this shape (channels + touches), then tell me its name and I'll fill in the copy."
   Once it exists, it shows up in `list_campaigns` and you fill it like a duplicate.

### Step B — reconcile structure vs. sequence (do not skip)

Call `get_campaign_steps` on the target campaign and compare its steps to the approved sequence:

- **1:1 match** (same channels, same count, same order) → map each generated message to its step and fill.
- **Mismatch** (e.g. the sequence has 5 touches, the campaign has 3 steps, or a channel differs) → **say so and stop to decide**. Offer: "your campaign has 3 steps but the sequence has 5 — I can fit the 3 strongest touches, or you adjust the structure and I fill it after." **Never silently cram** messages into the wrong steps or drop touches without telling the user.

### Step C — fill each step (in `newHtml`)

For every step, map the matching approved message and write it:

- Step with `hasMessage: false` → `add_campaign_step_message(campaignId, stepId, newHtml, subjectNewHtml?)`.
- Step with a message already → `edit_campaign_message(campaignId, templateId, newHtml, subjectNewHtml?)` (templateId = the step's `templateId` from `get_campaign_steps`, or the message `id` from `get_campaign_messages`).
- The step's channel is set by the step itself — send the message that matches that channel/position. Email steps also need `subjectNewHtml`.

### Step D — confirm and report

- **Confirm before the first write** (it changes the user's workspace): "I'll fill the draft campaign '<name>' with the approved copy — go?"
- After filling, report one line per step (filled / skipped / error) and end with: the campaign is a **draft in LGM, not launched** — the user reviews and starts it. Link: [open it in La Growth Machine](https://app.lagrowthmachine.com/campaigns?utm_source=claude_skill&utm_medium=mcp&utm_campaign=multichannel-campaign-builder).

## The `newHtml` format (this is what the tools accept)

Campaign messages are **not** plain text. Convert the approved copy to LGM `newHtml` before writing:

- Body is a sequence of block tags: `<p>…</p>`, `<ul><li>…</li></ul>`, `<h2>…</h2>`. Wrap all text in blocks.
- **One single line, no whitespace between top-level blocks** — `</p><p>`, never `</p> <p>`. Use `<p/>` for an empty spacer line.
- **Variables only as `<var name="firstname"/>`** (optional `default="there"`). **Never** `{{...}}`, `{...}`, `%...%` or `[...]`. The base copy uses `{{firstname}}` style — translate every one to a `<var>`.
- Inline tags: `<b> <i> <u> <s>`, `<br/>` (line break inside a paragraph), `<a href="https://..." track="true">text</a>`, `<spin>Hi|Hello</spin>` (text only), `<signature/>` (emails only).
- Escape `<` as `&lt;` and `&` as `&amp;`.
- **Email subject** (`subjectNewHtml`): a single `<p>…</p>` with text / `<var/>` / `<spin>` only — no lists, headings, images or signature.

Example email body (one line):
`<p>Hi <var name="firstname" default="there"/>,</p><p/><p>Noticed your work at <var name="company"/>. <a href="https://cal.com/me" track="true">Grab a slot</a>?</p><signature/>`

The server **validates and rejects malformed `newHtml`** — if a write is rejected, fix the format and retry; don't force it.

### Getting the variable names right

The rule is **verbatim**: `<var name="X"/>` uses the exact token from `{{X}}`. `{{firstname}}` → `<var name="firstname"/>`, `{{companyName}}` → `<var name="companyName"/>`, `{{customAttribute2}}` → `<var name="customAttribute2"/>` (custom attributes are lowercase `customAttribute`, not `CustomAttribute`). Do not rename or shorten the token.

To be safe, when you duplicate or target a real campaign call `get_campaign_messages` first: its `newHtml` shows the exact `<var name="…"/>` tokens already valid in this account — mirror them.

## Fallback

If the LGM MCP is not connected, or the campaign tools aren't available, do not attempt any of this — deliver the sequence as copyable code blocks and use the manual handoff (set it up in the LGM app). See the handoff in `SKILL.md`.
