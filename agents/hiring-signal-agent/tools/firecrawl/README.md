# Firecrawl

Finds the pages of a website and reads them as text. The second choice to read a company website, after the Apify
web fetch (the Apify MCP).

## When to use it

- The Apify fetch came back empty or blocked.
- The home page does not link to the page that says who the customers are: Firecrawl can search the pages of the
  site.
- The page needs a browser to show its content.

One page read by the Apify fetch is enough for most companies. Do not start with Firecrawl.

## How it is called

| Where | How | Checked |
|---|---|---|
| Claude Code | The `firecrawl` command line, signed in with your own Firecrawl account | Yes, 2026-11-17 |
| Claude, Cowork, another client | The Firecrawl MCP, once you connect it | Not checked |

```
firecrawl --status                                          the sign-in and the credits left
firecrawl map <site> --search "customers solutions" --limit 15    the pages of the site that match the words
firecrawl scrape <url> -o local/<file>.md                   one page as text
```

Write the output in a working folder that is never shared (`local/` of your project), never next to a skill.

## What it costs

One credit per page read and one per search of a site. A web search costs about 4 credits. The plan decides the credits per
cycle and the requests per minute. A sourcing run on job posts used 24 credits (2026-11-18): the
credits go fast when several agents share the account. Check
`firecrawl --status` before a batch and say the number of pages before starting.

## What the first test showed (2026-11-17)

On the website of a payments company of about 115 people:

- the search for "customers solutions" returned 3 pages, one of them an industry page. The home page read by the
  Apify fetch listed all three industry pages: the search does not replace reading the home page.
- one page read came back as 3.6 KB of text.
- 2 credits spent.

## Never

- Never crawl a whole site for one message: 3 pages per company at most.
- Never put the Firecrawl key in a file of this pack or in the chat.
