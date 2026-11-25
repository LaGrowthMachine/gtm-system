---
name: get-leads
description: "Shared sub-skill. Turns any source of leads into a list the next steps can read: a La Growth Machine audience, a LinkedIn or Sales Navigator search, the people who liked or commented on a LinkedIn post, the attendees of a LinkedIn event, or a file (CSV, Clay export, webinar list). Asks first whether the leads feed an existing campaign or a new one."
---

# Get the leads

The user brings leads from somewhere. This step makes them one list, with the same fields whatever the source, so
that sorting and writing work the same way.

## Step 0. Where the leads go

Ask once, unless the request already says it:

| The user wants | Where the leads go |
|---|---|
| **A new campaign** | A new audience, named with the user. It becomes the audience of the new campaign at the push. |
| **To feed an existing campaign** | The audience of that campaign (copy its name from `get_campaign`, never type it). |

Feeding an existing campaign, two ways:
- **Through the sort** (the default, and the only way when the campaign writes a message per lead): import into a
  working audience first, sort and write, then the agent's push step adds the kept leads to the campaign's audience.
- **Straight into its audience** (only when the user wants every lead of the source and the campaign has no
  per-lead message): import directly with the campaign's audience name. If the campaign is running, say first: "these
  leads will receive the first message as soon as they are imported". Go on only on a clear yes.

## Step 1. Name the source

| The user gives | Source |
|---|---|
| An audience name, "my audience X", "the leads already in LGM" | **LGM audience** |
| A URL starting with `linkedin.com/sales/search/` or `linkedin.com/search/results/people` | **LinkedIn search** |
| A URL of a LinkedIn post (`linkedin.com/posts/...`, `linkedin.com/feed/update/...`) | **Post engagers** |
| A URL of a LinkedIn event (`linkedin.com/events/...`) | **Event attendees** |
| A file: CSV, Excel, a Clay or Apollo export, a webinar or form export | **File** |
| A list pasted in the chat | **File** (same rules) |

No source yet → ask for one, in one question. A target with no list ("find me Heads of Sales in SaaS") is a search
to build first: when this pack has `{SKILL_BASE}/skills/sales-nav-search-builder`, build it with the user; otherwise say that
another La Growth Machine agent, Sourcing Agent, does it.

## Step 2. Read or import

### LGM audience

`list_audiences` → find the audience by name (the list is long: search its name in the full text). Then
`get_audience_leads` with `skip` (100 per page, `skip: 100` for page 2) and the fields the next steps need:
`include: ["location", "industry", "shortBio", "companyUrl", "signal"]`. Add `proEmail` and `linkedinUrl` only when a
later step needs them (choosing channels, writing to someone outside La Growth Machine): the leads keep their
`leadId`, which is enough to add them to another audience.
Fire the pages after the first one together. Read `total` on page 1.

If the audience is used by a running campaign, say so: its leads are already being contacted. No tool lists the
campaigns of an audience: compare its id with `audience.id` in `list_campaigns {status:"RUNNING"}`, paged with `skip`
(25 per page) until every running campaign is read.

`list_audiences` returns every audience of the workspace (80 KB or more): the result can exceed what the tool shows
and land in a file. Search the name in it (in Claude Code, `grep` the saved file); never read it all. Once you have
an audience id, use `get_audience` with it rather than `list_audiences` again.

### LinkedIn search, post engagers, event attendees

These go through `create_audience_from_linkedin_url`, into the audience chosen at Step 0. Importing into a new
audience that no campaign uses contacts nobody.

1. The identity: the sender identity of the scope (`list_identities`). For an event, it must be registered to the
   event on LinkedIn, or the import returns nobody. For a Sales Navigator URL, it needs Sales Navigator
   (`isSalesNav`).
2. The name: for a new audience, propose one and confirm it with the user (the tool's description gives the
   recommended format), and check it does not exist yet: an existing audience would receive the leads. For an
   existing campaign fed straight, the exact name of its audience.
3. For a post: ask likers, commenters or both (`linkedinPostCategory`: `like`, `comment`; both = two calls into the
   same audience).
4. Call it with `excludeContactedLeads: true` and **without** `autoImport`.
5. The import runs in the background. It returns no id: find the audience with `list_audiences` and check `size`
   and `importStatus` with `get_audience`. Expect a few minutes to 20 minutes. Tell the user, and read the leads
   when the size stops moving.
6. A search URL whose values are encoded once can return nobody with no error. If the audience stays empty after
   10 minutes, say so and check the URL with the user (the values inside a Sales Navigator query must be encoded
   twice, `urn%253Ali%253A...`).

Imports may use La Growth Machine credits depending on the plan: say it before the first import.

### File

Read the file. Map its columns to: first name, last name, job title, company, company website, LinkedIn URL,
email, location, industry, and **the signal** (what the file says about why this person is on it: attended the
webinar, downloaded the guide, a Clay column with a trigger). Keep every other column that says something about the
lead, under its own name.

- A row without a LinkedIn URL and without an email cannot be pushed later. Keep it, mark it.
- Never write the file's content anywhere else. The leads reach La Growth Machine only at the push.

## Step 3. Check against La Growth Machine

For leads that came from a file, look each one up with `search_lead` (LinkedIn URL first, email otherwise) before
anything is written for them. Note for each: already in the workspace (with its `leadId`), already in a campaign,
already contacted. Leads from an LGM audience or an import already carry their `leadId`.

On more than 100 leads, look up the ones kept by the sort only (`icp-fit` comes first).

## Output

One line: the source, the number of leads read, how many with a LinkedIn URL, with an email, with both, already
contacted. Then the list, one row per lead with the normalised fields, for the next step. The list stays in the
conversation (or in a working file the user asked for), never in a shared file.
