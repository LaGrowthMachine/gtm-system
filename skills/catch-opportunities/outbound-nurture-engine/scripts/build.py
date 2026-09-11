#!/usr/bin/env python3
"""
outbound-nurture-engine — deterministic engine.

Everything that can be silently wrong is built and validated here, never improvised:

    sitemap   discover content URLs from a site's sitemap (recursive index), filtered by path prefix
    index     merge freshly-read pages into the library index (diff by URL, keeps tags, stamps last_seen)
    match     pick 1..N contents per lead by relevance, never a content already sent, with a
              generic fallback, and report content gaps (pains no content covers)
    payload   validate the per-lead customAttribute sentences and emit the exact create_lead args
    newhtml   validate the campaign step messages (LGM newHtml) against the chosen slots
    --test    self-test with golden cases

Usage:
    python3 scripts/build.py sitemap https://example.com/sitemap.xml --prefix /gtm-playbooks/
    python3 scripts/build.py index  --library library-index.json --pages pages.json
    python3 scripts/build.py match  --library library-index.json --leads leads.json [--per-lead 3] [--today YYYY-MM-DD]
    python3 scripts/build.py payload --file payload.json [--slots 8,9,10] [--audience "Nurture 2026-09"]
    python3 scripts/build.py newhtml --file messages.json [--slots 8,9,10]
    python3 scripts/build.py --test

Exit codes: 0 ok · 2 refused (invalid input, nothing emitted).
"""
import argparse
import json
import re
import sys
from datetime import date, datetime
from urllib.parse import urlparse
from urllib.request import Request, urlopen

# ----------------------------------------------------------------------------- constants

SITUATIONS = {"not_now", "vague", "ghosted", "in_nurture"}
STAGES = {"reassure", "educate", "prove", "reactivate"}
TYPES = {"case_study", "playbook", "article", "podcast", "video", "post", "template", "other"}
SIZES = {"1-10", "11-50", "51-200", "201-1000", "1000+"}

DEFAULT_SLOTS = [8, 9, 10]        # 18/19/20 once the LGM MCP accepts customAttribute11-20 on create_lead
MAX_ATTR_LEN = 1000
DEFAULT_PER_LEAD = 3
DEFAULT_GHOST_DAYS = 10

# stage preference per touch index (0-based): first touch educates or reassures, second proves,
# third re-activates or proves. Small bonus, never overrides a pain match.
STAGE_PREFERENCE = [("educate", "reassure"), ("prove",), ("reactivate", "prove")]

URL_RE = re.compile(r"https?://[^\s<>\"']+")
DASH_RE = re.compile("[—–]|(?<!-)--(?!-)")
CURLY_RE = re.compile(r"\{\{|\}\}|%[a-zA-Z_]+%|\[[a-zA-Z_ ]+\]")


class ValidationError(Exception):
    pass


# ----------------------------------------------------------------------------- helpers

def _norm(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower()).strip()


def _norm_set(values):
    return {_norm(v) for v in (values or []) if _norm(v)}


def _today(arg):
    return datetime.strptime(arg, "%Y-%m-%d").date() if arg else date.today()


def _parse_date(s):
    if not s:
        return None
    s = str(s)[:10]
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        raise ValidationError(f"bad date {s!r}, expected YYYY-MM-DD")


# ----------------------------------------------------------------------------- sitemap

def _fetch(url, timeout=20):
    req = Request(url, headers={"User-Agent": "outbound-nurture-engine/1.0 (+https://lagrowthmachine.com)"})
    with urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")


def sitemap_urls(sitemap_url, prefix, fetch=_fetch, _depth=0, _seen=None):
    """Return the sorted list of page URLs under `prefix`, following sitemap indexes recursively."""
    if not prefix or not prefix.startswith("/"):
        raise ValidationError("prefix must be a path starting with '/', e.g. /gtm-playbooks/")
    if _depth > 3:
        return []
    _seen = _seen if _seen is not None else set()
    if sitemap_url in _seen:
        return []
    _seen.add(sitemap_url)
    xml = fetch(sitemap_url)
    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", xml)
    if not locs:
        raise ValidationError(f"no <loc> entries in {sitemap_url}: not a sitemap?")
    is_index = "<sitemapindex" in xml
    out = set()
    if is_index:
        for loc in locs:
            out.update(sitemap_urls(loc, prefix, fetch, _depth + 1, _seen))
    else:
        for loc in locs:
            path = urlparse(loc).path
            if path.startswith(prefix) and path.rstrip("/") != prefix.rstrip("/"):
                out.add(loc)
    return sorted(out)


