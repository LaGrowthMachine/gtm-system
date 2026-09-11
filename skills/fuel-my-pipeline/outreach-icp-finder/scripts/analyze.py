#!/usr/bin/env python3
"""analyze.py — turn an outreach dataset (who you contacted, who replied) into a
proven-ICP analysis.

Deterministic engine. It does the arithmetic the LLM must NOT improvise:
per-segment reply / positive-reply rates with 95% confidence intervals, lift vs
baseline, minimum-volume gating, campaign-confounding checks (a segment that
"replies well" only because one good campaign targeted it), 2-D crosstabs, and
attribute-coverage reporting. It validates the input and REFUSES to emit a
best-effort result on thin or unreadable data — an "ICP" built on 12 replies,
discovered downstream after a month of prospecting the wrong people, is exactly
the silent failure this tier exists to prevent.

INPUT — one row per lead (optionally per lead x campaign), CSV or JSON, with
whatever subset of these columns you have (header names are matched loosely,
FR/EN synonyms accepted, see SYNONYMS):
  identity   : lead id, email                      (never output; dedup only)
  attributes : job title, industry, location, company size, seniority, function
  context    : campaign, channel, contacted-at date
  outcomes   : contacted, accepted, replied, reply label, reply text, converted

OUTCOME HIERARCHY
  positive reply  = reply label in POSITIVE, or converted/meeting truthy
  reply           = replied truthy, or any label / reply text / converted
  accepted        = LinkedIn invitation accepted
The engine picks a PRIMARY outcome: positive replies when labels cover enough
of the replies (they separate "interested" from "no thanks"); plain replies
otherwise — and says which, so the caller can tell the user.

The engine produces NUMBERS. Reading them into 2-4 named ICP archetypes is the
model's job, on top of this output.

Usage
    python3 analyze.py outreach.csv
    python3 analyze.py outreach.json --min-cell 30
    cat outreach.csv | python3 analyze.py -
    python3 analyze.py --test

Output: a JSON report on stdout. Errors go to stderr with exit code 2 — when
the engine refuses, the caller should ASK the user (or collect more data), not
guess.
"""
import sys, csv, json, argparse, io, re, os, math
from collections import defaultdict, Counter
from datetime import datetime, date, timedelta

MIN_CELL_DEFAULT = 30          # contacted leads a segment needs to be reported on its own
MIN_CONTACTED_DEFAULT = 100    # below this the engine refuses: nothing reliable to say
MIN_OUTCOMES_DEFAULT = 20      # replies (or positives) needed before segments mean anything
MIN_STRATUM = 10               # contacted leads a (segment x campaign) cell needs to enter the stratified lift
CONFOUND_SHARE = 0.70          # segment mostly from one campaign -> flag as confounded
LABEL_COVERAGE_FOR_POSITIVE = 0.50   # share of replies that must carry a label to use positive-reply as primary outcome
LOW_COVERAGE = 0.50            # attribute filled on < 50% of contacted leads -> read with caution
SKIP_COVERAGE = 0.20           # attribute filled on < 20% -> not analyzable, reported as a gap
Z95 = 1.959964

TAXONOMY_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "..", "references", "title-taxonomy.json")

SYNONYMS = {
    "lead_id":    ["lead id", "leadid", "lead_id", "id", "contact id", "prospect id", "person id"],
    "email":      ["email", "pro email", "proemail", "work email", "email address", "e-mail"],
    "title":      ["job title", "jobtitle", "title", "position", "poste", "fonction", "intitulé",
                   "intitule", "headline", "role", "job", "current title"],
    "company":    ["company", "company name", "companyname", "organisation", "organization",
                   "société", "societe", "entreprise", "account", "employer"],
    "industry":   ["industry", "company industry", "secteur", "secteur d'activité",
                   "secteur d'activite", "vertical", "industrie", "sector"],
    "location":   ["location", "country", "pays", "geo", "region", "région", "localisation",
                   "company country", "lead location", "city", "ville", "hq country"],
    "size":       ["company size", "companysize", "headcount", "employees", "number of employees",
                   "numberofemployees", "no. of employees", "effectif", "effectifs", "size",
                   "employee count", "company headcount", "taille"],
    "seniority":  ["seniority", "seniority level", "niveau", "séniorité", "seniorite", "level"],
    "function":   ["function", "department", "département", "departement", "team", "équipe"],
    "campaign":   ["campaign", "campaign name", "campaignid", "campaign id", "campaign_id",
                   "sequence", "sequence name", "campagne", "cadence"],
    "channel":    ["channel", "canal", "last channel", "last message type"],
    "contacted":  ["contacted", "was contacted", "is contacted", "sent", "first contact",
                   "first_contact", "contacted at", "contacted_at", "first sent", "date contacted",
                   "contacté", "contacte"],
    "accepted":   ["accepted", "connection accepted", "invitation accepted", "linkedin accepted",
                   "accepted at", "accepted_at", "connected", "accepté", "accepte"],
    "replied":    ["replied", "has replied", "lead replied", "reply", "replies", "replied at",
                   "replied_at", "responded", "answered", "a répondu", "a repondu", "répondu",
                   "repondu", "reply count", "nb replies"],
    "reply_label":["reply label", "reply_label", "reply category", "reply sentiment", "sentiment",
                   "interest", "interest level", "lead category", "category", "label", "intent",
                   "qualification", "lead status", "reply status", "outcome", "catégorie", "categorie"],
    "converted":  ["converted", "meeting booked", "meeting", "booked", "won", "deal", "opportunity",
                   "converti", "rdv", "demo booked", "call booked", "is converted", "converted at"],
    "reply_text": ["reply text", "reply_text", "last reply", "reply message", "reply content",
                   "last message", "message", "réponse", "reponse", "texte réponse"],
}

