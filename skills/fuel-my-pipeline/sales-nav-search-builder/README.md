# Sales Nav Search Builder

> Turns a natural-language ICP description into a precise LinkedIn Sales Navigator search URL — complete with boolean strings, role normalization, and noise exclusion.

Maintained by [La Growth Machine](https://lagrowthmachine.com). Free to use.

## What it does

You describe who you're trying to find:

> "CMOs at B2B SaaS companies in France, 50-500 employees, exclude fractional and freelance."

Claude builds the matching Sales Navigator URL — industries mapped to LinkedIn IDs, the title field normalized into a boolean string (`CMO OR "Chief Marketing Officer" OR "VP Marketing"`), noise excluded (`NOT (Fractional OR Freelance OR Intern)`), headcount and region applied. Click the URL and Sales Navigator opens with every filter in place.

## Why it exists

Sales Navigator URLs are powerful but painful to hand-craft. The format is undocumented, double-URL-encoded, requires LinkedIn-specific IDs for industries, geographies and seniority levels, and breaks silently on small mistakes — a lowercase `or`, a curly quote, an unbalanced parenthesis.

This skill encodes the format, ships LinkedIn's reference IDs (350+ industries, 26 functions, 10 seniority levels, 9 headcount tranches, 22 languages), and validates boolean syntax before building the URL. It also bakes in the boolean patterns experienced prospectors learn the hard way — C-suite role normalization, fractional/freelance exclusion, tool-stack signals.

## Install

Clone the repo and copy the skill folder into your Claude skills directory:

```bash
git clone https://github.com/LaGrowthMachine/gtm-system.git
cd gtm-system
cp -r skills/fuel-my-pipeline/sales-nav-search-builder ~/.claude/skills/
```

Then ask Claude — e.g. *"Build a Sales Nav URL for senior RevOps leaders in US SaaS, 200-5,000 employees, who mention Outreach or Salesloft in their profile."*

**Prerequisites:** [Claude Code](https://claude.com/product/claude-code), and an active Sales Navigator subscription to open the resulting URL.

## What's supported

- **Filters with full ID mapping:** Industry (350+), Function (26), Seniority level (10), Company headcount (9), Company type (8), Years in current company / position / experience, Profile language (22), Region (curated list of common countries and native regions like EMEA, DACH, APAC).
- **Text filters with boolean support:** Keywords, Current job title, Past job title — all accept `AND`, `OR`, `NOT`, `"..."`, `(...)` with automatic validation.
- **Text filters without boolean:** First name, Last name.
- **Toggle filters:** Changed jobs (90d), Posted on LinkedIn (30d), Past colleague, Follows your company.

## What's not supported

Filters that require entity URN lookup are out of scope:

- Current / Past company (needs a LinkedIn company URN)
- Cities and metropolitan areas (the curated list covers countries and top-level regions)
- School, Groups, Persona, Account/Lead lists, Connections of

## Who it's for

- SDRs and BDRs running outbound on LinkedIn who want surgical search precision
- Sales managers and RevOps building target account lists
- Founders and CEOs doing their own prospecting
- Growth marketers running ABM campaigns
- Recruiters sourcing senior talent with boolean strings
- Agencies building lead lists for clients

## Limitations

- **Sales Navigator subscription required** — the URLs only work with an active Sales Nav subscription on the LinkedIn account in use.
- **English-oriented patterns** — the boolean title patterns assume English titles ("CMO", "Head of Sales"). For non-English prospects, adapt to local equivalents.
- **LinkedIn changes the URL format from time to time** — when it does, the skill needs an update.

## Works with

This skill runs standalone with any outreach stack. It also plugs into:

- **La Growth Machine MCP** — once the MCP exposes audience import, Claude pushes the Sales Nav search straight into an LGM audience, ready for a multichannel sequence (LinkedIn + email). Until then, the skill links you to import it in one step in the LGM app.

## Stay in the loop

- Browse all GTM skills: [the GTM System catalog](../../../README.md)
- Get new skills as they ship: [Subscribe](https://tally.so/r/NpRWgp)
- See how La Growth Machine fits your GTM stack: [Try LGM free](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=sales-nav-search-builder)

## License

MIT — see the LICENSE at the repo root.

## About La Growth Machine

La Growth Machine is a multichannel sales engagement platform that helps B2B teams run outbound on LinkedIn, email and more — from a single workspace.

---

Topics: LinkedIn prospecting, Sales Navigator search, Sales Nav URL, boolean search, ICP targeting, B2B outbound, lead generation, sales prospecting, find leads on LinkedIn, outbound sequences, SDR tools, RevOps, audience building, role normalization
