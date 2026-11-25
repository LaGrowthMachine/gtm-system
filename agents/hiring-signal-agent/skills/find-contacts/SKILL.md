---
name: find-contacts
description: "Finds the right person to write to inside a given company from what a signal says (for a job post, who the role reports to) and keeps the best match with a reason. Use after a signal points at a company. Not for searching people by job title across the market → find-leads."
---

# Find the right person in a company

A signal points at a company. This skill finds who to write to there. It reasons: it reads what the signal says,
looks with the tools it has, then judges the people found. When in doubt it asks.

## Input

For each company: its name, its website, its LinkedIn company id when known. Also what the signal says about who to
reach. For a job post: the role being hired, who it reports to or works with, the team.

## Step 1. Decide who to look for

Write to the person who owns the problem, never to HR.

| What the post says | Look for |
|---|---|
| The reporting line ("reports to the Head of Revenue", "you'll report to our Head of Growth") | That exact role. It wins over the rule by size. |
| The post is written in the first person by the founder. Also a post that says the hire works directly with the founders. | The founder. Name the person the rule by size would have given in the routing question of the last message. |
| Only the team (marketing, sales, operations) | The head of that team |
| Nothing | The role one level above the job posted, in the function it belongs to |

**By company size**

| Size | Who to write to | Also note |
|---|---|---|
| Under 10 people | The founder or the CEO, almost always. | |
| 10 to 30 | It depends on what the search finds. A full-time person who runs sales, revenue, growth or go-to-market (a head of sales, a head of growth, a founding GTM): that person, before the CEO. Nobody else found: the founder or the CEO. | Read the profile of the person before keeping them (step 3). |
| 30 to 200 | The role the post names. Otherwise the head of the team the role serves (sales, revenue, growth). Past 30 people the CEO rarely handles this: do not fall back on the CEO. | When the role the post names is not found, the campaign can ask in its last message whether it should go to that role. |
| Over about 200 (left out of our own campaigns for now) | Look inside the unit the post is for (a region, a segment, a product line). The head of that department first, then the head of the function there (marketing, revenue operations). | Up to two people, when both own a part of the problem. |

**When the title the post names is not found**, do not fall back at once. Titles differ from one company to the
next: a "CRO" can be a chief commercial officer, a president or a head of revenue. Run one wider search on the
senior titles of the company (chief, head, VP, director), read the list, then decide.

## Step 2. Look, with the tools available

**When the contact is already confirmed** (the post names the role, the person was found and their profile read),
do not import a search for one person. Create them with `create_lead` in the working audience: the LinkedIn URL, the
name, the job title, the company. No custom attribute and no note. It gives the lead id the enrichment and the push
need. A Sales Navigator import for one known person brings unrelated profiles into the working audience. Like the
import, this is not a push: the working audience belongs to no campaign.

Otherwise try the tools in this order and stop when one gives a usable answer.

1. **A Sales Navigator search** on the company and the titles, imported as an audience with the La Growth Machine MCP
   (`create_audience_from_linkedin_url`). **This import is allowed and expected.** It creates the people as leads
   in a working audience that no campaign uses, so nobody receives anything. It is not a push. Do not skip it
   because a brief says "do not push" or "do not create leads in the campaign": only skip it when the human says
   not to import. The tools below cost more and find less.

   How to build the search URL, so the import returns people:

   ```
   https://www.linkedin.com/sales/search/people?query=(filters%3AList((type%3ACURRENT_COMPANY%2Cvalues%3AList((id%3Aurn%253Ali%253Aorganization%253A<company id>%2Ctext%3A<company name>%2CselectionType%3AINCLUDED%2Cparent%3A(id%3A0))))%2C(type%3ACURRENT_TITLE%2Cvalues%3AList((text%3A<titles>%2CselectionType%3AINCLUDED)))))&viewAllFilters=true
   ```

   - The values inside are **encoded twice**: `urn:li:organization:123` becomes `urn%253Ali%253Aorganization%253A123`,
     a space becomes `%2520`. Encoded once, the import returns nobody and gives no error.
   - `<titles>` is one boolean text, also encoded twice: `("VP Sales" OR "Head of Sales" OR CRO)`.
   - Several companies fit in one search: repeat the company block inside `values%3AList(...)`, separated by `%2C`.
   - **Filter by title, not by seniority.** Keep the titles narrow: a word like "Head" or "Marketing" alone brings
     dozens of people.
   - **Check the headcount before importing.** A company with a creator or ambassador program can return a hundred
     people for one search (93 for one company on 2026-11-18). Do not import for a company that looks above the
     size of the campaign.
   - An import into an audience that exists adds to it. It takes 6 to 20 minutes to show. It needs an identity with Sales Navigator (`list_identities`) and the
   LinkedIn company id, which the job post gives. Never import into the audience of a campaign: use a working
   audience, named after the campaign. The import takes a few minutes: check the size with `get_audience`, then read
   the people with `get_audience_leads`. It returns exact job titles and LinkedIn URLs.