# ----------------------------------------------------------------------------- index

def _validate_content(c, where):
    for key in ("url", "title"):
        if not c.get(key):
            raise ValidationError(f"{where}: content without {key!r}: {c}")
    if not URL_RE.fullmatch(c["url"]):
        raise ValidationError(f"{where}: bad url {c['url']!r}")
    if c.get("type") and c["type"] not in TYPES:
        raise ValidationError(f"{where}: type {c['type']!r} not in {sorted(TYPES)}")
    if c.get("stage") and c["stage"] not in STAGES:
        raise ValidationError(f"{where}: stage {c['stage']!r} not in {sorted(STAGES)}")
    for s in c.get("company_sizes") or []:
        if s not in SIZES:
            raise ValidationError(f"{where}: company size {s!r} not in {sorted(SIZES)}")


def index_merge(library, pages, today):
    """Merge freshly-read pages into the library. Match on URL. Keep existing tags unless the page
    brings new ones. Stamp last_seen. Contents absent from `pages` are kept but not re-stamped."""
    lib = {"contents": list(library.get("contents") or [])}
    by_url = {c["url"]: c for c in lib["contents"]}
    for c in lib["contents"]:
        _validate_content(c, "library")
    added, updated = 0, 0
    for p in pages:
        _validate_content(p, "pages")
        cur = by_url.get(p["url"])
        if cur is None:
            new = {k: v for k, v in p.items()}
            new.setdefault("added_at", today.isoformat())
            new["last_seen"] = today.isoformat()
            lib["contents"].append(new)
            by_url[p["url"]] = new
            added += 1
        else:
            changed = False
            for k, v in p.items():
                if k in ("url",):
                    continue
                if v not in (None, "", [], {}) and cur.get(k) != v:
                    cur[k] = v
                    changed = True
            cur["last_seen"] = today.isoformat()
            updated += int(changed)
    lib["updated_at"] = today.isoformat()
    lib["stats"] = {"total": len(lib["contents"]), "added": added, "updated": updated}
    return lib


# ----------------------------------------------------------------------------- match

def _validate_lead(lead, i):
    if not lead.get("lead_id"):
        raise ValidationError(f"lead #{i}: missing lead_id (the LGM lead id, needed to write attributes)")
    sit = lead.get("situation")
    if sit and sit not in SITUATIONS:
        raise ValidationError(f"lead #{i} ({lead['lead_id']}): situation {sit!r} not in {sorted(SITUATIONS)}")


def infer_situation(lead, today, ghost_days):
    """Deterministic part of the triage. Claude labels not_now / vague from the thread text; the
    engine only decides 'ghosted' vs 'awaiting_reply' from dates when no label was given."""
    if lead.get("situation"):
        return lead["situation"], None
    lr, ls = _parse_date(lead.get("last_received_at")), _parse_date(lead.get("last_sent_at"))
    if lr and ls:
        if lr > ls:
            return None, "awaiting_reply"       # the lead spoke last → reply-draft-assistant, not nurture
        if (today - ls).days >= ghost_days:
            return "ghosted", None
        return None, "too_recent"
    return None, "no_label"


def score_content(lead, content, touch_index):
    """Relevance score. Pain dominates; language mismatch disqualifies; generic contents float at 0."""
    if content.get("language") and lead.get("language") and \
            _norm(content["language"]) != _norm(lead["language"]):
        return None
    s = 0
    reasons = []
    pains = _norm_set(lead.get("pains")) & _norm_set(content.get("pains"))
    if pains:
        s += 5 * len(pains); reasons.append("pain:" + ",".join(sorted(pains)))
    if lead.get("persona") and _norm(lead["persona"]) in _norm_set(content.get("personas")):
        s += 3; reasons.append("persona")
    if lead.get("industry") and _norm(lead["industry"]) in _norm_set(content.get("industries")):
        s += 2; reasons.append("industry")
    if lead.get("company_size") and lead["company_size"] in (content.get("company_sizes") or []):
        s += 1; reasons.append("size")
    if touch_index < len(STAGE_PREFERENCE) and content.get("stage") in STAGE_PREFERENCE[touch_index]:
        s += 1; reasons.append("stage")
    return s, reasons


