# La Growth Machine — GTM Skills for Claude

> The open-source toolkit to build your full GTM system as Claude skills.

A library of Claude skills built to help GTM teams run their go-to-market motion — from sourcing lists and building campaigns to qualifying meetings and securing channels. Each skill works with your existing stack. Plug the **La Growth Machine MCP** on top to execute the operational steps natively from Claude.

**[Get notified when new skills ship](https://tally.so/r/NpRWgp)** · **[Try La Growth Machine free](https://app.lagrowthmachine.com/register/?utm_source=github&utm_medium=readme&utm_campaign=github-gtm-skills-library&utm_content=github-gtm-skills-library-readme)**

---

## Catalog

Skills are organized into 4 categories, mirroring the GTM motion.

### Fuel my pipeline
Sourcing, list building, ICP — keeping the lead reservoir full.

| Skill | Type | What it does |
|---|---|---|
| [sales-nav-search-builder](skills/fuel-my-pipeline/sales-nav-search-builder/SKILL.md) | use-case | Turn a natural-language ICP into a precise LinkedIn Sales Navigator search URL, ready to import as an LGM audience |
| [won-deal-icp-finder](skills/fuel-my-pipeline/won-deal-icp-finder/SKILL.md) | use-case | Audit your biggest closed-won deals to find your proven ICP and a look-alike target list |

### Get qualified meetings
Campaigns, copywriting, sequences — what converts into meetings.

| Skill | Type | What it does |
|---|---|---|
| [multichannel-campaign-builder](skills/get-qualified-meetings/multichannel-campaign-builder/SKILL.md) | use-case | Generate a complete multichannel campaign — a full LinkedIn + email sequence — from a natural-language brief |
| [campaign-challenger](skills/get-qualified-meetings/campaign-challenger/SKILL.md) | use-case | Benchmark a campaign copy against your existing campaign history and return prioritized fixes before launch |
| [campaign-impact-analyzer](skills/get-qualified-meetings/campaign-impact-analyzer/SKILL.md) | use-case | Rank campaigns by real revenue impact — cross-references LGM campaigns with HubSpot deals |

### Catch opportunities
Reply handling, intent detection — not letting opportunities go cold.

| Skill | Type | What it does |
|---|---|---|
| [reply-manager](skills/catch-opportunities/reply-manager/SKILL.md) | use-case | Classify every reply to your cold outreach and draft the right answer per reply, ready to send in LGM |

### Secure my channels
Channel health, deliverability, identities — protecting the outbound engine.

*Coming soon.*

---

## Install

**Prerequisites:** [Claude Code](https://claude.com/product/claude-code), [Cursor](https://cursor.sh), [Codex](https://github.com/openai/codex), [Amp](https://ampcode.com), or any other supported agent.

**One-line (recommended)** — uses [`skills`](https://github.com/vercel-labs/skills) from Vercel Labs to install the skill into Claude Code (and Cursor, Codex, Amp, +30 other agents) in one command:

```bash
npx skills add LaGrowthMachine/gtm-system/skills/fuel-my-pipeline/sales-nav-search-builder
```

Replace the path with any skill from the catalog above. Add `-g` for a global install.

**Manual install** — if you'd rather not use the CLI, clone and copy:

```bash
git clone https://github.com/LaGrowthMachine/gtm-system.git
cd gtm-system
cp -r skills/fuel-my-pipeline/sales-nav-search-builder ~/.claude/skills/
```

Then ask Claude — e.g. *"Build me a Sales Navigator search for RevOps leaders in EMEA SaaS."*

---

## La Growth Machine MCP

These skills work with any outreach stack. Install the **LGM MCP** to execute the operational steps natively from Claude — no copy-pasting between tools.

| Skill | Without LGM MCP | With LGM MCP |
|---|---|---|
| sales-nav-search-builder | Sales Nav URL to open and import manually | Import the search as a ready-to-use LGM audience |
| won-deal-icp-finder | Works on a HubSpot export you paste | Pulls deals live, attribution clean |
| multichannel-campaign-builder | Sequence ready to copy into your tool | Set up the sequence as a campaign directly in LGM |
| campaign-challenger | Benchmarks against stats you paste | Benchmarks against your real campaign history, pulled automatically |
| campaign-impact-analyzer | Works on pasted campaigns and deals | Cross-references LGM campaigns with HubSpot deals in one click |
| reply-manager | Drafts answers for a conversation you paste | Pulls a campaign's replies, drafts each answer, links to the inbox to send |

**→ [Try La Growth Machine free](https://app.lagrowthmachine.com/register/?utm_source=github&utm_medium=readme&utm_campaign=github-gtm-skills-library&utm_content=github-gtm-skills-library-readme)**

---

## Get new skills as soon as they ship

We add new skills and use cases regularly. One email per batch, no spam.

**→ [Subscribe](https://tally.so/r/NpRWgp)**

---

## License

MIT — see [LICENSE](LICENSE).

## Built by La Growth Machine

LGM is the multichannel outbound platform behind these skills. We use this exact toolkit internally.

[lagrowthmachine.com](https://app.lagrowthmachine.com/register/?utm_source=github&utm_medium=readme&utm_campaign=github-gtm-skills-library&utm_content=github-gtm-skills-library-readme)
