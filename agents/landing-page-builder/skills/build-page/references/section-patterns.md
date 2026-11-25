# Section patterns

The blueprints of the sections between the header and the final call to action. They use the tokens and classes of
`components.md`. Each pattern says which box of the arc it carries. The copy comes from the validated structure.

## 1. Hero (angle + guide, box 6)

```html
<section class="hero">
  <div class="wrap hero-grid grid">
    <div>
      <h1>The hook on line one.<br><b>The promise on line two.</b></h1>
      <p class="kick">The main query in plain words (search pages)</p>
      <p class="lede">The guide in one sentence: what the visitor gets, not what the product is.</p>
      <!-- signup form + reassurance line of components.md -->
      <p class="proof-line">4.7/5 on G2 · 2,000+ teams</p>
    </div>
    <div class="hero-visual" aria-hidden="true">
      <!-- the product interface that shows the promise, recreated in HTML with invented data -->
    </div>
  </div>
</section>
```

```css
.hero { background: var(--bg-dark); color: var(--on-dark); padding: 72px 0 88px; position: relative; }
.hero::before { content: ''; position: absolute; inset: 0; pointer-events: none;
  background-image: radial-gradient(rgba(255,255,255,.07) 1px, transparent 1px); background-size: 22px 22px; }
.hero-grid { display: grid; grid-template-columns: 1.05fr .95fr; gap: 48px; align-items: center; position: relative; }
.hero h1 { font-size: clamp(32px, 5vw, 56px); line-height: 1.12; font-weight: 400; }
.hero h1 b { font-weight: 800; }
.kick { margin-top: 14px; font-weight: 700; color: var(--on-dark); }
.lede { margin: 12px 0 24px; color: var(--on-dark-muted); font-size: 18px; max-width: 520px; }
.proof-line { margin-top: 18px; font-size: 14px; color: var(--on-dark-muted); }
```

- H1 on two lines: the hook, then the promise. 2-3 strong options were validated in the arc: use the chosen one.
- Subline: 15 to 25 words, outcome first.
- The form sits above the fold on desktop and on a 375px phone.
- Visual: the interface that proves the promise. Cards may overlap a little, never over text.

## 2. Problem, or before and after (boxes 3 and 4)

One line of problem is often enough. When the contrast carries the arc, two columns:

```html
<section class="sec">
  <div class="wrap">
    <div class="head"><h2>Where the work <b>gets stuck today</b></h2></div>
    <div class="ba grid">
      <div class="ba-col before"><h3>Without it</h3><ul><li>A symptom the visitor sees this week</li></ul></div>
      <div class="ba-col after"><h3>With it</h3><ul><li>The same line, solved</li></ul></div>
    </div>
  </div>
</section>
```

```css
.ba { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.ba-col { border-radius: var(--radius); padding: 24px; }
.ba-col.before { background: var(--bg-alt); border: 1px solid var(--line); }
.ba-col.after { background: var(--bg-dark); color: var(--on-dark); }
.ba-col li { list-style: none; padding: 12px 0; border-top: 1px solid var(--line); }
```

Lines in the two columns run in parallel: each "without" line has its "with" line. Symptoms come from box 3, in the
visitor's words.

## 3. Pillars or use cases, cards grid (boxes 4 to 6)

```html
<section class="sec alt">
  <div class="wrap">
    <div class="head"><h2>What changes <b>for your team</b></h2></div>
    <div class="cards grid">
      <article class="card">
        <div class="card-ui" aria-hidden="true"><!-- a small interface that shows the result --></div>
        <h3>An outcome as the card title</h3>
        <p>Two sentences: what the visitor does, what they get.</p>
      </article>
      <!-- 4 cards at most, in the order of the hero's work -->
    </div>
  </div>
</section>
```

```css
.cards { display: grid; grid-template-columns: repeat(2, 1fr); grid-auto-rows: 1fr; gap: 18px; }
.card { background: var(--bg); border: 1px solid var(--line); border-radius: var(--radius); padding: 24px; }
.card h3 { font-size: 18px; margin: 16px 0 8px; }
.card p { color: var(--body); font-size: 15px; }
```

Cards have the same height (`grid-auto-rows: 1fr`), titles of the same style, and example texts of the same number of
lines. A card that grows too tall is cut to the essential. Show the result (an output and the button that approves it)
rather than a label.

## 4. Comparison table (boxes 4 and 7)

Two forms. Against one competitor (conquest page): one row per criterion, the competitor's column honest, the price
sourced and dated in one line under the table. Against categories of tools (generic query): one column per category,
no competitor named.

```html
<div class="cmp-wrap"><table class="cmp">
  <thead><tr><th></th><th>Rivalboard</th><th class="us">Acme Projects</th></tr></thead>
  <tbody><tr><th>Shared owners across projects</th><td>Per board only</td><td class="us">Across every board</td></tr></tbody>
</table></div>
<p class="cmp-src">Rivalboard pricing from its public page, checked on 2026-11-02.</p>
```

```css
.cmp-wrap { overflow-x: auto; }
.cmp { width: 100%; border-collapse: collapse; min-width: 560px; }
.cmp th, .cmp td { padding: 14px 16px; border-bottom: 1px solid var(--line); text-align: left; }
.cmp .us { background: var(--bg-alt); font-weight: 700; }
.cmp-src { font-size: 13px; color: var(--muted); margin-top: 10px; text-align: center; }
```

Say what the competitor does well: it buys credibility. Never claim as an advantage what they also have.

## 5. Proof (box 7)

- **Logo bar with a number**: "Used by 2,000+ teams" does the work, a bare row of logos does not. 6 to 9 logos,
  grey by default, color on hover. On desktop traffic, a result per logo on hover can replace a testimonial block.
- **Review quoted word for word**, cut with "[…]", linked to its source (`target="_blank" rel="noopener nofollow"`).
- **Story**: a cut-out photo next to the quote, the role and company, one outcome. No quote without a face.
- No invented stat banner, no footnotes.

```html
<figure class="story">
  <img src="assets/customer.png" alt="Head of Operations at a logistics company">
  <blockquote>"We stopped chasing status updates […] the board tells us."</blockquote>
  <figcaption>Head of Operations, a 60-person logistics company</figcaption>
</figure>
```

## 6. Steps (box 8)

For a switch from a competitor or a setup the visitor fears: 3 or 4 steps, each a verb and a result, an anchor `id`
the hero can link to ("Switch in 4 steps"). Not when a 2x2 grid already says it.

## 7. Install block (installable products only)

When the product installs by a command or a connector URL, the hero holds the install with tabs (most used method
first), a copyable block that flashes "Copied!", and the trust line under it (read-only mode, confirmation before
writes, account needed with a link to sign up). Every later button anchors to `#install`, with an up arrow when the
install is above.

## 8. Responsive (end of `<style>`)

```css
@media (max-width: 900px) {
  .hero-grid, .ba, .cards { grid-template-columns: 1fr; }
  .sec, .final { padding: 56px 0; }
}
@media (max-width: 560px) {
  .hero h1 { font-size: clamp(28px, 9vw, 38px); }
}
```

Use the breakpoints of the user's site builder when the page will be rebuilt there.
