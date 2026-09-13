# The content library

Where the content comes from, how it is tagged, and where the index lives. The engine (`scripts/build.py index`) owns the file; you own the reading and the tags.

## Three sources, cumulative

| Source | How to read it | Ask the user |
|---|---|---|
| **Website** | `build.py sitemap <sitemap url> --prefix <path>` lists the page URLs under a path, following sitemap indexes. Fetch each page and read it. | The blog category or folder that holds the resources. Never crawl a whole site: "everything under `/gtm-playbooks/`", "the `/customers/` section", "posts tagged case-study". If the sitemap is not at `/sitemap.xml`, ask for it. |
| **Notion** | Notion MCP: a database (one row per resource, tags often present as properties) or a parent page (one child page per resource). Read the content, keep the tags the page already carries, add the missing ones. | The database or page. |
| **Google Drive** | Drive MCP: a folder. Read titles and contents (docs, PDFs, slides). | The folder. Private documents get `"is_private": true`: the sentence then offers to send it rather than pasting a link the lead cannot open. |
| **Pasted list** | Title, URL, two lines each. Tag from the description. | Nothing. |

One library can mix sources: a site for public playbooks, a Drive for private case studies.

## Tag axes (same axes as the lead profile, so matching is a set intersection)

```json
{
  "url": "https://example.com/playbooks/not-now-replies",
  "title": "Turning not-now replies into meetings",
  "type": "playbook",
  "stage": "educate",
  "pains": ["not now replies", "reply handling"],
  "personas": ["founder", "sales"],
  "industries": [],
  "company_sizes": ["11-50", "51-200"],
  "language": "en",
  "summary": "Six-week cadence, one content per touch, ask before sending.",
  "generic": false,
  "is_private": false,
  "source": "website"
}
```

| Field | Values | Weight in matching |
|---|---|---|
| `pains[]` | the lead's vocabulary, short | 5 per shared pain, dominates |
| `personas[]` | founder, sales, marketing, ops, revops, growth, recruiting… | 3 |
| `industries[]` | plain words | 2 |
| `company_sizes[]` | `1-10`, `11-50`, `51-200`, `201-1000`, `1000+` | 1 |
| `stage` | `reassure` (social proof, testimonials), `educate` (how-to, playbook), `prove` (case study with numbers), `reactivate` (news, launch, benchmark) | 1 when it fits the touch: first touch educates or reassures, second proves, third re-activates or proves |
| `language` | `en`, `fr`… | English content can go to any lead; non-English content only to a lead of that language, where it gets +2 so it beats English on a tie |
| `type` | `case_study`, `playbook`, `article`, `podcast`, `video`, `post`, `template`, `other` | none, shown in the review table |
| `generic` | true for 1 or 2 evergreen pieces | fallback when nothing scores ≥ `--min-score`; flagged `weak` in the output |

Empty tags are allowed (the engine validates only the enumerations). A page with no pains never matches on pain: tag it from what it actually says, not from what it should say.

## Tagging rule of thumb

Read the page, then answer three questions in the lead's words: *which problem does this help with* (pains), *who is it written for* (personas, industries, sizes), *what does it do to a hesitant reader* (stage). A case study that names an agency of 20 people and a reply bottleneck gets `pains: ["reply handling"]`, `industries: ["marketing agency"]`, `company_sizes: ["11-50"]`, `stage: "prove"`. The point made by one of the sellers who shaped this skill: dropping a Fortune-500 logo on a small agency reads as "not for us". Tags are how the engine avoids that.

## Where the index lives

- **Claude Code, Cowork, any environment with files**: `library-index.json` in the user's working folder. `build.py index` merges by URL: new pages are added with `added_at`, existing ones keep their tags unless the fresh read brings new values, every page read today gets `last_seen`. Pages missing from the source are kept (they may be private or unlisted); delete by hand if needed.
- **claude.ai, no file system**: re-read the source on every run (a sitemap, a Notion database or a Drive folder takes seconds). The state that matters, which content went to which lead, lives on the lead in La Growth Machine (custom attributes and audiences), not in the index. Optional cache: write the index into a Notion page named "Nurture library index" through the Notion MCP and read it back next time.

A content added yesterday is eligible today, with no reconfiguration.

## When the library is empty or thin

Run the match anyway. The engine refuses on an empty library and reports `content_gaps` on a thin one: the pains the waiting leads voiced, ranked by how many leads wait. Turn that into the content plan (Step 6 of the skill): for each gap, the suggested format is `prove` (a case study) when the leads are `vague`, `educate` (a playbook or article) when they are `not_now`. A reply is a content brief.
