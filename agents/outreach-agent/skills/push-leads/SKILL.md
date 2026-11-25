---
name: push-leads
description: "Shared sub-skill. Pushes the leads and their custom attributes into the audience of the campaign, checks the campaign first, skips the leads already there, then reads the audience back. Never launches."
---

# Push the leads

Send leads into the audience of a campaign. This is the last step: a lead only gets here once it is sorted, enriched
and, when the campaign needs it, written for.

## Input

- The leads to push: for each, a LinkedIn URL or an email, the first name, the last name, the company, the job
  title, plus the custom attributes if the campaign uses them.
- The campaign file: the campaign id, the audience name, the number of leads per run, whether a
  routine is approved and whether pushing is allowed while the campaign runs.

## Steps

1. **Read the campaign** with `get_campaign`: its status, the name and the size of its audience. If the audience name
   differs from the campaign file, stop. Never type an audience name: copy it from `get_campaign`. A name that does
   not exist creates a new audience, with no warning.
   One exception: a new campaign whose file says its audience is "not attached yet". See "A new campaign made from
   a copy" below.
2. **Decide on the status.**
   - Not launched yet: go on.
   - Running, with a human in the session: say "these N leads will receive the first message right away" and ask.
   - Running, in a routine: go on only if the campaign file says the routine is approved and that pushing while the
     campaign runs is allowed. Otherwise stop.
3. **Check each lead** before any call: it has a LinkedIn URL or an email. Every custom attribute the campaign
   declares is there and not empty. A lead with a missing attribute is not pushed.
4. **Read the audience once** with `get_audience_leads` and note who is already in it. Then look each lead up with
   `search_lead` (LinkedIn URL first, email otherwise).
   - Already in this audience: nothing to do, skip.
   - Exists in the workspace and is involved in another campaign: leave it out and say so. Its custom attributes
     would be overwritten.
   - Exists in the workspace with no campaign: push **with its `leadId`**. Without it the lead is treated as a
     duplicate and its custom attributes are not written.
   - Not found: push as a new lead.
5. **Stop at the number of leads per run** from the campaign file. Say how many are left.
6. **Push one lead first** on the first push of a campaign, read it back (step 8), then push the others.
7. **Push** with `create_lead`, one lead per call: the `leadId` or the identifier, the name, the job title, the
   company, every custom attribute, `audience` with the name read at step 1 and `excludeContactedLeads: true`. On an error: one retry, then
   note it and go to the next lead. Three failures in a row: stop.
8. **Read the audience back** with `get_audience_leads` (`include`: `linkedinUrl`, `proEmail`, `customAttributes`). Every
   lead pushed must be there with its values and its email when it has one. A lead that is missing was either already contacted or failed: say which.
9. **Recap**: leads received, pushed, skipped with the reason, failed. End with: nothing was launched.

## A new campaign made from a copy

A copy of a user's campaign still carries the audience of its source, so `get_campaign` shows the wrong one. A copy of
a catalog template has no audience at all. The MCP cannot create an
empty audience. So, for a campaign whose file says its audience is "not attached yet":

1. Take the audience name written in the campaign file, exactly.
2. Push the first lead with that name. The push creates the audience.
3. Read the new audience back (step 8).
4. Ask the human, in plain words: "attach the audience X to the campaign Y?". On a clear yes, the agent calls
   `set_campaign_audience` on the copy. Never on the source. The campaign must be READY.
5. Read `get_campaign` on the copy (it shows the new audience and its size) and on the source when the source is one
   of the user's campaigns (unchanged). A catalog template cannot be read: skip it.
6. Push the other leads, then write in the campaign file that the audience is attached, with its id.

Until step 5 is done the copy must not be launched: it would write to the leads of its source.

## If it stops halfway

Run the skill again. Step 4 skips the leads that are already in the audience, so nothing is pushed twice.

## Never

- Never call `launch_campaign`, `resume_campaign` or `remove_lead_from_audience`. Never call `set_campaign_audience`
  outside the section "A new campaign made from a copy": once, on the copy, with the human's clear yes.
- Never write the `note` of a lead: it replaces the note the team reads in the app.
- Never write a lead name, an email or a LinkedIn URL into a shared file.

## Facts checked on a real account

See `{SKILL_BASE}/skills/push-leads/references/lgm-mcp-facts.md`.