TRUTHY = {"1", "true", "yes", "y", "oui", "x", "✓", "ok", "done", "success"}
FALSY = {"", "0", "false", "no", "n", "non", "none", "null", "nan", "-", "n/a", "na"}

SIZE_BUCKETS = [(1, 10, "1-10"), (11, 50, "11-50"), (51, 200, "51-200"),
                (201, 500, "201-500"), (501, 1000, "501-1000"),
                (1001, 5000, "1001-5000"), (5001, 10**9, "5001+")]

COUNTRY_ALIASES = {
    "United States": ["usa", "us", "u.s.", "u.s.a.", "united states", "united states of america",
                      "états-unis", "etats-unis", "america"],
    "United Kingdom": ["uk", "u.k.", "united kingdom", "royaume-uni", "england", "great britain",
                       "gb", "scotland", "wales"],
    "Germany": ["germany", "deutschland", "allemagne"],
    "France": ["france"],
    "Spain": ["spain", "españa", "espagne"],
    "Italy": ["italy", "italia", "italie"],
    "Netherlands": ["netherlands", "the netherlands", "nederland", "pays-bas", "holland"],
    "Belgium": ["belgium", "belgique", "belgië", "belgie"],
    "Switzerland": ["switzerland", "suisse", "schweiz", "svizzera"],
    "Canada": ["canada"],
    "Australia": ["australia", "australie"],
    "India": ["india", "inde"],
    "Brazil": ["brazil", "brasil", "brésil", "bresil"],
    "Portugal": ["portugal"],
    "Sweden": ["sweden", "sverige", "suède", "suede"],
    "Ireland": ["ireland", "irlande"],
    "Singapore": ["singapore", "singapour"],
    "United Arab Emirates": ["uae", "united arab emirates", "émirats arabes unis", "emirats arabes unis", "dubai"],
    "Israel": ["israel", "israël"],
    "Nigeria": ["nigeria"],
    "Mexico": ["mexico", "méxico", "mexique"],
    "Poland": ["poland", "polska", "pologne"],
    "Denmark": ["denmark", "danmark", "danemark"],
    "Norway": ["norway", "norge", "norvège", "norvege"],
    "Finland": ["finland", "suomi", "finlande"],
    "Austria": ["austria", "österreich", "osterreich", "autriche"],
    "Luxembourg": ["luxembourg"],
    "Morocco": ["morocco", "maroc"],
    "South Africa": ["south africa", "afrique du sud"],
    "Japan": ["japan", "japon"],
}
_ALIAS_INDEX = {a: c for c, aliases in COUNTRY_ALIASES.items() for a in aliases}

DIMENSIONS = ["seniority", "function", "industry", "country", "size_bucket"]
CROSSTAB_PAIRS = [("seniority", "industry"), ("seniority", "size_bucket"),
                  ("function", "industry"), ("industry", "country"), ("seniority", "country")]


class ValidationError(Exception):
    pass


# ---------------------------------------------------------------- taxonomy

_TAXONOMY = None

def load_taxonomy(path=TAXONOMY_PATH):
    global _TAXONOMY
    if _TAXONOMY is None:
        try:
            with open(path, encoding="utf-8") as f:
                raw = json.load(f)
        except FileNotFoundError:
            raise ValidationError(f"taxonomy file missing: {path} — the skill folder is incomplete")
        def compile_rules(rules):
            return [(r["label"], [re.compile(p, re.I) for p in r["patterns"]]) for r in rules]
        _TAXONOMY = {
            "seniority": compile_rules(raw["seniority"]),
            "seniority_default": raw.get("seniority_default", "Individual contributor"),
            "function": compile_rules(raw["function"]),
            "function_default": raw.get("function_default", "Other"),
            "reply_labels": [(lab, [re.compile(p, re.I) for p in pats])
                             for lab, pats in raw["reply_labels"].items() if not lab.startswith("_")],
        }
    return _TAXONOMY


