# Landing page rules

Rules that came from real rounds of feedback on landing pages. Each was said or corrected at least once, the most
important three times or more. They win over any copywriting or CRO habit. Rules marked **(default)** are style or
brand preferences: keep them, or change them in your context and in `landings/config.json` (`rules_off`). When a
rule changes, update it in your context with the date, not only in the conversation.

The lint script checks the rules that code can check. The id in brackets is its rule id.

## 1. The page

| Rule | Why or when |
|---|---|
| **One goal**: the primary action (signup, registration, demo request). No links to features, pricing or blog. `[off-goal-link]` | Every other link leaks visitors the ad paid for |
| **Exception: generic pages for cold visitors** may carry feature links as secondary text links at the bottom of blocks, same tab, measured. Never a button, never pricing. Removed after 14 days if they get more clicks than the primary action | A visitor who does not know you yet needs to see what the tool does |
| **Demo: a plain text link under the final form**, never in the header, never the main call to action. **(default)** `[demo-header]` | The demo competes with the signup. Sales-led companies may flip it |
| **Header: the logo is clickable to the home page**, next to the call to action. Never make it non-clickable | A visitor who wants to check who you are must be able to. Removing it was proposed as CRO and refused |
| **Go to the essential.** The idea is understood in a few seconds, one title per section, the problem in one line, no "step by step" section when a 2x2 grid says it | Sales pages that explain everything get skimmed |
| **The page repeats the angle and the promise of the ad**: same message, one action. One page per ad group. The H1 does not change per ad | A visitor who does not find the ad's promise leaves |
| **Search: answer the SERP questions on the page** ("People also ask") and write the query in plain words on the first screen | The visitor came with those questions |
| **Conquest: the visitor who types a competitor's name is looking for an alternative** | The page answers "alternative", not "who we are" |
| **Our style, their substance.** From a colleague's page or a competitor's, take the content, never the style or the sections. Their page leads to features, ours to the primary action | Mixed styles break the page and the brand |
| **Start from your existing landings** (your design system, your components) | Consistency, and fixes made once |
| **A page on a product keyword shows the product name on the first screen**, as a tag above the H1 | The visitor clicked that word: they must see it. The only exception to "no eyebrow" |
| **Calls to action name the offer of the page** ("Try the integration free", "Connect your calendar"), not the same "Start free trial" everywhere | A contextual call to action tells what happens next |
| **Show the result, not a label.** In a "what it does" block, each step shows an example output and the button that approves it, rather than a bullet "waits for your OK" | Showing beats telling |

## 2. Design and rendering

- **Hero**: the email form and the call to action stand out, the trust line under it ("Free trial · No credit card"),
  a proof line (ratings, customer count). Mobile traffic (social ads): capture the email in the hero.
- **Visuals = the product interface recreated in HTML, never a real screenshot.** Invented data, crisp at any size,
  no customer data. Cards may overlap a little, never over text (measure it). **(default)**
- **Cards of the same size, titles aligned and of the same style.** A card that grows too tall is cut to the
  essential. Example texts side by side have the same number of lines.
- **Spacing**: not too much space, equal top and bottom margins, section backgrounds that follow each other cleanly.
- **Center** the section calls to action, the comparison titles, the FAQ and the final form. **(default)**
- **Button hovers are those of your site.** Visitors notice a button that behaves differently.
- **The key anchor call to action** ("See the comparison", "Switch in 4 steps") is visible above the fold, mobile
  included.
- **Section titles in two beats**: a regular part, then a bold part. **H1 on two lines**: the hook on line one, the
  promise on line two. **(default)**
- **No eyebrow above a title** (except the product name of a product keyword page). **(default)** `[eyebrow]`
- **Check desktop and mobile before showing**: broken image, pixelated photo or photo on a white box, icon shown as a
  word, overlap, overflow. Each was caught at least once. `[broken-image]`

## 3. Proof

