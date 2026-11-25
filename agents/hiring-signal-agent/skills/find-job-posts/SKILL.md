---
name: find-job-posts
description: "Finds companies hiring for given roles on LinkedIn (Apify job scraper), scores each post against the campaign and keeps the good ones with the mission, tools and team to cite. First step of a hiring-signal campaign. Does not find people or write messages."
---

# Find the job posts

A job post is a public signal: the company says what it is building and with which tools. It also says the budget exists.
This skill turns a few criteria into a short list of companies worth writing to, each with what its post says.

## Input

From the campaign file:

- the roles to watch (for example "GTM Engineer", "Revenue Operations");
- the location;
- the company size and the industries that count, if any;
- how far back to look: the last 24 hours, the last week or the last month.

## Step 1. Search, on two sources

The two sources do not overlap: on the same brief, LinkedIn and the career pages returned different companies.
Use both, then merge by company.

**Pick the boards of the market first.** The boards differ from one country to the next. Searching only the US
boards on a French brief returns staffing agencies and companies of another region.

| Market | Career pages and boards to search | Aggregators to spot a post |
|---|---|---|
| United States, UK, tech startups anywhere | Ashby (`jobs.ashbyhq.com`), Greenhouse (`job-boards.greenhouse.io`, `boards.greenhouse.io`), Lever (`jobs.lever.co`) | BuiltIn, Wellfound |
| France | Welcome to the Jungle (`welcometothejungle.com`), Teamtailor (`*.teamtailor.com`), SmartRecruiters (`jobs.smartrecruiters.com`), Workday (`*.myworkdayjobs.com`), SAP SuccessFactors (`*.successfactors.eu`, `career*.successfactors.com`), the company's own career page or PDF | HelloWork, Indeed, APEC |
| Germany, Benelux, Nordics | Personio (`*.jobs.personio.de`), Teamtailor, SmartRecruiters, Workday, Join (`join.com`) | StepStone, Indeed |
| Elsewhere | Ask the user which boards the companies of that market use, then search those | Indeed |

**A region is a list of cities.** LinkedIn `locations` and the web search work on cities or official region names.
Turn a region into its main cities, and say the list: for example "PACA" or "Provence-Alpes-Côte d'Azur" → Marseille,
Aix-en-Provence, Nice, Toulon, Sophia Antipolis, Antibes, Cannes, Avignon. "Bay Area" → San Francisco, Oakland, San
Jose, Palo Alto. Add the official region name as one more location.

**Career pages.** They give the exact title, the true publication date and the full text.

1. **Search the job boards** of the market with a web search limited to their domains. Put every role in quotes
   (example for the US boards):

   ```
   "Head of Growth" OR "Head of Growth Marketing" ("San Francisco" OR "Bay Area") (site:jobs.ashbyhq.com OR site:job-boards.greenhouse.io OR site:boards.greenhouse.io OR site:jobs.lever.co)
   ```

   One search per group of roles, in the language of the posts of that market ("Responsable RH" in France). Add
   `-<company>` for the companies already seen. Tool: the web search of the client you run in, or the Apify MCP
   `apify--web-search`; the Firecrawl search (about 4 credits per search) only when the user connected Firecrawl.
2. **Read each board through its public API**, with no key:

   | Board | Where | Full text | Date |
   |---|---|---|---|
   | Ashby | `https://api.ashbyhq.com/posting-api/job-board/<slug>` | `descriptionPlain` | `publishedAt` |
   | Greenhouse | `https://boards-api.greenhouse.io/v1/boards/<token>/jobs`, then `/jobs/<id>` | `content` (HTML to unescape) | `first_published`, not `updated_at` |

   Ashby returns every post of a board in one call, with its text and its date. The slug or the token is the part of
   the post URL right after the domain. A slug can answer 404 or an empty
   board while the post lives under another slug: then read the page of the post itself.
3. **Keep the full text of the post.** A link alone is not enough to score it.
4. **Aggregators** (BuiltIn, HelloWork, Indeed and the like) help to spot a post. Their titles and their dates can be
   wrong: always go back to the board. **When the board page is gone** (404) and the aggregator is the only full
   text, keep the aggregator's text, write its URL and its date as the source, and check that the post is less old
   than the period of the campaign. Mark it "aggregator only" in the review attribute.

Checked from this repository on 2026-11-18: both APIs answer with the fields above. One Firecrawl search on
"Head of Growth" in San Francisco returned 5 posts with the exact title.

**LinkedIn.** It gives the headcount and the LinkedIn id of the company. Its keyword search is loose: put the roles
in quotes and still expect neighboring titles. Call the Apify actor `cheap_scraper/linkedin-job-scraper` with the Apify MCP (`call-actor`, then
`get-dataset-items`). No script and no key are needed.