def classify_title(title):
    """-> (seniority, function). Empty title -> (None, None)."""
    t = (title or "").strip()
    if not t:
        return None, None
    tax = load_taxonomy()
    sen = next((lab for lab, pats in tax["seniority"] if any(p.search(t) for p in pats)),
               tax["seniority_default"])
    fun = next((lab for lab, pats in tax["function"] if any(p.search(t) for p in pats)),
               tax["function_default"])
    return sen, fun


def normalize_label(raw):
    """Free-text reply label -> POSITIVE | NOT_NOW | NEGATIVE | OOO | OTHER | None (empty)."""
    s = (raw or "").strip()
    if not s or s.lower() in FALSY:
        return None
    up = s.upper().replace(" ", "_")
    if up in ("POSITIVE", "NOT_NOW", "NEGATIVE", "OOO", "OTHER"):
        return up
    for lab, pats in load_taxonomy()["reply_labels"]:
        if any(p.search(s) for p in pats):
            return lab
    return "OTHER"


# ---------------------------------------------------------------- parsing

def parse_bool(raw):
    """Truthy if yes/1/true, a date-like string, or a positive number. Falsy if empty/0/no."""
    if raw is None:
        return False
    if isinstance(raw, bool):
        return raw
    if isinstance(raw, (int, float)):
        return raw > 0
    s = str(raw).strip().lower()
    if s in FALSY:
        return False
    if s in TRUTHY:
        return True
    if re.match(r"^\d{4}-\d{2}-\d{2}", s) or re.match(r"^\d{1,2}/\d{1,2}/\d{2,4}", s) \
            or re.match(r"^\d{10,13}$", s):
        return True
    try:
        return float(s.replace(",", ".")) > 0
    except ValueError:
        return True   # any other non-empty text (e.g. "Replied", "Connected") counts as a signal


def parse_date(raw):
    if raw is None:
        return None
    s = str(raw).strip()
    if not s:
        return None
    if re.match(r"^\d{13}$", s):
        return datetime.utcfromtimestamp(int(s) / 1000).date()
    if re.match(r"^\d{10}$", s):
        return datetime.utcfromtimestamp(int(s)).date()
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y", "%m/%d/%Y",
                "%d/%m/%y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s[:len(datetime.now().strftime(fmt))], fmt).date()
        except ValueError:
            continue
    m = re.match(r"^(\d{4}-\d{2}-\d{2})", s)
    return date.fromisoformat(m.group(1)) if m else None


def size_bucket(raw):
    if raw is None:
        return None
    s = str(raw).strip()
    if not s:
        return None
    for lo, hi, label in SIZE_BUCKETS:       # already a LinkedIn-style bucket
        if s.replace(",", "").replace(" ", "").startswith(label.replace("+", "")) and (
                label.endswith("+") or re.search(r"[-–]", s)):
            return label
    m = re.search(r"\d[\d,\. ]*", s)
    if not m:
        return None
    n = int(re.sub(r"[^\d]", "", m.group(0)) or 0)
    if n <= 0:
        return None
    return next(label for lo, hi, label in SIZE_BUCKETS if lo <= n <= hi)


def country_of(location):
    s = (location or "").strip()
    if not s:
        return None
    parts = [p.strip() for p in s.split(",") if p.strip()]
    for candidate in ([parts[-1]] if parts else []) + [s]:
        key = candidate.lower().strip(" .")
        if key in _ALIAS_INDEX:
            return _ALIAS_INDEX[key]
    low = " " + re.sub(r"[^\w\s]", " ", s.lower()) + " "
    for alias, country in sorted(_ALIAS_INDEX.items(), key=lambda kv: -len(kv[0])):
        if len(alias) > 2 and f" {alias} " in low:
            return country
    return parts[-1].title() if parts else s.title()


def norm_key(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower())


def resolve_columns(headers):
    """Map our canonical field names onto the file's headers (loose, FR/EN). Exact match beats contains."""
    hmap = {norm_key(h): h for h in headers}
    found = {}
    for field, syns in SYNONYMS.items():
        for syn in syns:
            if syn in hmap:
                found[field] = hmap[syn]
                break
    for field, syns in SYNONYMS.items():          # second pass: header contains the synonym
        if field in found:
            continue
        for h_norm, h in hmap.items():
            if h in found.values():
                continue
            if any(re.search(r"\b" + re.escape(syn) + r"\b", h_norm) for syn in syns if len(syn) > 3):
                found[field] = h
                break
    return found


def read_rows(raw_text):
    txt = raw_text.strip()
    if not txt:
        raise ValidationError("empty input")
    if txt[0] in "[{":
        data = json.loads(txt)
        if isinstance(data, dict):
            for k in ("rows", "data", "leads", "results"):
                if isinstance(data.get(k), list):
                    data = data[k]
                    break
        if not isinstance(data, list):
            raise ValidationError("JSON input must be a list of row objects")
        return [dict(r) for r in data]
    sample = txt[:4096]
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
    except csv.Error:
        dialect = csv.excel
    return list(csv.DictReader(io.StringIO(txt), dialect=dialect))


