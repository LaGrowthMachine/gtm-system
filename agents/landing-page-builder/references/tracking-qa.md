# Tracking and QA checklist

A checklist for whoever builds and publishes the page: the designer, the site builder owner or the user. Copy it into
`landings/<slug>/HANDOVER.md`. The HTML draft already carries the script of
`{SKILL_BASE}/skills/build-page/references/components.md`: it shows the contract to keep in the live page.

## The tracking contract

| Element | What the live page must do |
|---|---|
| UTMs and click ids | Read from the URL: `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `utm_content` and the click ids of each platform (`gclid`, `gbraid`, `wbraid`, `fbclid`, `li_fat_id`, `msclkid`, and any id an AI-chat ad platform adds). Keep them for the session (sessionStorage) |
| Carried to the signup | Copied on every call to action link and on the action of every form, so the signup page and the CRM receive them |
| Email prefill | The form adds `?email=` to the signup URL when the signup page can prefill it |
| Lead | The form sends to the endpoint of your site: email, `source = lp_<slug>`, `landing_version = <slug>-vN`, form position, page URL, referrer, submitted at, the UTMs |
| Analytics events | `cta_click` {position} · `faq_open` {question} · `review_click`, each with `landing_version` and the UTMs. **Never the email** |
| Local guard | Outside the production host (local file, staging, preview), nothing is sent: the lead is logged in the console |
| Indexing | Ads page: `noindex`, out of the sitemap, no canonical to another page. SEO page: indexed, with a canonical to itself |

## QA before showing (local draft)

Open the draft with test parameters, for example
`index.html?utm_source=google&utm_medium=paid_search&utm_campaign=test&gclid=TEST`.

1. `lint_landing.py` with no ERROR.
2. Desktop 1366×860 and mobile 375 wide: capture the hero, then each section.
3. No horizontal scroll:
   `document.documentElement.scrollWidth === document.documentElement.clientWidth`
4. Hero form above the fold:
   `document.querySelector('#hero-cta').getBoundingClientRect().bottom < innerHeight`
5. Cards of the same height, titles not cut: for each card, `offsetHeight === scrollHeight`.
6. UTMs carried to the signup:
   ```js
   document.querySelector('a[data-cta=header]').href   // holds utm_* and gclid
   ```
   Submit the hero form with a test email: the signup URL holds the email, the UTMs and the click id. Same for the final
   form.
7. Console: `[<slug>] lead (local, not sent)` with the right `source` and `landing_version`. No error.
8. Images loaded: `[...document.images].filter(i => !i.naturalWidth)` is empty. Icons show as icons, not as words.
9. Animated visual: capture after the end of the cycle (6-7 s). `prefers-reduced-motion` shows the final state.

## Publishing (in your site builder)

1. Duplicate an existing page of the same kind when you have one: it keeps the folder, the indexing settings and the
   absence of navigation on ads pages.
2. Rebuild the sections with your site's components, or paste the draft's HTML, CSS and script in a custom code block
   when your builder allows it.
3. Wire the lead endpoint, the analytics tag and the consent banner of the site.
4. SEO fields: title `<promise> | <brand>` (about 60 characters), meta description (150 to 200 characters, ends with
   the offer line), social preview = SEO. Indexing as in the contract above.
5. Preview, then publish.

## After publishing (5 minutes later)

- [ ] The production URL with UTMs and a test click id (`gclid=TEST`, `fbclid=TEST`) shows the right H1.
- [ ] Icons show as icons, no word in their place.
- [ ] Mobile: no horizontal scroll, the sticky bar shows.
- [ ] The header, the hero form and the final form lead to the signup with the email, the UTMs and the click id.
- [ ] The analytics debugger shows `cta_click` without the email.
- [ ] A test lead (throwaway email) reaches the endpoint with `source` and `landing_version`.
- [ ] The date and time the page went live are written in the README of the page.
- [ ] Your analytics tool masks emails in URLs (the signup URL carries `?email=`): set it once.