def match(library, leads, per_lead=DEFAULT_PER_LEAD, today=None, ghost_days=DEFAULT_GHOST_DAYS,
          min_score=2):
    today = today or date.today()
    contents = library.get("contents") or []
    if not contents:
        raise ValidationError("library is empty: index at least one content first (or run the content-gap "
                              "report from the leads' pains and create content)")
    for c in contents:
        _validate_content(c, "library")
    if not leads:
        raise ValidationError("no leads to match")
    if per_lead < 1 or per_lead > 5:
        raise ValidationError("per_lead must be between 1 and 5")

    generic = [c for c in contents if c.get("generic")]
    results, excluded, gap_pains = [], [], {}
    for i, lead in enumerate(leads):
        _validate_lead(lead, i)
        situation, why = infer_situation(lead, today, ghost_days)
        if situation is None:
            excluded.append({"lead_id": lead["lead_id"], "reason": why})
            continue
        already = set(lead.get("already_sent") or [])
        picks, used = [], set()
        weak = False
        for t in range(per_lead):
            best = None
            for c in contents:
                if c["url"] in already or c["url"] in used:
                    continue
                sc = score_content(lead, c, t)
                if sc is None:
                    continue
                score, reasons = sc
                key = (score, -contents.index(c))     # deterministic tie-break: library order
                if best is None or key > best[0]:
                    best = (key, c, score, reasons)
            if best is None or best[2] < min_score:
                # fallback 1: first unused generic content; fallback 2: best remaining content with
                # any signal at all (score >= 1), flagged weak; else the slot stays empty (gap)
                fb = next((g for g in generic if g["url"] not in already and g["url"] not in used
                           and not (g.get("language") and lead.get("language")
                                    and _norm(g["language"]) != _norm(lead["language"]))), None)
                if fb is not None:
                    picks.append({"url": fb["url"], "title": fb["title"], "score": 0, "reasons": ["generic"]})
                    used.add(fb["url"]); weak = True
                    continue
                if best is not None and best[2] >= 1:
                    _, c, score, reasons = best
                    picks.append({"url": c["url"], "title": c["title"], "score": score, "reasons": reasons + ["weak"]})
                    used.add(c["url"]); weak = True
                    continue
                break
            _, c, score, reasons = best
            picks.append({"url": c["url"], "title": c["title"], "score": score, "reasons": reasons})
            used.add(c["url"])
        if len(picks) < per_lead or weak:
            for p in lead.get("pains") or []:
                gap_pains[_norm(p)] = gap_pains.get(_norm(p), 0) + 1
        results.append({"lead_id": lead["lead_id"], "situation": situation, "picks": picks,
                        "complete": len(picks) == per_lead, "weak": weak})

    gaps = sorted(({"pain": p, "leads_waiting": n} for p, n in gap_pains.items()),
                  key=lambda g: (-g["leads_waiting"], g["pain"]))
    return {"per_lead": per_lead, "matched": results, "excluded": excluded, "content_gaps": gaps,
            "library_size": len(contents)}


# ----------------------------------------------------------------------------- payload

def _validate_sentence(text, where):
    if not isinstance(text, str) or not text.strip():
        raise ValidationError(f"{where}: empty sentence")
    if len(text) > MAX_ATTR_LEN:
        raise ValidationError(f"{where}: {len(text)} chars > {MAX_ATTR_LEN}")
    if "\n" in text or "\r" in text:
        raise ValidationError(f"{where}: newline in a customAttribute value (keep it one line)")
    urls = URL_RE.findall(text)
    if len(urls) != 1:
        raise ValidationError(f"{where}: expected exactly one URL, found {len(urls)}")
    if re.search(r"https?://\S*[.,;:!?)]$", text.strip()) or re.search(r"https?://\S*[.,;:!?](\s|$)", text):
        raise ValidationError(f"{where}: punctuation glued to the URL (it becomes part of the link)")
    if DASH_RE.search(text):
        raise ValidationError(f"{where}: em/en dash found (replace with a comma or a new sentence)")
    if CURLY_RE.search(text):
        raise ValidationError(f"{where}: template token found ({{{{…}}}}, %…% or […]) in a value")
    if text.count("?") > 1:
        raise ValidationError(f"{where}: more than one question in a sentence")


