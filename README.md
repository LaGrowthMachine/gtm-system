# GTM Skills for Claude

> The open-source GTM toolkit for Claude: skills and an MCP server to run outbound from the chat.

Source your next list, write multichannel LinkedIn and email campaigns, pressure-test them against what already converted, rank your live campaigns by revenue, and handle every reply. Each skill works on its own with any stack. Connect the **La Growth Machine** MCP and Claude acts inside your workspace: it imports audiences, pulls your inbox, and sends your replies. Free, open source, MIT licensed.

[Browse skills](#catalog) · [Quick start](#install-everything-in-one-command) · [Skills library](https://lagrowthmachine.com/claude-skills/?utm_source=github&utm_medium=readme&utm_campaign=github-gtm-skills-library&utm_content=hero-skills-library) · [MCP server](https://lagrowthmachine.com/mcp/?utm_source=github&utm_medium=readme&utm_campaign=github-gtm-skills-library&utm_content=hero-mcp) · Built by [La Growth Machine](https://lagrowthmachine.com/?utm_source=github&utm_medium=readme&utm_campaign=github-gtm-skills-library&utm_content=hero-brand)

---

## Who it's for

- RevOps and SalesOps wiring outreach into the CRM and the rest of the stack
- GTM and Growth Engineers automating the prospecting workflow
- Heads of Sales and Marketing, and CROs, who want qualified pipeline without the busywork
- Founders running their own outbound

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
| [reply-manager](skills/catch-opportunities/reply-manager/SKILL.md) | use-case | Triage your inbox or a campaign's replies, draft the right answer from the full thread, and send it in LGM on your approval |

### Secure my channels
Channel health, deliverability, identities — protecting the outbound engine.

*Coming soon.*

---

## Install everything in one command

The fastest way: install all the GTM skills **and** the LGM MCP server (so Claude can act inside your La Growth Machine workspace) in one go.

```bash
curl -fsSL https://raw.githubusercontent.com/LaGrowthMachine/gtm-system/main/install.sh | sh
```

This installs:

- **The GTM skills** — for Claude Code, Cursor, and Codex (via the [Vercel Labs `skills`](https://github.com/vercel-labs/skills) CLI under the hood)
- **The LGM MCP** — registered with Claude Code via `claude mcp add --scope user --transport http` (user scope → config stored in `~/.claude.json`, available in every project). The installer is **interactive**: it asks if you have an LGM account, then prompts for your API key (hidden input). If you don't have an account, it shows a quick pitch + register link and skips the MCP setup without touching your Claude config.

The script is idempotent — re-running it is safe. Want to review before running?

```bash
curl -fsSL https://raw.githubusercontent.com/LaGrowthMachine/gtm-system/main/install.sh -o lgm-install.sh
less lgm-install.sh
sh lgm-install.sh
```

**Prerequisites:** [Claude Code](https://claude.com/product/claude-code) (or [Cursor](https://cursor.sh), [Codex](https://github.com/openai/codex), [Amp](https://ampcode.com), any other supported agent) and Node.js ≥ 18.

---

## Other ways to install

### Install one skill at a time

If you only need a specific skill (no MCP), use the [Vercel Labs `skills`](https://github.com/vercel-labs/skills) CLI directly:

```bash
npx skills add LaGrowthMachine/gtm-system/skills/fuel-my-pipeline/sales-nav-search-builder
```

Replace the path with any skill from the catalog above. Add `-g` for a global install. Works with Claude Code, Cursor, Codex, Amp + 30 other agents.

### Manual install

Clone the repo and copy the skill folder yourself:

```bash
git clone https://github.com/LaGrowthMachine/gtm-system.git
cd gtm-system
cp -r skills/fuel-my-pipeline/sales-nav-search-builder ~/.claude/skills/
```

### LGM MCP on Claude.ai (web)

Claude.ai accepts HTTP MCP connectors natively. Add the LGM MCP manually:

> Settings → Connectors → Add custom connector → `https://mcpapp.lagrowthmachine.com/mcp`

Then ask Claude — e.g. *"Build me a Sales Navigator search for RevOps leaders in EMEA SaaS."*

---

## La Growth Machine MCP

These skills work with any outreach stack. Install the **LGM MCP** to execute the operational steps natively from Claude — no copy-pasting between tools.

**[See the full MCP page →](https://lagrowthmachine.com/mcp/?utm_source=github&utm_medium=readme&utm_campaign=github-gtm-skills-library&utm_content=mcp-section)**

| Skill | Without LGM MCP | With LGM MCP |
|---|---|---|
| sales-nav-search-builder | Sales Nav URL to open and import manually | Import the search as a ready-to-use LGM audience |
| won-deal-icp-finder | Works on a HubSpot export you paste | Pulls deals live, attribution clean |
| multichannel-campaign-builder | Sequence ready to copy into your tool | Set up the sequence as a campaign directly in LGM |
| campaign-challenger | Benchmarks against stats you paste | Benchmarks against your real campaign history, pulled automatically |
| campaign-impact-analyzer | Works on pasted campaigns and deals | Cross-references LGM campaigns with HubSpot deals in one click |
| reply-manager | Drafts answers for a conversation you paste | Pulls your inbox/campaign replies, drafts each answer, sends them natively on your approval |

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