# ---------------------------------------------------------------- stats

def wilson(k, n, z=Z95):
    if n <= 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    centre = p + z * z / (2 * n)
    adj = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return ((centre - adj) / denom, (centre + adj) / denom)


def r4(x):
    return None if x is None else round(x, 4)


# ---------------------------------------------------------------- engine

def normalize(rows, cols, today):
    """One dict per input row with derived fields. Never keeps names/emails beyond a dedup key."""
    out = []
    for i, r in enumerate(rows):
        g = lambda f: (r.get(cols[f]) if f in cols else None)
        title = (g("title") or "").strip()
        sen_col, fun_col = (g("seniority") or "").strip(), (g("function") or "").strip()
        sen_d, fun_d = classify_title(title)
        label = normalize_label(g("reply_label"))
        reply_text = (str(g("reply_text") or "")).strip()
        converted = parse_bool(g("converted"))
        replied = parse_bool(g("replied")) or label is not None or bool(reply_text) or converted
        contacted = parse_bool(g("contacted")) if "contacted" in cols else True
        if replied:
            contacted = True                     # a reply proves a contact happened
        campaign = (str(g("campaign") or "")).strip() or None
        out.append({
            "key": (str(g("lead_id") or g("email") or f"row{i}")).strip().lower(),
            "campaign": campaign,
            "seniority": sen_col or sen_d,
            "function": fun_col or fun_d,
            "industry": (str(g("industry") or "")).strip() or None,
            "country": country_of(g("location")),
            "size_bucket": size_bucket(g("size")),
            "has_title": bool(title),
            "contacted": contacted,
            "accepted": parse_bool(g("accepted")),
            "replied": replied,
            "label": label,
            "positive": (label == "POSITIVE") or converted,
            "has_text": bool(reply_text),
            "contacted_at": parse_date(g("contacted")) if "contacted" in cols else None,
        })
    return out


def dedup(recs):
    """Same lead in the same campaign twice -> merge (any truthy outcome wins)."""
    merged = {}
    for r in recs:
        k = (r["key"], r["campaign"])
        if k not in merged:
            merged[k] = dict(r)
            continue
        m = merged[k]
        for f in ("contacted", "accepted", "replied", "positive", "has_text", "has_title"):
            m[f] = m[f] or r[f]
        for f in ("seniority", "function", "industry", "country", "size_bucket", "label"):
            m[f] = m[f] or r[f]
    return list(merged.values())


def segment_stats(recs, dim, outcome, baseline, min_cell, campaigns_total):
    """Per-value stats for one dimension. Small values are pooled into an 'other' bucket."""
    groups = defaultdict(list)
    for r in recs:
        if r[dim] is not None:
            groups[r[dim]].append(r)
    values, pooled = [], []
    for val, rs in groups.items():
        (values if len(rs) >= min_cell else pooled).append((val, rs))

    def build(val, rs, pooled_from=None):
        n = len(rs)
        k = sum(1 for r in rs if r[outcome])
        rate = k / n if n else 0.0
        lo, hi = wilson(k, n)
        signal = "above" if lo > baseline else "below" if hi < baseline else "inconclusive"
        entry = {"value": val, "n": n, "outcomes": k, "rate": r4(rate), "ci95": [r4(lo), r4(hi)],
                 "lift": r4(rate / baseline) if baseline else None, "signal": signal}
        if pooled_from is not None:
            entry["pooled_values"] = pooled_from
            return entry
        # campaign mix + stratified lift (Simpson's-paradox guard)
        by_c = Counter(r["campaign"] for r in rs if r["campaign"])
        if by_c and campaigns_total >= 2:
            top_c, top_n = by_c.most_common(1)[0]
            entry["top_campaign"] = top_c
            entry["top_campaign_share"] = r4(top_n / n)
            entry["confounded"] = (top_n / n) >= CONFOUND_SHARE
            wsum, lsum = 0, 0.0
            for c, nc in by_c.items():
                if nc < MIN_STRATUM:
                    continue
                camp_rs = [x for x in recs if x["campaign"] == c]
                camp_rate = sum(1 for x in camp_rs if x[outcome]) / len(camp_rs) if camp_rs else 0
                if camp_rate <= 0:
                    continue
                seg_rate = sum(1 for x in rs if x["campaign"] == c and x[outcome]) / nc
                wsum += nc
                lsum += nc * (seg_rate / camp_rate)
            entry["stratified_lift"] = r4(lsum / wsum) if wsum else None
        return entry

    result = [build(v, rs) for v, rs in values]
    result.sort(key=lambda e: (-e["rate"], -e["n"]))
    other = None
    if pooled:
        flat = [r for _, rs in pooled for r in rs]
        other = build(f"other (each < {min_cell})", flat, pooled_from=sorted(v for v, _ in pooled))
    return result, other


