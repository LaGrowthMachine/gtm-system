# Collecting the material

The material is what the visitor says and sees before they land: reviews, search results, search terms, questions.
It fills boxes 3, 5 and 7 of the arc with real words. It belongs to the user: save it in their project,
`landings/<slug>/material/`, dated, never in this skill folder.

## What to collect, by page type

| Material | Ads, search | Ads, AI chat or social | SEO | Comparison | Product | Webinar |
|---|---|---|---|---|---|---|
| Your own reviews, 4-5★ | yes | yes | yes | yes | yes | if any |
| Competitors' reviews, 1-3★ | if conquest | neighbours | if the query names a tool | **yes** | if relevant | - |
| SERP and "People also ask" of the 2-3 main queries | **yes** | - | **yes** | yes | if search traffic | - |
| Search terms (if traffic already runs) | **yes** | - | queries of the page in your search console | yes | - | - |
| Contextual hints of the ad, visitor data | - | **yes** | - | - | - | - |
| Support tickets, sales call notes | if you have them | same | same | same | **yes** | - |
| Registration questions, past attendee feedback | - | - | - | - | - | **yes** |
| Competitor's public pricing page | if prices show | - | - | **yes** | - | - |
| Value propositions and product facts | **always** | **always** | **always** | **always** | **always** | **always** |

## Reviews

**Where**: G2, Capterra, Trustpilot, GetApp, app marketplaces (an integration's listing often has the harshest
reviews), the competitor's community forum.

**How**:
1. Your own 4-5★ reviews: they hold the "before" (what customers did before you) and the "after" (box 8). Keep the
   ones from people who look like the hero.
2. Competitors' 1-3★ reviews: they hold box 3. Read 20 to 50, the most recent first.
3. Copy each useful review with its date, its source link, the role and company size when shown. Never the
   reviewer's full name in a file that leaves the user's machine.
4. Tag each review with one theme (a short noun phrase: "no view across boards", "price per seat at scale", "support
   slow to answer"). Create themes as you go, then merge close ones.
5. Count: "theme, number of reviews, out of how many read". The count is what goes on the page ("the most common
   complaint in their reviews"), never the quote.

File: `material/reviews-<source>-<date>.md`, a table `Theme · Verbatim · Rating · Date · Link`.

## Search results

For each of the 2-3 main queries (the ones with the most volume in the group):

1. The top 10 results: type of page (list, guide, product page, forum, video), who ranks, the angle of each.
2. "People also ask": every question, word for word.
3. The ads shown, if any: their promises (what the visitor reads just before your page).
4. What nobody answers: the gap your page fills.

An SEO tool (Ahrefs, Semrush) gives the volume of each keyword and its share of the group. Without one, a manual
search in a private window, set to the target country, does the job for the SERP. Announce the cost before running a
paid tool.

File: `material/serp-<query>-<date>.md`.

## Search terms

If the campaign already runs: the search terms report of the last 30 days, sorted by clicks. Group them by intent and
give each group its share of the volume. Terms that convert tell the hero's words. Terms that waste clicks become
negatives (for whoever runs the campaign).

File: `material/search-terms-<date>.csv` (no personal data in it).

## Forums and communities

Reddit and some forums block automated reading: read them by hand, copy the useful posts with their link and date.
They are often the best source of box 5 (what people say off the record).

## Before moving to the arc

- [ ] Each source dated and linked.
- [ ] Reviews tagged by theme and counted.
- [ ] SERP of the 2-3 main queries captured, with "People also ask".
- [ ] Value propositions read (`landings/value-propositions.md`), product facts at hand.
- [ ] What is missing written down ("box 5: no source yet").
