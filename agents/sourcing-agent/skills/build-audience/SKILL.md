---
name: build-audience
description: "Sub-skill of sourcing-agent. Puts the leads kept by the sort into a La Growth Machine audience, each with its reason, reads it back and says what is ready. Contacts nobody unless the user chose to feed a running campaign and said yes."
---

# Build the audience

The last step of the Sourcing Agent. The leads kept by `icp-fit` land in one audience, ready for a campaign. Nobody
is contacted by this step, unless the user chose to feed a running campaign.

## Input

- The leads kept (bucket "match", plus the "needs review" leads the user accepted), each with its `leadId` when it is
  already in La Growth Machine, its LinkedIn URL or email otherwise, and its reason.
- Where they go, decided at Step 0 of `{SKILL_BASE}/skills/get-leads`: a new audience, or the audience of an existing campaign.

## Steps

1. **The name.**
   - New audience: propose a name and confirm it with the user (the `create_lead` description gives the recommended
     format). Check with `list_audiences` that it does not exist yet: an existing audience would receive the leads.
     When the leads came from an import, this audience is not the import's working audience: the working audience
     keeps everyone, this one keeps the matches only.
   - Existing campaign: copy the audience name from `get_campaign`, never type it. If the campaign runs, say "these N
     leads will receive the first message right away" and go on only on a clear yes. If the campaign writes a message
     per lead (its steps hold `customAttribute` variables), stop: the leads need their messages first, that is the
     Outreach Agent's job. Hand them over.
2. **Check each lead** before the call: it has a `leadId`, a LinkedIn URL or an email. A lead with none of them
   cannot be added: list it.
3. **Push one lead first**, then find the new audience once with `list_audiences` (search its name in the result,
   it is large) to get its id; from then on use `get_audience` with that id. The first `create_lead` with a new name
   creates the audience.
4. **Push the others** with `create_lead`, one per call: the `leadId` when there is one (without it, a lead that
   exists is treated as a duplicate), otherwise the identifier, the first name, the last name, the company, the job
   title, and `audience` with the exact name. With a `leadId`, the answer is always "Lead is a duplicate & has been
   merged": that is the normal success. Add `excludeContactedLeads: true` when the user does not want leads already
   contacted. Never write the `note` field: it replaces the note the team reads in the app. On an error: one
   retry, then note it and go on. Three errors in a row: stop.
5. **Read it back** with `get_audience_leads` (100 per page, `skip`). Every lead pushed must be there. A missing lead
   was skipped (already contacted) or failed: say which.

## Output

1. One line: the audience name, its size, how many leads were kept, set aside, to review, not added (and why).
2. The kept leads as a table: name, title, company, the reason they match.
3. The set-aside leads in one short list with the reason, grouped (for example "12 · not a decision maker").
4. The next step: "Launch a campaign on this audience, or hand it to Outreach Agent to write a message for each
   lead."

The reasons stay in the conversation: they are not written into La Growth Machine.

## Never

- Never call `launch_campaign`, `resume_campaign`, `remove_lead_from_audience` or `set_campaign_audience`.
- Never write lead data into a shared file.