def payload(spec, slots=None, audience=None):
    """spec: {"leads": [{"lead_id", "sentences": ["...", "..."], "context": "..."?}]}
    Emits one create_lead argument object per lead, ready for the MCP."""
    slots = slots or DEFAULT_SLOTS
    if len(set(slots)) != len(slots) or any(not (1 <= s <= 20) for s in slots):
        raise ValidationError(f"slots must be distinct integers in 1..20, got {slots}")
    leads = spec.get("leads") or []
    if not leads:
        raise ValidationError("no leads in payload")
    audience = audience or spec.get("audience")
    if not audience or not str(audience).strip():
        raise ValidationError("audience name is required (the wave's audience, e.g. 'Nurture 2026-09')")
    out = []
    for i, l in enumerate(leads):
        if not l.get("lead_id"):
            raise ValidationError(f"lead #{i}: missing lead_id")
        sents = l.get("sentences") or []
        if len(sents) != len(slots):
            raise ValidationError(f"lead {l['lead_id']}: {len(sents)} sentences for {len(slots)} slots "
                                  f"(every slot must be filled, the campaign reads all of them)")
        urls = set()
        args = {"leadId": l["lead_id"], "audience": audience}
        for slot, s in zip(slots, sents):
            _validate_sentence(s, f"lead {l['lead_id']} slot {slot}")
            u = URL_RE.findall(s)[0]
            if u in urls:
                raise ValidationError(f"lead {l['lead_id']}: same URL used twice")
            urls.add(u)
            args[f"customAttribute{slot}"] = s.strip()
        out.append(args)
    return {"slots": slots, "audience": audience, "create_lead_args": out}


# ----------------------------------------------------------------------------- newhtml

BLOCK_RE = re.compile(r"<(p|ul|h2)(\s[^>]*)?>.*?</\1>|<p/>", re.S)
VAR_RE = re.compile(r'<var name="([a-zA-Z0-9_]+)"(?: default="[^"]*")?/>')
ALLOWED_VARS = {"firstname", "lastname", "company", "jobTitle", "companyName"}


def validate_newhtml(html, expected_var, where):
    if not isinstance(html, str) or not html.strip():
        raise ValidationError(f"{where}: empty newHtml")
    if "\n" in html or re.search(r">\s+<(p|ul|h2|/)", html):
        raise ValidationError(f"{where}: newHtml must be one line with no whitespace between blocks")
    stripped = BLOCK_RE.sub("", html)
    if stripped.strip():
        raise ValidationError(f"{where}: text outside a block tag: {stripped.strip()[:60]!r}")
    if CURLY_RE.search(html):
        raise ValidationError(f"{where}: template token found, variables must be <var name=\"…\"/>")
    names = VAR_RE.findall(html)
    bad = [n for n in names if n not in ALLOWED_VARS and not re.fullmatch(r"customAttribute([1-9]|1[0-9]|20)", n)]
    if bad:
        raise ValidationError(f"{where}: unknown variable(s) {bad}")
    if names.count(expected_var) != 1:
        raise ValidationError(f"{where}: expected exactly one <var name=\"{expected_var}\"/>, found {names.count(expected_var)}")
    if URL_RE.search(re.sub(r'<var[^>]*/>', '', html)):
        raise ValidationError(f"{where}: a raw URL in the message body (the link lives in the customAttribute)")
    if DASH_RE.search(html):
        raise ValidationError(f"{where}: em/en dash found")
    text = re.sub(r"<[^>]+>", " ", html)
    if text.count("?") > 1:
        raise ValidationError(f"{where}: more than one question")
    if len(text) > 900:
        raise ValidationError(f"{where}: message too long ({len(text)} chars of text)")


def newhtml(spec, slots=None):
    """spec: {"steps": [{"step_id": "...", "newHtml": "..."}, ...]} — one per slot, in order."""
    slots = slots or DEFAULT_SLOTS
    steps = spec.get("steps") or []
    if len(steps) != len(slots):
        raise ValidationError(f"{len(steps)} steps for {len(slots)} slots: the campaign needs one message per content")
    out = []
    for slot, st in zip(slots, steps):
        if not st.get("step_id"):
            raise ValidationError("step without step_id (from get_campaign_steps)")
        validate_newhtml(st.get("newHtml"), f"customAttribute{slot}", f"step {st['step_id']}")
        out.append({"stepId": st["step_id"], "newHtml": st["newHtml"]})
    return {"slots": slots, "add_campaign_step_message_args": out}


