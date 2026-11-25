---
name: build-campaign
description: "Shared sub-skill. Picks the structure of the campaign in La Growth Machine (the user's own campaigns first, the catalog otherwise), duplicates it, fills its steps with the approved outline and writes the campaign file. Never launches."
---

# Build the campaign

The copy comes first. This skill takes the approved outline, finds the structure that fits it best, adapts where
needed with the human, then fills it. The campaign always stays a draft.

## Three ways to get the structure, in this order

1. **Create it.** If the MCP offers a tool that creates a campaign or adds steps (look in your tool list for a name
   like `create_campaign` or `add_campaign_step`), build the structure from the outline with it.
2. **Duplicate it.** Otherwise (the case today): the MCP can duplicate a campaign and rewrite every message, but it
   cannot add or remove a step, change a delay or a condition. The shape comes from a campaign that exists: one of
   the user's own campaigns or a catalog template (Part 1).
3. **Give the exact structure.** When nothing fits and no tool creates one: write the structure for the user to set
   up in the app (each step with its channel, its delay in days, its condition such as "if not connected" or "if
   no reply", and the message it holds), then fill it once they give its name.

## Part 1. Choose the structure

Input: the approved outline (its channels, its number of touches, their order).

1. **Look at the user's own campaigns first.** Call `list_campaigns`. For the plausible candidates, call
   `get_campaign_steps` and compare: same channels, a step count and an order close to the outline. Prefer a campaign
   whose messages already use custom attributes: it was built for per-lead copy.
2. **Propose the 1 to 3 closest**, each with its shape in one line and what differs from the outline. Let the user
   confirm. Never pick alone.
3. **If the user has no campaign that fits**, fall back on the catalog (`list_public_campaigns`):

   | Channel mix | Catalog template |
   |---|---|
   | LinkedIn + email | "Linkedin > Email \| 3 follow-ups" |
   | Email only | "Email Only - 4 Follow-ups" |
   | LinkedIn only | "LinkedIn Only - 3 Follow-ups" |

4. **If nothing fits and the user wants their own shape**, ask them to create it in the app (channels and touches),
   then give its name.
5. **Duplicate** the chosen campaign with `duplicate_campaign` and work on the copy. A catalog template can only be
   read after it is duplicated.
6. **Read the shape** of the copy with `get_campaign_steps`: each step with its channel and its position.
7. **Check what came with the copy** with `get_campaign`: identity, language, CRM sync, audience.
   - A copy of one of the user's campaigns keeps the audience, identity, language and CRM sync of its source.
   - A copy of a **catalog template** has **no audience** (`get_campaign` then shows no audience field at all), may
     come with a disconnected identity, the language French and the CRM sync on. The template itself cannot be read
     (`get_campaign` returns 404 on its id).
   Set the identity now (`set_campaign_identity`, with the human's agreement). The audience is attached at the push.
   The language and the CRM sync cannot be set by the MCP: list them for the human to check in the app.
8. **The connection request.** `get_campaign_steps` lists the message steps only. The LinkedIn invitation step is
   not visible and no tool writes its note: say whether the structure sends one, and that a note is set in the app.

A new user starts from a catalog template. A user with their own campaigns starts from the closest one.

## Part 2. Adapt and fill

1. **Reconcile.** Compare the steps of the copy with the outline. If they match one to one, go on. If they do not,
   say what differs and offer the options: fit the strongest touches into the steps that exist, ask
   the agent's writing step for the missing messages (`write-sequence`, or the outline for a hiring campaign) or let the user change the structure in the app. Never cram messages
   into the wrong steps. Never drop a touch without saying it.
2. **Confirm before the first write**: it changes the user's workspace.
3. **Fill each step**, in the `newHtml` format described in `references/lgm-campaign-create.md`:
   - an empty step: `add_campaign_step_message`;
   - a step that has a message: `edit_campaign_message`.
4. **Fill each step according to the mode** of the outline:
   - **Personalised**: the step holds only its attribute, `<p><var name="customAttribute2"/></p>`. Give it the
     fallback version as default: `<var name="customAttribute2" default="the fallback message"/>` (accepted by the
     MCP, checked 2026-11-25), so a lead with no value still gets a full message. An email whose subject changes per
     lead gets its subject attribute the same way in `subjectNewHtml`.
   - **Template**: the final text of the outline, with `<var name="firstname"/>` as the only variable.
   When the copy already has messages, mirror the variable names it uses (`get_campaign_messages`). A catalog copy
   has none: use the names above.
5. **Rename** the copy with the campaign name (`rename_campaign`).
6. **Write the campaign file** from `references/campaign-file-template.md`: objective, target, signal, structure
   used, campaign id, audience name, the mode, the outline and the attribute table. When the client can write files, save it as
   `campaigns/<campaign-slug>.md` in the user's project folder; otherwise give it as one block for the user to keep.
   It holds no lead data.
7. **Report** one line per step (filled, skipped, error). End with: the campaign is a draft, not launched.

## Rules

- Never launch or resume a campaign.
- Voice steps and call steps are left as they are: their content is recorded in the app.
- If a write is rejected, fix the format and retry. Do not force it.

## To verify on a real account

- The real steps of the three catalog templates.
- How a message written with a custom attribute variable renders for a lead (the variable itself is accepted).