- **A testimonial is a cut-out photo next to the quote.** No quote without a face.
- **Desktop search traffic**: a logo bar with a result on hover can replace a testimonials block.
- **Ratings shown the same way as on your other pages.** No invented stat banner.
- **No footnotes, sources or disclaimers on the page.** One exception: the date and source of a competitor's price,
  in one line under the comparison table.
- **FAQ: 3 or 4 questions**, centered or at the width of the other sections. It carries box 5 of the arc
  (objections, fear of switching, "what happens after the trial"). `[faq-count]`
- **Reviews quoted word for word**, cut with "[…]", linked to the original review (`target="_blank"
  rel="noopener nofollow"`). `[review-rel]`

## 4. Message

- **Sell the outcome the buyer reports to their boss** (deals, revenue, projects on time), not the mechanism
  (automation, AI). **(default)**
- **Write the query's words** when they are the query ("project tracking software"), but no tag that rings false.
- **Banned phrases** live in `landings/config.json` (`banned_phrases`): typically "all-in-one", "autopilot", "magic",
  "replace your team", a number of integrations. `[banned]`
- **Integration and sync claims**: write exactly what the product does ("native sync", "two-way sync") for each tool,
  never more. `[watch]`
- **The full brand name before the short one.** `[brand-order]`

## 5. Numbers, prices, plans

- **No performance claim** ("3x replies", "50% faster", a support time). A named customer's number goes on the
  landing, never in an ad. `[multiplier-claim]` `[time-claim]`
- **Prices only on pages that compare prices** (conquest). Generic pages: no price, no pricing link.
- **A competitor's price is sourced, dated and checked again** on its public page before each reuse.
- **The currency of the country** of the page. "/seat/month" on both sides if the competitor bills per seat.
  `[wrong-currency]`
- **Never oppose your entry price to a feature of a higher plan.** If you show it, write the condition.
- **No plan names** on the page, except a condition that must sit next to a price. **(default)** `[plan-names]`
- **The offer is the free trial alone**, without a length ("Free trial · No credit card"), without a monthly promo.
  **(default)** `[trial-length]`

## 6. Competitors

- **Search conquest**: the competitor's name is allowed, but every title says the offer is yours.
- **AI-chat ads**: no competitor named.
- **Never quote a competitor review on the page.** Themes only, counted honestly. Neither bugs nor billing.
- **Say what the competitor does well.** It buys credibility.
- **Never present as an advantage what they also have** (check it before writing). **Never attack what turns
  against you** (a cheaper competitor on price).
- **Generic query**: compare by category of tools, name no competitor.

## 7. Writing (the anti-AI checklist)

- **A "wow" effect.** A flat title gets refused. Propose 2-3 strong options from the start.
- **Each sentence says a concrete result.** "Data in. Deals out." says nothing.
- **No colon linking two clauses**: write two sentences (titles, FAQ answers). **(default)** `[colon-heading]`
- **No comma before "and" or "or".** **(default)** `[comma-and-or]`
- **No em dash** `[em-dash]`. **No "No X. No Y. Just Z."** `[no-x-no-y]`. Nothing that sounds AI-written
  (supercharge, unlock, seamless, game-changer, leverage, elevate, empower) `[ai-tells]`.
- **No elliptic punchline.** "The edge moved." sounds good and says nothing (the edge of what, moved where?). Each
  sentence says what it means with its consequence: "Everyone tracks the same signals now, so everyone sends the same
  message."
- **No jargon word repeated.** A vague word used five times ("play") loses the reader. One clear word (playbook,
  workflow, campaign), twice per page at most.
- **Native proofreading** before going live in a language that is not the writer's.

## 8. Way of working

- The user approves the text before it goes into a tool or a visual.
- "Before changing, propose the improvements." In doubt, show before touching.
- **CRO ideas are proposed, not applied.** Rejected in the past: a non-clickable logo, "Already a customer?", "5
  minutes" under the call to action, a review added only for mobile.
- **A V2 never replaces the V1 in the project**: separate file (`index-v1.html`) or folder, switch date noted.