2. **An Apify employee search**, when no identity has Sales Navigator: the actor
   `memo23/linkedin-company-employees-scraper`, called through the Apify MCP with the company **names** and the
   target titles. Keep only the rows whose title matched. It returns the LinkedIn profile URL.
3. **The company mode of the Apify lead finder** (`{SKILL_BASE}/tools/apify/lgm-lead-enrichment/run_actor.py companies`). It takes
   company websites and returns people by department, with their job title and often an email. It does not return
   their LinkedIn URL. Give it a spend cap of 2 dollars at least.
4. **Nothing usable**: say so for this company and leave it out. Do not guess a name.

Do not use the search by job title of `find-leads` for this. Tested inside one company, it returned people with no
job title and people from other companies.

## Step 3. Rank the people found

For each company, judge every person against what step 1 asked for:

- **Best match**: the role named by the post. Otherwise the head of the team.
- **Possible**: the right function, another level (a manager when a head was asked for).
- **No**: another function. Also anyone with no job title.

**Read the profile when the title does not say enough.** "GTM", "Founding GTM", "Advisor" or "Consultant" can be a
full-time head of sales, a sales rep or a freelancer who works for several companies. Before keeping such a person,
read their current positions with the Apify actor `harvestapi/linkedin-profile-scraper` (Apify MCP, `profileIds` set
to the last part of the LinkedIn URL the import returned). Ask only for the fields `headline`, `currentPosition` and
`experience`. On a free Apify plan the actor can refuse the run ("free user item limit exceeded", seen on
2026-11-18): then confirm the person with public web results and say so.

| What the profile shows | What to do |
|---|---|
| One current position, full-time, in the company | Keep. The description of the position often says what the title hides ("1st GTM hire"). |
| Several current positions. Also "Freelance", "Self-employed" or "Fractional". | A freelancer. Do not write to them as the owner of the problem: go back to the rule by size. |
| A past role close to the job posted | Worth noting: this person has done the job and will understand the offer at once. |

A contact kept in an earlier run is checked again against the new import: people leave. In the second run one head of
sales was no longer in the company.

Keep one person per company. Two at most when the post points at two teams or when the company is large. In a team
of a few people, write to one first and keep the second in reserve: two colleagues who get the same email talk. Give one line of reason for each.
Keep the questions for the end and ask them together. Write the answers into the target lists of the campaign file.

## Output

One row per company: the person kept, the job title, why this one, the email or the LinkedIn URL when known, and
what is still missing to reach them. These rows stay in the conversation or in a file under `local/`. Never
elsewhere in the repository.

## What the tests showed (2026-11-17)

Five companies that were hiring a GTM engineer or a RevOps lead.

| Tool | Result |
|---|---|
| Sales Navigator search imported with the MCP | **The best result.** On one company: 17 people about 4 minutes after the call, every one with an exact job title and a LinkedIn URL. Among them the director of revenue operations, the head of growth, the chief revenue officer and a VP of sales. Also in the list: a recruiter, an intern, an investor. The ranking of step 3 is needed. One person was already in the workspace. |
| Apify employee search (`memo23/linkedin-company-employees-scraper`) | Usable, with noise. With company names: 36 rows for 4 companies in 22 seconds, 6 with a job title, among them a head of growth, a chief revenue officer and a VP of GTM operations. The right person in 3 companies out of 4, nobody for the smallest. 30 rows had no title and were billed anyway: $0.15 in all. With LinkedIn company URLs instead of names, only 1 company out of 5 answered. |
| Apify employee search (`harvestapi/linkedin-company-employees`) | Refused on the free Apify plan: "free user run limit exceeded", 0 result. |
| Company mode of the Apify lead finder | Worked: 13 people for 5 companies in 34 seconds, 12 with a job title and an email, none with a LinkedIn URL. The people are not chosen by seniority: a head of marketing next to a customer success manager. One company returned nobody. Real cost: $0.41, billed by the contact scraper it calls. |
| Search by job title inside one company (`find-leads`) | Not usable: 6 people, 4 with no job title, 1 from another company. |

The profile reader (`harvestapi/linkedin-profile-scraper`), tested on 2 people: it runs on a free Apify plan, takes
the profile ids of a Sales Navigator import, answers in 5 seconds and costs $0.004 per profile. It showed that two
"Founding GTM" were full-time with one position each. One of them was a former GTM engineer.

The New York run (2026-11-18, 4 companies kept): 2 posts named the contact ("you'll report to our
Head of Growth", a head of growth in a company of 24), 2 pointed at the founders. Confirmed contacts were created
one by one in the working audience. That audience held 194 people by then, 9 of them leads of the day: the rest came
from the imports.

The first run of the agent, on 4 companies: one Sales Navigator search can hold two companies, so one import. It
took 6 to 9 minutes to arrive. In 2 companies out of 4 the title named by the post did not exist on LinkedIn. The
lists also held investors, assistants and a namesake company: the ranking of step 3 is needed every time.
