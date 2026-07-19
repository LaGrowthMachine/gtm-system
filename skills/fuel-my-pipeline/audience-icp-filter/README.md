# Audience ICP Filter

> Takes an audience you already have — in your sales tool or as a CSV — and splits it into three actionable segments: ICP match, needs review, out of ICP. Your own team and competitors stripped out.

Maintained by [La Growth Machine](https://lagrowthmachine.com). Free to use. Updated: 2026-07-19.

## What it does

You have 400 people in an audience. Maybe 60 are worth contacting. The rest are colleagues, competitors, students, and people whose job title tells you nothing.

This skill first checks whether your data can even support the filtering you want, asks a handful of questions about your ICP, then sorts every lead into **ICP match**, **needs review**, or **out of ICP**, with a reason attached to each. Your own team and any competitors you name are removed before scoring.

Concretely: you point it at an audience and say *"who should we contact?"* — you get back `150 leads → 33 ICP match · 50 to review · 53 out of ICP · 14 excluded`, the matches listed with why, and the ambiguous ones flagged for your call rather than quietly binned.

It starts from a list that already exists. It does not import or scrape — that's a separate job with its own timing and prerequisites, and bolting it on here would make the skill slower and less reliable for no gain.

## Why it exists

The bottleneck in outbound is rarely the sending — it's working out who is worth sending to. Doing it by hand means scrolling a spreadsheet of job titles and guessing whether "Founder's Office - GTM & Growth" is a buyer.

Doing it with an unassisted LLM is worse: it looks confident, drops people silently, and leaks. On a real 150-lead list, filtering by company name alone let **twelve** of the host's own colleagues through — one had an empty company field and an empty email, with only their bio revealing where they worked.

So classification runs in two passes, and neither is optional:

1. **A deterministic pass** — a script with a test suite handles patterns, exclusions and reconciliation. It cannot lose a lead, and it applies exclusions the same way every run.
2. **A semantic pass** — the model reviews every bucket, because patterns can't read meaning. `Chief Happiness Officer` matches the C-level pattern but is an HR role; a competitor you forgot to list is invisible to a regex. Every override needs a stated reason, and the script re-validates the result so the second pass can't lose anyone either.

Fast and wrong at the edges, or smart and unauditable — you need both.

## Install

Copy the skill folder into your Claude skills directory:

```bash
cp -r skills/fuel-my-pipeline/audience-icp-filter ~/.claude/skills/
```

Then ask Claude — e.g. *"Here's our webinar list, who matches our ICP?"*

## What's supported

- **Any list you already have** — an audience in La Growth Machine, event and webinar attendee exports (Livestorm, Luma, Zoom, Eventbrite, Hopin, Meetup), a Sales Navigator import you've already run, CRM and CSV exports, newsletter or community lists
- **A coverage check before filtering** — reports field fill rates and tells you which criteria your data can honestly support, with the exact enrichment cost if it can't
- ICP definition by **seniority**, **function**, **geography** and **industry**
- Explicit handling of founders whose title states no function — the biggest single source of ambiguity
- Exclusion of your own team and named competitors, matched across company name, both email fields, bio and company URL
- Tolerant company matching — `La Growth Machine`, `@LaGrowthMachine` and `la-growth-machine` all resolve to the same exclusion
- Noise detection — students, interns, "open to work", investors
- Mandatory two-pass classification with a validated, auditable override trail
- A **fixed result layout** — same four zones every run: data coverage, segmentation, what the review pass changed, audiences to create
- Three-bucket output with a reason per lead and reconciled counts
- Write-back to segmented audiences when La Growth Machine is connected

## What's not supported

- **It does not import or scrape.** Bring a list that already exists — an audience, a CSV, an export
- It does not find emails or phone numbers — it sorts what you have
- It does not judge intent or engagement; it scores fit, not interest
- Geography and industry filtering only work if those fields are in your export or added by enrichment — the coverage check tells you upfront rather than failing quietly

## Who it's for

- **SDRs and BDRs** qualifying inbound lists and post-event follow-up
- **RevOps** cleaning and segmenting audiences before they reach sales
- **Growth and demand gen** teams handing off registrants and signups
- **Field marketing and event-led growth** teams working conference and webinar lists
- **Founders** doing their own prospecting and ICP refinement

## Limitations

- Classification quality depends on job-title quality. Sparse or joke titles land in the review bucket by design — that's honesty, not failure.
- A review bucket of roughly a third is normal on unenriched lists, mostly founders with no stated function.
- On a real 150-lead audience straight out of the API, `location`, `industry` and bio were all empty — so geography and industry filtering were unavailable until profile enrichment ran. The coverage check surfaces this before you define your ICP, not after.
- Enrichment costs credits. Profile enrichment is 1 credit per lead; email enrichment is 5 and adds nothing to ICP scoring, so the skill does not use it.
- Requires Python 3 to run the classification engine.

## Works with

This skill runs standalone with any stack — a CSV is enough. It also plugs into:

- **La Growth Machine MCP** — read an existing audience, enrich profiles when fields are missing, and write the ICP-match and to-review segments back as complementary audiences, leaving the source untouched
- **Livestorm, Luma, Eventbrite, Zoom** — via their attendee CSV exports
- **HubSpot / Salesforce** — export a list, score it, re-import the qualified segment

## Stay in the loop

- Browse all GTM skills: [the GTM System catalog](../../../README.md)
- Get new skills as they ship: [Subscribe](https://tally.so/r/NpRWgp)
- See how La Growth Machine fits your GTM stack: [Try LGM free](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=audience-icp-filter)

## License

MIT — see the LICENSE at the repo root.

## About La Growth Machine

La Growth Machine is the multichannel outbound platform behind these skills — it runs prospecting sequences across LinkedIn, email, X and phone from a single workspace.

---

Topics: ICP filtering, lead list qualification, audience segmentation, lead scoring, event lead qualification, webinar attendee list, post-event follow-up, LinkedIn event attendees, Sales Navigator import, CRM list cleanup, B2B prospecting list, RevOps audience building, outbound list building, demand generation
