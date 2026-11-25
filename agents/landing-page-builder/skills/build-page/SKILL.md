---
name: build-page
description: "Sub-skill of landing-page-builder. Writes the validated landing as one self-contained HTML draft (header, hero with form, sections of the validated structure, FAQ, final call to action, tracking hooks) with the user's brand or a clean neutral style, then checks it against the CRO checklist. Runs after the arc and the structure are approved."
---

# Build page

The step "the page as a local HTML draft" of Landing Page Builder. It turns the validated arc and structure into one
HTML file that a person can open in a browser, read, click and check on a phone. It does not decide the message: the
arc and the structure already did. It does not publish: the master hands over at the end.

## Before you start

You need, from the master:

| Input | Where |
|---|---|
| The validated arc (angle, H1, guide, proofs) | `landings/<slug>/arc.md` |
| The validated structure (`# · Section · Arc box · Content · Taken from`) | `landings/<slug>/arc.md`, section "Structure" |
| The page type (ads, SEO, product, webinar, comparison, case study) | the arc file |
| The primary action (signup form, demo form, registration, install command) | the arc file, "Angle" row |
| Brand, signup URL, allowed links | `landings/config.json` |

If one is missing, go back to the master step that produces it. Do not ask the brief questions again: the master
gathered them.

## The brand

1. Read the brand from `{SKILL_BASE}/context/offer.md` or `landings/config.json` (key `design`: colors, font, logo).
   If it is not there, ask once for the main color, the action color, the font and the logo file, then save the
   answer in `landings/config.json` under `design`.
2. Put the brand on the tokens of `references/components.md`. Nothing else changes.
3. Without a brand, keep the neutral tokens of `references/components.md`: a clean, readable page. A designer will
   restyle it, the copy and the structure stay.

## Build

1. Say the plan in 4 to 6 lines: page type, sections in order (from the validated structure), primary action and
   where it repeats. No HTML yet.
2. Read, in this order:
   - `references/page-anatomy.md`: the section stack of the page type, to check the structure misses nothing required.
   - `references/components.md`: tokens, header, form, FAQ, final call to action, sticky mobile bar, tracking script.
   - `references/section-patterns.md`: hero, before and after, cards grid, comparison table, proof, steps.
3. Write the page in one shot to `landings/<slug>/index.html`: one file, CSS in one `<style>`, JS in one `<script>`
   at the end, no external CSS or font imports, images in `landings/<slug>/assets/`. The copy is the validated copy,
   word for word: this step never rewrites the message.
4. Keep the markup hooks of `references/components.md` (`data-cta`, `data-trial`, `id="hero-cta"`, `data-faq`): the
   lint script and the QA read them.
5. Visuals: the product interface recreated in HTML and CSS with invented data, never a real screenshot with real
   customer data. Cards that overlap a little are fine, never over text.
6. Check against `references/cro-checklist.md`, then give the user the `file://` path or the local preview URL and a
   capture of the hero at desktop and mobile widths.

The landing rules of the master (`{SKILL_BASE}/references/rules.md`) win over this sub-skill when they disagree.

## Common follow-ups

| Request | Do |
|---|---|
| "Make the hero bigger" | H1 up one step of the scale, hero padding up by a third |
| "Add a testimonial" | Testimonial pattern of `section-patterns.md`, a real quote with a face, linked to its source |
| "Show me the source" | Return the HTML of the section asked, not the whole page |
| "New version" | Copy `index.html` to `index-v1.html` first, then edit, then raise `landing_version` |
