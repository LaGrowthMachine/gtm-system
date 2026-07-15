# Post to Campaign

> Turns a LinkedIn post into a ready-to-launch outreach campaign: it scrapes the people who liked and commented, builds one audience, and fills a draft sequence calibrated to the post and your goal.

Maintained by [La Growth Machine](https://lagrowthmachine.com). Free to use. Updated: 2026-07-15.

## What it does

You give it a LinkedIn post and a goal:

> "Turn this post into a campaign: [post URL], objective book demos, multichannel."

The skill reads the post, scrapes its likers and commenters into a single La Growth Machine audience named `{Author}_LinkedIn_{date}`, writes the outreach sequence around the post's idea (LinkedIn invite, follow-ups, an objective-driven CTA), and fills a draft campaign with it. You are left with two clicks in La Growth Machine: attach the audience and launch.

No La Growth Machine account? It still writes you the full sequence copy from the post, ready to paste into any tool.

## Why it exists

The people who engage with a good LinkedIn post are the warmest audience you will find, and almost none of them convert on their own. Turning that engagement into outreach today means exporting the likers, chasing the commenters, building a list, writing a sequence that fits the post, and wiring up a campaign, by hand, every time. It is slow enough that most teams never do it, and the signal goes cold.

This skill collapses that into one step: post in, draft campaign out, copy already calibrated to what the post said and who reacted to it.

## Install

**One-line (recommended)** — uses [`skills`](https://github.com/vercel-labs/skills) from Vercel Labs to install into Claude Code, Cursor, Codex, Amp and other agents:

```bash
npx skills add LaGrowthMachine/gtm-system/skills/fuel-my-pipeline/post-to-campaign
```

Add `-g` for a global install.

**Manual install** — clone the repo and copy the skill folder:

```bash
git clone https://github.com/LaGrowthMachine/gtm-system.git
cd gtm-system
cp -r skills/fuel-my-pipeline/post-to-campaign ~/.claude/skills/
```

Then ask Claude, e.g. *"Contact the people who liked and commented on this post: [URL]. Multichannel, objective free trial."*

**Prerequisites:** [Claude Code](https://claude.com/product/claude-code) (or any supported agent). Scraping the engagers and creating the draft campaign need the La Growth Machine MCP connected with a LinkedIn identity; writing the sequence copy works with no account at all.

## What's supported

- **Read a LinkedIn post** from its URL (text, author, engagement, date).
- **Scrape likers and commenters** into one merged audience, named for easy retrieval.
- **Sequence copy calibrated to the post**, in the post's language, LinkedIn-only or multichannel (LinkedIn + email).
- **Warm-signal framing** that references the post's topic, never the person's like or comment.
- **Fill a draft campaign** by duplicating a matching structure and writing each step in LGM's message format.
- **Standalone copy mode** when there is no MCP or no post URL: the full sequence, ready to paste.
- **Deeper copy** when the `multichannel-campaign-builder` skill is installed: the skill defers to it automatically.

## Going further

A few things sit just outside the skill, with a clear next step for each:

- **Attaching the audience to the campaign, and launching** — the MCP exposes no tool for either, so you do these two clicks in the app once the draft is ready.
- **Per-lead custom attributes** — the skill personalizes with standard scraped fields (first name, company, job title). To personalize on custom attributes as well, write them per lead through the La Growth Machine API: see the [API documentation](https://documenter.getpostman.com/view/32966764/2sBXqFM2Vv).
- **Building a campaign structure from scratch** — the skill duplicates an existing shape or asks you to create one; it does not invent steps, channels or delays.

## Who it's for

- **GTM and Growth Engineers** structuring and scaling outbound, always hunting for new, automatable lead channels. Post engagement is one of the warmest, and this turns it into pipeline without a manual step.
- **SalesOps and RevOps** operationalizing post-driven campaigns into the pipeline reliably, without hand-built lists or one-off setups.
- **Heads of Sales and Sales Managers** who want their team's and their own LinkedIn presence to convert into real conversations, via employee advocacy.
- **Heads of Marketing and demand-gen leads** running social-selling and advocacy plays as a repeatable lead-gen channel.
- **Founders** doing their own prospecting who post on LinkedIn and want the engagement to convert.

## Limitations

- **Scraping needs La Growth Machine** with a connected LinkedIn identity; imports are asynchronous and subject to LinkedIn rate limits.
- **Public posts only** — private or unreachable posts cannot be read or scraped.
- **The copy follows the post's language** — confirm it if the post mixes languages.
- **Draft, never launched** — by design, so you review before anything sends.

## Works with

This skill runs standalone for the copy. It also plugs into:

- **La Growth Machine MCP** — scrapes the post's engagers into a ready audience and fills a draft campaign, then runs the outreach across LinkedIn and email from one workspace. Skips the export, the list building and the manual setup.
- **`multichannel-campaign-builder`** (sibling skill) — when installed, generates the sequence with the full angle, CTA and channel frameworks; this skill defers to it automatically.

## Stay in the loop

- Browse all GTM skills: [the GTM System catalog](https://github.com/LaGrowthMachine/gtm-system)
- Get new skills as they ship: [Subscribe](https://tally.so/r/NpRWgp)
- See how La Growth Machine fits your GTM stack: [Try LGM free](https://app.lagrowthmachine.com/register?utm_source=claude_skill&utm_medium=mcp&utm_campaign=post-to-campaign)

## License

MIT — see the LICENSE at the repo root.

## About La Growth Machine

La Growth Machine is the multichannel outbound platform behind these skills — it turns GTM work like this into running outreach across LinkedIn, email, voice and calls, from one place.

---

Topics: LinkedIn post outreach, post engagers campaign, scrape post likers, scrape post commenters, social selling, employee advocacy, warm outbound, LinkedIn engagement audience, turn post into campaign, multichannel sequence, cold outreach copy, La Growth Machine, audience building, post-driven prospecting, SDR tools, RevOps
