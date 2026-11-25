# Signals

A signal is the reason to write to someone now. The signal chooses where the leads come from. A search by job title
alone carries no signal: it is the means to find the right people once the signal has pointed at a company or a
group.

A signal can be cold. Someone who just changed company may never have heard of us: the lead is cold, the timing is
not.

## How Brice scores an account

Add the strength of every positive signal seen on the same account in the last 30 days. Subtract the negative ones.

| Score | Priority | What to do |
|---|---|---|
| 15 or more | Hot | Same day. A human writes or calls, personalized on the strongest signal. |
| 8 to 14 | Warm | Within 48 hours. Enroll in the sequence of the strongest signal. |
| 4 to 7 | Lukewarm | This week. A light touch, then wait for a second signal. |
| Under 4 | Cold | No action. Keep scoring. |
| Any negative signal | Hold | Check before anything goes out. |

## The signals we can act on from outside

Signals about people who are not customers yet, with a source we can reach. The number and the strength are those of
the library. Signals read from our own product, CRM or emails are in the library and not repeated here.

| # | Signal | Strength | Act within | Write to | Where the leads come from | State |
|---|---|---|---|---|---|---|
| 1 | A past customer or champion changed company | 9 | 30 days in the role | The person, from someone they know | Customer list matched against a Sales Navigator search | not explored |
| 3, 8 | A person or a company visited the website | 9, 8 | 24 to 48 hours | The visitor | A visitor identification tool (RB2B) | running, in another campaign |
| 14 | A job posting mentions our category or a competitor | 7 | 2 weeks | The hiring manager, never HR | A job scraper on Apify, then the contacts of the company | **to test first** |
| 24 | Comments on a post about the pain we solve | 7 | 48 hours | The commenter | The post URL, imported as an audience | not explored |
| 26 | Engaged with a competitor's content | 7 | 48 hours | The engager | The competitor's post URL, imported as an audience | not explored |
| 29 | Liked or commented our own content | 7 | 24 to 48 hours | The engager | Our post URL, imported as an audience | running, in other campaigns |
| 30 | Posted a negative review about a competitor | 7 | 1 week | The reviewer | A review scraper on Apify | not explored |
| 34 | A lead changed job | 6 | 30 days in the role | The person | Sales Navigator, "changed jobs in the last 90 days" | not explored |
| 35 | New hires in the department | 6 | 2 weeks | The head of the department | Sales Navigator, department headcount growth | not explored |
| 43 | Uses a competitor's product | 6 | No urgency | The owner of the tool | Technology detected on the company website (the actor's company scorer), job ads | not explored |
| 46 | Raised funding | 5 | 30 to 60 days after | The head of sales or growth | A funding database or news alerts | not explored |
| 57 | Attended a LinkedIn event | 5 | Before the event or within days | The attendee | The event page | to test |
| 63 | Talks about the pain we solve on LinkedIn | 5 | 48 hours | The author | A keyword search on posts | not explored |
| 64 | Uses a tool that works well with ours | 5 | No urgency | The owner of the tool | Technology detected on the company website | not explored |
| 77 | Surge in hiring | 3 | 1 month | Context only | A count of open jobs | context, not a trigger |

Negative signals to check before writing: a surge in layoffs (pause 60 to 90 days), negative press (pause 30 days).

## How to use a signal

1. The campaign file names its signal.
2. `find-leads` takes the source of that signal.
3. The opening of the message starts from the signal, when the lead made it public (a job post, a comment, a post).
   A signal we tracked (a visit, an open) sets the timing and is not written in the message.
4. Once a signal has been run for real, write down how in this folder: one short file per signal, with the source,
   the steps and what was learned.

## Signal 14, job postings: the first one to test

Why this one: strength 7 in the library. The lead made it public, so the message can cite it. It is also the
signal behind the best cold campaign of the copy analysis (30% of replies on companies hiring).

The chain to test, all on Apify then La Growth Machine:

1. A job scraper finds the companies that are hiring for the roles we look for (for example sales development,
   revenue operations, GTM engineering). Some scrapers filter on company size and industry.
2. For each company, find the hiring manager with the lead finder actor (`icpCompany` plus the job title).
3. Sort, enrich, push, as for any other source.

### First test (2026-11-17): "GTM Engineer", San Francisco Bay Area, last 30 days

Step 1 works, through the Apify MCP, with no script and no key. Actor `cheap_scraper/linkedin-job-scraper`, 10 job
posts in about 11 seconds.

- **What each post carries**: the job title, the full job description, the date, the company name, its website, its
  industry and its headcount. Enough to cite the post and to filter on company size.
- **Relevance**: 10 posts, 8 companies. 4 posts on the exact role (GTM Engineer, Head of GTM Engineering), 2 on a
  neighbor (a RevOps lead, the same post in two cities), 4 off target (a consulting firm, a solution engineer, a
  marketing engineer). The posts have to be sorted like leads.
- **The hiring manager is not in the post**: the poster field came back empty on all 10.

Step 2 does not work as tested. The lead finder actor, searching inside one of the companies for three sales and
growth titles, returned 6 people: 4 with no job title, 1 from another company, 1 network engineer. It cannot be
trusted to find the hiring manager this way.

What the post says about who to write to, on the 5 relevant posts: the reporting line is stated in 1 ("you report
to the Head of Revenue"), 3 others name the team the role works with, none describes the interview process. 3 of
the 5 name the tools in place (Clay, HubSpot, Salesforce, Gong). The agent reads the post first: the reporting line
when it is there, the team otherwise, the tools for the angle.

To try next for step 2:

- The actor's company mode (`run_actor.py companies`): it takes company websites and returns contacts by
  department. Two runs failed on a budget rule, not on the search: the actor splits its spend cap across 4 steps
  and the contact step needs $0.50, so the cap must be 2 dollars at least. Not tested beyond that.
- A Sales Navigator search on the company and the title, imported with the La Growth Machine MCP. Not tested.

For a routine, the job scraper filters on the publication date (last 24 hours, last week). Each run then only sees
the new posts, which settles the question of finding new leads every day.

The opening line of the library, to adapt: "Saw you're hiring a [job title] to work on [mission]. While you look for
that person, here's how [similar company] covered the gap."
