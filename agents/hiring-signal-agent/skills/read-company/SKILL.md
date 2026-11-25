---
name: read-company
description: "Reads the website of a company to understand what it sells and to whom: the value proposition, the customers it targets, the industries and the roles it names. Use it when a message has to be shaped on who the company sells to, after a signal has pointed at the company. It does not find people and does not write messages."
---

# Read a company

A message that says "an agent that finds your leads" could go to anyone. A message that says who those leads are
was written for this company. This skill reads the website and brings back, in a few lines, what the company sells
and to whom.

## Input

The website of the company. When it is known: the short description and the industry the job scraper returned.

## Step 1. Fetch the home page

Use the Apify MCP tool `apify--web-fetch` with the URL and `formats: ["markdown"]`. It handles bot protection and
needs no key. It costs $0.0015 per page read on a free Apify plan.

If it fails or comes back empty, try in this order:

1. Firecrawl, when it is available where you run (`{SKILL_BASE}/tools/firecrawl/README.md`). One credit per page.
2. The web reading of the client you run in.
3. Nothing worked: say so and go on with the description from the job scraper.

Read first: the page title, the meta description, the main heading and the first paragraph. They usually state the
value proposition in one sentence.

## Step 2. Look for the pages that name the customers

In the links of the home page, look for pages that say who the company sells to:

| Kind of page | Usual names in the URL or the menu |
|---|---|
| By industry or segment | solutions, industries, use cases, for |
| By role or persona | for sales, for marketing, teams, roles, who it's for |
| Customers | customers, case studies, stories |
| Pricing | pricing, plans: the plan names often say the size of the customer |

Fetch 2 pages at most, the ones that say the most about the customer. Do not crawl the site.

If the home page links to none of these pages, Firecrawl can search the site for them (`firecrawl map` with a few
words such as "customers solutions"). It is a fallback: in the first test the home page listed more of these pages
than the search did.

## Step 3. Write down what was found

In the words of the site, without interpreting:

- **What they sell**, in one line.
- **Who they sell to**: the industries, the company types, the roles. This is the target a message can name.
- **The customers they show**, when they name some.
- **Anything recent the home page announces**: a funding round, a launch, a new market. It can be a second signal on
  the same company: note it with its link, do not cite it without checking its date.

If the site does not say who the customers are, say so. Do not guess a target from the product alone.

## Output

For each company, four lines at most: what they sell, who they sell to, the customers shown, the news if any. Plus
the target in a few words, ready for a message. Plus the pages it comes from.

This is public information about a company: it can be written into the campaign file when the user wants a trace.

## What the first test showed (2026-11-17)

One company from the job posts, a payments company of about 115 people. One fetch of the home page was enough:

- the value proposition was in the title and the first heading;
- the menu had three pages by industry, which gave the target in the company's own words;
- three customers were named;
- the first line of the page announced a funding round: a second signal on the same company.

The page came back as 14 KB of text. Ask for `markdown` only, never `html`.

Firecrawl on the same website: the search returned 3 pages (one industry page out of the three the home page
listed) and one page read came back as 3.6 KB. 2 credits.
