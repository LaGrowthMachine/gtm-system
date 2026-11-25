# Applying the Fixes in La Growth Machine (MCP)

How to write the prioritized fixes **straight into the campaign** using the MCP, when the campaign being challenged is a real LGM campaign (you fetched it by name/ID, so you have its `campaignId` and each message's `templateId`). This edits the campaign **in place** — no copy is made — so it needs extra care (see the safety rule). It runs only when the user asks to apply the fixes and the LGM campaign tools are available.

## When this applies

- **The challenged campaign is a live LGM campaign** (you loaded it via `get_campaign_messages`, not a pasted copy). You have `campaignId` + `templateId` per message → you can rewrite each message where it lives.
- If the campaign was **pasted copy** (no `campaignId`), you cannot edit in place. Rewrite it (via `multichannel-campaign-builder`, or inline) and create it as a new draft — that path lives in the main handoff, not here.

## Safety — this touches a real campaign

- **Confirm before the first write.** "I'll apply these fixes directly to '<campaign name>' in La Growth Machine — go?"
- **Check the campaign status first.** If it is **RUNNING**, warn the user: editing changes the messages leads will receive from now on. Offer to **duplicate it first** (`duplicate_campaign`) and apply the fixes to the copy instead, so the live campaign is untouched. Only edit a running campaign in place if the user explicitly confirms.
- Never apply fixes the user hasn't seen and approved. The analysis (the ranked fixes) is shown first; this step only writes what they greenlit.

## The flow

1. **Re-fetch the messages** so your template IDs are current: `get_campaign_messages(campaignId)`. Each message exposes `id` (= `templateId`), `channel`, and the current `newHtml`/`subjectNewHtml`.
2. **Map each fix to the message(s) it changes.** A fix like "opener is too long, cut to one line" targets a specific step; a fix like "same CTA three times in a row" spans several. Only rewrite the messages a fix actually touches — leave the rest untouched.
3. **Rewrite the affected message in `newHtml`** (format below), keeping every personalization variable that was in the original (do not drop a `<var .../>`).
4. `edit_campaign_message(campaignId, templateId, newHtml, subjectNewHtml?)` per affected message. Email steps also take `subjectNewHtml`.
5. **Report** one line per message (fixed / unchanged / error) and end: the fixes are applied; the campaign is a **draft the user reviews and starts** (or, if it was running, the changes are now live — remind them).

## The `newHtml` format (what the tool accepts)

Messages are **not** plain text. Write the rewrite as LGM `newHtml`:

- Body is a sequence of block tags: `<p>…</p>`, `<ul><li>…</li></ul>`, `<h2>…</h2>`. Wrap all text in blocks.
- **One single line, no whitespace between top-level blocks** — `</p><p>`, never `</p> <p>`. Empty spacer line = `<p/>`.
- **Variables verbatim as `<var name="X"/>`** — the `name` is the exact token from `{{X}}`. `{{firstname}}` → `<var name="firstname"/>`, `{{companyName}}` → `<var name="companyName"/>`, `{{customAttribute2}}` → `<var name="customAttribute2"/>`. Never `{{...}}`, `{...}`, `%...%` or `[...]`. To be safe, mirror the exact `<var .../>` tokens already present in the message's current `newHtml`.
- Inline: `<b> <i> <u> <s>`, `<br/>` (line break in a paragraph), `<a href="https://..." track="true">text</a>`, `<spin>Hi|Hello</spin>` (text only), `<signature/>` (emails only). A plain URL as text also works.
- Escape `<` as `&lt;`, `&` as `&amp;`.
- **Email subject** (`subjectNewHtml`): a single `<p>…</p>` with text / `<var/>` / `<spin>` only.

The server **validates and rejects malformed `newHtml`** — if a write is rejected, fix the format and retry; don't force it.

## Fallback

No LGM MCP, or the campaign tools aren't available, or the campaign was pasted copy → do not edit in place. Deliver the rewritten copy as code blocks and use the main handoff (rewrite via `multichannel-campaign-builder`, then set it up). See `SKILL.md`.
