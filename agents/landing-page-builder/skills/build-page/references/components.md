# Components

The constants of every draft. Copy them, then put the brand on the tokens. Replace `HOME_URL`, `SIGNUP_URL`,
`PROD_HOST`, `SLUG` and `BRAND` with the values of `landings/config.json`.

## Tokens and base (top of `<style>`)

The neutral tokens give a clean page. The brand changes the tokens only.

```css
:root {
  --bg: #FFFFFF; --bg-alt: #F4F3F7; --bg-dark: #16131F;
  --ink: #16131F; --body: #4A4458; --muted: #7A7388; --line: #E4E1EA;
  --on-dark: #FFFFFF; --on-dark-muted: #B9B3C4;
  --action: #1F7A4D; --on-action: #FFFFFF; --accent: #3B5BDB;
  --radius: 14px;
  --font: system-ui, -apple-system, 'Segoe UI', sans-serif;
  --mono: ui-monospace, 'SF Mono', Consolas, monospace;
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { overflow-x: hidden; }
body { font-family: var(--font); background: var(--bg); color: var(--ink); font-size: 16px; line-height: 1.55;
       -webkit-font-smoothing: antialiased; }
a { color: inherit; }
img, svg { display: block; max-width: 100%; }
.wrap { max-width: 1080px; margin: 0 auto; padding: 0 24px; }
.sec { padding: 88px 0; }
.sec.alt { background: var(--bg-alt); }
.head { max-width: 720px; margin: 0 auto 48px; text-align: center; }
.head h2 { font-size: clamp(28px, 4vw, 42px); line-height: 1.1; font-weight: 400; }
.head h2 b { font-weight: 800; }
.head p { color: var(--body); margin-top: 12px; font-size: 17px; }
.sr { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }
.grid > * { min-width: 0; }
```

Section titles in two beats: a regular part and a bold part (`<h2>Why teams switch <b>this quarter</b></h2>`). Default
style rule, change it in your context.

## Buttons

```css
.btn { display: inline-flex; align-items: center; gap: 8px; border-radius: 999px; padding: 12px 22px;
       font-weight: 700; text-decoration: none; border: 1.5px solid transparent; cursor: pointer; font: inherit; }
.btn-action { background: var(--action); color: var(--on-action); }
.btn-action:hover { filter: brightness(1.08); transform: translateY(-1px); }
.btn-line { border-color: var(--line); background: var(--bg); color: var(--ink); }
.tlink { color: var(--muted); text-decoration: underline; font-size: 14px; }
```

Use the hover styles of the user's site when they exist: visitors notice a button that behaves differently.

## Header (conversion page)

```html
<header class="top">
  <div class="wrap top-in">
    <a class="logo" href="HOME_URL" data-nav="logo"><img src="assets/logo.svg" alt="BRAND" height="28"></a>
    <a class="btn btn-action" href="SIGNUP_URL" data-cta="header">Start free trial</a>
  </div>
</header>
```

```css
.top { background: var(--bg-dark); }
.top-in { display: flex; align-items: center; justify-content: space-between; height: 68px; }
```

The logo stays clickable. No demo button in the header: the demo is a text link under the final form.

## Signup form (hero and final call to action)

```html
<form class="trial" id="hero-cta" data-trial="hero" action="SIGNUP_URL" method="get">
  <label class="sr" for="hero-email">Work email</label>
  <input id="hero-email" type="email" name="email" placeholder="Work email" required>
  <button class="btn btn-action" type="submit" data-cta="hero">Start free trial</button>
</form>
<p class="reassure">Free trial · No credit card</p>
```

```css
.trial { display: flex; gap: 8px; background: rgba(255,255,255,.08); padding: 6px; border-radius: 999px;
         border: 1px solid rgba(255,255,255,.18); max-width: 480px; }
.trial input { flex: 1; min-width: 0; border: 0; border-radius: 999px; padding: 12px 16px; font: inherit; }
.reassure { font-size: 13.5px; color: var(--on-dark-muted); margin-top: 10px; }
@media (max-width: 560px) { .trial { flex-direction: column; border-radius: var(--radius); } }
```

The final form uses the same markup with `data-trial="final"`, an `id` of its own and `data-cta="final"`.

## FAQ (accessible accordion)

```html
<section class="sec">
  <div class="wrap">
    <div class="head"><h2>Questions <b>before you start</b></h2></div>
    <div class="faq">
      <div class="fq" data-faq>
        <button class="fq-q" aria-expanded="false">The main objection, in the visitor's words?</button>
        <p class="fq-a" hidden>The answer in two or three plain sentences.</p>
      </div>
      <!-- 3 or 4 items on a conversion page -->
    </div>
  </div>
</section>
```

```css
.faq { max-width: 760px; margin: 0 auto; text-align: left; }
.fq { border-bottom: 1px solid var(--line); }
.fq-q { width: 100%; text-align: left; background: none; border: 0; font: inherit; font-weight: 700;
        padding: 20px 32px 20px 0; cursor: pointer; position: relative; color: var(--ink); }
.fq-q::after { content: '+'; position: absolute; right: 4px; top: 16px; font-size: 22px; color: var(--muted); }
.fq-q[aria-expanded="true"]::after { content: '\2212'; }
.fq-a { color: var(--body); padding-bottom: 20px; }
```

A `<button>` with `aria-expanded` works with a keyboard and survives most site builders' CSS, unlike
`<details>`/`<summary>`.

