---
name: choose-channels
description: "Sub-skill of outreach-agent. Picks the channel mix of a campaign (LinkedIn first, email first or both) from the user's own results, the contact data the leads have and the industry of the target, and says why."
---

# Choose the channels

Some people answer on LinkedIn, others by email. This step picks the mix before any message is written, and says
why in two lines. The user can always overrule it.

## Step 1. What the leads allow

From the list of `get-leads`:

- Leads with a LinkedIn URL and no email → LinkedIn only for them, unless the user wants to enrich (it costs
  credits: say how many before).
- Leads with an email and no LinkedIn URL → email only for them.
- Most leads have both → go on.
- No lead has an email and the user does not want to enrich → LinkedIn only. Say it, and stop here.

## Step 2. What the user's own results say

Read the campaigns of the sender identity chosen at Scope (`list_campaigns`, keep `identity.id` = the sender, then
`get_campaign_stats` on those with at least 30 leads contacted, 10 at most, the most recent first). For each, the LinkedIn reply rate
(`replies.linkedinReplied / replies.linkedinContacted`) and the email reply rate
(`replies.emailReplied / replies.emailContacted`).

- **At least 3 campaigns on each channel, and one channel replies 1.5 times more** (pooled: total replies over
  total leads contacted, per channel) → lead with that channel. Say the two rates.
- **Not enough history** → step 3 decides.

When the past campaigns targeted another persona or another industry than this one, say that the history is a hint,
not a proof.

## Step 3. The default by industry

When the history does not decide, take the industry of most leads (the `industry` field, or the target the user
described):

| Industry of the leads | Lead with | Why |
|---|---|---|
| Software, SaaS, tech, startups and scale-ups | LinkedIn, then email | These buyers live on LinkedIn and answer there |
| Agencies (marketing, sales, recruiting), consulting, staffing | LinkedIn, then email | Their job is to be reachable on LinkedIn |
| Financial services, insurance, real estate | Both from the start | Active on LinkedIn, but decisions travel by email |
| Manufacturing, industry, construction, logistics, transport | Email, then LinkedIn | Fewer daily LinkedIn users, the inbox is where work happens |
| Retail, e-commerce operations, hospitality, healthcare, public sector, education | Email, then LinkedIn | Same reason |
| Unknown or mixed | LinkedIn, then email | The general default |

The source can override the table:

| Source | Lead with |
|---|---|
| Post engagers, event attendees, a LinkedIn or Sales Navigator search | LinkedIn: they are active there and the signal lives there |
| A webinar or form list | Email first, the same day or the day after: they gave their email for this |

## Step 4. Say it and move on

Two lines: the mix, and why (the user's rates, or the industry, or the source). For example: "LinkedIn first, then
email. Your LinkedIn campaigns reply at 18% against 4% by email." Then go on to the sequence. If the user disagrees,
take their mix without discussion.

## Rules

- Ask the question on LinkedIn, use email to deliver, remind or answer (the `copywriting` rules).
- A LinkedIn step needs a connection first: plan the invitation, then the message after acceptance.
- Never plan more than one channel touch on the same day for the same lead.
