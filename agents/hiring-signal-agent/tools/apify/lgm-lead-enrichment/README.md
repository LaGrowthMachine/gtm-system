# Apify · La Growth Machine Lead Finder & Enrichment

The actor the agent uses to find and enrich leads: `sameh.jarour/lgm-lead-enrichment`
(https://apify.com/sameh.jarour/lgm-lead-enrichment), built by Sameh Jarour at Apify.

Read through the Apify MCP on 2026-11-17 (input schema, pricing, server interface). First successful run the same
day, through the script.

## What it does

1. Finds people who match a target (job title, seniority, function, location), without a LinkedIn login.
2. Enriches them through the La Growth Machine API: professional email, personal email, phone.
3. Returns one row per lead in a dataset, with the outcome and the reason.

In this agent, the actor stops there. The push into the audience is done by `push-leads` through the La Growth Machine
MCP, once the messages are written.

## How to keep the actor from writing into La Growth Machine

Leave `targetAudience` empty. The input schema says: "Leave empty to only produce a dataset without touching your LGM
account." `writeBackToLgm` is on by default only when an audience is named.

## How the agent calls it

Through the script next to this file, which calls the Apify API:

```bash
python3 {SKILL_BASE}/tools/apify/lgm-lead-enrichment/run_actor.py search --title "GTM Engineer" --location Paris --max 10
python3 {SKILL_BASE}/tools/apify/lgm-lead-enrichment/run_actor.py enrich --leads local/kept.json
```

`search` finds people and spends no credit. It leaves out people already contacted in La Growth Machine. A file of
leads only ever lives in `local/`, which Git ignores. `enrich` finds the professional email of a list of leads, the ones kept
after the sort (5 La Growth Machine credits per lead). The script starts the run, waits for it, then prints the leads
as JSON. It never writes into La Growth Machine. Run it with `--help` for every option.

A run started through the Apify MCP (`call-actor`) fails: the actor needs the La Growth Machine API key in its input
in every mode, even with no enrichment. Tested twice on 2026-11-17.

First enrichment run (2026-11-17): 2 leads in, 2 valid professional emails out, 12 seconds, 5 credits each. The output
says `writtenBackToLgm: false`: nothing is written into La Growth Machine.

## Inputs for a search from a target (`leadSource: icpSearch`)

| Input | Meaning |
|---|---|
| `icpJobTitle` | List of job titles. Each title is a separate search. |
| `icpSeniorityLevels` | Intern, Entry, Senior, Manager, Director, VP, CXO, Partner, Owner |
| `icpJobFunctions` | Sales, Marketing, Engineering, Data, Product, Operations, Customer Success and others |
| `icpLocation` | A keyword, not a geo filter. Set `strictLocationMatch: true` to drop people outside it. |
| `icpCompany` | Optional company-name keyword, to prospect inside one account |
| `icpKeywords` | Optional free text across role, skills and headline |
| `maxProfilesToDiscover` | How many people the search looks for (default 50). Search wide: rows are dropped afterwards. |
| `maxLeads` | Cap on leads enriched and delivered |
| `requireCompany` | On by default: drops profiles with no company before enrichment |
| `excludeContactedLeads` | Skips people already contacted by a La Growth Machine campaign |
| `enrichType` | `EMAIL_ENRICH` (5 credits per lead, works for people not yet in La Growth Machine) or `NONE` |
| `maxCreditsToSpend` | The run refuses to start if its worst case exceeds this |

**No filter on company size or industry.** A target such as "B2B SaaS, 50 to 200 people" can only be approached with
`icpKeywords` or with the company scorer below.

## Other sources the actor offers

| `leadSource` | What it does |
|---|---|
| `leadScorer` | Scores a list of company websites (technology detected, yes/no questions answered on the homepage), then finds contacts in the companies that qualify. The closest thing to a signal-based search. |
| `lgmLinkedinImport` | Imports a LinkedIn search, a Sales Navigator search or the engagers of a post, through a La Growth Machine identity |
| `leadList` | Enriches a list of leads passed in the input |
| `lgmAudience` | Enriches an existing La Growth Machine audience |

## Keys

The script needs two keys:

| Key | Where to get it |
|---|---|
| `APIFY_TOKEN` | Apify Console > Settings > API & Integrations |
| `LGM_API_KEY` | https://app.lagrowthmachine.com/settings/api |

Put them in a `.env` file next to the script (copy `.env.example`). They can also live in the environment of the
machine that runs the agent. **The `.env` file is never committed**: Git ignores it. On a new machine, create it again by hand.

Without keys, use the Sales Navigator variant of `find-leads`, which only needs the La Growth
Machine MCP.

## Cost

Measured on 2026-11-17, on a free Apify plan. The lead finder actor itself costs almost nothing. The actors it calls
are billed separately on the same account. That is where the cost is.

| What | Real cost |
|---|---|
| `search` on one job title | About $0.04, billed by the people search it calls |
| `companies` on 5 websites | About $0.41, billed by the contact scraper it calls |
| A job scraper run, 10 posts | About $0.01 |
| An employee search, 36 rows | $0.15 |

The script prints the cost of its own run only. The total is in the Apify console.

**The free plan**: $5 of usage per month, 5 runs at a time, results kept 7 days. New accounts get $50 more with the
coupon `LGM50`: https://console.apify.com/sign-up?couponId=LGM50. Some actors refuse free accounts.

La Growth Machine: 5 credits per lead for email enrichment, charged whether or not an email is found.

## Server mode

The actor also answers HTTP requests (through `send-server-actor-request`): `GET /credits` returns the La Growth
Machine credit balance, `POST /enrich` enriches one lead.

## First real run (2026-11-17)

`run_actor.py search --title "GTM Engineer" --location Paris --max 10`.

- **It works**: run finished in 100 seconds, 7 leads returned for 10 asked, 0 La Growth Machine credit. The
  script reported $0.0002: that was the actor alone, the people search it calls cost about $0.04 more.
- **What each lead carries**: first name, last name, LinkedIn URL and location (7 of 7), company name (6 of 7), job
  function (6 of 7), job title (5 of 7), seniority (3 of 7).
- **What it does not carry**: headline, bio, company website, company size, industry, recent activity.
- **Last names**: 2 of 7 are an initial only.
- **Relevance**: 3 of 7 hold the exact title, 2 hold a neighboring title (RevOps, marketing execution), 2 have no title.
- The search behind it is the actor `memo23/linkedin-people-search`.

**What this means for the messages**: the actor gives enough to push a lead, not enough to write a line that is
true about this lead only. `personalize` needs a second source for the fact (a profile enrichment through La Growth
Machine or another actor).

## Still to verify

- A run of `enrich`: how many emails come back and how long it takes. How the initial-only last names behave.
- Whether Sameh can make the key optional when nothing is enriched and nothing is written to La Growth Machine.
