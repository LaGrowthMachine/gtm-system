# Touch rules

Two things get written: the **sentence** stored on each lead (one per content, inserted verbatim into the message by the variable), and the **three campaign messages** shared by every lead in the wave. The engine validates both (`build.py payload`, `build.py newhtml`); these rules are what you write to.

## The three non-negotiables (from the sellers who shaped this skill)

1. **Ask before you send content.** The first touch offers the content and asks if they want it. Getting a reply is the first win, and it avoids the unsolicited PDF. The link is still in the sentence: the lead can click without answering.
2. **Never pitch-slap.** A nurture message is never a pitch. No "we help companies like yours", no feature list, no meeting ask in the first two touches. Social proof is one line, chosen to look like the lead (industry, size), one name, never three.
3. **Pick up where the thread left off.** Quote the lead's own point or their return condition ("you said October", "you mentioned the reply backlog"). A nurture touch that could have been sent to anyone is spam with a delay.

## The sentence on the lead (custom attribute)

One line that completes the message naturally after the variable. Shape:

```
<what it is, in 5-8 words> <why it fits them, in their words>: <URL>
```

Examples that pass:

```
our playbook on turning not-now replies into meetings, it covers the timing point you raised: https://example.com/playbooks/not-now
```
```
a two-page case study from a 20-person agency that had the same reply backlog, numbers included: https://example.com/customers/agency-x
```
```
the checklist we use before launching any campaign, since you mentioned the messy first sends: https://example.com/playbooks/pre-launch
```

Rules the engine enforces (it refuses otherwise): one line, at most 1000 characters (aim for 120 to 200), exactly one URL, nothing glued to the URL (no trailing period), no em or en dash, no `{{token}}`, at most one question, the same URL never twice for a lead. Rules you enforce: lowercase start (it follows the message text), the lead's language, their vocabulary, no marketing words (game-changer, leverage, unlock, best-in-class), no emoji. For a private document (`is_private`), replace the URL with the document's share link the user gives you, or write "happy to send it over" and keep the link to a public landing page.

## The three campaign messages (shared by the wave)

Each message is a frame around one variable. The variable carries everything lead-specific, so the frame must read well with any sentence inserted.

| Touch | Job | Frame |
|---|---|---|
| 1 (week 0) | Re-open and offer | Context in one line (the exchange, the return condition if any) + "if useful, " + `<var name="customAttribute8"/>` + a closing that expects nothing. |
| 2 (week 6) | Prove | "Following up on our exchange" without saying "following up": one observation about their world + `<var name="customAttribute9"/>` + optional one-line social proof. |
| 3 (week 12) | Re-activate, soft door | One line on what changed since + `<var name="customAttribute10"/>` + the only question of the wave, an easy one ("worth a look, or should I leave you be?"). |

LinkedIn messages: 3 to 5 sentences, under 600 characters of text. Email steps also need a subject in `subjectNewHtml` (a single `<p>`): plain, no variable needed.

A frame that passes (touch 1, LinkedIn):

```
<p>Hi <var name="firstname" default="there"/>,</p><p/><p>When we spoke you had other priorities, so no pitch here. If useful, <var name="customAttribute8"/></p><p/><p>Thought of you when it went out, that is all.</p>
```

## newHtml, what the tools accept

The server validates and rejects malformed newHtml. One line, no whitespace between blocks (`</p><p>`, never `</p> <p>`), every text wrapped in `<p>`, `<ul><li>`, or `<h2>`; `<p/>` for a blank line; variables only as `<var name="…"/>` with an optional `default`; inline `<b> <i> <u> <s> <br/>`; escape `<` as `&lt;` and `&` as `&amp;`. **No raw URL in the message body**: the link lives in the sentence on the lead. Standard variables: `firstname`, `lastname`, `company`, `jobTitle`; custom ones `customAttribute1` to `customAttribute20`. Call `get_campaign_messages` on the duplicated campaign first if in doubt about the exact tokens in this account.

## Quality bar (run before showing the wave)

- [ ] Every sentence reads as one person writing to another, in the lead's language
- [ ] The first touch offers, it does not send; no meeting ask before touch 3
- [ ] Each sentence quotes something the lead actually said or asked for
- [ ] No dash, no punctuation on the URL, no template token, no marketing words, no emoji
- [ ] The three frames read well with a short sentence and with a long one
- [ ] Social proof, if any, looks like the lead (industry, size), one name
- [ ] Both validators pass (`payload`, `newhtml`)