| Input | Value |
|---|---|
| `keyword` | The roles to watch, as a list |
| `locations` | The location, as a list |
| `publishedAt` | `r86400` (24 hours), `r604800` (a week) or `r2592000` (a month) |
| `maxItems` | The cap for this run |
| `enrichCompanyData` | `true`, to get the website, the industry and the headcount |
| `excludeRecruitingAgencies` | `true` |
| `saveOnlyUniqueItems` | `true` |
| `companySizeMin`, `companySizeMax` | From the campaign file, when it sets a size |

For every post, whatever its source:

- **Keep only the posts of the period** the campaign sets (30 days by default). A post still open after that is
  left out. **The date of the board is the reference**: LinkedIn re-posts offers, so its date can be weeks younger.
- **Get the headcount**, in this order: the public LinkedIn page of the company (the Apify MCP tool
  `apify--web-fetch`, formats among `markdown`, `html`, `text`, `links`, `raw`: ask for `text` and `links`, then look
  for "View all N employees". It also gives the company id. It can time out
  or come back cut, then, when Firecrawl is connected, a targeted Firecrawl request reads the size band, for about 14
  credits), the headcount the LinkedIn job scraper returns, an aggregator, the text of the
  post. Write the source next to the number. When two sources fall on each side of the size limit, say so and
  ask.
- **Sort by size before reading**: leave out the companies above the size of the campaign.
- **Check the roles of the campaign first.** Before keeping a neighboring post, look on the company's own job board
  for a post that is one of the roles of the campaign: it is the better signal.

In a routine, set `publishedAt` to the time since the last run. Each run then only sees the new posts.

A test run of 10 posts took about 11 seconds and cost less than one cent.

**Say the cost before each run, computed.** `fetch-actor-details` gives the prices per event, not a total: the cost is
the price per start plus the price per result times `maxItems`. On the free Apify tier in November 2026:
$0.005 per start and $0.0007 per job, so a run capped at 30 to 50 posts costs about $0.03 to $0.04.

## Step 2. Read every post and score it

The title is not enough. In the first test, 1 "GTM Engineer" post out of 5 was about the website and had nothing
on outreach. 

Fetch `jobDescription` for every post and score it against the missions your offer covers: the outline
(`{SKILL_BASE}/references/hiring-signal-outline.md`, "How a post is scored") and `mission-families.md`, both set up from your
offer at the first campaign.

A role that is in none of the lists of the campaign file is a question for the human, not a "None". Ask, then
write the answer in the campaign file.

Group the posts by company: the same post in two cities is one company. Read the target lists of the campaign file
first and write the user's answers back into them, as in `icp-fit`. When in doubt on a post, ask.

## Step 3. Note what each kept post says

For each company kept:

- **The mission to cite**: the one closest to what the campaign offers, in the words of the post.
- **The mission family**, from `mission-families.md` in this folder. Read it before scoring.
- **The tools named** (CRM, enrichment, sequencing, data).
- **Who the role reports to or works with.** The reporting line when it is written ("you report to the Head of
  Revenue"). The team otherwise (marketing, sales, leadership). This tells `find-contacts` who to look for.
- **A deadline or a milestone for the role**, when the post gives one ("in 60 days", "in the first 90 days").
- **The company description** the scraper returns. The `read-company` skill then reads the website to say who the
  company sells to.
- **A stated principle on human review**, when the post has one.
- **The date of the post** and the headcount of the company.

In the first test, on 5 posts: 2 strong, 2 partial, 1 none. 1 post named the reporting line, 3 named the team, 3
named the tools, 2 gave a deadline. None described the interview process. The post does not give the name of the
hiring manager: the poster field was empty on all 10.

The second run (2026-11-18, "Head of Growth", same area): 30 posts, 26 companies. The LinkedIn keyword search is loose:
most titles were neighbors (Head of Marketing, VP Revenue Marketing, Director of Growth Marketing). 11 companies had 200
people at most. Among them 2 strong posts and 1 partial were kept. Also seen: a recruiting firm posting for a client
despite the filter, a post filled with placeholder text, B2C companies. Hence two habits: sort by size before reading
and read before keeping.

What a search costs (run of 2026-11-18, 5 companies kept): 6 Firecrawl searches (24 credits), 2 runs of the
LinkedIn job scraper ($0.09), about 7 minutes.

What went wrong in the runs: a post that was already filled or was a replacement, a contact title that nobody
confirmed, a run that only searched the neighboring roles and found none of the roles of the campaign.

Quote the post exactly when you note something. Do not infer a tool, a team or a mission that is not written.

## Output

One row per company kept: the fit, the role, the date, the website, the industry, the headcount, the LinkedIn
company id, the mission to cite, its family, the tools, who the role reports to or works with, plus the link to
the post. Then the posts left out, each with its reason. Then stop: `find-contacts`
takes over.

A post is public and about a company, so these rows can be written into the campaign file when the user wants a
trace. No person is named at this step.
