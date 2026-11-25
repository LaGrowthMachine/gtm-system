---
name: icp-fit
description: "Shared sub-skill. Sorts leads against the target before any credit or writing is spent on them: match, needs review or no match, with a reason for each. Reads meaning, never patterns. Works on 10 leads or 1,000."
---

# Sort the leads against the target

A search returns neighbors and blanks along with the right people. This skill keeps the right ones, so that
enrichment and writing are only spent on leads worth contacting. Nobody is dropped silently: every lead gets a
bucket and a reason.

## How it judges

By reading and reasoning, never with patterns. The target lives as plain lists in the campaign file: titles that
count, neighboring titles that count, titles that do not, companies to exclude. The lists are a memory, not a
filter: a lead that fits none of them is judged on its own. When in doubt the agent asks.

Every answer the user gives goes back into the lists, so the same question is never asked twice and a routine
gets sharper run after run.

## Input

- The leads of `get-leads`, from any source (not enriched yet).
- The target and its lists: from the campaign or target file when one exists (`campaigns/<audience or campaign
  name>.md` in the folder the user works in); on a first run, build them from the brief and save them at the end.
  Job titles, seniority, functions and location. What excludes a lead.
- The number of matches the user asked for.

## Step 1. Say what the data can judge

Look at which fields are filled. A fresh LinkedIn or Sales Navigator import gives the name, the job title, the
company and the location, often not the industry. An audience of leads already enriched in La Growth Machine often
has the industry and a short bio. No source gives the company size.

Sort only on what the data supports. If the target has a criterion the data cannot judge (company size, industry),
say so once and do not pretend to have applied it.

## Step 2. Remove the exclusions first

Before judging fit, remove:

- the user's own company;
- the user's own colleagues: people at the user's company (from the context; ask once if it does not say);
- competitors named in the context (positioning or offer);
- existing customers, when the user gave a way to know them;
- leads already contacted in La Growth Machine. `get_audience_leads` does not say it (status "unknown"): when
  leads are added to an audience, `excludeContactedLeads: true` skips them, so do not look each lead up one by one
  unless the user asks for the count before.

These go to **no match** with the reason "excluded".

## Step 3. Sort into three buckets

| Bucket | When | Example for a target "GTM Engineer, Paris" |
|---|---|---|
| **Match** | The title, the seniority and the function fit the target. The location fits. | "Senior GTM Engineer", Paris |
| **Needs review** | The title is empty, unclear or a neighbor of the target. | No title. "RevOps". "Growth Ops". |
| **No match** | The function or the seniority is clearly outside the target. | "Marketing Execution Manager" |

Rules:

- **Read the meaning, not the keyword.** "Chief Happiness Officer" is not a C-level buyer. A title in another language
  can be a clear match.
- **A neighbor is a question for the user, once.** Ask whether neighboring titles count ("RevOps" for "GTM
  Engineer"), apply the answer to the whole batch, then write it into the lists of the campaign file.
- **An empty title is never a match.** It goes to review. It can be rescued by a profile enrichment, not by a guess.
- **Give one short reason per lead.**

## Step 4. Work the review bucket down

Resolve what you honestly can from the fields you have. Leave only the genuinely unclear leads for the user. A long
review list handed over untouched is not a result.

If the review bucket is large, the cause is usually upstream: the target is too vague or the search too wide. Say
which.

When the user's target leaves out a profile the context ranks as a priority (for example an individual contributor
the persona file names as a buyer), say it once and let the user decide.

## Step 5. Top up until the number is reached (a search only)

Skip this step when the source is a fixed list or an audience: there is nothing to top up from.

If there are fewer matches than requested:

1. Ask for more leads with the same target and a wider source (a wider search, another post), through `get-leads`.
2. Sort the new leads the same way. Skip the ones already seen.
3. Stop when the number is reached, after 3 rounds or when a round brings no new match. Then say how many matches
   exist and why the number was not reached.

## Step 6. Output

1. One line: leads seen, matches, needs review, no match.
2. The matches, as a table: name, title, company, reason.
3. The review leads the user must decide on.
4. What could not be judged from the data.

Only the matches go on to enrichment. In a routine, skip the questions: neighbors and empty titles are left out, and
the recap says how many.

## Any size of list

The method is the same for 10 leads or for 1,000. On a large list, work in batches of about 50: apply the lists
first, since they settle most leads, then judge the rest. Keep the questions for the end of the batch and ask them
together.

## Keeping the memory

- With a file system: update the lists in the campaign file at the end of the sort.
- Without one: give the user the updated lists as a block to save.
