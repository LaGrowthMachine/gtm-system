# Building an Audience from a Post's Engagers (LGM MCP)

How to turn a LinkedIn post into a single La Growth Machine audience containing the people who **liked** and **commented** on it. This runs only when the LGM MCP is connected and the user gave a post URL.

## The tools

- `list_identities` → the connected LinkedIn / email identities. Each import runs *as* one identity.
- `create_audience_from_linkedin_url(audience, linkedinUrl, identityId, linkedinPostCategory)` → scrapes engagers from a post URL into a named audience.
  - `audience` is a **name, not an ID**. If it does not exist, LGM creates it. If it exists, new leads are **added** to it (merge). This is what lets likers and commenters land in one audience.
  - `linkedinPostCategory` is `"like"` or `"comment"`. One call scrapes one engagement type.
  - The import is **asynchronous** and needs the underlying LinkedIn account connected in La Growth Machine.
  - **It returns only a status (no audience ID).** Keep this in mind: it means there is no handle to poll (see below).

## What you cannot check via the MCP (important)

The create call returns **no `audienceId`**, and there is **no tool to list audiences**. So once the scrape is launched you **cannot** poll its status, read its size, or fetch its leads through the MCP: `get_audience` and `get_audience_leads` both need an ID you do not have. The audience is verified by its **name** in the LGM Audiences view. Its ID only becomes reachable through the MCP later, once a campaign uses it (then `list_campaigns` surfaces `audience.id` and its size). Do not promise the user a live lead count from the MCP right after scraping; point them to the audience by name instead.

## The flow

### 1. Pick the identity

Call `list_identities`. If there is exactly one, use it. If there are several, ask the user which LinkedIn account should do the scrape (in English), and use its `identityId`. Do not guess.

### 2. Name the audience

Use a simple, findable convention so the user spots it in their audience list:

```
{PostAuthor}_LinkedIn_{YYYY-MM-DD}
```

- `{PostAuthor}` = the post author's name with spaces removed (from `get_linkedin_post`, e.g. `JaneDoe`).
- `{YYYY-MM-DD}` = the post date if you have it, otherwise today.
- Example: `JaneDoe_LinkedIn_2026-07-15`.

Keep the **same name** for both scrape calls so they merge into one audience.

### 3. Confirm, then scrape both engagement types

Confirm first, because the scrape runs on the user's connected LinkedIn identity:

> "I will scrape the likers and commenters of this post into one audience named `{name}`. This runs on your `{identity}` LinkedIn account. Go?"

On yes, call the tool twice, same `audience` name, same `identityId`, same post URL:

1. `linkedinPostCategory: "like"`
2. `linkedinPostCategory: "comment"`

Order does not matter; both feed the one audience.

### 4. Confirm and hand off (no polling)

Each call returns only a status, not an audience ID, and there is no list-audiences tool, so you cannot poll the import or read the size from the MCP. Instead:

- Confirm to the user that both scrapes were launched (both returned a success status), under the audience name you chose.
- Tell them the import runs asynchronously and the audience fills in the background.
- Point them to the [LGM Audiences view](https://app.lagrowthmachine.com/audiences?utm_source=claude_skill&utm_medium=mcp&utm_campaign=post-to-campaign) to watch it populate and see the final count, found by its name.

The audience becomes readable via the MCP (`get_audience`, `get_audience_leads`) only after a campaign uses it, when `list_campaigns` surfaces its ID.

## Edge cases

- **0 leads imported.** The post may have little engagement, or the LinkedIn account may not be connected in La Growth Machine. Tell the user plainly and suggest checking that the LinkedIn identity is connected, then retry.
- **Import blocked or stuck.** LinkedIn rate-limits scraping. If the status does not progress, tell the user it is being throttled and the audience will keep filling in the background; they can proceed with the campaign draft and attach the audience once it is ready.
- **Private or unreachable post.** `get_linkedin_post` or the scrape may return nothing for a non-public post. Say so and ask for a public post URL.
- **No URL, only pasted text.** Scraping is impossible without the URL. Skip audience creation and deliver the sequence copy instead; the user can build the audience later in LGM.

## What the MCP cannot do here

- **No audience ID on creation, no list-audiences tool** → you cannot poll status, size, or leads after scraping (covered above).
- **No tool to attach the audience to a campaign, and no launch tool.** The skill stops at "audience scraped + draft campaign filled"; attaching the audience to the campaign and launching are done by the user in the LGM app.
