# Sales Nav Search Builder

> A Claude skill that turns a natural-language ICP description into a precise LinkedIn Sales Navigator search URL — complete with boolean strings, role normalization, and noise exclusion.

**Maintained by [La Growth Machine](https://lagrowthmachine.com).** Free to use, MIT licensed.

---

## What it does

You describe who you're trying to find:

> "CMOs at B2B SaaS companies in France, 50-500 employees, exclude fractional and freelance."

Claude builds the right Sales Navigator URL:

```
https://www.linkedin.com/sales/search/people?query=(filters:List(
  (type:INDUSTRY,values:List(...Software Development, IT Services, Tech Internet...)),
  (type:CURRENT_TITLE,values:List(text:(CMO OR "Chief Marketing Officer" OR "VP Marketing" OR "Head of Marketing") NOT (Fractional OR Freelance OR Intern))),
  (type:COMPANY_HEADCOUNT,values:List(51-200, 201-500)),
  (type:REGION,values:List(France))
))
```

Click the URL. Sales Nav opens with all the filters applied.

## Why this exists

Sales Navigator URLs are powerful but painful to hand-craft. The format is undocumented, double-URL-encoded, requires LinkedIn-specific IDs for industries, geos, and seniority levels, and breaks silently on small mistakes (a lowercase `or`, a curly quote, an unbalanced paren).

This skill encodes the format, ships LinkedIn's reference IDs (350+ industries, 26 functions, 10 seniority levels, 9 headcount tranches, 22 languages), and validates boolean syntax before building the URL. It also documents the boolean patterns that experienced prospectors learn the hard way — C-suite role normalization, fractional/freelance exclusion, tool stack signals.

## Quick start

### 1. Install the skill

Download the `.skill` file from the [latest release](https://github.com/lagrowthmachine/skills/releases) and install it via your Claude client.

### 2. Ask Claude to build a search

```
"Build a Sales Nav URL for senior RevOps leaders in US SaaS, 200-5,000 employees,
who mention Outreach or Salesloft in their profile."
```

### 3. Open the URL

Click the link Claude provides. Sales Nav opens with the filters applied. **Requires an active Sales Navigator subscription.**

### 4. (Optional) Import leads into La Growth Machine in one click

If you have the [La Growth Machine MCP](https://mcpapp.lagrowthmachine.com/mcp) installed and an LGM account, Claude can pull the leads directly into your LGM workspace — ready to be added to a multichannel outbound sequence (LinkedIn + email + Twitter + phone).

[Sign up for LGM (14-day free trial, unlimited imports during trial)](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=sales-nav-search-builder)

## What's supported

**Filters with full ID mapping**: Industry (350+), Function (26), Seniority level (10), Company headcount (9), Company type (8), Years in current company / position / experience, Profile language (22), Region (curated list of common countries).

**Text filters with boolean support**: Keywords (global), Current job title, Past job title — all accept `AND`, `OR`, `NOT`, `"..."`, `(...)` with automatic validation.

**Text filters without boolean**: First name, Last name.

**Toggle filters**: Changed jobs (90d), Posted on LinkedIn (30d), Past colleague, Follows your company.

## What's not supported (yet)

Filters that require entity URN lookup are out of scope:
- Current/Past company (needs LinkedIn company URN)
- Cities and metropolitan areas (the curated list covers countries and top-level regions only)
- School, Groups, Persona, Account/Lead lists, Connections of

The country list ([`references/regions.json`](./references/regions.json)) covers the COUNTRY_REGION level of LinkedIn's Bing Geo taxonomy. See [`references/geo-locations.md`](./references/geo-locations.md) for the schema and how to add missing entries.

## Keywords this skill helps with

LinkedIn prospecting · LinkedIn search · Sales Navigator search · Sales Nav URL · boolean search · ICP targeting · B2B outbound · cold outreach · cold email · lead generation · sales prospecting · prospect targeting · find leads on LinkedIn · find prospects · sales engagement · outbound sequences · SDR tools · BDR tools · LinkedIn automation · sales operations · revenue operations · multichannel outreach · role normalization · audience building

## Who it's for

- **SDRs and BDRs** running outbound on LinkedIn who want surgical search precision
- **Sales managers and RevOps** building target account lists
- **Founders and CEOs** doing their own prospecting at small companies
- **Growth marketers** running ABM or account-based campaigns
- **Recruiters** sourcing senior talent with boolean strings
- **Agencies** building lead lists for clients

## Limitations

- **Sales Navigator subscription required**: The URLs only work if you have an active Sales Nav subscription on the LinkedIn account you're using. LinkedIn redirects to an upsell page otherwise.
- **English-oriented patterns**: The boolean patterns in this skill assume English-language titles ("CMO", "Head of Sales"). For French, German, Spanish, or other non-English prospects, adapt the titles to local equivalents (e.g., "Directeur Marketing", "Geschäftsführer").
- **LinkedIn changes the URL format from time to time**: When it does, the skill needs an update. Watch this repo for releases. If something breaks, open an issue.

## Feedback and bug reports

Open an issue at https://github.com/lagrowthmachine/skills/issues. Pull requests welcome.

## License

MIT — see [LICENSE](./LICENSE).

## About La Growth Machine

[La Growth Machine](https://lagrowthmachine.com) is a multichannel sales engagement platform that helps B2B sales teams safely run outbound on LinkedIn, email, Twitter, and phone — from a single workspace. 25,000+ users, bootstrapped from Bordeaux, France.

Try it free for 14 days, unlimited imports during the trial: [https://app.lagrowthmachine.com/register](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=sales-nav-search-builder)
