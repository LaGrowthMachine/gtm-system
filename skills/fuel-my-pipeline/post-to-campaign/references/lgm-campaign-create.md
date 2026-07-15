# Creating the Draft Campaign in La Growth Machine (MCP)

How to turn the approved sequence into a **draft campaign** in LGM. Runs only when the LGM MCP is connected. Nothing is ever launched: the campaign is left in a draft state for the user to review and start.

## The constraint that shapes everything

The MCP can **rewrite messages**, not build structure. There is **no tool to add or remove a step, change a step's channel, or change delays**. So a campaign's shape (number of steps, channels, cadence) comes from an existing campaign you duplicate, or one the user creates. You then fully fill or rewrite the copy of each step.

Creating a campaign = **get a structure, then fill it with the approved copy.** You never build a sequence shape from scratch through the MCP.

## The tools

- `list_campaigns` → the account's campaigns (used to find a structural match to duplicate).
- `get_campaign_steps(campaignId)` → the steps in order: `stepId`, `type`, `channel`, `position`, `hasMessage`, `templateId`.
- `get_campaign_messages(campaignId)` → each step's current copy, including the editable `newHtml` source and the exact `<var name="..."/>` tokens valid in this account.
- `duplicate_campaign(campaignId)` → a full draft copy (new template IDs), not launched.
- `add_campaign_step_message(campaignId, stepId, newHtml, subjectNewHtml?)` → fill an **empty** step (`hasMessage: false`).
- `edit_campaign_message(campaignId, templateId, newHtml, subjectNewHtml?)` → rewrite a step that already has a message.

## The flow

### Step A — find or create the structure

1. **Look for a structural match.** Call `list_campaigns`; for a few plausible candidates call `get_campaign_steps` and compare to the sequence's shape (same channel mix, similar step count and order). Propose the closest and let the **user confirm** which to use. Do not auto-pick a wrong one.
2. **If the user picks one, duplicate it.** `duplicate_campaign(campaignId)` makes a draft copy. Work on the copy so the original is untouched.
3. **If nothing fits, ask the user to create the shape**, then fill it:
   > "I don't see a campaign with this structure. Create one in La Growth Machine matching this shape (channels + touches), then tell me its name and I'll fill in the copy."
   Once it exists it shows up in `list_campaigns` and you fill it like a duplicate.

### Step B — reconcile structure vs. sequence (do not skip)

Call `get_campaign_steps` on the target and compare its steps to the sequence:

- **1:1 match** (same channels, count, order) → map each message to its step and fill.
- **Mismatch** (step count or a channel differs) → say so and stop to decide. Offer: "your campaign has 3 steps but the sequence has 5. I can fit the 3 strongest touches, or you adjust the structure and I fill it after." Never silently cram messages into the wrong steps or drop touches without telling the user.

### Step C — fill each step (in newHtml)

For every step, write the matching message:

- Empty step (`hasMessage: false`) → `add_campaign_step_message`.
- Step with a message → `edit_campaign_message` (templateId = the step's `templateId`).
- The step's channel is fixed by the step. Email steps also need `subjectNewHtml`.

### Step D — confirm and report

- **Confirm before the first write** (it changes the user's workspace): "I'll fill the draft campaign with the approved copy. Go?"
- After filling, report one line per step (filled / skipped / error) and hand off per the SKILL.md output section: the campaign is a **draft, not launched**.
- **Warn about the inherited audience.** A duplicated campaign keeps the seed's audience (and often its name and `language` flag). Confirm this by checking `list_campaigns` for the new draft: its `audience` field still shows the seed's audience. The MCP cannot detach or swap it, so the handoff must tell the user, in bold, to remove that audience and attach the post's audience before launch, otherwise the sequence sends to the seed's leads. Renaming and the language flag are manual in the app too.

## The newHtml format (what the tools accept)

Messages are **not** plain text. Convert the copy to LGM `newHtml` before writing. The server **validates and rejects malformed newHtml**, so if a write is rejected, fix the format and retry rather than forcing it.

- Body is a sequence of block tags: `<p>...</p>`, `<ul><li>...</li></ul>`, `<h2>...</h2>`. Wrap all text in blocks.
- **One single line, no whitespace between top-level blocks** — `</p><p>`, never `</p> <p>`. Use `<p/>` for an empty spacer line.
- **Variables only as `<var name="firstname"/>`** (optional `default="there"`). Never `{{...}}`, `{...}`, `%...%` or `[...]`. In V1 use only standard scraped fields (`firstname`, `lastname`, `company`, `jobTitle`, etc.), not custom attributes.
- Inline tags: `<b> <i> <u> <s>`, `<br/>` (line break inside a paragraph), `<a href="https://..." track="true">text</a>`, `<spin>Hi|Hello</spin>` (text only), `<signature/>` (emails only).
- Escape `<` as `&lt;` and `&` as `&amp;`.
- **Email subject** (`subjectNewHtml`): a single `<p>...</p>` with text / `<var/>` / `<spin>` only, no lists, headings, images or signature.

Example email body (one line):
`<p>Hi <var name="firstname" default="there"/>,</p><p/><p>Your take on <var name="company"/>'s pipeline hit home. <a href="https://example.com/demo" track="true">Worth a look?</a></p><signature/>`

To get variable names exactly right, call `get_campaign_messages` on the duplicated campaign first: its `newHtml` shows the exact `<var name="..."/>` tokens valid in this account. Mirror them.

## Deeper copy generation

For the sequence copy itself (angles, CTA progression, per-channel rules), the base rules live in `references/copywriting-rules.md`. If the `multichannel-campaign-builder` skill is installed, defer copy generation to it for a sharper result, then convert its output to `newHtml` here.

## What the MCP cannot do

- **No launch.** There is no tool to start a campaign.
- **No audience binding.** There is no tool to attach the imported audience to the campaign.

So the skill fills a reviewed draft and hands off: the user attaches the audience and launches in the LGM app.
