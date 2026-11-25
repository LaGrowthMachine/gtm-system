# `landings/config.json`

The settings of the user's brand that the lint script reads. Write it at step 1 from
`{SKILL_BASE}/scripts/config.example.json`. Every key is optional: without a key, the check that needs it is skipped
or stays generic. Command-line flags win over the file.

## Keys

| Key | Type | What it does | Example |
|---|---|---|---|
| `brand` | text | Full brand name | `"Acme Projects"` |
| `brand_short` | text | Short form, never before the full name | `"Acme"` |
| `currency` | `$`, `€` or `£` | Currency of the page: a price in another currency is an ERROR | `"$"` |
| `plan_names` | list | Plan names: a WARNING when one appears outside a price condition | `["Starter", "Team"]` |
| `banned_phrases` | list | Phrases never written: ERROR | `["all-in-one", "autopilot"]` |
| `watch_phrases` | list | Phrases to check each time: WARNING | `["two-way sync"]` |
| `signup_url_prefix` | URL | Where the primary action leads. The page must link to it | `"https://app.acme.example/signup"` |
| `home_url` | URL | The home page, allowed as a link (the logo) | `"https://acme.example/"` |
| `allowed_link_prefixes` | list | Other links allowed without a WARNING (demo page) | `["https://acme.example/demo"]` |
| `production_host` | text | The live host. The script must test it so a local copy sends nothing | `"acme.example"` |
| `lead_endpoint` | text | The form endpoint, when the draft already wires it | `""` |
| `page_type` | `ads`, `seo` or `other` | `ads`: noindex required. `seo`: noindex forbidden, meta description expected | `"ads"` |
| `max_faq` | number | FAQ questions before a WARNING | `4` |
| `rules_off` | list | Rule ids switched off | `["comma-and-or"]` |
| `severity` | object | Rule id → `ERROR` or `WARNING` | `{"comma-and-or": "ERROR"}` |
| `design` | object | The brand for the draft (not read by the script) | `{"action": "#1F7A4D", "font": "Inter", "logo": "assets/logo.svg"}` |

Review sites (G2, Capterra, Trustpilot, GetApp), anchors (`#...`) and `mailto:` links are always allowed.

## Rule ids of `lint_landing.py`

| Id | Severity | What it checks |
|---|---|---|
| `em-dash` | ERROR | An em dash in the visible text |
| `spaced-en-dash` | ERROR | An en dash between spaces (an em dash in disguise) |
| `comma-and-or` | WARNING | A comma before "and" or "or" (default style) |
| `trial-length` | ERROR | A trial length ("14-day trial") (default offer rule) |
| `multiplier-claim` | WARNING | An "Nx" claim |
| `time-claim` | WARNING | A time promise ("in under 5 minutes", "within 2 hours") |
| `ai-tells` | WARNING | Words that sound AI-written (supercharge, unlock, seamless...) |
| `no-x-no-y` | WARNING | The "No X. No Y. Just Z." pattern |
| `placeholder` | ERROR | `{{...}}`, `[topic]`, TODO, TBD, lorem ipsum left in the copy |
| `banned` / `watch` | ERROR / WARNING | The phrases of the config |
| `plan-names` | WARNING | A plan named outside a price condition |
| `wrong-currency` | ERROR / WARNING | A price, or an amount, in another currency |
| `colon-heading` | ERROR | A colon in an H1, H2 or H3 (default style) |
| `one-h1` | ERROR | Not exactly one H1 |
| `title` | WARNING | No `<title>` |
| `brand-order` | WARNING | The short brand before the full one |
| `eyebrow` | WARNING | A class `eyebrow`, `kicker` or `overline` (default style) |
| `cta` | ERROR | No call to action, or the signup URL of the config missing |
| `email-form` | WARNING | No email field |
| `demo-header` | WARNING | A demo link in the header |
| `off-goal-link` | WARNING | A link outside the allowed list |
| `review-rel` | WARNING | A review link without `rel="noopener nofollow"` |
| `faq-count` | WARNING | More FAQ items (`data-faq`) than `max_faq` |
| `noindex` | ERROR | Ads page without noindex, or SEO page with it |
| `meta-description` | WARNING | SEO page without a meta description |
| `utm` | WARNING | No UTM handling in the scripts |
| `landing-version` | WARNING | No `landing_version` |
| `local-guard` | ERROR | The production host is not tested in the scripts |
| `lead-endpoint` | ERROR | The lead endpoint of the config is missing |
| `email-in-datalayer` | ERROR | The email pushed to the analytics data layer |
| `broken-image` | ERROR | A local image file that does not exist |
| `img-alt` | WARNING | An image without alt text |
| `competitor-count` | WARNING | With `--competitor`: the name appears fewer than 3 times |

## Example

See `{SKILL_BASE}/scripts/config.example.json`.