def crosstabs(recs, outcome, baseline, min_cell):
    out = []
    for a, b in CROSSTAB_PAIRS:
        cells = defaultdict(list)
        for r in recs:
            if r[a] is not None and r[b] is not None:
                cells[(r[a], r[b])].append(r)
        rows = []
        for (va, vb), rs in cells.items():
            if len(rs) < min_cell:
                continue
            k = sum(1 for r in rs if r[outcome])
            n = len(rs)
            lo, hi = wilson(k, n)
            rows.append({a: va, b: vb, "n": n, "outcomes": k, "rate": r4(k / n),
                         "ci95": [r4(lo), r4(hi)], "lift": r4((k / n) / baseline) if baseline else None,
                         "signal": "above" if lo > baseline else "below" if hi < baseline else "inconclusive"})
        if rows:
            rows.sort(key=lambda e: (-e["rate"], -e["n"]))
            out.append({"dimensions": [a, b], "cells": rows[:12]})
    return out


def analyze(rows, min_cell=MIN_CELL_DEFAULT, min_contacted=MIN_CONTACTED_DEFAULT,
            min_outcomes=MIN_OUTCOMES_DEFAULT, today=None):
    today = today or date.today()
    if not rows:
        raise ValidationError("no rows in input")
    headers = list(rows[0].keys())
    cols = resolve_columns(headers)
    warnings = []

    if not any(f in cols for f in ("replied", "reply_label", "reply_text", "converted")):
        raise ValidationError("no outcome column found (replied / reply label / reply text / "
                              "converted) — I can't tell who replied. Headers seen: " + ", ".join(headers))
    if not any(f in cols for f in ("title", "industry", "location", "size", "seniority", "function")):
        raise ValidationError("no attribute column found (job title / industry / location / company "
                              "size / seniority / function) — nothing to profile the repliers on")
    if "contacted" not in cols:
        warnings.append("No 'contacted' column: every row is assumed to have been contacted.")
    if "campaign" not in cols:
        warnings.append("No campaign column: campaign-confounding checks are skipped. If several "
                        "campaigns with different messages are mixed here, segment lifts may reflect "
                        "the message, not the persona.")

    recs = dedup(normalize(rows, cols, today))
    contacted = [r for r in recs if r["contacted"]]
    n_contacted = len(contacted)
    n_replied = sum(1 for r in contacted if r["replied"])
    n_positive = sum(1 for r in contacted if r["positive"])
    n_accepted = sum(1 for r in contacted if r["accepted"])
    n_labeled = sum(1 for r in contacted if r["replied"] and r["label"] is not None)

    if n_contacted < min_contacted:
        raise ValidationError(f"only {n_contacted} contacted leads — below the {min_contacted} needed "
                              f"to say anything reliable about who replies. Widen the date range or "
                              f"add campaigns.")
    if n_replied < min_outcomes:
        raise ValidationError(f"only {n_replied} replies among {n_contacted} contacted leads — below "
                              f"the {min_outcomes} needed to profile repliers. Add campaigns or wait "
                              f"for replies to come in.")

    # primary outcome
    label_cov = n_labeled / n_replied if n_replied else 0.0
    if n_positive >= min_outcomes and label_cov >= LABEL_COVERAGE_FOR_POSITIVE:
        outcome, reason = "positive", (f"{n_labeled}/{n_replied} replies carry a label "
                                       f"({label_cov:.0%}) and {n_positive} are positive — profiling on "
                                       f"POSITIVE replies (interest), not on any reply.")
    else:
        outcome = "replied"
        if n_labeled == 0:
            reason = ("No reply labels: profiling on ANY reply. A 'no thanks' counts the same as a "
                      "meeting request — label the replies (POSITIVE / NOT_NOW / NEGATIVE / OOO / OTHER) "
                      "to profile on real interest.")
        else:
            reason = (f"Only {n_labeled}/{n_replied} replies are labeled ({label_cov:.0%}) or only "
                      f"{n_positive} positives — too thin to profile on positives; using any reply.")
        warnings.append(reason)

    baseline = sum(1 for r in contacted if r[outcome]) / n_contacted

    # attribute coverage
    coverage = {
        "title": sum(1 for r in contacted if r["has_title"]) / n_contacted,
        "industry": sum(1 for r in contacted if r["industry"]) / n_contacted,
        "country": sum(1 for r in contacted if r["country"]) / n_contacted,
        "size_bucket": sum(1 for r in contacted if r["size_bucket"]) / n_contacted,
        "reply_label": label_cov,
    }
    coverage["seniority"] = sum(1 for r in contacted if r["seniority"]) / n_contacted
    coverage["function"] = sum(1 for r in contacted if r["function"]) / n_contacted
    gaps = []
    for attr in ("title", "industry", "country", "size_bucket"):
        if coverage[attr] < SKIP_COVERAGE:
            gaps.append({"attribute": attr, "coverage": r4(coverage[attr]), "status": "missing"})
        elif coverage[attr] < LOW_COVERAGE:
            gaps.append({"attribute": attr, "coverage": r4(coverage[attr]), "status": "partial"})
            warnings.append(f"'{attr}' is filled on only {coverage[attr]:.0%} of contacted leads — "
                            f"its segments describe a subset; read with caution.")
    if coverage["reply_label"] < LABEL_COVERAGE_FOR_POSITIVE and n_replied:
        gaps.append({"attribute": "reply_label", "coverage": r4(coverage["reply_label"]), "status": "partial" if n_labeled else "missing"})

    campaigns = Counter(r["campaign"] for r in contacted if r["campaign"])
    campaigns_total = len(campaigns)

    # recency: replies still arriving?
    dated = [r for r in contacted if r["contacted_at"]]
    if dated:
        recent = sum(1 for r in dated if (today - r["contacted_at"]).days < 14)
        if recent / len(dated) > 0.30:
            warnings.append(f"{recent / len(dated):.0%} of contacted leads were first contacted in the "
                            f"last 14 days — their replies are still coming in; rates are understated.")

    dims = {}
    for dim in DIMENSIONS:
        cov_key = "title" if dim in ("seniority", "function") else dim
        if coverage[cov_key] < SKIP_COVERAGE:
            dims[dim] = {"skipped": True, "coverage": r4(coverage[cov_key]),
                         "reason": "attribute missing on >80% of leads"}
            continue
        values, other = segment_stats(contacted, dim, outcome, baseline, min_cell, campaigns_total)
        dims[dim] = {"coverage": r4(coverage[cov_key]), "values": values,
                     "other": other, "min_cell": min_cell}

    winning, losing = {}, {}
    for dim, d in dims.items():
        if d.get("skipped"):
            continue
        winning[dim] = [v for v in d["values"] if v["signal"] == "above"
                        and not v.get("confounded")][:4]
        losing[dim] = sorted([v for v in d["values"] if v["signal"] == "below"],
                             key=lambda v: v["rate"])[:4]

    camp_rows = []
    for c, n in campaigns.most_common():
        rs = [r for r in contacted if r["campaign"] == c]
        k = sum(1 for r in rs if r[outcome])
        lo, hi = wilson(k, n)
        camp_rows.append({"campaign": c, "n": n, "outcomes": k, "rate": r4(k / n), "ci95": [r4(lo), r4(hi)]})

    label_dist = Counter(r["label"] for r in contacted if r["replied"])

    return {
        "summary": {
            "rows_in": len(rows), "leads_x_campaigns": len(recs),
            "contacted": n_contacted, "accepted": n_accepted, "replied": n_replied,
            "positive": n_positive,
            "reply_rate": r4(n_replied / n_contacted),
            "positive_rate": r4(n_positive / n_contacted),
            "accept_rate": r4(n_accepted / n_contacted) if n_accepted else None,
            "primary_outcome": "positive_reply" if outcome == "positive" else "reply",
            "primary_outcome_reason": reason,
            "baseline_rate": r4(baseline),
            "campaigns": campaigns_total,
            "min_cell": min_cell,
            "scope_note": "Rates describe the leads you actually contacted. Segments you never "
                          "targeted cannot appear — this is your ICP within your targeted universe.",
        },
        "reply_labels": {k or "UNLABELED": v for k, v in label_dist.items()},
        "coverage": {k: r4(v) for k, v in coverage.items()},
        "attribute_gaps": gaps,
        "dimensions": dims,
        "crosstabs": crosstabs(contacted, outcome, baseline, min_cell),
        "winning": winning,
        "losing": losing,
        "campaigns": camp_rows,
        "columns_used": cols,
        "data_quality": {"warnings": warnings},
    }