# ----------------------------------------------------------------------------- self-test

def _selftest():
    failures = []

    def check(name, fn, should_raise=False):
        try:
            r = fn()
            if should_raise:
                failures.append(f"{name}: expected refusal, got {str(r)[:80]}")
            return r
        except ValidationError as e:
            if not should_raise:
                failures.append(f"{name}: unexpected refusal: {e}")
        except Exception as e:  # noqa
            failures.append(f"{name}: crashed: {e!r}")

    # --- sitemap (offline fetch stub, index → children, prefix filter, self-link excluded)
    pages = {
        "https://x.com/sitemap.xml": "<sitemapindex><sitemap><loc>https://x.com/a.xml</loc></sitemap>"
                                     "<sitemap><loc>https://x.com/b.xml</loc></sitemap></sitemapindex>",
        "https://x.com/a.xml": "<urlset><url><loc>https://x.com/gtm-playbooks/</loc></url>"
                               "<url><loc>https://x.com/gtm-playbooks/one</loc></url>"
                               "<url><loc>https://x.com/blog/two</loc></url></urlset>",
        "https://x.com/b.xml": "<urlset><url><loc>https://x.com/gtm-playbooks/three/</loc></url></urlset>",
    }
    r = check("sitemap.index", lambda: sitemap_urls("https://x.com/sitemap.xml", "/gtm-playbooks/", pages.get))
    if r != ["https://x.com/gtm-playbooks/one", "https://x.com/gtm-playbooks/three/"]:
        failures.append(f"sitemap.index: wrong urls {r}")
    check("sitemap.badprefix", lambda: sitemap_urls("https://x.com/sitemap.xml", "gtm", pages.get), True)
    check("sitemap.notsitemap", lambda: sitemap_urls("https://x.com/none", "/g/", lambda u: "<html/>"), True)

    # --- index
    today = date(2026, 9, 11)
    lib = {"contents": [{"url": "https://x.com/a", "title": "A", "pains": ["reply handling"], "added_at": "2026-01-01"}]}
    r = check("index.merge", lambda: index_merge(lib, [
        {"url": "https://x.com/a", "title": "A", "pains": ["reply handling", "timing"]},
        {"url": "https://x.com/b", "title": "B", "type": "case_study"}], today))
    if r and (r["stats"] != {"total": 2, "added": 1, "updated": 1} or r["contents"][0]["last_seen"] != "2026-09-11"
              or r["contents"][0]["added_at"] != "2026-01-01"):
        failures.append(f"index.merge: {r and r['stats']}")
    check("index.badtype", lambda: index_merge({}, [{"url": "https://x.com/c", "title": "C", "type": "meme"}], today), True)
    check("index.nourl", lambda: index_merge({}, [{"title": "C"}], today), True)

    # --- match
    library = {"contents": [
        {"url": "https://x.com/cs-agency", "title": "Agency case study", "type": "case_study", "stage": "prove",
         "pains": ["reply handling"], "industries": ["marketing agency"], "company_sizes": ["11-50"], "language": "en"},
        {"url": "https://x.com/pb-notnow", "title": "Not-now playbook", "type": "playbook", "stage": "educate",
         "pains": ["not now replies", "reply handling"], "personas": ["founder"], "language": "en"},
        {"url": "https://x.com/generic", "title": "Outbound basics", "type": "article", "generic": True, "language": "en"},
        {"url": "https://x.com/fr-guide", "title": "Guide FR", "type": "article", "pains": ["reply handling"], "language": "fr"},
    ]}
    leads = [
        {"lead_id": "L1", "situation": "not_now", "pains": ["reply handling"], "persona": "founder",
         "industry": "Marketing agency", "company_size": "11-50", "language": "en"},
        {"lead_id": "L2", "situation": "vague", "pains": ["pricing"], "language": "en"},
        {"lead_id": "L3", "last_received_at": "2026-09-10", "last_sent_at": "2026-09-01"},          # awaiting reply
        {"lead_id": "L4", "last_received_at": "2026-08-20", "last_sent_at": "2026-08-25"},          # ghosted (17 days)
        {"lead_id": "L5", "situation": "not_now", "pains": ["reply handling"], "language": "en",
         "already_sent": ["https://x.com/pb-notnow"]},
    ]
    r = check("match.basic", lambda: match(library, leads, per_lead=2, today=today))
    if r:
        m = {x["lead_id"]: x for x in r["matched"]}
        if m["L1"]["picks"][0]["url"] != "https://x.com/pb-notnow":        # pain 5 + persona 3 + stage 1 = 9 > cs 5+2+1 = 8
            failures.append(f"match.L1 first pick {m['L1']['picks'][0]}")
        if m["L1"]["picks"][1]["url"] != "https://x.com/cs-agency":
            failures.append(f"match.L1 second pick {m['L1']['picks'][1]}")
        if not (m["L2"]["weak"] and m["L2"]["picks"][0]["reasons"] == ["generic"]):
            failures.append(f"match.L2 should fall back to generic: {m['L2']}")
        if r["content_gaps"][0] != {"pain": "pricing", "leads_waiting": 1}:
            failures.append(f"match.gaps {r['content_gaps']}")
        if any(e["lead_id"] == "L3" and e["reason"] == "awaiting_reply" for e in r["excluded"]) is False:
            failures.append("match.L3 should be excluded as awaiting_reply")
        if m["L4"]["situation"] != "ghosted":
            failures.append(f"match.L4 situation {m['L4']['situation']}")
        if any(p["url"] == "https://x.com/pb-notnow" for p in m["L5"]["picks"]):
            failures.append("match.L5 re-sent an already_sent content")
        if any("fr-guide" in p["url"] for x in r["matched"] for p in x["picks"]):
            failures.append("match: french content matched to an english lead")
    r2 = check("match.fr_generic", lambda: match(library, [{"lead_id": "F1", "situation": "vague", "language": "fr",
                                                             "pains": ["reply handling"]}], per_lead=2, today=today))
    if r2 and (any(p["url"] == "https://x.com/generic" for p in r2["matched"][0]["picks"])
               or r2["matched"][0]["complete"]):
        failures.append(f"match.fr_generic: english generic given to a french lead {r2['matched'][0]}")
    check("match.emptylib", lambda: match({"contents": []}, leads), True)
    check("match.noleadid", lambda: match(library, [{"situation": "vague"}]), True)
    check("match.badsituation", lambda: match(library, [{"lead_id": "X", "situation": "hot"}]), True)

    # --- payload
    good = {"audience": "Nurture 2026-09", "leads": [{"lead_id": "L1", "sentences": [
        "our playbook on turning not-now replies into meetings, it covers exactly the timing point you raised: https://x.com/pb-notnow",
        "a short case study from an 11-person agency that had the same reply bottleneck: https://x.com/cs-agency",
        "the outbound basics we share with every new team, worth ten minutes: https://x.com/generic"]}]}
    r = check("payload.good", lambda: payload(good, [8, 9, 10]))
    if r and (r["create_lead_args"][0]["customAttribute8"] != good["leads"][0]["sentences"][0]
              or r["create_lead_args"][0]["audience"] != "Nurture 2026-09"):
        failures.append("payload.good: wrong args")
    bad = lambda s: {"audience": "N", "leads": [{"lead_id": "L1", "sentences": [s, "b https://x.com/b", "c https://x.com/c"]}]}
    check("payload.nourl", lambda: payload(bad("no link here")), True)
    check("payload.twourls", lambda: payload(bad("https://x.com/a and https://x.com/d")), True)
    check("payload.gluedpunct", lambda: payload(bad("see https://x.com/a.")), True)
    check("payload.emdash", lambda: payload(bad("see this — https://x.com/a")), True)
    check("payload.token", lambda: payload(bad("hi {{firstname}} https://x.com/a")), True)
    check("payload.toolong", lambda: payload(bad("x" * 1001 + " https://x.com/a")), True)
    check("payload.missingslot", lambda: payload({"audience": "N", "leads": [{"lead_id": "L1", "sentences": ["a https://x.com/a"]}]}), True)
    check("payload.noaudience", lambda: payload({"leads": good["leads"]}), True)
    check("payload.badslots", lambda: payload(good, [8, 8, 21]), True)
    check("payload.dupurl", lambda: payload({"audience": "N", "leads": [{"lead_id": "L1", "sentences": [
        "a https://x.com/a", "b https://x.com/a", "c https://x.com/c"]}]}), True)

    # --- newhtml
    ok_html = ('<p>Hi <var name="firstname" default="there"/>,</p><p/><p>When we spoke you mentioned timing. '
               'If useful, <var name="customAttribute8"/></p><p/><p>No rush, thought of you when it went out.</p>')
    r = check("newhtml.good", lambda: newhtml({"steps": [
        {"step_id": "s1", "newHtml": ok_html},
        {"step_id": "s2", "newHtml": ok_html.replace("customAttribute8", "customAttribute9")},
        {"step_id": "s3", "newHtml": ok_html.replace("customAttribute8", "customAttribute10")}]}, [8, 9, 10]))
    if r and r["add_campaign_step_message_args"][2]["stepId"] != "s3":
        failures.append("newhtml.good: wrong args")
    one = lambda h: newhtml({"steps": [{"step_id": "s1", "newHtml": h}]}, [8])
    check("newhtml.wrongvar", lambda: one(ok_html.replace("customAttribute8", "customAttribute9")), True)
    check("newhtml.curly", lambda: one("<p>Hi {{firstname}} <var name=\"customAttribute8\"/></p>"), True)
    check("newhtml.outsideblock", lambda: one("Hi <p><var name=\"customAttribute8\"/></p>"), True)
    check("newhtml.whitespace", lambda: one("<p>a <var name=\"customAttribute8\"/></p> <p>b</p>"), True)
    check("newhtml.rawurl", lambda: one("<p>see https://x.com <var name=\"customAttribute8\"/></p>"), True)
    check("newhtml.twoq", lambda: one("<p>ok? <var name=\"customAttribute8\"/> fine?</p>"), True)
    check("newhtml.unknownvar", lambda: one("<p><var name=\"email\"/> <var name=\"customAttribute8\"/></p>"), True)
    check("newhtml.count", lambda: newhtml({"steps": [{"step_id": "s1", "newHtml": ok_html}]}, [8, 9]), True)

    total = 47
    for f in failures:
        print("FAIL:", f, file=sys.stderr)
    print(f"{total - len(failures)}/{total} passed")
    return 1 if failures else 0


