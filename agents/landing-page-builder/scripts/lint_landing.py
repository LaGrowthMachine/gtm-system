#!/usr/bin/env python3
"""Check a landing page draft before you show it to anyone.

    python3 -I lint_landing.py landings/<slug>/index.html [--config landings/config.json] [--type ads|seo|other]
        [--brand "Acme"] [--competitor Rivalboard] [--currency '$'] [--banned "all-in-one"] [--off rule-id]

ERROR   = a settled rule. Fix it before showing the page (exit code 1).
WARNING = look at it. It is sometimes legitimate: say so when you show the page.

The copy checked is the visible text (tags, <style> and <script> removed) plus the strings of the scripts that are
displayed (animated threads and the like). Settings come from landings/config.json (see references/config.md), then
from the flags, which win. Standard library only.
"""
import argparse
import html as htmlmod
import json
import os
import re
import sys

# (id, pattern, severity, message). Case-insensitive, applied to each line of visible text.
COPY_RULES = [
    ('em-dash', r'—', 'ERROR', 'em dash: write two sentences or use a comma'),
    ('spaced-en-dash', r'\s–\s', 'ERROR', 'en dash between spaces is an em dash in disguise (fine inside a range like 16–20)'),
    ('comma-and-or', r',\s+(and|or)\b', 'WARNING', 'comma before and / or (default style rule)'),
    ('trial-length', r'\b\d{1,2}[- ]days?\b[^.]{0,25}\btrial\b|\btrial\b[^.]{0,25}\b\d{1,2}[- ]days?\b',
     'ERROR', 'trial length on the page: the default offer line is "Free trial · No credit card"'),
    ('multiplier-claim', r'\b\d+(\.\d+)?\s?x\b(?![-\w])', 'WARNING',
     '"Nx" claim: on a landing only when a named customer said it, never in an ad'),
    ('time-claim', r'\b(in|within|under|less than)\s+\d+\s?(min(ute)?s?|h|hours?|hrs?)\b|<\s?\d+\s?h\b', 'WARNING',
     'time promise (setup time, support time): only if your product facts back it'),
    ('ai-tells', r'\b(game[- ]chang\w*|supercharg\w*|unlock\w*|seamless(ly)?|effortless(ly)?|leverag\w*|revolutioni[sz]\w*|'
     r'delve|elevate|empower\w*|cutting[- ]edge|next[- ]level|unleash\w*|harness\w*|in today.s fast[- ]paced)\b',
     'WARNING', 'phrase that sounds AI-written or like an ad: rewrite it in plain words'),
    ('no-x-no-y', r'\bNo\s[^.!?]{1,40}[.!]\s+No\s[^.!?]{1,40}[.!]\s+(Just|Only)\b', 'WARNING',
     '"No X. No Y. Just Z." pattern: sounds AI-written'),
    ('placeholder', r'\{\{|\}\}|\bTODO\b|\bTBD\b|\bXXX\b|lorem ipsum|\[(insert|placeholder|topic|company|name)[^\]]*\]'
     r'|<[a-z][\w -]{0,30}>', 'ERROR', 'placeholder left in the copy'),
]

AUTO_SEVERITY = {'ERROR', 'WARNING'}
REVIEW_SITES = r'https://(www\.)?(g2\.com|capterra\.[a-z.]+|trustpilot\.com|[a-z]{2}\.trustpilot\.com|getapp\.com)/'
CURRENCIES = {'$': r'\$', '€': '€', '£': '£'}


def load_config(path):
    if path is None and os.path.isfile(os.path.join('landings', 'config.json')):
        path = os.path.join('landings', 'config.json')
    if not path:
        return {}
    try:
        with open(path, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError) as e:
        sys.exit('cannot read the config %s: %s' % (path, e))


def phrase_pattern(p):
    return r'(?<![\w-])' + re.escape(p) + r'(?![\w-])'