# ---------------------------------------------------------------- self-test

def _synth(n, **fields):
    """n rows with constant fields; outcome columns given as rates -> deterministic fill."""
    rows = []
    for i in range(n):
        r = {"Lead id": f"{fields.get('prefix','L')}{i}"}
        for k, v in fields.items():
            if k == "prefix":
                continue
            if k in ("replied", "positive", "accepted") and isinstance(v, float):
                rate = v
                r_replied = (i % 100) < round(rate * 100)
                if k == "replied":
                    r["Replied"] = "yes" if r_replied else ""
                elif k == "positive":
                    r["Reply label"] = "Interested" if r_replied else ("Not interested" if r.get("Replied") else "")
                elif k == "accepted":
                    r["Accepted"] = "1" if r_replied else "0"
            else:
                r[k] = v
        rows.append(r)
    return rows


def _selftest():
    failures, total = [], [0]
    def check(name, cond, detail=""):
        total[0] += 1
        if not cond:
            failures.append(f"{name} {detail}")

    # 1. title classification goldens
    goldens = [
        ("Founder & CEO", "Owner / Founder", "General management"),
        ("GTM Engineer", "Individual contributor", "RevOps / GTM Ops"),
        ("VP Sales", "VP", "Sales"),
        ("Head of Growth", "Director / Head", "Marketing / Growth"),
        ("Partnerships Manager", "Manager / Lead", "Sales"),
        ("Senior Account Executive", "Senior IC", "Sales"),
        ("Stagiaire marketing", "Entry / Student", "Marketing / Growth"),
        ("Directrice Marketing", "Director / Head", "Marketing / Growth"),
        ("Chief Revenue Officer", "C-level", "Sales"),
        ("Responsable RH", "Manager / Lead", "People / HR"),
        ("Fractional CMO", "C-level", "Marketing / Growth"),
        ("Software Engineer", "Individual contributor", "Engineering / Data"),
        ("", None, None),
    ]
    for t, es, ef in goldens:
        s, f = classify_title(t)
        check("classify_title", (s, f) == (es, ef), f"{t!r} -> {(s, f)} expected {(es, ef)}")

    # 2. reply label normalization
    for raw, exp in [("Not interested", "NEGATIVE"), ("Intéressé", "POSITIVE"), ("Out of office", "OOO"),
                     ("Meeting booked", "POSITIVE"), ("Pas maintenant", "NOT_NOW"), ("", None),
                     ("Referral to colleague", "OTHER"), ("weird label", "OTHER"), ("POSITIVE", "POSITIVE")]:
        check("normalize_label", normalize_label(raw) == exp, f"{raw!r} -> {normalize_label(raw)} expected {exp}")

    # 3. parsing helpers
    check("parse_bool date", parse_bool("2026-08-10") is True)
    check("parse_bool yes", parse_bool("yes") is True)
    check("parse_bool 0", parse_bool("0") is False)
    check("parse_bool empty", parse_bool("") is False)
    check("size 11-50 employees", size_bucket("11-50 employees") == "11-50")
    check("size 1,001-5,000", size_bucket("1,001-5,000") == "1001-5000")
    check("size 250", size_bucket("250") == "201-500")
    check("size 10001+", size_bucket("10,001+") == "5001+")
    check("country lagos", country_of("Lagos, Lagos State, Nigeria") == "Nigeria")
    check("country us", country_of("United States") == "United States")
    check("country paris", country_of("Paris, Île-de-France, France") == "France")
    check("country uk", country_of("Greater London Area, UK") == "United Kingdom")
    lo, hi = wilson(30, 100)
    check("wilson", abs(lo - 0.2189) < 0.001 and abs(hi - 0.3958) < 0.001, f"{(lo, hi)}")

    # 4. planted signal: CXO 30% vs Manager 10% -> above / below
    rows = (_synth(200, prefix="A", **{"Job title": "CEO", "Industry": "Software", "Location": "France",
                                        "Campaign": "camp-1", "replied": 0.30})
            + _synth(200, prefix="B", **{"Job title": "Marketing Manager", "Industry": "Software",
                                          "Location": "France", "Campaign": "camp-1", "replied": 0.10}))
    rep = analyze(rows)
    sen = {v["value"]: v for v in rep["dimensions"]["seniority"]["values"]}
    check("signal CXO above", sen["C-level"]["signal"] == "above", str(sen.get("C-level")))
    check("signal Manager below", sen["Manager / Lead"]["signal"] == "below", str(sen.get("Manager / Lead")))
    check("primary reply when no labels", rep["summary"]["primary_outcome"] == "reply")
    check("winning has C-level", any(v["value"] == "C-level" for v in rep["winning"]["seniority"]))
    check("industry skipped? no", not rep["dimensions"]["industry"].get("skipped"))
    check("no campaign confound flag with 1 campaign", "confounded" not in sen["C-level"])

    # 5. confounding: Fintech only in the good campaign -> naive lift > 1 but flagged, stratified ≈ 1
    rows = (_synth(150, prefix="F", **{"Job title": "Sales Manager", "Industry": "Fintech",
                                        "Campaign": "good", "replied": 0.30})
            + _synth(150, prefix="R", **{"Job title": "Sales Manager", "Industry": "Retail",
                                          "Campaign": "bad", "replied": 0.10}))
    rep = analyze(rows)
    ind = {v["value"]: v for v in rep["dimensions"]["industry"]["values"]}
    check("confound naive lift", ind["Fintech"]["lift"] > 1.2, str(ind["Fintech"]))
    check("confound flagged", ind["Fintech"].get("confounded") is True, str(ind["Fintech"]))
    check("confound stratified ~1", abs(ind["Fintech"]["stratified_lift"] - 1.0) < 0.01, str(ind["Fintech"]))
    check("confounded excluded from winning", not any(v["value"] == "Fintech" for v in rep["winning"]["industry"]))

    # 6. min-cell pooling
    rows = (_synth(120, prefix="X", **{"Job title": "CEO", "Industry": "Software", "replied": 0.25})
            + _synth(5, prefix="Y", **{"Job title": "CEO", "Industry": "Maritime", "replied": 0.20}))
    rep = analyze(rows)
    check("pooled other", rep["dimensions"]["industry"]["other"] is not None
          and "Maritime" in rep["dimensions"]["industry"]["other"]["pooled_values"])
    check("pooled not in values", all(v["value"] != "Maritime" for v in rep["dimensions"]["industry"]["values"]))

    # 7. positive-reply primary outcome when labels cover replies
    rows = (_synth(200, prefix="P", **{"Job title": "CEO", "Industry": "Software", "replied": 0.30, "positive": 0.30}))
    # positive fill uses same modulo as replied -> all repliers labeled Interested
    rep = analyze(rows)
    check("primary positive", rep["summary"]["primary_outcome"] == "positive_reply", rep["summary"]["primary_outcome_reason"])
    check("positive count", rep["summary"]["positive"] == 60, str(rep["summary"]["positive"]))

    # 8. FR headers + JSON input + dedup
    fr = [{"Poste": "Directeur Commercial", "Secteur": "Logiciels", "Pays": "France", "A répondu": "oui",
           "Campagne": "c1", "Email": f"p{i}@x.fr"} for i in range(60)]
    fr += [{"Poste": "Directeur Commercial", "Secteur": "Logiciels", "Pays": "France", "A répondu": "",
            "Campagne": "c1", "Email": f"q{i}@x.fr"} for i in range(60)]
    fr += [dict(fr[0])]      # exact duplicate lead -> merged
    rep = analyze(json.dumps(fr) and read_rows(json.dumps(fr)))
    check("fr headers replied", rep["summary"]["replied"] == 60, str(rep["summary"]))
    check("fr dedup", rep["summary"]["contacted"] == 120, str(rep["summary"]["contacted"]))
    check("fr seniority", rep["dimensions"]["seniority"]["values"][0]["value"] == "Director / Head")

    # 9. refusals
    def refuses(rows, frag):
        try:
            analyze(rows)
            return False
        except ValidationError as e:
            return frag in str(e)
    check("refuse too few contacted", refuses(_synth(50, **{"Job title": "CEO", "replied": 0.5}), "contacted leads"))
    check("refuse too few replies", refuses(_synth(200, **{"Job title": "CEO", "replied": 0.05}), "replies"))
    check("refuse no outcome", refuses([{"Job title": "CEO", "Industry": "x"} for _ in range(150)], "outcome column"))
    check("refuse no attributes", refuses([{"Lead id": str(i), "Replied": "yes"} for i in range(150)], "attribute column"))
    check("refuse empty", refuses([], "no rows"))

    # 10. attribute gap reporting (industry missing -> gap + dimension skipped)
    rows = _synth(150, **{"Job title": "CEO", "replied": 0.30})
    rep = analyze(rows)
    check("gap industry missing", any(g["attribute"] == "industry" and g["status"] == "missing" for g in rep["attribute_gaps"]))
    check("industry skipped", rep["dimensions"]["industry"].get("skipped") is True)
    check("label gap when unlabeled", any(g["attribute"] == "reply_label" for g in rep["attribute_gaps"]))

    n = total[0]
    if failures:
        for f in failures:
            print("FAIL:", f, file=sys.stderr)
        print(f"{n - len(failures)}/{n} checks passed — {len(failures)} FAILED", file=sys.stderr)
        return 1
    print(f"{n}/{n} checks passed")
    return 0


