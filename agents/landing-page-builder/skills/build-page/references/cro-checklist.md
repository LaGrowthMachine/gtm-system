# CRO checklist

Check every line before delivering a draft. The structure step uses it too, to check a structure before the user
approves it. These patterns come from real iterations on production pages: skipping them costs conversions. Where a
line and the master's `references/rules.md` disagree, `rules.md` wins.

## Goal and calls to action

- [ ] **One goal.** Every button leads to the primary action. No links to features, pricing or blog on a conversion
      page (a generic page for cold visitors may carry secondary text links, measured).
- [ ] **The primary action has an `id` in the hero** (`hero-cta`, `install`, `register`). Lower buttons anchor back to
      it, except the final call to action, which repeats the form.
- [ ] **The final call to action is there**, before the footer, dark like the hero: title = the transformation, the
      form, a discreet demo link under it.
- [ ] **The call to action names the offer of the page** ("Try the integration free", "Register for the session"),
      not a generic "Submit".
- [ ] **Arrows point the right way.** Up when the target is above, down when it is below.
- [ ] **The key anchor call to action** ("See the comparison", "4 steps to switch") is visible above the fold, on
      mobile too.

## Copy

- [ ] **The visitor understands the idea in a few seconds.** One title per section, the problem in one line.
- [ ] **H1 on two lines**: the hook, then the promise. It matches the promise of the ad or the query word for word.
- [ ] **The query is written in plain words on the first screen** (search pages).
- [ ] **Outcomes, not mechanisms.** "See which project slips before Friday" beats "Save time" or "Boost productivity".
- [ ] **Every sentence says a concrete result.** No elliptic punchline that sounds good and says nothing.
- [ ] **No em dash, no "No X. No Y. Just Z.", nothing that sounds AI-written.**
- [ ] **Card titles are outcomes** ("Know who owns what"), not features ("Ownership module").

## Trust

- [ ] **Trust line right under the primary action**: "Free trial · No credit card" or its equivalent, not scattered
      across the FAQ.
- [ ] **What the visitor needs before acting is said in the hero** (an account, a plan, a tool), with the link to get
      it.
- [ ] **No claim the product facts do not back**: no invented rate, no "Nx", no setup or support time unless proven.

## Proof

- [ ] **The logo bar has a number.** 6 to 9 real logos, grey by default.
- [ ] **Quotes come with a face, a role and a link to the source.**
- [ ] **The proof looks like the visitor** (same role, same size of company). Prestigious logos with no link to the
      visitor do little.

## Cards and sections

- [ ] **4 cards at most.** Beyond that, choice paralysis.
- [ ] **Cards of the same height**, titles aligned, example texts of the same number of lines.
- [ ] **Alternating backgrounds.** Never two consecutive sections of the same color without a clear visual break.
- [ ] **Every section carries a box of the arc.**

## FAQ

- [ ] **3 or 4 questions on a conversion page**, 6 at most on a product or hub page.
- [ ] **It carries box 5 of the arc**: the main objection, the fear of switching, "what happens after the trial", one
      SERP question.
- [ ] **Order**: what it is → what it does → is it safe → what it costs.
- [ ] **Centered** or at the width of the other sections.

## Rendering

- [ ] **Desktop (1366px) and mobile (375px) checked**: no horizontal scroll, no broken image, no pixelated photo, no
      icon showing as a word, nothing overlapping, nothing overflowing.
- [ ] **The hero form is above the fold** on both.
- [ ] **Animated visual**: the capture waits for the end of the cycle; `prefers-reduced-motion` shows the final state.

## Common mistakes (real examples)

1. **No visible primary button in the hero.** Visitors skimmed past install steps. Fix: a clear action button.
2. **An eyebrow tag that steals the eye from the H1** and adds nothing. Removed, the hero got cleaner.
3. **"Save time" framing.** Switch to what the visitor sees: "Stop running projects on guesses."
4. **6 cards.** Cut to 4 plus a "see all" link: engagement went up.
5. **A left-aligned FAQ on a centered page.** Visual incoherence.
6. **Trust signals scattered** across the FAQ and the subline. Grouped under the form, where the decision happens.
7. **Logos without a number.** "Used by 2,000+ teams" does the work.
8. **A CRO idea applied without asking.** Propose the list, the user picks: many good-looking ideas get rejected for
   reasons the page owner knows.
