# Handover file from a sourcing agent

> v1.0 (2026-11-18). The format the Buying Signal Detector bot of Apify uses to hand its search over to the Hiring
> Signal Agent. Any sourcing agent can use it.

The file names people. It lives on the machine of the agent that writes it. In this repository its only place is `local/`. **Never in Git.**

One JSON file per run, for example `handoffs/hiring-signal-2026-11-18.json`. A CSV does not fit: the full text of a
post is too long for a cell.

## The root

| Field | Meaning |
|---|---|
| `run_date` | The date of the run |
| `campaign_file` | The campaign file the search was made for |
| `source_bot` | The agent that wrote the file |
| `leads` | One entry per post kept |

## One entry

| Field | Type | Meaning |
|---|---|---|
| `company`, `domain`, `linkedin_company_url`, `industry` | string | The company |
| `headcount` | number | The headcount kept |
| `headcount_source` | string | Where the number comes from, with its date |
| `job_title` | string | The exact title |
| `job_url` | string | The post on the career page |
| `job_source` | string | `career_page`, `linkedin_jobs` or `both` |
| `linkedin_job_url` | string or null | The post on LinkedIn |
| `posted_date` | string | The date of the board, `YYYY-MM-DD` |
| `location` | string | The place and the work mode |
| `job_description` | string | The full text of the post. The receiving agent scores and writes from it. |
| `reporting_line` | string or null | The exact sentence of the post, otherwise null |
| `reports_to_team` | string | The team or the role the hire reports to |
| `contact_first_name`, `contact_last_name`, `contact_title`, `contact_linkedin` | string | The proposed contact |
| `contact_confidence` | string | `from_posting` (read in the post), `size_rule` (deduced from the company size), `sales_nav` (found by a search) or `guess` |
| `contact_reason` | string | Why this person |
| `already_in_lgm`, `already_contacted` | boolean | From `search_lead`, read only |
| `involved_campaigns` | array | The campaigns the lead is in |
| `lgm_lead_id` | string or null | The lead id, so its custom attributes are not overwritten by a duplicate |
| `recruiter_name`, `recruiter_linkedin` | string or null | The recruiter the post shows. For information: we never write to HR. |
| `source_note` | string | Context and limits |

## What the receiving agent does with it

- It scores every post itself, from `job_description`. The sourcer does not score.
- It keeps the contact when `contact_confidence` is `from_posting`. For any other value it runs `find-contacts`.
- It checks the headcount when the source is not the LinkedIn page of the company.
- It leaves out a lead whose `already_contacted` is true. Also a lead that is in another campaign.

## Example

Every value is made up.

```json
{
  "company": "Acme Robotics",
  "domain": "acme-robotics.example",
  "linkedin_company_url": "https://www.linkedin.com/company/acme-robotics-example",
  "industry": "Software Development",
  "headcount": 42,
  "headcount_source": "LinkedIn company page, 42 employees, 2026-11-18",
  "job_title": "Head of Growth",
  "job_url": "https://jobs.ashbyhq.com/acme-robotics-example/00000000-0000-0000-0000-000000000000",
  "job_source": "career_page",
  "linkedin_job_url": null,
  "posted_date": "2026-11-02",
  "location": "San Francisco, CA (on-site)",
  "job_description": "ABOUT THE ROLE: ... WHAT YOU'LL DO: Run outbound ...",
  "reporting_line": null,
  "reports_to_team": "CEO / founders",
  "contact_first_name": "Julien",
  "contact_last_name": "Moreau",
  "contact_title": "Head of Sales",
  "contact_linkedin": "https://www.linkedin.com/in/julien-moreau-example",
  "contact_confidence": "size_rule",
  "contact_reason": "No manager named in the post. 42 people: the rule by size points to the head of sales.",
  "already_in_lgm": false,
  "already_contacted": false,
  "involved_campaigns": [],
  "lgm_lead_id": null,
  "recruiter_name": null,
  "recruiter_linkedin": null,
  "source_note": "Board date 2026-11-02. search_lead: not found."
}
```
