---
name: find-leads
description: "Finds the people who match a target and enriches them, with the Apify actor La Growth Machine Lead Finder & Enrichment."
---

# Find and enrich leads

## Purpose

Turn a target into a list of leads, in two moments: search first, then enrich only the leads that `icp-fit` kept.
This skill does not push anything into La Growth Machine: `push-leads` does, once the messages are written.

## Start from the signal

Read `signals.md` in this folder. The signal named in the campaign file chooses the source of the leads. A search
by job title alone carries no signal: use it as the means to find people once a signal has pointed at a company or
a group.

## Input

A target: job titles, seniority, job functions and location, plus a maximum number of leads.

## Output

One row per lead: first name, last name, company, LinkedIn URL, professional email when found, plus the enrichment
outcome. Kept in the conversation, never written to the repository.

## Tool

The Apify actor `sameh.jarour/lgm-lead-enrichment`, called with the script `{SKILL_BASE}/tools/apify/lgm-lead-enrichment/run_actor.py`. See
`{SKILL_BASE}/tools/apify/lgm-lead-enrichment/README.md` for the options and the keys. If the script says the keys are missing, tell the user where
to put them and offer the Sales Navigator variant.

## Two ways to get an email

| Way | When | What it does | Cost |
|---|---|---|---|
| `enrich_lead` of the La Growth Machine MCP | The lead already exists in La Growth Machine, for example after a Sales Navigator import | Shows the cost first and asks for a confirmation. Writes the email on the lead. The status can stay "pending" while the email is already readable with `search_lead`. | 5 credits per lead |
| The Apify actor, through `run_actor.py enrich` | The leads are not in La Growth Machine yet | Returns the email in its output. It writes nothing into La Growth Machine: `push-leads` sends the email with the lead. | 5 credits per lead, a fraction of a cent on Apify |

Both were run on 2 leads on 2026-11-17 and 2026-11-18: 2 emails found each time. Before a launch, read the email
status of every lead: an email still in validation is not a valid email yet.

## Rules

- **Search** (`run_actor.py search`): no credit spent. Ask for more leads than needed, the sort removes some. People
  already contacted in La Growth Machine are left out by default.
- **A file of leads only ever lives in `local/`**, which Git ignores. Never anywhere else in the repository.
- **Enrich** (`run_actor.py enrich`): only the matches from `icp-fit`. Announce the cost first, 5 La Growth Machine
  credits per lead, charged whether or not an email is found. Test on 3 to 5 leads before the full batch.
- Set a cap on leads and on credits for every run.
- The actor must not write into the audience itself. The push happens later, with the messages.

## Variant

A LinkedIn Sales Navigator search imported with the La Growth Machine MCP (`create_audience_from_linkedin_url`), for
users who do not use the actor.

## To verify

- Done on 2026-11-17: an enrichment run on 2 leads (first name, last name, company, website, LinkedIn URL) returned 2
  valid professional emails in 12 seconds, for 10 credits. The actor did not write into La Growth Machine: the email
  is in the output only, `push-leads` has to send it with the lead.
- Still to see: the share of emails found on a larger batch. Also a lead whose last name is an initial.
- Where the La Growth Machine API key lives (see `{SKILL_BASE}/tools/apify/lgm-lead-enrichment/README.md`).
- How to express company size and industry: the actor's target search has no filter for them.
