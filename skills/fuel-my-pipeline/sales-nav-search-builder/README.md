# Sales Nav Search Builder

> Turns a natural-language ICP description into a precise LinkedIn Sales Navigator search URL — complete with boolean strings, role normalization, and noise exclusion.

Maintained by [La Growth Machine](https://lagrowthmachine.com). Free to use. Updated: 2026-05-26.

## What it does

You describe who you're trying to find:

> "CMOs at B2B SaaS companies in France, 50-500 employees, exclude fractional and freelance."

The skill builds the matching Sales Navigator URL — industries mapped to LinkedIn IDs, the title field normalized into a boolean string (`CMO OR "Chief Marketing Officer" OR "VP Marketing"`), noise excluded (`NOT (Fractional OR Freelance OR Intern)`), headcount and region applied. Click the URL and Sales Navigator opens with every filter in place.

## Why it exists

Sales Navigator URLs are powerful but painful to hand-craft. The format is undocumented, double-URL-encoded, requires LinkedIn-specific IDs for industries, geographies and seniority levels, and breaks silently on small mistakes — a lowercase `or`, a curly quote, an unbalanced parenthesis.

This skill encodes the format, ships LinkedIn's reference IDs (350+ industries, 26 functions, 10 seniority levels, 9 headcount tranches, 22 languages), and validates boolean syntax before building the URL — refusing to emit an invalid one. It also bakes in the boolean patterns experienced prospectors learn the hard way: C-suite role normalization, fractional/freelance exclusion, tool-stack signals.

## Install

**One-line (recommended)** — uses [`skills`](https://github.com/vercel-labs/skills) from Vercel Labs to install into Claude Code, Cursor, Codex, Amp + 30 other agents in one go:

```bash
npx skills add LaGrowthMachine/gtm-system/skills/fuel-my-pipeline/sales-nav-search-builder
```

Add `-g` for a global install.

**Manual install** — clone the repo and copy the skill folder yourself:

```bash
git clone https://github.com/LaGrowthMachine/gtm-system.git
cd gtm-system
cp -r skills/fuel-my-pipeline/sales-nav-search-builder ~/.claude/skills/
```

Then ask Claude — e.g. *"Build a Sales Nav URL for senior RevOps leaders in US SaaS, 200-5,000 employees, who mention Outreach or Salesloft in their profile."*

**Prerequisites:** [Claude Code](https://claude.com/product/claude-code) (or any other supported agent), and an active Sales Navigator subscription to open the resulting URL.

## What's supported

- **Filters with full ID mapping** — Industry (350+), Function (26), Seniority level (10), Company headcount (9), Company type (8), Years in current company / position / experience, Profile language (22), Region (curated list of countries).
- **Text filters with boolean** — Keywords (global), Current job title, Past job title — accept `AND`, `OR`, `NOT`, `"…"`, `(…)` with automatic validation (refuses lowercase operators, curly quotes, unbalanced parentheses, wildcards, exceeded operator budget).
- **Text filters without boolean** — First name, Last name.
- **Toggle filters** — Changed jobs (90d), Posted on LinkedIn (30d), Past colleague, Follows your company.
- **Deterministic URL builder + validator** (`scripts/build_url.py`, `scripts/validate_boolean.py`) — refuses to emit an invalid URL and ships a regression suite that reproduces real captured Sales Nav URLs.

## What's not supported

Filters that require entity URN lookup are out of scope:

- Current/Past company (needs LinkedIn company URN)
- Cities and metropolitan areas (the curated list covers countries and top-level regions only)
- School, Groups, Persona, Account/Lead lists, Connections of

## Who it's for

- **SDRs and BDRs** running outbound on LinkedIn who want surgical search precision.
- **Sales managers and RevOps** building target account lists.
- **Founders and CEOs** doing their own prospecting at small companies.
- **Growth marketers** running ABM or account-based campaigns.
- **Recruiters** sourcing senior talent with boolean strings.
- **Agencies** building lead lists for clients.

## Limitations

- **Sales Navigator subscription required.** The URLs only work if you have an active Sales Nav subscription on the LinkedIn account you're using. LinkedIn redirects to an upsell page otherwise.
- **English-oriented patterns.** The boolean patterns assume English-language titles ("CMO", "Head of Sales"). For French, German, Spanish or other non-English prospects, adapt the titles to local equivalents (e.g. "Directeur Marketing", "Geschäftsführer").
- **LinkedIn changes the URL format from time to time.** When it does, the skill needs an update — watch this repo for releases.

## Works with

This skill runs standalone with any stack. It also plugs into:

- **La Growth Machine MCP** — imports the search as a ready-to-use audience in one click, then runs the outreach across LinkedIn, email, voice and calls from a single workspace. Skips the CSV export and the manual import.

## Stay in the loop

- Browse all GTM skills: [the GTM System catalog](../../../README.md)
- Get new skills as they ship: [Subscribe](https://tally.so/r/NpRWgp)
- See how La Growth Machine fits your GTM stack: [Try LGM free](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=sales-nav-search-builder)

## License

MIT — see the LICENSE at the repo root.

## About La Growth Machine

La Growth Machine is the multichannel outbound platform behind these skills — it turns GTM work like this into running outreach across LinkedIn, email, voice and calls, from one place.

---

Topics: LinkedIn prospecting, Sales Navigator URL, Sales Nav search, boolean search builder, ICP targeting, B2B outbound, cold outreach, lead generation, sales prospecting, find leads on LinkedIn, audience building, role normalization, SDR tools, BDR tools, RevOps, sales engagement, multichannel outreach