## Final call to action

```html
<section class="final">
  <div class="wrap">
    <h2>The transformation, <b>in one line</b></h2>
    <p class="sub">The guide again, in one sentence.</p>
    <form class="trial" id="final-cta" data-trial="final" action="SIGNUP_URL" method="get">
      <label class="sr" for="final-email">Work email</label>
      <input id="final-email" type="email" name="email" placeholder="Work email" required>
      <button class="btn btn-action" type="submit" data-cta="final">Start free trial</button>
    </form>
    <p class="demo"><a class="tlink" href="DEMO_URL" data-demo="final">Prefer a demo?</a></p>
  </div>
</section>
```

```css
.final { background: var(--bg-dark); color: var(--on-dark); text-align: center; padding: 88px 0; }
.final .trial { margin: 28px auto 0; }
.final .sub { color: var(--on-dark-muted); margin-top: 12px; }
.final .demo { margin-top: 16px; }
```

## Sticky mobile bar

```html
<div class="sticky" id="sticky" hidden><a class="btn btn-action" href="SIGNUP_URL" data-cta="sticky">Start free trial</a></div>
```

```css
.sticky { position: fixed; left: 0; right: 0; bottom: 0; padding: 10px 16px; background: var(--bg);
          border-top: 1px solid var(--line); text-align: center; z-index: 20; }
@media (min-width: 768px) { .sticky { display: none !important; } }
```

It appears when the hero form leaves the screen (script below).

## Footer (conversion page)

```html
<footer class="foot"><div class="wrap">© BRAND</div></footer>
```

On a page that lives in the site, the site builder provides header and footer: draft a placeholder bar only.

## The script (end of `<body>`)

One script. It carries the UTMs and click ids to every call to action, logs the lead locally and sends nothing outside
production, opens the FAQ, shows the sticky bar. It never sends the email to analytics.

```html
<script>
(function () {
  const SLUG = 'SLUG', LANDING_VERSION = 'SLUG-v1';
  const LOCAL = location.hostname !== 'PROD_HOST';
  const UTM_KEYS = ['utm_source','utm_medium','utm_campaign','utm_term','utm_content',
                    'gclid','gbraid','wbraid','fbclid','li_fat_id','msclkid'];
  const store = 'lp_' + SLUG + '_utms';
  let saved = {};
  try { saved = JSON.parse(sessionStorage.getItem(store) || '{}'); } catch (e) {}
  const qs = new URLSearchParams(location.search);
  UTM_KEYS.forEach(k => { if (qs.get(k)) saved[k] = qs.get(k); });
  try { sessionStorage.setItem(store, JSON.stringify(saved)); } catch (e) {}

  const withParams = (url, extra) => {
    const u = new URL(url, location.href);
    Object.entries(Object.assign({}, saved, extra || {})).forEach(([k, v]) => u.searchParams.set(k, v));
    return u.toString();
  };
  const push = (event, data) => {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({ event, landing_version: LANDING_VERSION }, saved, data || {}));
  };

  document.querySelectorAll('a[data-cta], a[data-demo]').forEach(a => {
    a.href = withParams(a.href);
    a.addEventListener('click', () => push('cta_click', { cta_position: a.dataset.cta || 'demo' }));
  });
  document.querySelectorAll('form[data-trial]').forEach(f => f.addEventListener('submit', e => {
    e.preventDefault();
    const email = f.querySelector('input[type=email]').value.trim();
    const lead = { source: 'lp_' + SLUG, landing_version: LANDING_VERSION, form_position: f.dataset.trial,
                   page_url: location.href, referrer: document.referrer, submitted_at: new Date().toISOString() };
    if (LOCAL) console.log('[' + SLUG + '] lead (local, not sent)', lead);
    // In production, send { email, ...lead, ...saved } to your form endpoint here.
    push('cta_click', { cta_position: f.dataset.trial });
    location.href = withParams(f.action, { email });
  }));
  document.querySelectorAll('[data-faq] .fq-q').forEach(b => b.addEventListener('click', () => {
    const open = b.getAttribute('aria-expanded') === 'true';
    b.setAttribute('aria-expanded', String(!open));
    b.nextElementSibling.hidden = open;
    if (!open) push('faq_open', { faq_question: b.textContent.trim() });
  }));
  const hero = document.getElementById('hero-cta'), sticky = document.getElementById('sticky');
  if (hero && sticky && 'IntersectionObserver' in window) {
    new IntersectionObserver(([e]) => { sticky.hidden = e.isIntersecting; }).observe(hero);
  }
})();
</script>
```

The lead endpoint, the analytics tag and the consent banner belong to the site: whoever publishes wires them
(`{SKILL_BASE}/references/tracking-qa.md`).

## Markup hooks (the lint script and the QA read them)

| Hook | On | Why |
|---|---|---|
| `data-cta="header" / "hero" / "final" / "sticky"` | every signup link and button | UTMs copied, click measured |
| `data-trial="hero" / "final"` + `id="hero-cta"` | the forms | form position in the lead, sticky bar |
| `data-faq` | each FAQ item | FAQ count, `faq_open` event |
| `data-demo="final"` | the demo link | measured apart from the signup |
| `data-nav="logo"` | the logo link | the logo stays clickable |
| `<meta name="robots" content="noindex">` | ads pages only | an ads page stays out of search results |