def visible_text(src):
    """Visible text line by line (line numbers kept) plus the displayed strings of the scripts."""
    blank = lambda m: '\n' * m.group(0).count('\n')
    no_style = re.sub(r'<style.*?</style>', blank, src, flags=re.S | re.I)
    no_comments = re.sub(r'<!--.*?-->', blank, no_style, flags=re.S)
    script_strings = []
    for m in re.finditer(r'<script[^>]*>(.*?)</script>', no_comments, flags=re.S | re.I):
        start = no_comments[:m.start()].count('\n') + 1
        for i, line in enumerate(m.group(1).split('\n')):
            if re.match(r'\s*//', line):
                continue
            for s in re.findall(r"'((?:[^'\\]|\\.){12,})'|\"((?:[^\"\\]|\\.){12,})\"", line):
                s = s[0] or s[1]
                if ' ' in s and not re.search(r'[{}();=]|https?:|^[\w.-]+$', s):
                    script_strings.append((start + i, re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', s)).strip()))
    no_script = re.sub(r'<script.*?</script>', blank, no_comments, flags=re.S | re.I)
    lines = []
    for i, line in enumerate(no_script.split('\n'), 1):
        t = htmlmod.unescape(re.sub(r'<[^>]+>', ' ', line))
        if t.strip():
            lines.append((i, re.sub(r'\s+', ' ', t).strip()))
    return lines + script_strings


def main():
    ap = argparse.ArgumentParser(description='Check a landing page draft.')
    ap.add_argument('file')
    ap.add_argument('--config', help='JSON settings (default: landings/config.json when it exists)')
    ap.add_argument('--type', choices=['ads', 'seo', 'other'],
                    help='ads: noindex required; seo: noindex forbidden and a meta description expected')
    ap.add_argument('--brand', help='full brand name')
    ap.add_argument('--brand-short', help='short form of the brand, never before the full name')
    ap.add_argument('--competitor', help='competitor this page attacks (conquest page)')
    ap.add_argument('--currency', help='currency of the page: $, € or £')
    ap.add_argument('--banned', action='append', default=[], help='banned phrase (repeat)')
    ap.add_argument('--off', action='append', default=[], help='rule id to switch off (repeat)')
    a = ap.parse_args()

    cfg = load_config(a.config)
    brand = a.brand or cfg.get('brand', '')
    brand_short = a.brand_short or cfg.get('brand_short', '')
    currency = a.currency or cfg.get('currency', '')
    banned = list(cfg.get('banned_phrases', [])) + a.banned
    watch = list(cfg.get('watch_phrases', []))
    plans = list(cfg.get('plan_names', []))
    off = set(cfg.get('rules_off', [])) | set(a.off)
    sev_over = {k: v.upper() for k, v in cfg.get('severity', {}).items() if v.upper() in AUTO_SEVERITY}
    allowed = list(cfg.get('allowed_link_prefixes', []))
    signup = cfg.get('signup_url_prefix', '')
    if signup:
        allowed.append(signup)
    home_exact = {'/', cfg.get('home_url', '')} - {''}
    max_faq = int(cfg.get('max_faq', 4))
    page_type = a.type or cfg.get('page_type', 'other')

    try:
        src = open(a.file, encoding='utf-8').read()
    except OSError as e:
        sys.exit('cannot read %s: %s' % (a.file, e))
    base_dir = os.path.dirname(os.path.abspath(a.file))
    out = []

    def add(rule, sev, line, msg, ctx=''):
        if rule in off:
            return
        out.append((sev_over.get(rule, sev), line, '[%s] %s' % (rule, msg), ctx))

    text = visible_text(src)
    flat = ' '.join(t for _, t in text)

    for ln, t in text:
        for rule, pat, sev, msg in COPY_RULES:
            m = re.search(pat, t, 0 if rule in ('em-dash', 'spaced-en-dash', 'placeholder') else re.I)
            if m:
                add(rule, sev, ln, msg, t[max(0, m.start() - 35):m.end() + 35])
        for p in banned:
            m = re.search(phrase_pattern(p), t, re.I)
            if m:
                add('banned', 'ERROR', ln, 'banned phrase "%s" (config)' % p, t[max(0, m.start() - 35):m.end() + 35])
        for p in watch:
            m = re.search(phrase_pattern(p), t, re.I)
            if m:
                add('watch', 'WARNING', ln, 'phrase to watch "%s" (config)' % p, t[max(0, m.start() - 35):m.end() + 35])
        for p in plans:
            if re.search(r'\b' + re.escape(p) + r'\s+(plan|plans|tier)\b|\b(on|from|with)\s+(the\s+)?' + re.escape(p) + r'\b', t, re.I):
                add('plan-names', 'WARNING', ln, 'plan named "%s": only as a condition right next to a price' % p, t[:90])
        if currency in CURRENCIES:
            for sym, rx in CURRENCIES.items():
                if sym == currency:
                    continue
                if re.search(rx + r'\s?\d[\d,.]*\s*(/|per |a )\s*(mo|month|seat|user|year|yr)', t, re.I):
                    add('wrong-currency', 'ERROR', ln, 'price in %s on a page in %s' % (sym, currency), t[:90])
                elif sym in t:
                    add('wrong-currency', 'WARNING', ln, 'amount in %s on a page in %s (customer figure or mockup?)' % (sym, currency), t[:90])

    # Headings
    for m in re.finditer(r'<(h[1-3])[^>]*>(.*?)</\1>', src, re.S | re.I):
        ln = src[:m.start()].count('\n') + 1
        t = htmlmod.unescape(re.sub(r'<[^>]+>', ' ', m.group(2))).strip()
        if ':' in t:
            add('colon-heading', 'ERROR', ln, 'colon in a heading: write a sentence', t)
    n_h1 = len(re.findall(r'<h1[\s>]', src, re.I))
    if n_h1 != 1:
        add('one-h1', 'ERROR', 0, 'exactly one H1 expected (found %d)' % n_h1)
    if not re.search(r'<title>[^<]{5,}</title>', src, re.I):
        add('title', 'WARNING', 0, 'no <title>: write the promise and the brand (about 60 characters)')
    if brand_short and brand:
        s = re.search(r'\b' + re.escape(brand_short) + r'\b', flat)
        f = re.search(re.escape(brand), flat)
        if s and (not f or s.start() < f.start()):
            add('brand-order', 'WARNING', 0, '"%s" appears before "%s"' % (brand_short, brand))
    if re.search(r'class="[^"]*\b(eyebrow|kicker|overline)\b', src):
        add('eyebrow', 'WARNING', 0, 'eyebrow above a heading (default style rule: none, except a product name the visitor searched)')

    # Goal and conversion
    links = [(src[:m.start()].count('\n') + 1, m.group(1)) for m in re.finditer(r'<a\s[^>]*href="([^"]*)"', src, re.I)]
    actions = re.findall(r'<form[^>]*action="([^"]*)"', src, re.I)
    has_cta = 'data-cta' in src or re.search(r'<form', src, re.I) or (signup and any(h.startswith(signup) for _, h in links))
    if not has_cta:
        add('cta', 'ERROR', 0, 'no call to action found (a form, a data-cta link or a link to the signup URL)')
    if signup and not any(h.startswith(signup) for _, h in links) and not any(x.startswith(signup) for x in actions) \
            and signup not in src:
        add('cta', 'ERROR', 0, 'the signup URL of the config (%s) is nowhere on the page' % signup)
    if not re.search(r'<input[^>]*type="email"', src, re.I):
        add('email-form', 'WARNING', 0, 'no email field: the hero captures the email (default rule)')
    header = re.search(r'<header.*?</header>', src, re.S | re.I)
    if header and re.search(r'demo', header.group(0), re.I):
        add('demo-header', 'WARNING', src[:header.start()].count('\n') + 1,
            'demo in the header: the default is a plain link under the final form')
    for ln, h in links:
        if h.startswith('#') or h.startswith('mailto:') or h in home_exact or re.match(REVIEW_SITES, h):
            continue
        if not any(h.startswith(p) for p in allowed):
            add('off-goal-link', 'WARNING', ln, 'link that leaves the signup goal (justify it or remove it)', h)
    for m in re.finditer(r'<a\s([^>]*href="' + REVIEW_SITES[:-1] + r'[^"]*"[^>]*)>', src, re.I):
        if not re.search(r'rel="[^"]*nofollow', m.group(1), re.I):
            add('review-rel', 'WARNING', src[:m.start()].count('\n') + 1,
                'review link without rel="noopener nofollow" and target="_blank"')
    n_faq = len(re.findall(r'\sdata-faq[\s=>]', src)) or len(re.findall(r'<details[\s>]', src, re.I))
    if n_faq > max_faq:
        add('faq-count', 'WARNING', 0, 'FAQ of %d questions: keep %d at most' % (n_faq, max_faq))

    # Indexing and tracking
    noindex = re.search(r'name="robots"\s+content="[^"]*noindex', src, re.I)
    if page_type == 'ads' and not noindex:
        add('noindex', 'ERROR', 0, 'meta robots noindex missing: an ads landing stays out of search results')
    if page_type == 'seo' and noindex:
        add('noindex', 'ERROR', 0, 'noindex on an SEO page: it would never rank')
    if page_type == 'seo' and not re.search(r'name="description"\s+content="[^"]{50,}', src, re.I):
        add('meta-description', 'WARNING', 0, 'no meta description (about 150 characters, the promise and the call to action)')
    js = ' '.join(re.findall(r'<script[^>]*>(.*?)</script>', src, re.S | re.I))
    if 'utm_' not in js:
        add('utm', 'WARNING', 0, 'no utm_ handling in the scripts: UTMs and click ids must reach the signup')
    if 'landing_version' not in js:
        add('landing-version', 'WARNING', 0, 'no landing_version: two versions of the page cannot be compared')
    host = cfg.get('production_host', '')
    if host and host not in js:
        add('local-guard', 'ERROR', 0, 'no guard on the production host (%s): a local copy would send real leads' % host)
    endpoint = cfg.get('lead_endpoint', '')
    if endpoint and endpoint not in js:
        add('lead-endpoint', 'ERROR', 0, 'the lead endpoint of the config is missing: form leads would be lost')
    if re.search(r"dataLayer\.push\([^)]*email", js, re.I):
        add('email-in-datalayer', 'ERROR', 0, 'email sent to the dataLayer: never send the email to analytics')

    # Images
    for m in re.finditer(r'<img\s[^>]*>', src, re.I):
        tag, ln = m.group(0), src[:m.start()].count('\n') + 1
        s = re.search(r'src="([^"]+)"', tag)
        if s and not re.match(r'(https?:|data:|//)', s.group(1)):
            if not os.path.isfile(os.path.join(base_dir, s.group(1).split('?')[0])):
                add('broken-image', 'ERROR', ln, 'image not found', s.group(1))
        if not re.search(r'\salt="', tag):
            add('img-alt', 'WARNING', ln, 'image without alt text')

    if a.competitor:
        n = len(re.findall(r'\b' + re.escape(a.competitor) + r'\b', flat, re.I))
        if n < 3:
            add('competitor-count', 'WARNING', 0,
                '%s is named %d time(s): a conquest page answers "%s alternative"' % (a.competitor, n, a.competitor))

    order = {'ERROR': 0, 'WARNING': 1}
    for sev, ln, msg, ctx in sorted(out, key=lambda x: (order[x[0]], x[1])):
        print('%-8s l.%-5s %s%s' % (sev, ln or '-', msg, ('  "' + ctx.strip() + '"') if ctx else ''))
    n_err = sum(1 for o in out if o[0] == 'ERROR')
    print('\n%d error(s), %d warning(s)' % (n_err, len(out) - n_err))
    sys.exit(1 if n_err else 0)


if __name__ == '__main__':
    main()