# ----------------------------------------------------------------------------- cli

def _load(path):
    with open(path) as f:
        return json.load(f)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--test", action="store_true")
    sub = p.add_subparsers(dest="cmd")
    s = sub.add_parser("sitemap"); s.add_argument("url"); s.add_argument("--prefix", required=True)
    s = sub.add_parser("index"); s.add_argument("--library", required=True); s.add_argument("--pages", required=True)
    s.add_argument("--today")
    s = sub.add_parser("match"); s.add_argument("--library", required=True); s.add_argument("--leads", required=True)
    s.add_argument("--per-lead", type=int, default=DEFAULT_PER_LEAD); s.add_argument("--today")
    s.add_argument("--ghost-days", type=int, default=DEFAULT_GHOST_DAYS); s.add_argument("--min-score", type=int, default=2)
    s = sub.add_parser("payload"); s.add_argument("--file", required=True); s.add_argument("--slots")
    s.add_argument("--audience")
    s = sub.add_parser("newhtml"); s.add_argument("--file", required=True); s.add_argument("--slots")
    a = p.parse_args()
    if a.test:
        sys.exit(_selftest())
    if not a.cmd:
        p.print_help(); sys.exit(2)
    slots = [int(x) for x in a.slots.split(",")] if getattr(a, "slots", None) else None
    try:
        if a.cmd == "sitemap":
            out = sitemap_urls(a.url, a.prefix)
        elif a.cmd == "index":
            lib = _load(a.library) if __import__("os").path.exists(a.library) else {}
            out = index_merge(lib, _load(a.pages), _today(a.today))
            with open(a.library, "w") as f:
                json.dump(out, f, indent=2, ensure_ascii=False)
        elif a.cmd == "match":
            out = match(_load(a.library), _load(a.leads), a.per_lead, _today(a.today), a.ghost_days, a.min_score)
        elif a.cmd == "payload":
            out = payload(_load(a.file), slots, a.audience)
        elif a.cmd == "newhtml":
            out = newhtml(_load(a.file), slots)
        print(json.dumps(out, indent=2, ensure_ascii=False))
    except ValidationError as e:
        print(f"error: {e}", file=sys.stderr); sys.exit(2)
    except OSError as e:
        print(f"error: {e}", file=sys.stderr); sys.exit(2)


if __name__ == "__main__":
    main()