# ---------------------------------------------------------------- main

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input", nargs="?", help="CSV/JSON path, or - for stdin")
    p.add_argument("--min-cell", type=int, default=MIN_CELL_DEFAULT,
                   help=f"contacted leads a segment needs to be reported alone (default {MIN_CELL_DEFAULT})")
    p.add_argument("--min-contacted", type=int, default=MIN_CONTACTED_DEFAULT)
    p.add_argument("--min-outcomes", type=int, default=MIN_OUTCOMES_DEFAULT)
    p.add_argument("--today", help="YYYY-MM-DD (for recency checks; default today)")
    p.add_argument("--test", action="store_true", help="run the self-test")
    a = p.parse_args()
    if a.test:
        sys.exit(_selftest())
    if not a.input:
        p.print_help()
        sys.exit(2)
    raw = sys.stdin.read() if a.input == "-" else open(a.input, encoding="utf-8-sig").read()
    try:
        rows = read_rows(raw)
        today = date.fromisoformat(a.today) if a.today else None
        report = analyze(rows, min_cell=a.min_cell, min_contacted=a.min_contacted,
                         min_outcomes=a.min_outcomes, today=today)
    except ValidationError as e:
        print(f"error: {e}", file=sys.stderr)
        sys.exit(2)
    print(json.dumps(report, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
