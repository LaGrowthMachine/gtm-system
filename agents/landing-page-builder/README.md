# Landing Page Builder

Landing Page Builder builds the message, the structure and the copy of a landing page with you, for ads, SEO, product,
webinar or comparison pages. It starts from what your visitors say (reviews, search results, search terms), writes
the story of the visitor, has you approve it, then writes the page as an HTML draft and checks it. **It never
publishes a page: you or your designer build the live page from the approved draft.**

## 1. Install (5 minutes)

| Client | How |
|---|---|
| Claude (claude.ai or the desktop app) | Settings → Capabilities → Skills → Upload skill → pick this zip. |
| Cowork | Same as Claude: upload the zip as a skill. |
| Claude Code | Unzip into `~/.claude/skills/` so you get `~/.claude/skills/landing-page-builder/SKILL.md`. |
| Another agent (Cursor, ChatGPT, Codex…) | Unzip it anywhere and tell your agent: "Read landing-page-builder/SKILL.md and follow it." Connect the same tools in that agent. |

## 2. Connect

No connector is required. The agent works with what you give it and the files of your project.

| Optional | Needed for | How |
|---|---|---|
| An SEO tool (Ahrefs, Semrush) | Keyword volumes and the search results page | Its connector in your client, if it has one |
| Web reading | Reading review pages and competitor pages | Built into most clients. Some sites (Reddit) block it: copy the text by hand |
| Python 3 | The page check script | Built into Claude Code and most Macs. Without it, the agent applies the checks by hand |

The agent announces any paid tool run before it starts. **Never paste an API key in the chat.**

## 3. Tell it about your offer

On the first run the agent asks what you sell, to whom and how you talk, then keeps it in `context/offer.md`. It also
asks for your brand colors, font and logo once, so the draft looks like your site. Without them, the draft is a clean
neutral page that your designer or your site builder restyles.

## 4. Run

Say, for example:

- "Build a landing page for our Google Ads campaign on project tracking software."
- "Landing page for a Rivalboard alternative."
- "Write the arc of this page." (then paste or point to your material)
- "Structure this landing."
- "Rework this landing." (with the file or the URL of the page)

Your work goes into a `landings/` folder of your project: the material, the arc, the draft, the handover brief.

## 5. What it does and where it stops

| Step | What it does | It stops to ask you |
|---|---|---|
| 1 | Collects the material: your reviews, competitors' negative reviews, the search results, the search terms | Only when something is missing |
| 2 | Writes the narrative arc: who arrives, from where, what they know, what they fear, what moves them | **Yes: you approve the arc** |
| 3 | Picks the value propositions and the proofs, checks every claim against your product facts | Only on doubt |
| 4 | Decides whether to reuse, translate, duplicate or create a page | Only on doubt |
| 5 | Proposes the structure, section by section, each tied to the arc | **Yes: you approve the structure** |
| 6 | Writes the page as one HTML file you can open in a browser | No |
| 7 | Checks it (script, AI-sounding phrases, does the page keep the arc's promise), lists CRO ideas without applying them | **Yes: you pick the CRO ideas and approve the final copy** |
| 8 | Writes the handover brief for design and publication, with the tracking and QA checklist | No |

Answer its proposals in numbered lists: it answers point by point.

## 6. Feedback

At the end of a run the agent lists what could be better. Open an issue on
https://github.com/LaGrowthMachine/gtm-system.

---

Landing Page Builder · version 0.1.0 · maintained by La Growth Machine.
