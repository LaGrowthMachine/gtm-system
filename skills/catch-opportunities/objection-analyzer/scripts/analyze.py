#!/usr/bin/env python3
"""analyze.py — the objection engine behind the objection-analyzer skill.

Deterministic. It does the arithmetic the model must NOT improvise: count
objection instances, compute shares, compute the recovery rate on a matured
cohort, merge runs without double-counting, and render the playbook. It
validates its input and REFUSES to emit a best-effort result on garbage — a
recovery rate that is plausible and wrong is exactly the silent failure this
tier exists to prevent. Someone coaches the wrong objection for a quarter and
only finds out from the pipeline.

THE SPLIT (this is the part that matters):
  • The MODEL judges  — which objection type, is it a smokescreen, how good was
    our reply on the 9-dimension rubric, and all the prose.
  • The SCRIPT counts — instances, shares, recovery, trend, merge, dedup, and
    the rendered cards.
The script also owns the maturity window and the small-n suppression. Those are
policy, not arithmetic, but they are the two places a model produces a number
that is both plausible and flattering, so they live in code.

RECOVERY (why it is defined this narrowly):
  handled   = a `sent` message exists after the objection, status != SEND_FAILED
              (a SEND_FAILED can appear as direction=received; it is a failed
              outbound of ours, not a reply)
  pending   = handled, but younger than --maturity-days -> excluded from BOTH
              numerator and denominator, because a thread from Tuesday is not
              a failure yet
  recovered = handled, matured, and the lead replied again (not auto/OOO, not
              a firm no)
  dead      = handled, matured, no qualifying reply
  recovery_rate = recovered / (recovered + dead)     [null below --min-n]
  no_reply_rate = unhandled / count                  [we never answered]

Usage
    python3 analyze.py doctor [--export]
    python3 analyze.py normalize threads.csv > threads.json
    python3 analyze.py analyze run.json [--as-of YYYY-MM-DD] > report.json
    python3 analyze.py merge report.json [--write] [--reclassify] > state.json
    python3 analyze.py render [--window 90] [--out DIR]
    python3 analyze.py purge --before YYYY-MM-DD [--redact]
    python3 analyze.py --test

Output: JSON on stdout. Errors go to stderr with exit code 2 — when the engine
refuses, the caller should ASK the user, not guess.
"""
import sys, os, csv, json, argparse, io, re, statistics, shutil
from datetime import datetime, timedelta, timezone

STATE_VERSION = 1
MATURITY_DAYS_DEFAULT = 7
MIN_N_DEFAULT = 5
WINDOW_DEFAULT = 90
BACKUPS_KEPT = 10

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAXONOMY_PATH = os.path.join(SKILL_DIR, "references", "objection-taxonomy.json")
BASELINE_PATH = os.path.join(SKILL_DIR, "references", "baseline-playbook.md")
LOCATION_PATH = os.path.join(SKILL_DIR, "playbook", "LOCATION")

RECOVERY_EXCLUDED = {"none", "auto_ooo", "not_interested", "voice_message"}
# The recovery numerator is a membership test, so an unrecognised string reads as a
# recovery. That fails in the flattering direction on the one number the whole tool is
# judged by, which is exactly what this tier exists to prevent. Both vocabularies are
# closed and refused on, like `type` and `goal`.
POST_CATEGORIES = {"interested", "curious", "question", "not_interested",
                   "auto_ooo", "voice_message", "none"}
REPLY_CATEGORIES = {"interested", "curious", "question", "objection", "wrong_fit",
                    "not_interested", "auto_ooo", "voice_message"}
PRODUCT_MIN_N = 15             # a roadmap conversation needs more than five threads
COPY_LIFT_POINTS = 0.15        # points above the base rate of the OTHER types
SETTLE_DAYS = 30               # below this an outcome can still change, so keep re-reading
PROGRESSED = {"interested", "question", "curious"}
RUBRIC_KEYS = ["tone_match", "addresses_message", "length_mirrors", "one_question_max",
               "no_forbidden_phrases", "not_pushy", "resource_priority", "not_creepy",
               "process_compliant"]
BEST_REPLY_FLOOR = 22          # out of 27
# The goal is not arithmetic, but it decides what dimension 7 of the rubric even means,
# so it is recorded with the run rather than left in the chat. A playbook that does not
# say what it was scored against cannot be re-read six weeks later.
GOALS = ["meeting", "signup", "resource", "partnership", "nurture", "unspecified"]
WELL_HANDLED_FLOOR = 18        # median rubric above which "we answer it well"


class ValidationError(Exception):
    pass


# ---------------------------------------------------------------- taxonomy

_TAX = None

def taxonomy():
    global _TAX
    if _TAX is None:
        try:
            with open(TAXONOMY_PATH, encoding="utf-8") as fh:
                _TAX = json.load(fh)
        except FileNotFoundError:
            raise ValidationError(
                "references/objection-taxonomy.json is missing. The skill folder is "
                "incomplete — reinstall it.")
    return _TAX

def canonical_ids():
    return [t["id"] for t in taxonomy()["types"]]

def type_meta(tid):
    for t in taxonomy()["types"]:
        if t["id"] == tid:
            return t
    return None

def resolve_alias(raw):
    """Map a foreign label onto a canonical id. Returns None if unknown."""
    if not raw:
        return None
    key = str(raw).strip().lower().replace(" ", "_").replace("-", "_")
    for t in taxonomy()["types"]:
        if key == t["id"]:
            return t["id"]
        for a in t["aliases"]:
            if key == a.lower().replace(" ", "_").replace("-", "_"):
                return t["id"]
    return None


# ---------------------------------------------------------------- helpers

def parse_ts(raw, where=""):
    """ISO 8601 WITH an offset. Naive timestamps are refused: without a zone,
    a 7-day maturity window silently shifts by up to a day per record."""
    if raw is None or str(raw).strip() == "":
        raise ValidationError("Missing timestamp %s." % where)
    s = str(raw).strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        raise ValidationError("Unparseable timestamp %r %s. Use ISO 8601, e.g. 2026-08-18T09:12:00+00:00." % (raw, where))
    if dt.tzinfo is None:
        raise ValidationError("Timestamp %r %s has no UTC offset. Add one (…+00:00) — a naive timestamp shifts the maturity window." % (raw, where))
    return dt.astimezone(timezone.utc)


def parse_day(raw, where=""):
    if raw is None or str(raw).strip() == "":
        raise ValidationError("Missing date %s." % where)
    s = str(raw).strip()
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(timezone.utc) \
            if ("T" in s or "+" in s) else datetime.fromisoformat(s + "T00:00:00+00:00")
    except ValueError:
        raise ValidationError("Unparseable date %r %s. Use YYYY-MM-DD." % (raw, where))


def apportion(counts, total):
    """Shares to 3dp that sum to exactly 1.000 (largest remainder). Naive
    per-item rounding drifts by up to 0.0045 across 9 types, which then shows
    up as a table of percentages that does not add to 100."""
    if not total:
        return {k: 0.0 for k in counts}
    scaled = {k: (v * 1000.0) / total for k, v in counts.items()}
    floors = {k: int(v) for k, v in scaled.items()}
    rest = 1000 - sum(floors.values())
    order = sorted(counts, key=lambda k: (-(scaled[k] - floors[k]), k))
    for k in order[:rest]:
        floors[k] += 1
    return {k: round(v / 1000.0, 3) for k, v in floors.items()}


def pct(x):
    return None if x is None else int(round(x * 100))


def rate(num, den, min_n):
    """A rate plus its n, or an explicit suppression. Never a bare number."""
    if den < min_n:
        return {"value": None, "n": den, "suppressed": True}
    return {"value": round(num / den, 3), "n": den, "suppressed": False}


def dumps(obj):
    return json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False)


# ---------------------------------------------------------------- location

def _writable(path):
    try:
        os.makedirs(path, exist_ok=True)
        probe = os.path.join(path, ".write-probe")
        with open(probe, "w") as fh:
            fh.write("ok")
        os.remove(probe)
        return True
    except Exception:
        return False


def resolve_location():
    """Walk the ladder. The skill folder is the ANCHOR (this file locates
    itself), but the DATA lives wherever survives: a package update replaces
    the skill folder, and a sandbox keeps nothing at all."""
    env = os.environ.get("OBJECTION_PLAYBOOK_DIR")
    if env:
        p = os.path.abspath(os.path.expanduser(env))
        if _writable(p):
            return {"tier": "env", "path": p, "why": "OBJECTION_PLAYBOOK_DIR is set"}
    xdg = os.environ.get("XDG_DATA_HOME")
    home = os.path.join(xdg, "objection-analyzer") if xdg else \
        os.path.join(os.path.expanduser("~"), ".gtm-skills", "objection-analyzer")
    if _writable(home):
        return {"tier": "home", "path": home, "why": "default — survives a skill reinstall"}
    skill = os.path.join(SKILL_DIR, "playbook")
    if _writable(skill):
        return {"tier": "skill", "path": skill,
                "why": "home not writable — WARNING: a skill update can erase this"}
    cwd = os.path.abspath(os.path.join(os.getcwd(), ".objection-playbook"))
    if _writable(cwd):
        return {"tier": "cwd", "path": cwd, "why": "home and skill folder not writable"}
    return {"tier": "paste", "path": None,
            "why": "nothing writable — carry the state by hand, and label every number estimated"}


def state_path(loc):
    return None if not loc["path"] else os.path.join(loc["path"], "state.json")


def write_anchor(loc):
    try:
        os.makedirs(os.path.dirname(LOCATION_PATH), exist_ok=True)
        with open(LOCATION_PATH, "w", encoding="utf-8") as fh:
            fh.write("%s\t%s\n" % (loc["tier"], loc["path"] or "-"))
    except Exception:
        pass


def empty_state():
    return {"state_version": STATE_VERSION, "created_at": None, "updated_at": None,
            "runs": [], "instances": {}, "reply_mix_runs": [], "seen_thread_ids": [],
            "cards": {}, "not_computed": []}


def load_state(loc):
    sp = state_path(loc)
    if not sp or not os.path.exists(sp):
        return empty_state()
    with open(sp, encoding="utf-8") as fh:
        st = json.load(fh)
    v = st.get("state_version")
    if v != STATE_VERSION:
        raise ValidationError(
            "state.json is version %r, this engine speaks version %d. Refusing to "
            "merge — unknown fields would be dropped silently. Back the file up and "
            "migrate it deliberately." % (v, STATE_VERSION))
    return st


# ---------------------------------------------------------------- validation

def validate_run(run):
    if not isinstance(run, dict):
        raise ValidationError("Input must be a JSON object, got %s." % type(run).__name__)
    for k in ("run_id", "as_of"):
        if not run.get(k):
            raise ValidationError("Missing required field %r." % k)
    parse_day(run["as_of"], "in as_of")
    goal = (run.get("scope") or {}).get("goal", "unspecified")
    if goal not in GOALS:
        raise ValidationError(
            "Unknown conversation goal %r. Allowed: %s. The goal decides what a good "
            "dimension-7 score means, so it cannot be guessed silently." % (goal, ", ".join(GOALS)))

    threads = run.get("threads") or []
    if not isinstance(threads, list):
        raise ValidationError("`threads` must be a list.")
    by_id = {}
    for t in threads:
        tid = t.get("thread_id")
        if not tid:
            raise ValidationError("A thread has no thread_id.")
        if tid in by_id:
            raise ValidationError("Duplicate thread_id %r." % tid)
        msgs = t.get("messages") or []
        if not msgs:
            raise ValidationError("Thread %r has no messages." % tid)
        last = None
        for i, m in enumerate(msgs):
            d = m.get("direction")
            if d not in ("sent", "received"):
                raise ValidationError("Thread %r message %d: direction must be 'sent' or 'received', got %r." % (tid, i, d))
            # Platform events (LGM status lines, AUTO_QUALIFY notes) arrive with
            # direction=received. They are not the person. Left unmarked, one landing
            # after our reply would count as the lead coming back — a silent, and
            # always flattering, inflation of the recovery rate.
            m["_event"] = bool(m.get("is_event")) or \
                str(m.get("status", "")).upper() == "INFO" or \
                str(m.get("channel", "")).upper() in ("LGM", "AUTO_QUALIFY")
            ts = parse_ts(m.get("at"), "in thread %r message %d" % (tid, i))
            if last is not None and ts < last:
                raise ValidationError("Thread %r message %d goes back in time (%s before %s). Sort the timeline." % (tid, i, m.get("at"), last.isoformat()))
            last = ts
            m["_ts"] = ts
        by_id[tid] = t

    valid = set(canonical_ids())
    seen_inst = set()
    for ann in (run.get("annotations") or []):
        tid = ann.get("thread_id")
        if tid not in by_id:
            raise ValidationError("Annotation references unknown thread_id %r." % tid)
        th = by_id[tid]
        msgs = th["messages"]
        cat = ann.get("reply_category")
        if not cat:
            raise ValidationError("Annotation for thread %r has no reply_category." % tid)
        if cat not in REPLY_CATEGORIES:
            raise ValidationError(
                "Unknown reply_category %r on thread %r. Allowed: %s."
                % (cat, tid, ", ".join(sorted(REPLY_CATEGORIES))))
        for ob in (ann.get("objections") or []):
            ot = ob.get("type")
            if ot not in valid:
                hint = resolve_alias(ot)
                raise ValidationError(
                    "Unknown objection type %r on thread %r.%s Allowed: %s."
                    % (ot, tid,
                       (" Did you mean %r?" % hint) if hint else "",
                       ", ".join(sorted(valid))))
            iid = ob.get("instance_id") or "%s#%s" % (tid, ob.get("objection_msg_index"))
            ob["instance_id"] = iid
            if iid in seen_inst:
                raise ValidationError("Duplicate instance_id %r in this run." % iid)
            seen_inst.add(iid)
            post = ob.get("post_objection_category")
            if post is not None and str(post).strip().lower() not in POST_CATEGORIES:
                raise ValidationError(
                    "Unknown post_objection_category %r on thread %r. Allowed: %s. This field "
                    "decides the recovery numerator, so it is never guessed."
                    % (post, tid, ", ".join(sorted(POST_CATEGORIES))))
            oi = ob.get("objection_msg_index")
            if not isinstance(oi, int) or oi < 0 or oi >= len(msgs):
                raise ValidationError("Thread %r: objection_msg_index %r is out of range (0..%d)." % (tid, oi, len(msgs) - 1))
            if msgs[oi]["direction"] != "received":
                raise ValidationError("Thread %r: objection_msg_index %d points at a `sent` message. An objection lives on a message the lead sent." % (tid, oi))
            if msgs[oi]["_event"]:
                raise ValidationError("Thread %r: objection_msg_index %d points at a platform event (an INFO or AUTO_QUALIFY line), not at something the lead wrote." % (tid, oi))
            h = ob.get("handling")
            if h:
                ri = h.get("reply_msg_index")
                if not isinstance(ri, int) or ri < 0 or ri >= len(msgs):
                    raise ValidationError("Thread %r: handling.reply_msg_index %r is out of range." % (tid, ri))
                if ri <= oi:
                    raise ValidationError("Thread %r: handling.reply_msg_index %d is not after the objection at %d." % (tid, ri, oi))
                if msgs[ri]["direction"] != "sent":
                    raise ValidationError("Thread %r: handling.reply_msg_index %d points at a `received` message. That is not our reply." % (tid, ri))
                if msgs[ri]["_event"]:
                    raise ValidationError("Thread %r: handling.reply_msg_index %d points at a platform event, not at a message we sent." % (tid, ri))
                if str(msgs[ri].get("status", "")).upper() == "SEND_FAILED":
                    raise ValidationError("Thread %r: handling.reply_msg_index %d points at a SEND_FAILED message. It never reached the lead, so it is not a handling reply." % (tid, ri))
                rub = h.get("rubric")
                if rub is not None:
                    if set(rub) != set(RUBRIC_KEYS):
                        missing = sorted(set(RUBRIC_KEYS) - set(rub))
                        extra = sorted(set(rub) - set(RUBRIC_KEYS))
                        raise ValidationError("Thread %r: rubric keys wrong. Missing %s, unexpected %s." % (tid, missing or "none", extra or "none"))
                    for k, v in rub.items():
                        if not isinstance(v, int) or v < 0 or v > 3:
                            raise ValidationError("Thread %r: rubric %s=%r must be an integer 0-3." % (tid, k, v))
    return by_id


# ---------------------------------------------------------------- analyze

def analyze(run, maturity_days=MATURITY_DAYS_DEFAULT, min_n=MIN_N_DEFAULT, as_of=None):
    by_id = validate_run(run)
    as_of_dt = parse_day(as_of or run["as_of"], "in as_of")
    warnings = []

    anns = run.get("annotations") or []
    instances = []
    for ann in anns:
        th = by_id[ann["thread_id"]]
        msgs = th["messages"]
        first_recv = next((i for i, m in enumerate(msgs)
                           if m["direction"] == "received" and not m["_event"]), None)
        for ob in (ann.get("objections") or []):
            oi = ob["objection_msg_index"]
            h = ob.get("handling") or {}
            ri = h.get("reply_msg_index")
            handled = ri is not None
            t1 = msgs[ri]["_ts"] if handled else None
            matured = handled and (as_of_dt - t1) >= timedelta(days=maturity_days)
            post = (ob.get("post_objection_category") or "none").strip().lower()
            recovered = bool(matured and post not in RECOVERY_EXCLUDED)
            if recovered:
                if not any(m["direction"] == "received" and not m["_event"] and m["_ts"] > t1
                           for m in msgs):
                    raise ValidationError(
                        "Thread %r claims post_objection_category=%r but the timeline has no "
                        "received message after our reply. One of the two is wrong."
                        % (ann["thread_id"], post))
            mk = ob.get("smokescreen_markers") or {}
            rub = h.get("rubric")
            instances.append({
                "instance_id": ob["instance_id"],
                "thread_id": ann["thread_id"],
                "type": ob["type"],
                "objection_at": msgs[oi]["_ts"].isoformat(),
                "campaign_id": th.get("campaign_id"),
                "identity_id": th.get("identity_id"),
                "channel": th.get("channel"),
                "lead_ref": th.get("lead_ref"),
                "verbatim": (ob.get("verbatim") or "")[:200],
                "reply_verbatim": (h.get("verbatim") or "")[:400],
                "is_first_touch": (first_recv is not None and oi == first_recv),
                "smokescreen": sum(1 for k in ("pre_information", "no_specifics", "immediate_drop") if mk.get(k)) >= 2,
                "handled": handled,
                "matured": bool(matured),
                "outcome": ("unhandled" if not handled else
                            "pending" if not matured else
                            "recovered" if recovered else "dead"),
                "progressed": bool(recovered and post in PROGRESSED),
                "response_hours": (round((t1 - msgs[oi]["_ts"]).total_seconds() / 3600.0, 1)
                                   if handled else None),
                "rubric_total": (sum(rub.values()) if rub else None),
                "should_have": h.get("should_have"),
                "post_objection_category": post,
            })

    total = len(instances)
    def ft_base_excluding(tid):
        """First-touch share of every OTHER type. Including the type under test lets it drag
        its own baseline, which made the verdict a function of corpus composition: the same
        90 price threads scored `inconclusive` next to 10 timing objections and `copy` next
        to 90. Leave-one-out is the standard construction for exactly this."""
        others = [i for i in instances if i["type"] != tid]
        if not others:
            return None
        return round(sum(1 for i in others if i["is_first_touch"]) / len(others), 3)
    counts = {}
    for inst in instances:
        counts[inst["type"]] = counts.get(inst["type"], 0) + 1
    shares = apportion(counts, total)

    account_shares = dict(shares)
    by_type = []
    for tid in sorted(counts, key=lambda k: (-counts[k], k)):
        rows = [i for i in instances if i["type"] == tid]
        rec = [r for r in rows if r["outcome"] == "recovered"]
        dead = [r for r in rows if r["outcome"] == "dead"]
        unh = [r for r in rows if r["outcome"] == "unhandled"]
        pend = [r for r in rows if r["outcome"] == "pending"]
        den = len(rec) + len(dead)
        rts = [r["rubric_total"] for r in rows if r["rubric_total"] is not None]
        hrs = [r["response_hours"] for r in rows if r["response_hours"] is not None]
        scored = sorted([r for r in rows if r["rubric_total"] is not None],
                        key=lambda r: (-r["rubric_total"], r["instance_id"]))
        best = scored[0] if scored and scored[0]["rubric_total"] >= BEST_REPLY_FLOOR else None
        # A single scored reply is an exemplar or nothing. Calling the same 27/27 reply the
        # "weakest, coach this one" is how a card loses a reader's trust on sight.
        worst = (scored[-1] if scored and (len(scored) > 1 or scored[-1] is not best)
                 and scored[-1]["rubric_total"] < BEST_REPLY_FLOOR else None)

        camp = {}
        for r in rows:
            if r["campaign_id"]:
                camp[r["campaign_id"]] = camp.get(r["campaign_id"], 0) + 1
        camp_rows, lift_max = [], None
        if camp:
            camp_tot = {}
            for i in instances:
                if i["campaign_id"]:
                    camp_tot[i["campaign_id"]] = camp_tot.get(i["campaign_id"], 0) + 1
            for cid in sorted(camp):
                in_c = camp[cid] / camp_tot[cid]
                lift = round(in_c / account_shares[tid], 2) if account_shares[tid] else None
                camp_rows.append({"campaign_id": cid, "count": camp[cid],
                                  "share_in_campaign": round(in_c, 3), "lift_vs_account": lift})
                if camp[cid] >= min_n and lift is not None and (lift_max is None or lift > lift_max):
                    lift_max = lift

        ft_share = round(sum(1 for r in rows if r["is_first_touch"]) / len(rows), 3)
        handled_share = round(sum(1 for r in rows if r["handled"]) / len(rows), 3)
        med_rub = round(statistics.median(rts), 1) if rts else None
        recovery = rate(len(rec), den, min_n)

        ft_base = ft_base_excluding(tid)
        sig_copy = (ft_share >= 0.5 and ft_base is not None
                    and (ft_share - ft_base) >= COPY_LIFT_POINTS)
        sig_target = lift_max is not None and lift_max > 2.0
        sig_product = (not sig_copy
                       and recovery["value"] is not None and recovery["value"] < 0.20
                       and recovery["n"] >= PRODUCT_MIN_N
                       and handled_share > 0.70
                       and med_rub is not None and med_rub >= WELL_HANDLED_FLOOR)
        n = len(rows)
        conf = "high" if n >= 20 else "medium" if n >= 10 else "low" if n >= min_n else None
        # Precedence collapses three independent booleans into one owner. Emit all three so
        # the caller can say "copy: yes, targeting: yes" instead of hiding the collision.
        verdict = ("product" if sig_product else "targeting" if sig_target
                   else "copy" if sig_copy else "inconclusive")
        also = [k for k, v in (("copy", sig_copy), ("targeting", bool(sig_target)),
                               ("product", sig_product)) if v and k != verdict]
        if conf is None:
            # Below min_n a verdict is a coin flip dressed as a finding.
            verdict = "inconclusive"

        by_type.append({
            "type": tid, "label": (type_meta(tid) or {}).get("label", tid),
            "family": (type_meta(tid) or {}).get("family"),
            "count": n, "share": shares[tid], "share_pct": pct(shares[tid]),
            "handled": len([r for r in rows if r["handled"]]), "handled_share": handled_share,
            "pending": len(pend), "recovered": len(rec), "dead": len(dead),
            "recovery_rate": recovery,
            "progression_rate": rate(sum(1 for r in rec if r["progressed"]), den, min_n),
            "no_reply_rate": rate(len(unh), n, min_n),
            "median_response_hours": (round(statistics.median(hrs), 1) if hrs else None),
            "median_rubric": med_rub,
            "first_touch_share": ft_share,
            "smokescreen_share": round(sum(1 for r in rows if r["smokescreen"]) / n, 3),
            "by_campaign": camp_rows,
            "diagnosis": {"copy": sig_copy, "targeting": (None if not camp else sig_target),
                          "product": sig_product, "verdict": verdict, "confidence": conf,
                          "max_lift": lift_max,
                          "also_firing": also,
                          "first_touch_base": ft_base,
                          "first_touch_lift_points": (round(ft_share - ft_base, 3)
                                                      if ft_base is not None else None)},
            "best_reply": ({"instance_id": best["instance_id"], "score": best["rubric_total"],
                            "objection": best["verbatim"], "reply": best["reply_verbatim"],
                            "lead_ref": best["lead_ref"]} if best else None),
            "worst_reply": ({"instance_id": worst["instance_id"], "score": worst["rubric_total"],
                             "objection": worst["verbatim"], "reply": worst["reply_verbatim"],
                             "should_have": worst["should_have"]} if worst else None),
        })

    # reply mix — wrong_fit and not_interested are first-class output, never
    # folded into the objection share
    mix_counts, wf_sub = {}, {}
    for ann in anns:
        c = ann["reply_category"]
        mix_counts[c] = mix_counts.get(c, 0) + 1
        if c == "wrong_fit" and ann.get("wrong_fit_subtype"):
            wf_sub[ann["wrong_fit_subtype"]] = wf_sub.get(ann["wrong_fit_subtype"], 0) + 1
    mix_total = len(anns)
    mix_shares = apportion(mix_counts, mix_total)
    vmap = taxonomy()["segmentation_verdict_map"]
    ranked = sorted(wf_sub, key=lambda k: (-wf_sub[k], k))
    dom = (ranked[0] if ranked and (len(ranked) == 1 or wf_sub[ranked[0]] > wf_sub[ranked[1]])
           else None)
    wf_campaigns = {}
    for ann in anns:
        if ann["reply_category"] == "wrong_fit":
            cid = by_id[ann["thread_id"]].get("campaign_id")
            if cid:
                wf_campaigns[cid] = wf_campaigns.get(cid, 0) + 1

    if not any(t.get("campaign_id") for t in (run.get("threads") or [])):
        warnings.append("No campaign dimension in this data — the targeting signal is not assessable (null, not zero).")
    if not any(str(m.get("status", "")).upper() == "SEND_FAILED"
               for t in (run.get("threads") or []) for m in t["messages"]) and \
       not any("status" in m for t in (run.get("threads") or []) for m in t["messages"]):
        warnings.append("No `status` field on any message — the SEND_FAILED correction could not be applied. Sends are assumed to have landed.")

    return {
        "engine_version": STATE_VERSION,
        "run_id": run["run_id"], "as_of": run["as_of"],
        "source": run.get("source"), "scope": run.get("scope"),
        "goal": (run.get("scope") or {}).get("goal", "unspecified"),
        "params": {"maturity_days": maturity_days, "min_n": min_n},
        "coverage": {
            "threads_in": len(run.get("threads") or []),
            "threads_annotated": mix_total,
            "objection_instances": total,
            "objection_threads": len({i["thread_id"] for i in instances}),
            "objection_rate_of_replies": (round(len({i["thread_id"] for i in instances}) / mix_total, 3)
                                          if mix_total else None),
            "reads_replies_only": "This reads replies. It cannot tell you what the people who never replied objected to — usually the majority.",
        },
        "baseline_mode": total == 0,
        "by_type": by_type,
        "reply_mix": {
            "total_replies": mix_total,
            "categories": [{"category": c, "count": mix_counts[c], "share": mix_shares[c],
                            "share_pct": pct(mix_shares[c])}
                           for c in sorted(mix_counts, key=lambda k: (-mix_counts[k], k))],
            "wrong_fit": {
                "count": mix_counts.get("wrong_fit", 0),
                "share": mix_shares.get("wrong_fit", 0.0),
                "subtypes": [{"subtype": s, "count": wf_sub[s]} for s in sorted(wf_sub, key=lambda k: (-wf_sub[k], k))],
                "dominant_subtype": dom,
                "segmentation_verdict": vmap.get(dom) if dom else None,
                "by_campaign": [{"campaign_id": c, "count": wf_campaigns[c]} for c in sorted(wf_campaigns)],
            },
            "not_interested": {"count": mix_counts.get("not_interested", 0),
                               "share": mix_shares.get("not_interested", 0.0)},
        },
        "instances": sorted(instances, key=lambda i: i["instance_id"]),
        "warnings": warnings,
        "not_computed": [
            "Revenue or meetings lost to an objection — no deal field exists in a conversation payload. Use campaign-impact-analyzer.",
            "Which sequence step caused an objection — conversations carry no step index. First-received-message is the only reliable proxy.",
            "Whether the lead read our handling reply — no per-message read signal.",
            "Numeric sentiment — a label, never a percentage.",
            "Statistical significance — no p-values. `confidence` is a coarse label based on n.",
            "What non-repliers objected to — invisible here, and usually the largest group.",
            "Per-rep team ranking — computed only on explicit request; the rollup belongs to team-performance-dashboard.",
        ],
    }


# ---------------------------------------------------------------- merge

def merge(state, report, reclassify=False):
    """Counts are DERIVED from the instance ledger, never incremented. That is
    what makes merging commutative: two reps' states union in any order and
    produce the same numbers, and re-running a report changes nothing."""
    if state.get("state_version") != STATE_VERSION:
        raise ValidationError("state_version mismatch: %r vs %d." % (state.get("state_version"), STATE_VERSION))
    new, dupe, reclassified, rematured, conflicts = 0, 0, 0, 0, []
    for inst in report["instances"]:
        iid = inst["instance_id"]
        prior = state["instances"].get(iid)
        if prior is None:
            rec = dict(inst)
            rec["first_seen_run"] = report["run_id"]
            rec["last_seen_as_of"] = report["as_of"]
            rec["reclassified_from"] = None
            state["instances"][iid] = rec
            new += 1
        else:
            dupe += 1
            # Outcome is time-dependent: `pending` matures, and a lead can answer on day 20
            # after being written off on day 8. Freezing it at first sight biases the
            # headline rate downwards and permanently truncates the tail.
            if prior.get("outcome") != "recovered" and \
               (prior.get("last_seen_as_of") or "") <= report["as_of"]:
                before = prior.get("outcome")
                for k in ("outcome", "matured", "handled", "progressed", "response_hours",
                          "rubric_total", "reply_verbatim", "should_have",
                          "post_objection_category"):
                    if k in inst:
                        prior[k] = inst[k]
                prior["last_seen_as_of"] = report["as_of"]
                if before != prior.get("outcome"):
                    rematured += 1
            if prior["type"] != inst["type"]:
                conflicts.append({"instance_id": iid, "kept": prior["type"],
                                  "proposed": inst["type"], "applied": bool(reclassify)})
                if reclassify:
                    was = prior["type"]
                    prior.update({k: v for k, v in inst.items() if k != "first_seen_run"})
                    prior["reclassified_from"] = was
                    reclassified += 1
    # Only park a thread in the skip-list once its outcomes can no longer change. A
    # `pending` instance that is skipped forever is frozen out of the recovery denominator
    # for good, which is how re-maturation became unreachable in practice.
    as_of_dt = parse_day(report["as_of"])
    unsettled = set()
    for inst in state["instances"].values():
        if inst.get("outcome") == "recovered":
            continue
        if (as_of_dt - parse_ts(inst["objection_at"])) < timedelta(days=SETTLE_DAYS):
            unsettled.add(inst["thread_id"])
    seen = set(state.get("seen_thread_ids") or [])
    seen.update(t["thread_id"] for t in (report.get("threads") or []))
    seen.update(i["thread_id"] for i in report["instances"])
    seen -= unsettled
    state["seen_thread_ids"] = sorted(seen)
    state["recheck_thread_ids"] = sorted(unsettled)

    if not any(r["run_id"] == report["run_id"] for r in state["runs"]):
        state["runs"].append({
            "run_id": report["run_id"], "as_of": report["as_of"],
            "source": report.get("source"),
            "threads_in": report["coverage"]["threads_in"],
            "goal": report.get("goal", "unspecified"),
            "new_instances": new,
            "totals": {"objection_instances": report["coverage"]["objection_instances"]},
        })
        state["runs"] = sorted(state["runs"], key=lambda r: (r["as_of"], r["run_id"]))[-12:]
        state["reply_mix_runs"] = (state.get("reply_mix_runs") or [])
        state["reply_mix_runs"].append({"run_id": report["run_id"], "as_of": report["as_of"],
                                        "reply_mix": report["reply_mix"]})
        state["reply_mix_runs"] = state["reply_mix_runs"][-12:]

    state["created_at"] = state.get("created_at") or report["as_of"]
    state["updated_at"] = report["as_of"]
    state["not_computed"] = report["not_computed"]
    return state, {"new_instances": new, "duplicate_instances": dupe,
                   "reclassified": reclassified, "rematured": rematured,
                   "recheck_threads": len(unsettled),
                   "conflicts": conflicts, "new_this_run": new}


def rollup(state, window=WINDOW_DEFAULT, min_n=MIN_N_DEFAULT, as_of=None):
    """Ranking is WINDOWED, accumulation is not. Lifetime counts only grow, so
    ranking on them would keep a solved objection at #1 forever."""
    insts = list(state["instances"].values())
    ref = parse_day(as_of or state.get("updated_at") or "1970-01-01")
    cutoff = ref - timedelta(days=window) if window else None
    recent = [i for i in insts
              if not cutoff or parse_ts(i["objection_at"]) >= cutoff]
    life, win = {}, {}
    for i in insts:
        life[i["type"]] = life.get(i["type"], 0) + 1
    for i in recent:
        win[i["type"]] = win.get(i["type"], 0) + 1
    shares = apportion(win, len(recent))
    rows = []
    for tid in sorted(win, key=lambda k: (-win[k], k)):
        rws = [r for r in recent if r["type"] == tid]
        rec = sum(1 for r in rws if r["outcome"] == "recovered")
        dead = sum(1 for r in rws if r["outcome"] == "dead")
        unh = sum(1 for r in rws if r["outcome"] == "unhandled")
        hrs = [r["response_hours"] for r in rws if r.get("response_hours") is not None]
        rts = [r["rubric_total"] for r in rws if r.get("rubric_total") is not None]
        scored = sorted([r for r in rws if r.get("rubric_total") is not None],
                        key=lambda r: (-r["rubric_total"], r["instance_id"]))
        best = scored[0] if scored and scored[0]["rubric_total"] >= BEST_REPLY_FLOOR else None
        worst = (scored[-1] if scored and (len(scored) > 1 or scored[-1] is not best)
                 and scored[-1]["rubric_total"] < BEST_REPLY_FLOOR else None)
        rows.append({
            "type": tid, "label": (type_meta(tid) or {}).get("label", tid),
            "family": (type_meta(tid) or {}).get("family"),
            "count_window": win[tid], "count_lifetime": life.get(tid, 0),
            "share": shares[tid], "share_pct": pct(shares[tid]),
            "recovery_rate": rate(rec, rec + dead, min_n),
            "no_reply_rate": rate(unh, len(rws), min_n),
            "median_response_hours": (round(statistics.median(hrs), 1) if hrs else None),
            "median_rubric": (round(statistics.median(rts), 1) if rts else None),
            "first_touch_share": round(sum(1 for r in rws if r.get("is_first_touch")) / len(rws), 3),
            "smokescreen_share": round(sum(1 for r in rws if r.get("smokescreen")) / len(rws), 3),
            "card": (state.get("cards") or {}).get(tid) or {},
            "best_reply": ({"score": best["rubric_total"], "objection": best.get("verbatim"),
                            "reply": best.get("reply_verbatim"),
                            "lead_ref": best.get("lead_ref")} if best else None),
            "worst_reply": ({"score": worst["rubric_total"], "objection": worst.get("verbatim"),
                             "reply": worst.get("reply_verbatim"),
                             "should_have": worst.get("should_have")} if worst else None),
        })
    prev = None
    if len(state.get("reply_mix_runs") or []) >= 2:
        prev = state["reply_mix_runs"][-2]
    return {"window_days": window, "as_of": ref.date().isoformat(),
            "instances_lifetime": len(insts), "instances_window": len(recent),
            "runs": len(state.get("runs") or []),
            "by_type": rows,
            "reply_mix": (state["reply_mix_runs"][-1]["reply_mix"] if state.get("reply_mix_runs") else None),
            "reply_mix_prev": (prev["reply_mix"] if prev else None)}


# ---------------------------------------------------------------- render

def load_baseline():
    """Baseline card bodies ship in references/ and are NEVER mutated. A
    reinstall can only cost the accumulated half, never the useful-on-day-1
    half."""
    out = {}
    if not os.path.exists(BASELINE_PATH):
        return out
    with open(BASELINE_PATH, encoding="utf-8") as fh:
        txt = fh.read()
    for m in re.finditer(r"<!--\s*BASELINE:([a-z_]+)\s*-->(.*?)<!--\s*/BASELINE:\1\s*-->", txt, re.S):
        out[m.group(1)] = m.group(2).strip()
    return out


def fmt_rate(r):
    if r is None:
        return "—"
    if r.get("suppressed") or r.get("value") is None:
        return "n=%d — too few to rate" % r.get("n", 0)
    return "%d%% (n=%d)" % (pct(r["value"]), r["n"])


def render_card(row, baseline, run_id, rank, total_types, scope="last window"):
    L = []
    L.append("# %s — `%s`" % (row["label"], row["type"]))
    L.append("")
    L.append("Family: %s · Rank #%d of %d (%s) · %d in scope / %d lifetime"
             % (row["family"], rank, total_types, scope, row["count_window"], row["count_lifetime"]))
    L.append("")
    L.append("## The numbers")
    L.append("")
    L.append("| Metric | Value |")
    L.append("|---|---|")
    L.append("| Share of objections | %d%% |" % row["share_pct"])
    L.append("| Recovery rate | %s |" % fmt_rate(row["recovery_rate"]))
    L.append("| Never answered | %s |" % fmt_rate(row["no_reply_rate"]))
    L.append("| Median response | %s |" % ("%sh" % row["median_response_hours"] if row["median_response_hours"] is not None else "—"))
    L.append("| Median handling score | %s |" % ("%s/27" % row["median_rubric"] if row["median_rubric"] is not None else "—"))
    L.append("| Lands on the first message | %d%% |" % pct(row["first_touch_share"]))
    L.append("| Likely smokescreen | %d%% |" % pct(row["smokescreen_share"]))
    L.append("")
    L.append("## From your own data")
    L.append("")
    b = row["best_reply"]
    if b:
        L.append("**Clone this reply** (%d/27) — to %s" % (b["score"], b.get("lead_ref") or "a lead"))
        L.append("")
        if b.get("objection"):
            L.append("They said: _%s_" % b["objection"].replace("\n", " "))
            L.append("")
        if b.get("reply"):
            L.append("```")
            L.append(b["reply"].strip())
            L.append("```")
        else:
            L.append("> Reply text not captured on this run. Pass `handling.verbatim` so the card can quote it.")
        L.append("")
    else:
        L.append("> No reply scored %d/27 or above yet — no exemplar promoted. Nothing is invented here." % BEST_REPLY_FLOOR)
        L.append("")
    w = row["worst_reply"]
    if w:
        L.append("**Worth redoing** (%d/27)%s" % (w["score"], " — " + w["should_have"] if w.get("should_have") else "."))
        L.append("")
    tmpl = (row.get("card") or {}).get("template")
    if tmpl:
        L.append("## Response template")
        L.append("")
        prov = (row.get("card") or {}).get("template_provenance")
        if prov:
            L.append("_%s_" % prov)
            L.append("")
        L.append("```")
        L.append(tmpl.strip())
        L.append("```")
        L.append("")
    b = baseline.get(row["type"])
    L.append("## Baseline playbook")
    L.append("")
    L.append(b if b else "_Baseline body not found in references/baseline-playbook.md._")
    L.append("")
    L.append('<!-- objection-analyzer: %s -->' % json.dumps(
        {"type": row["type"], "state_version": STATE_VERSION, "run_id": run_id}, sort_keys=True))
    return "\n".join(L) + "\n"


def render(state, out_dir, window=WINDOW_DEFAULT, min_n=MIN_N_DEFAULT):
    roll = rollup(state, window=window, min_n=min_n)
    if not roll["by_type"] and roll["instances_lifetime"]:
        # Nothing recent, but the playbook is not empty. Ranking on lifetime and
        # saying so beats rendering a baseline-only card over real data.
        roll = rollup(state, window=0, min_n=min_n)
        roll["window_fallback"] = window
    baseline = load_baseline()
    run_id = state["runs"][-1]["run_id"] if state.get("runs") else "baseline"
    cards_dir = os.path.join(out_dir, "cards")
    os.makedirs(cards_dir, exist_ok=True)

    written, skipped = [], []
    rows = roll["by_type"]
    if not rows and roll["instances_lifetime"]:
        raise ValidationError("Internal: lifetime instances exist but no rows to rank.")
    if not rows:
        for tid in canonical_ids():
            rows_stub = {"type": tid, "label": (type_meta(tid) or {}).get("label", tid),
                         "family": (type_meta(tid) or {}).get("family"),
                         "count_window": 0, "count_lifetime": 0, "share": 0.0, "share_pct": 0,
                         "recovery_rate": None, "no_reply_rate": None,
                         "median_response_hours": None, "median_rubric": None,
                         "first_touch_share": 0.0, "smokescreen_share": 0.0,
                         "best_reply": None, "worst_reply": None}
            path = os.path.join(cards_dir, "%s.md" % tid)
            body = render_card(rows_stub, baseline, run_id, canonical_ids().index(tid) + 1, 9)
            body = body.replace("## The numbers\n", "## The numbers\n\n_No data yet — baseline only._\n")
            _write_card(path, body, written, skipped)
    else:
        scope = "full history" if roll.get("window_fallback") else "last %d days" % roll["window_days"]
        for n, row in enumerate(rows, 1):
            path = os.path.join(cards_dir, "%s.md" % row["type"])
            _write_card(path, render_card(row, baseline, run_id, n, len(rows), scope), written, skipped)

    index = _render_index(roll, state)
    with open(os.path.join(out_dir, "playbook.md"), "w", encoding="utf-8") as fh:
        fh.write(index)
    return {"cards_written": written, "cards_skipped_user_edited": skipped,
            "index": os.path.join(out_dir, "playbook.md"), "rollup": roll}


def _write_card(path, body, written, skipped):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            old = fh.read()
        if "<!-- objection-analyzer:" not in old:
            skipped.append(path)   # hand-written: warn, never clobber
            return
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(body)
    written.append(path)


def _render_index(roll, state):
    L = ["# Objection playbook", ""]
    if roll.get("window_fallback"):
        L.append("Nothing in the last %d days. Ranking on the full history instead: %d objections over %d run(s), as of %s."
                 % (roll["window_fallback"], roll["instances_lifetime"], roll["runs"], roll["as_of"]))
        L.append("")
        L.append("| # | Objection | Share | Recovery | Never answered | Lifetime |")
        L.append("|---|---|---|---|---|---|")
        for n, r in enumerate(roll["by_type"], 1):
            L.append("| %d | %s | %d%% | %s | %s | %d |"
                     % (n, r["label"], r["share_pct"], fmt_rate(r["recovery_rate"]),
                        fmt_rate(r["no_reply_rate"]), r["count_lifetime"]))
        L.append("")
    elif roll["instances_lifetime"] == 0:
        L.append("**Baseline only — 0 conversations analyzed.** The nine cards in `cards/` are the")
        L.append("shipped best-practice versions. Run the analysis when you have replies and they")
        L.append("fill in with your own numbers.")
        L.append("")
    else:
        L.append("%d objections over %d run(s) · %d in the last %d days · as of %s"
                 % (roll["instances_lifetime"], roll["runs"], roll["instances_window"],
                    roll["window_days"], roll["as_of"]))
        L.append("")
        L.append("| # | Objection | Share | Recovery | Never answered | Window / lifetime |")
        L.append("|---|---|---|---|---|---|")
        for n, r in enumerate(roll["by_type"], 1):
            L.append("| %d | %s | %d%% | %s | %s | %d / %d |"
                     % (n, r["label"], r["share_pct"], fmt_rate(r["recovery_rate"]),
                        fmt_rate(r["no_reply_rate"]), r["count_window"], r["count_lifetime"]))
        L.append("")
    mix = roll.get("reply_mix")
    if mix and mix.get("total_replies"):
        L.append("## Reply mix (%d replies)" % mix["total_replies"])
        L.append("")
        L.append("| Category | Count | Share |")
        L.append("|---|---|---|")
        for c in mix["categories"]:
            L.append("| %s | %d | %d%% |" % (c["category"], c["count"], c["share_pct"]))
        L.append("")
        wf = mix.get("wrong_fit") or {}
        if wf.get("segmentation_verdict"):
            L.append("**Segmentation:** %s (%d wrong-fit %s, dominant sub-type `%s`)"
                     % (wf["segmentation_verdict"], wf["count"],
                        "reply" if wf["count"] == 1 else "replies", wf["dominant_subtype"]))
            L.append("")
    L.append("_Reads replies only. It cannot tell you what the people who never replied objected to._")
    L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------- csv

CSV_REQUIRED = ["thread_id", "direction", "timestamp", "content"]
CSV_OPTIONAL = ["channel", "campaign", "identity", "rep", "lead_ref", "status"]

def normalize_csv(text):
    rdr = csv.DictReader(io.StringIO(text))
    if not rdr.fieldnames:
        raise ValidationError("The CSV has no header row.")
    heads = {(h or "").strip().lower(): (h or "") for h in rdr.fieldnames}
    missing = [c for c in CSV_REQUIRED if c not in heads]
    if missing:
        raise ValidationError(
            "CSV is missing required column(s): %s. Required: %s. Optional: %s."
            % (", ".join(missing), ", ".join(CSV_REQUIRED), ", ".join(CSV_OPTIONAL)))
    threads, order = {}, []
    for n, row in enumerate(rdr, start=2):
        tid = (row.get(heads["thread_id"]) or "").strip()
        if not tid:
            raise ValidationError("CSV row %d has an empty thread_id." % n)
        d = (row.get(heads["direction"]) or "").strip().lower()
        if d not in ("sent", "received"):
            raise ValidationError("CSV row %d: direction must be 'sent' or 'received', got %r." % (n, d))
        ts = parse_ts(row.get(heads["timestamp"]), "on CSV row %d" % n)
        if tid not in threads:
            threads[tid] = {"thread_id": tid, "messages": []}
            order.append(tid)
            for src, dst in (("campaign", "campaign_id"), ("identity", "identity_id"),
                             ("rep", "identity_id"), ("channel", "channel"), ("lead_ref", "lead_ref")):
                if src in heads and (row.get(heads[src]) or "").strip():
                    threads[tid].setdefault(dst, (row.get(heads[src]) or "").strip())
        msg = {"direction": d, "at": ts.isoformat(),
               "content": (row.get(heads["content"]) or "").strip()}
        if "status" in heads and (row.get(heads["status"]) or "").strip():
            msg["status"] = (row.get(heads["status"]) or "").strip()
        threads[tid]["messages"].append(msg)
    for tid in order:
        threads[tid]["messages"].sort(key=lambda m: m["at"])
    return [threads[t] for t in order]


# ---------------------------------------------------------------- purge

def purge(state, before, redact=False):
    cut = parse_day(before, "in --before")
    removed, redacted = 0, 0
    keep = {}
    for iid, inst in state["instances"].items():
        if parse_ts(inst["objection_at"]) < cut:
            if redact:
                inst = dict(inst)
                inst["verbatim"] = ""
                inst["lead_ref"] = None
                redacted += 1
                keep[iid] = inst
            else:
                removed += 1
            continue
        keep[iid] = inst
    state["instances"] = keep
    return state, {"removed": removed, "redacted": redacted, "remaining": len(keep)}


# ---------------------------------------------------------------- backup

def backup_state(state):
    home = os.path.join(os.path.expanduser("~"), ".gtm-skills", "objection-analyzer", "backup")
    try:
        os.makedirs(home, exist_ok=True)
        rid = (state["runs"][-1]["run_id"] if state.get("runs") else "manual")
        safe = re.sub(r"[^A-Za-z0-9_.-]", "-", rid)
        with open(os.path.join(home, "state-%s.json" % safe), "w", encoding="utf-8") as fh:
            fh.write(dumps(state))
        files = sorted(f for f in os.listdir(home) if f.startswith("state-"))
        for f in files[:-BACKUPS_KEPT]:
            os.remove(os.path.join(home, f))
        return os.path.join(home, "state-%s.json" % safe)
    except Exception:
        return None


# ---------------------------------------------------------------- selftest

def _selftest():
    fails = []

    def check(name, cond, detail=""):
        if cond:
            print("  ok    %s" % name)
        else:
            print("  FAIL  %s %s" % (name, detail))
            fails.append(name)

    def must_raise(name, fn, needle=None):
        try:
            fn()
        except ValidationError as e:
            if needle and needle.lower() not in str(e).lower():
                print("  FAIL  %s (wrong message: %s)" % (name, e))
                fails.append(name)
            else:
                print("  ok    %s (refused)" % name)
            return
        except Exception as e:
            print("  FAIL  %s (wrong exception %s: %s)" % (name, type(e).__name__, e))
            fails.append(name)
            return
        print("  FAIL  %s (should have refused)" % name)
        fails.append(name)

    D = "2026-08-18"
    def ts(day, h=9):
        return "2026-%02d-%02dT%02d:00:00+00:00" % (int(day.split("-")[1]), int(day.split("-")[2]), h)

    def thread(tid, msgs, campaign=None, lead="A. B. · Acme"):
        t = {"thread_id": tid, "messages": msgs, "lead_ref": lead, "channel": "linkedin"}
        if campaign:
            t["campaign_id"] = campaign
        return t

    def m(direction, day, h=9, status="OK"):
        return {"direction": direction, "at": ts(day, h), "status": status}

    def ann(tid, typ, oi, ri=None, post="none", rub=None, cat="objection", mk=None, sh=None):
        o = {"type": typ, "objection_msg_index": oi, "post_objection_category": post,
             "verbatim": "…", "smokescreen_markers": mk or {}}
        if ri is not None:
            o["handling"] = {"reply_msg_index": ri, "rubric": rub, "should_have": sh}
        return {"thread_id": tid, "reply_category": cat, "objections": [o]}

    def run(threads, annotations, rid="r1", as_of=D):
        return {"run_id": rid, "as_of": as_of, "source": "test",
                "threads": threads, "annotations": annotations}

    print("objection-analyzer engine self-test")
    print("-" * 52)

    # 1 counts and shares
    r = analyze(run(
        [thread("t1", [m("sent", "2026-06-01"), m("received", "2026-06-02")]),
         thread("t2", [m("sent", "2026-06-01"), m("received", "2026-06-02")]),
         thread("t3", [m("sent", "2026-06-01"), m("received", "2026-06-02")])],
        [ann("t1", "price_budget", 1), ann("t2", "price_budget", 1), ann("t3", "timing", 1)]))
    top = r["by_type"][0]
    check("two_types_counts", top["type"] == "price_budget" and top["count"] == 2
          and top["share"] == 0.667 and r["by_type"][1]["count"] == 1,
          "got %s" % [(b["type"], b["count"], b["share"]) for b in r["by_type"]])

    # 2 recovery basic
    r = analyze(run(
        [thread("a1", [m("received", "2026-06-01"), m("sent", "2026-06-02"), m("received", "2026-06-03")]),
         thread("a2", [m("received", "2026-06-01"), m("sent", "2026-06-02")])],
        [ann("a1", "timing", 0, 1, "interested"), ann("a2", "timing", 0, 1, "none")]), min_n=2)
    rr = r["by_type"][0]["recovery_rate"]
    check("recovery_basic", rr["value"] == 0.5 and rr["n"] == 2, "got %s" % rr)

    # 3 maturity excludes a fresh thread
    r = analyze(run(
        [thread("b1", [m("received", "2026-08-15"), m("sent", "2026-08-16")])],
        [ann("b1", "timing", 0, 1, "none")]), min_n=1, maturity_days=7)
    check("maturity_excluded", r["by_type"][0]["pending"] == 1
          and r["by_type"][0]["recovery_rate"]["n"] == 0,
          "got pending=%s n=%s" % (r["by_type"][0]["pending"], r["by_type"][0]["recovery_rate"]["n"]))

    # 4 unhandled is out of the recovery denominator, in no_reply_rate
    r = analyze(run(
        [thread("c1", [m("received", "2026-06-01")])],
        [ann("c1", "price_budget", 0)]), min_n=1)
    t = r["by_type"][0]
    check("unhandled_excluded", t["recovery_rate"]["n"] == 0 and t["no_reply_rate"]["value"] == 1.0,
          "got %s / %s" % (t["recovery_rate"], t["no_reply_rate"]))

    # 5 SEND_FAILED is not a handling reply
    must_raise("send_failed_not_handling", lambda: analyze(run(
        [thread("d1", [m("received", "2026-06-01"), m("sent", "2026-06-02", status="SEND_FAILED")])],
        [ann("d1", "timing", 0, 1)])), "send_failed")

    # 6 auto-reply after our handling is not a recovery
    r = analyze(run(
        [thread("e1", [m("received", "2026-06-01"), m("sent", "2026-06-02"), m("received", "2026-06-03")])],
        [ann("e1", "timing", 0, 1, "auto_ooo")]), min_n=1)
    check("auto_ooo_not_recovery", r["by_type"][0]["recovered"] == 0 and r["by_type"][0]["dead"] == 1)

    # 7 small-n suppression
    r = analyze(run(
        [thread("f%d" % i, [m("received", "2026-06-01"), m("sent", "2026-06-02"), m("received", "2026-06-03")])
         for i in range(3)],
        [ann("f%d" % i, "timing", 0, 1, "interested") for i in range(3)]), min_n=5)
    rr = r["by_type"][0]["recovery_rate"]
    check("min_n_suppression", rr["value"] is None and rr["suppressed"] and rr["n"] == 3, "got %s" % rr)

    # 8 THE critical one: merging twice is a no-op
    rep = analyze(run(
        [thread("g1", [m("received", "2026-06-01"), m("sent", "2026-06-02")])],
        [ann("g1", "price_budget", 0, 1)]))
    s1, _ = merge(empty_state(), rep)
    a = dumps(s1)
    s2, rpt2 = merge(json.loads(a), rep)
    check("dedup_idempotent", dumps(s2) == a and rpt2["new_instances"] == 0 and rpt2["duplicate_instances"] == 1,
          "new=%s dupe=%s" % (rpt2["new_instances"], rpt2["duplicate_instances"]))

    # 9 merge grows by the new instances only
    rep2 = analyze(run(
        [thread("g1", [m("received", "2026-06-01"), m("sent", "2026-06-02")]),
         thread("g2", [m("received", "2026-06-05"), m("sent", "2026-06-06")])],
        [ann("g1", "price_budget", 0, 1), ann("g2", "timing", 0, 1)], rid="r2"))
    s3, rpt3 = merge(json.loads(dumps(s1)), rep2)
    check("merge_grows", len(s3["instances"]) == 2 and rpt3["new_instances"] == 1)

    # 10 reclassification is reported, not silent
    rep3 = analyze(run(
        [thread("g1", [m("received", "2026-06-01"), m("sent", "2026-06-02")])],
        [ann("g1", "value_doubt", 0, 1)], rid="r3"))
    s4, rpt4 = merge(json.loads(dumps(s1)), rep3)
    kept = s4["instances"]["g1#0"]["type"] == "price_budget"
    s5, rpt5 = merge(json.loads(dumps(s1)), rep3, reclassify=True)
    check("reclassify_reported", kept and len(rpt4["conflicts"]) == 1
          and s5["instances"]["g1#0"]["type"] == "value_doubt"
          and s5["instances"]["g1#0"]["reclassified_from"] == "price_budget")

    # 11 campaign lift drives the targeting verdict
    th, an = [], []
    for i in range(6):
        th.append(thread("h%d" % i, [m("received", "2026-06-01"), m("sent", "2026-06-02", 12),
                                     m("received", "2026-06-03")], campaign="C1"))
        an.append(ann("h%d" % i, "price_budget", 0, 1, "interested"))
    for i in range(6):
        th.append(thread("k%d" % i, [m("received", "2026-06-01"), m("sent", "2026-06-02", 12),
                                     m("received", "2026-06-03")], campaign="C2"))
        an.append(ann("k%d" % i, "timing", 0, 1, "interested"))
    r = analyze(run(th, an), min_n=5)
    pb = [x for x in r["by_type"] if x["type"] == "price_budget"][0]
    check("campaign_lift", pb["diagnosis"]["max_lift"] == 2.0 or pb["diagnosis"]["max_lift"] > 1.9,
          "lift=%s" % pb["diagnosis"]["max_lift"])

    # 12 product-gap rule: answered, answered well, still dead
    th, an = [], []
    good = {k: 2 for k in RUBRIC_KEYS}
    for i in range(16):          # PRODUCT_MIN_N: a roadmap conversation needs >5 threads
        th.append(thread("p%d" % i, [m("sent", "2026-06-01"), m("received", "2026-06-02"),
                                     m("sent", "2026-06-03")]))
        an.append(ann("p%d" % i, "feature_gap", 1, 2, "none", rub=good))
    r = analyze(run(th, an), min_n=5)
    fg = r["by_type"][0]
    check("product_gap_rule", fg["diagnosis"]["verdict"] == "product",
          "verdict=%s rec=%s med=%s handled=%s" % (fg["diagnosis"]["verdict"], fg["recovery_rate"],
                                                   fg["median_rubric"], fg["handled_share"]))

    # 13 the copy verdict is a LIFT over the corpus first-touch base, not a fixed cutoff.
    #    channel_trust always lands first; timing lands mid-thread. Base = 0.5.
    th, an = [], []
    for i in range(10):
        th.append(thread("q%d" % i, [m("received", "2026-06-01"), m("sent", "2026-06-02"),
                                     m("received", "2026-06-03")]))
        an.append(ann("q%d" % i, "channel_trust", 0, 1, "curious"))
    for i in range(10):
        # the lead speaks at index 1, but the objection only lands at index 3, so this
        # type is NOT first-touch
        th.append(thread("qt%d" % i, [m("sent", "2026-06-01"), m("received", "2026-06-02"),
                                      m("sent", "2026-06-03"), m("received", "2026-06-04"),
                                      m("sent", "2026-06-05"), m("received", "2026-06-06")]))
        an.append(ann("qt%d" % i, "timing", 3, 4, "curious"))
    r = analyze(run(th, an), min_n=5)
    ct = [x for x in r["by_type"] if x["type"] == "channel_trust"][0]
    tm = [x for x in r["by_type"] if x["type"] == "timing"][0]
    # leave-one-out: channel_trust is measured against timing's 0.0, not against a pooled base
    check("copy_verdict_is_a_lift", ct["diagnosis"]["verdict"] == "copy"
          and ct["diagnosis"]["first_touch_base"] == 0.0
          and ct["diagnosis"]["first_touch_lift_points"] == 1.0
          and tm["diagnosis"]["verdict"] != "copy",
          "ct=%s base=%s tm=%s" % (ct["diagnosis"]["verdict"],
                                   ct["diagnosis"]["first_touch_base"], tm["diagnosis"]["verdict"]))

    # 13c the verdict must not depend on what ELSE was swept. Same price data, two corpora.
    def _corpus(n_price, n_timing):
        th2, an2 = [], []
        for i in range(n_price):
            th2.append(thread("cp%d" % i, [m("received", "2026-06-01"), m("sent", "2026-06-02")]))
            an2.append(ann("cp%d" % i, "price_budget", 0, 1))
        for i in range(n_timing):
            th2.append(thread("ct%d" % i, [m("sent", "2026-06-01"), m("received", "2026-06-02"),
                                           m("sent", "2026-06-03"), m("received", "2026-06-04"),
                                           m("sent", "2026-06-05")]))
            an2.append(ann("ct%d" % i, "timing", 3, 4))
        r2 = analyze(run(th2, an2), min_n=5)
        p2 = [x for x in r2["by_type"] if x["type"] == "price_budget"][0]
        return p2["diagnosis"]["verdict"], p2["diagnosis"]["first_touch_base"]
    vA, bA = _corpus(30, 5)
    vB, bB = _corpus(30, 30)
    check("copy_verdict_is_composition_independent", vA == vB == "copy" and bA == bB == 0.0,
          "A=%s/%s B=%s/%s" % (vA, bA, vB, bB))

    # 13d a type our own opener provokes is not reported as a product wall
    th3, an3 = [], []
    for i in range(20):
        th3.append(thread("pw%d" % i, [m("received", "2026-06-01"), m("sent", "2026-06-02")]))
        an3.append(ann("pw%d" % i, "feature_gap", 0, 1, "none", rub={k: 2 for k in RUBRIC_KEYS}))
    for i in range(20):
        # objection at index 3, so this type is NOT first-touch and gives feature_gap a real base
        th3.append(thread("pv%d" % i, [m("sent", "2026-06-01"), m("received", "2026-06-02"),
                                       m("sent", "2026-06-03"), m("received", "2026-06-04"),
                                       m("sent", "2026-06-05"), m("received", "2026-06-06")]))
        an3.append(ann("pv%d" % i, "timing", 3, 4, "interested"))
    r3 = analyze(run(th3, an3), min_n=5)
    fg3 = [x for x in r3["by_type"] if x["type"] == "feature_gap"][0]
    check("copy_beats_product_when_both_fire", fg3["diagnosis"]["verdict"] == "copy"
          and fg3["diagnosis"]["product"] is False,
          "verdict=%s product=%s" % (fg3["diagnosis"]["verdict"], fg3["diagnosis"]["product"]))

    # 13b a single-type corpus cannot show a deviation, so no copy verdict is issued
    th, an = [], []
    for i in range(10):
        th.append(thread("u%d" % i, [m("received", "2026-06-01"), m("sent", "2026-06-02"),
                                     m("received", "2026-06-03")]))
        an.append(ann("u%d" % i, "channel_trust", 0, 1, "curious"))
    r = analyze(run(th, an), min_n=5)
    check("no_copy_verdict_without_a_base", r["by_type"][0]["diagnosis"]["verdict"] != "copy"
          and r["by_type"][0]["first_touch_share"] == 1.0)

    # 14 zero objections is a valid run, not an error
    r = analyze(run([thread("z1", [m("received", "2026-06-01")])],
                    [{"thread_id": "z1", "reply_category": "interested", "objections": []}]))
    check("zero_objections_ok", r["baseline_mode"] is True and r["by_type"] == []
          and r["reply_mix"]["total_replies"] == 1)

    # 15 shares always sum to exactly 1.000
    th, an = [], []
    for i, tid in enumerate(canonical_ids()):
        for j in range(i + 1):
            k = "s%d_%d" % (i, j)
            th.append(thread(k, [m("received", "2026-06-01")]))
            an.append(ann(k, tid, 0))
    r = analyze(run(th, an))
    tot = sum(b["share"] for b in r["by_type"])
    check("share_rounding", abs(tot - 1.0) <= 0.001, "sum=%r" % tot)

    # 16 wrong_fit is counted and yields a segmentation verdict
    r = analyze(run(
        [thread("w1", [m("received", "2026-06-01")]), thread("w2", [m("received", "2026-06-01")]),
         thread("w3", [m("received", "2026-06-01")])],
        [{"thread_id": "w1", "reply_category": "wrong_fit", "wrong_fit_subtype": "not-icp-segment"},
         {"thread_id": "w2", "reply_category": "wrong_fit", "wrong_fit_subtype": "not-icp-segment"},
         ann("w3", "price_budget", 0)]))
    wf = r["reply_mix"]["wrong_fit"]
    check("wrong_fit_first_class", wf["count"] == 2 and wf["dominant_subtype"] == "not-icp-segment"
          and "segment" in (wf["segmentation_verdict"] or "").lower()
          and r["coverage"]["objection_instances"] == 1,
          "got %s" % wf)

    # 16b a tie between wrong-fit sub-types yields no dominant verdict
    r = analyze(run(
        [thread("wt1", [m("received", "2026-06-01")]), thread("wt2", [m("received", "2026-06-01")])],
        [{"thread_id": "wt1", "reply_category": "wrong_fit", "wrong_fit_subtype": "job-seeker"},
         {"thread_id": "wt2", "reply_category": "wrong_fit", "wrong_fit_subtype": "wrong-person"}]))
    wf2 = r["reply_mix"]["wrong_fit"]
    check("wrong_fit_tie_no_verdict", wf2["dominant_subtype"] is None
          and wf2["segmentation_verdict"] is None and wf2["count"] == 2)

    # 17 windowed ranking vs lifetime accumulation
    rep_old = analyze(run(
        [thread("o1", [m("received", "2026-01-05"), m("sent", "2026-01-06")])],
        [ann("o1", "scope_mismatch", 0, 1)], rid="old", as_of="2026-01-20"))
    rep_new = analyze(run(
        [thread("n1", [m("received", "2026-08-01"), m("sent", "2026-08-02")])],
        [ann("n1", "timing", 0, 1)], rid="new"))
    st, _ = merge(empty_state(), rep_old)
    st, _ = merge(st, rep_new)
    roll = rollup(st, window=90, as_of=D)
    check("window_ranking", roll["instances_lifetime"] == 2 and roll["instances_window"] == 1
          and [x["type"] for x in roll["by_type"]] == ["timing"]
          and roll["by_type"][0]["count_lifetime"] == 1,
          "life=%s win=%s types=%s" % (roll["instances_lifetime"], roll["instances_window"],
                                       [x["type"] for x in roll["by_type"]]))

    # 17b an empty window over a non-empty playbook falls back to lifetime
    import tempfile
    st_old, _ = merge(empty_state(), rep_old)          # only a January objection
    st_old["updated_at"] = D                            # ...looked at in August
    with tempfile.TemporaryDirectory() as td:
        out = render(json.loads(dumps(st_old)), td, window=90, min_n=1)
        idx = open(os.path.join(td, "playbook.md"), encoding="utf-8").read()
        card = open(os.path.join(td, "cards", "scope_mismatch.md"), encoding="utf-8").read()
    check("window_fallback_not_baseline",
          "Ranking on the full history" in idx and "No data yet" not in card
          and len(out["cards_written"]) == 1,
          "cards=%d idx=%r" % (len(out["cards_written"]), idx[:80]))

    # 17d a genuinely empty playbook still renders all nine baseline cards
    with tempfile.TemporaryDirectory() as td:
        out0 = render(empty_state(), td, min_n=1)
        idx0 = open(os.path.join(td, "playbook.md"), encoding="utf-8").read()
    check("baseline_only_when_truly_empty",
          len(out0["cards_written"]) == 9 and "Baseline only" in idx0)

    # 17c a verdict is never emitted below min_n
    r = analyze(run([thread("v1", [m("received", "2026-06-01")])], [ann("v1", "timing", 0)]), min_n=5)
    check("no_verdict_below_min_n", r["by_type"][0]["diagnosis"]["verdict"] == "inconclusive"
          and r["by_type"][0]["diagnosis"]["confidence"] is None)

    # 17e platform events never masquerade as the lead coming back
    #     (observed live: LGM status lines and AUTO_QUALIFY notes carry direction=received)
    evt = {"direction": "received", "at": ts("2026-06-03"), "status": "INFO", "channel": "LGM"}
    must_raise("recovery_not_satisfied_by_event", lambda: analyze(run(
        [{"thread_id": "ev1", "messages": [m("received", "2026-06-01"), m("sent", "2026-06-02"), evt]}],
        [ann("ev1", "timing", 0, 1, "interested")])), "no received message after")
    r = analyze(run(
        [{"thread_id": "ev2", "messages": [m("received", "2026-06-01"), m("sent", "2026-06-02"), evt]}],
        [ann("ev2", "timing", 0, 1, "none")]), min_n=1)
    check("event_counts_as_dead_not_recovered",
          r["by_type"][0]["dead"] == 1 and r["by_type"][0]["recovered"] == 0)
    must_raise("objection_on_platform_event", lambda: analyze(run(
        [{"thread_id": "ev3", "messages": [m("sent", "2026-06-01"), evt]}],
        [ann("ev3", "timing", 1)])), "platform event")
    r = analyze(run(
        [{"thread_id": "ev4", "messages": [
            {"direction": "received", "at": ts("2026-06-01"), "status": "INFO", "channel": "LGM"},
            m("received", "2026-06-02")]}],
        [ann("ev4", "timing", 1)]), min_n=1)
    check("first_touch_skips_events", r["by_type"][0]["first_touch_share"] == 1.0)

    # 17f the conversation goal is recorded, and an unknown one is refused
    r = analyze({"run_id": "g1", "as_of": D, "scope": {"goal": "signup"},
                 "threads": [thread("g0", [m("received", "2026-06-01")])],
                 "annotations": [ann("g0", "timing", 0)]})
    st_g, _ = merge(empty_state(), r)
    check("goal_recorded", r["goal"] == "signup" and st_g["runs"][0]["goal"] == "signup")
    r2 = analyze(run([thread("g2", [m("received", "2026-06-01")])], [ann("g2", "timing", 0)]))
    check("goal_defaults_unspecified", r2["goal"] == "unspecified")
    must_raise("unknown_goal_refused", lambda: analyze({
        "run_id": "g3", "as_of": D, "scope": {"goal": "demo-booking"},
        "threads": [thread("g4", [m("received", "2026-06-01")])],
        "annotations": [ann("g4", "timing", 0)]}), "unknown conversation goal")

    # 17g a persisted response template renders into its card, with provenance
    st_t = json.loads(dumps(st))
    st_t["cards"] = {"timing": {
        "template": "Understood. What is taking the priority right now?",
        "template_provenance": "Built from 2 of your replies that scored 22+."}}
    with tempfile.TemporaryDirectory() as td:
        render(st_t, td, window=0, min_n=1)
        card_t = open(os.path.join(td, "cards", "timing.md"), encoding="utf-8").read()
        card_o = open(os.path.join(td, "cards", "scope_mismatch.md"), encoding="utf-8").read()
    check("template_renders_with_provenance",
          "## Response template" in card_t and "What is taking the priority" in card_t
          and "scored 22+" in card_t and "## Response template" not in card_o,
          "no template section" if "## Response template" not in card_t else "leaked to other card")

    # 17h the exemplar quotes OUR reply, not the objection, and a lone reply is never
    #     also reported as the weakest
    r = analyze(run(
        [thread("cl1", [m("received", "2026-06-01"), m("sent", "2026-06-02"), m("received", "2026-06-03")])],
        [{"thread_id": "cl1", "reply_category": "objection", "objections": [
            {"type": "timing", "objection_msg_index": 0, "verbatim": "not right now",
             "post_objection_category": "interested",
             "handling": {"reply_msg_index": 1, "rubric": {k: 3 for k in RUBRIC_KEYS},
                          "verbatim": "What is taking the priority right now?"}}]}]), min_n=1)
    t = r["by_type"][0]
    check("exemplar_quotes_our_reply",
          t["best_reply"]["reply"] == "What is taking the priority right now?"
          and t["best_reply"]["objection"] == "not right now")
    check("lone_reply_is_not_also_worst", t["worst_reply"] is None,
          "got %s" % t["worst_reply"])
    with tempfile.TemporaryDirectory() as td:
        st_c, _ = merge(empty_state(), r)
        render(st_c, td, window=0, min_n=1)
        card_c = open(os.path.join(td, "cards", "timing.md"), encoding="utf-8").read()
    check("card_shows_reply_in_a_code_block",
          "Clone this reply" in card_c and "What is taking the priority right now?" in card_c
          and "Worth redoing" not in card_c)

    # 17i the recovery numerator is fail-CLOSED. An unrecognised post-objection value used
    #     to read as a recovery, which failed in the flattering direction on the one number
    #     this whole tier exists to protect.
    for bad in ("not interested", "notInterested", "declined", "banana"):
        must_raise("post_category_%s_refused" % bad.replace(" ", "_"), (lambda v: lambda: analyze(run(
            [thread("pc", [m("received", "2026-06-01"), m("sent", "2026-06-02"),
                           m("received", "2026-06-03")])],
            [ann("pc", "timing", 0, 1, v)])))(bad), "unknown post_objection_category")
    must_raise("reply_category_refused", lambda: analyze(run(
        [thread("rc", [m("received", "2026-06-01")])],
        [{"thread_id": "rc", "reply_category": "kinda_interested", "objections": []}])),
        "unknown reply_category")

    # 17j an outcome is a function of time, so a later run re-matures it. Frozen at first
    #     sight, the headline rate carries a structural downward bias and a truncated tail.
    late = [thread("lt", [m("received", "2026-06-01"), m("sent", "2026-06-02"),
                          m("received", "2026-06-20")])]
    lann = [ann("lt", "timing", 0, 1, "interested")]
    r_early = analyze(run(late, lann, rid="early", as_of="2026-06-05"), min_n=1)
    r_late = analyze(run(late, lann, rid="late", as_of="2026-07-01"), min_n=1)
    check("pending_then_recovered_in_isolation",
          r_early["instances"][0]["outcome"] == "pending"
          and r_late["instances"][0]["outcome"] == "recovered")
    st_m, _ = merge(empty_state(), r_early)
    st_m, rpt_m = merge(st_m, r_late)
    check("merge_rematures_a_pending_instance",
          list(st_m["instances"].values())[0]["outcome"] == "recovered"
          and rpt_m["rematured"] == 1,
          "outcome=%s rematured=%s" % (list(st_m["instances"].values())[0]["outcome"], rpt_m["rematured"]))
    # ...but a recovery is terminal: an older report must never walk it back
    st_b, _ = merge(empty_state(), r_late)
    st_b, _ = merge(st_b, r_early)
    check("recovered_is_terminal",
          list(st_b["instances"].values())[0]["outcome"] == "recovered")

    # 17k re-merging the same report after re-maturation is still a no-op
    a_m = dumps(st_m)
    st_m2, _ = merge(json.loads(a_m), r_late)
    check("rematuration_stays_idempotent", dumps(st_m2) == a_m)

    # 17l a thread whose outcome can still change is NOT parked in the skip-list, or
    #     re-maturation is unreachable and the recovery denominator loses its tail
    fresh = analyze(run(
        [thread("fr1", [m("received", "2026-08-10"), m("sent", "2026-08-11")])],
        [ann("fr1", "timing", 0, 1, "none")], rid="fresh"), min_n=1)
    st_f, rpt_f = merge(empty_state(), fresh)
    check("unsettled_thread_stays_rereadable",
          "fr1" not in st_f["seen_thread_ids"] and "fr1" in st_f["recheck_thread_ids"]
          and rpt_f["recheck_threads"] == 1)
    settled = analyze(run(
        [thread("st1", [m("received", "2026-06-01"), m("sent", "2026-06-02"),
                        m("received", "2026-06-03")])],
        [ann("st1", "timing", 0, 1, "interested")], rid="settled"), min_n=1)
    st_s, _ = merge(empty_state(), settled)
    check("recovered_thread_is_parked", "st1" in st_s["seen_thread_ids"]
          and st_s["recheck_thread_ids"] == [])

    # 18 CSV round-trip equals the JSON path
    csv_text = (
        "thread_id,direction,timestamp,content,campaign,status\n"
        "t1,sent,2026-06-01T09:00:00+00:00,hello,C1,OK\n"
        "t1,received,2026-06-02T09:00:00+00:00,too expensive,C1,OK\n"
        "t1,sent,2026-06-03T09:00:00+00:00,what budget,C1,OK\n"
        "t1,received,2026-06-04T09:00:00+00:00,around 400 a month,C1,OK\n"
        "t2,sent,2026-06-01T09:00:00+00:00,hello,C1,OK\n"
        "t2,received,2026-06-02T09:00:00+00:00,not now,C1,OK\n"
        "t2,sent,2026-06-03T09:00:00+00:00,when,C1,OK\n")
    th = normalize_csv(csv_text)
    r_csv = analyze(run(th, [ann("t1", "price_budget", 1, 2, "interested"),
                             ann("t2", "timing", 1, 2, "none")]), min_n=1)
    th_json = [thread("t1", [m("sent", "2026-06-01"), m("received", "2026-06-02"), m("sent", "2026-06-03"),
                             m("received", "2026-06-04")], campaign="C1"),
               thread("t2", [m("sent", "2026-06-01"), m("received", "2026-06-02"), m("sent", "2026-06-03")], campaign="C1")]
    r_json = analyze(run(th_json, [ann("t1", "price_budget", 1, 2, "interested"),
                                   ann("t2", "timing", 1, 2, "none")]), min_n=1)
    check("csv_roundtrip", len(th) == 2 and
          [(b["type"], b["count"], b["share"]) for b in r_csv["by_type"]] ==
          [(b["type"], b["count"], b["share"]) for b in r_json["by_type"]] and
          r_csv["coverage"]["objection_instances"] == r_json["coverage"]["objection_instances"],
          "csv=%s json=%s" % ([b["type"] for b in r_csv["by_type"]], [b["type"] for b in r_json["by_type"]]))

    # 19 analyze is deterministic
    a1 = dumps(analyze(run(th_json, [ann("t1", "price_budget", 1, 2, "interested"),
                                     ann("t2", "timing", 1, 2, "none")])))
    a2 = dumps(analyze(run(th_json, [ann("t1", "price_budget", 1, 2, "interested"),
                                     ann("t2", "timing", 1, 2, "none")])))
    check("analyze_deterministic", a1 == a2)

    # 20 best reply promoted only above the floor
    perfect = {k: 3 for k in RUBRIC_KEYS}
    weak = {k: 1 for k in RUBRIC_KEYS}
    r = analyze(run(
        [thread("x1", [m("received", "2026-06-01"), m("sent", "2026-06-02"), m("received", "2026-06-03")]),
         thread("x2", [m("received", "2026-06-01"), m("sent", "2026-06-02")])],
        [ann("x1", "timing", 0, 1, "interested", rub=perfect),
         ann("x2", "timing", 0, 1, "none", rub=weak, sh="ask what IS the priority")]), min_n=1)
    t = r["by_type"][0]
    check("best_reply_floor", t["best_reply"]["score"] == 27 and t["worst_reply"]["score"] == 9
          and t["worst_reply"]["should_have"] == "ask what IS the priority")
    r2 = analyze(run(
        [thread("y1", [m("received", "2026-06-01"), m("sent", "2026-06-02")])],
        [ann("y1", "timing", 0, 1, "none", rub=weak)]), min_n=1)
    check("no_exemplar_when_below_floor", r2["by_type"][0]["best_reply"] is None)

    # 21 smokescreen needs 2 of 3
    r = analyze(run(
        [thread("m1", [m("received", "2026-06-01")]), thread("m2", [m("received", "2026-06-01")])],
        [ann("m1", "price_budget", 0, mk={"pre_information": True, "no_specifics": True}),
         ann("m2", "price_budget", 0, mk={"pre_information": True})]), min_n=1)
    check("smokescreen_two_of_three", r["by_type"][0]["smokescreen_share"] == 0.5)

    # 22 targeting is null, not false, with no campaign dimension
    r = analyze(run([thread("u1", [m("received", "2026-06-01")])], [ann("u1", "timing", 0)]))
    check("targeting_null_without_campaign", r["by_type"][0]["diagnosis"]["targeting"] is None
          and any("targeting signal is not assessable" in w for w in r["warnings"]))

    # 23 purge and redact
    st2, rp = purge(json.loads(dumps(st)), "2026-06-01")
    check("purge_before", rp["removed"] == 1 and rp["remaining"] == 1)
    st3, rp3 = purge(json.loads(dumps(st)), "2026-06-01", redact=True)
    check("purge_redact", rp3["redacted"] == 1 and rp3["remaining"] == 2
          and st3["instances"]["o1#0"]["verbatim"] == "")

    # --- refusals -------------------------------------------------------
    must_raise("unknown_type", lambda: analyze(run(
        [thread("r1", [m("received", "2026-06-01")])], [ann("r1", "pricing", 0)])), "unknown objection type")
    must_raise("objection_on_sent_message", lambda: analyze(run(
        [thread("r2", [m("sent", "2026-06-01")])], [ann("r2", "timing", 0)])), "sent")
    must_raise("handling_before_objection", lambda: analyze(run(
        [thread("r3", [m("sent", "2026-06-01"), m("received", "2026-06-02")])],
        [ann("r3", "timing", 1, 0)])), "not after")
    must_raise("handling_points_at_received", lambda: analyze(run(
        [thread("r4", [m("received", "2026-06-01"), m("received", "2026-06-02")])],
        [ann("r4", "timing", 0, 1)])), "received")
    must_raise("duplicate_instance_id", lambda: analyze({
        "run_id": "x", "as_of": D,
        "threads": [thread("r5", [m("received", "2026-06-01")])],
        "annotations": [{"thread_id": "r5", "reply_category": "objection", "objections": [
            {"type": "timing", "instance_id": "dup", "objection_msg_index": 0},
            {"type": "price_budget", "instance_id": "dup", "objection_msg_index": 0}]}]}), "duplicate")
    must_raise("orphan_annotation", lambda: analyze(run(
        [thread("r6", [m("received", "2026-06-01")])], [ann("nope", "timing", 0)])), "unknown thread_id")
    must_raise("bad_rubric_key", lambda: analyze(run(
        [thread("r7", [m("received", "2026-06-01"), m("sent", "2026-06-02")])],
        [ann("r7", "timing", 0, 1, rub={"tone_match": 3})])), "rubric keys")
    must_raise("rubric_value_out_of_range", lambda: analyze(run(
        [thread("r8", [m("received", "2026-06-01"), m("sent", "2026-06-02")])],
        [ann("r8", "timing", 0, 1, rub={k: (4 if k == "not_pushy" else 2) for k in RUBRIC_KEYS})])), "0-3")
    must_raise("nonmonotonic_timestamps", lambda: analyze(run(
        [thread("r9", [m("received", "2026-06-05"), m("sent", "2026-06-01")])],
        [ann("r9", "timing", 0, 1)])), "back in time")
    must_raise("naive_timestamp_no_offset", lambda: analyze(run(
        [{"thread_id": "r10", "messages": [{"direction": "received", "at": "2026-06-01T09:00:00"}]}],
        [ann("r10", "timing", 0)])), "offset")
    must_raise("index_out_of_range", lambda: analyze(run(
        [thread("r11", [m("received", "2026-06-01")])], [ann("r11", "timing", 5)])), "out of range")
    must_raise("state_version_mismatch", lambda: merge({"state_version": 99, "instances": {}, "runs": []},
                                                       analyze(run([thread("r12", [m("received", "2026-06-01")])],
                                                                   [ann("r12", "timing", 0)]))), "mismatch")
    must_raise("csv_missing_direction", lambda: normalize_csv(
        "thread_id,timestamp,content\nt1,2026-06-01T09:00:00+00:00,hi\n"), "direction")
    must_raise("csv_bad_direction_value", lambda: normalize_csv(
        "thread_id,direction,timestamp,content\nt1,outbound,2026-06-01T09:00:00+00:00,hi\n"), "row 2")
    must_raise("recovery_without_received", lambda: analyze(run(
        [thread("r13", [m("received", "2026-06-01"), m("sent", "2026-06-02")])],
        [ann("r13", "timing", 0, 1, "interested")])), "no")
    must_raise("missing_run_id", lambda: analyze({"as_of": D, "threads": [], "annotations": []}), "run_id")

    print("-" * 52)
    if fails:
        print("%d FAILED: %s" % (len(fails), ", ".join(fails)))
        return 1
    print("all green")
    return 0


# ---------------------------------------------------------------- cli

def read_input(path):
    if path == "-" or path is None:
        return sys.stdin.read()
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def main():
    p = argparse.ArgumentParser(description="Objection analysis engine.")
    p.add_argument("--test", action="store_true", help="run the self-test and exit")
    sub = p.add_subparsers(dest="cmd")

    d = sub.add_parser("doctor", help="resolve where the playbook lives")
    d.add_argument("--export", action="store_true", help="print the current state to stdout")

    n = sub.add_parser("normalize", help="CSV export -> threads JSON")
    n.add_argument("path")

    a = sub.add_parser("analyze", help="annotated run -> report")
    a.add_argument("path")
    a.add_argument("--as-of")
    a.add_argument("--maturity-days", type=int, default=MATURITY_DAYS_DEFAULT)
    a.add_argument("--min-n", type=int, default=MIN_N_DEFAULT)

    mg = sub.add_parser("merge", help="report -> accumulated state")
    mg.add_argument("path")
    mg.add_argument("--write", action="store_true")
    mg.add_argument("--reclassify", action="store_true")

    rd = sub.add_parser("render", help="state -> playbook.md + cards/")
    rd.add_argument("--window", type=int, default=WINDOW_DEFAULT)
    rd.add_argument("--min-n", type=int, default=MIN_N_DEFAULT)
    rd.add_argument("--out")

    pg = sub.add_parser("purge", help="drop or redact old instances")
    pg.add_argument("--before", required=True)
    pg.add_argument("--redact", action="store_true")

    args = p.parse_args()
    if args.test:
        sys.exit(_selftest())
    if not args.cmd:
        p.print_help()
        sys.exit(2)

    try:
        loc = resolve_location()
        if args.cmd == "doctor":
            write_anchor(loc)
            if args.export:
                print(dumps(load_state(loc)))
                sys.exit(0)
            st = load_state(loc)
            out = dict(loc)
            out.update({
                "state_path": state_path(loc),
                "state_exists": bool(state_path(loc) and os.path.exists(state_path(loc))),
                "instances": len(st.get("instances") or {}),
                "runs": len(st.get("runs") or []),
                "seen_threads": len(st.get("seen_thread_ids") or []),
                "baseline_cards_available": len(load_baseline()),
                "numbers_are_estimates": loc["tier"] == "paste",
            })
            print(dumps(out))
            sys.exit(0)

        if args.cmd == "normalize":
            print(dumps({"threads": normalize_csv(read_input(args.path))}))
            sys.exit(0)

        if args.cmd == "analyze":
            print(dumps(analyze(json.loads(read_input(args.path)),
                                maturity_days=args.maturity_days, min_n=args.min_n,
                                as_of=args.as_of)))
            sys.exit(0)

        if args.cmd == "merge":
            rep = json.loads(read_input(args.path))
            st, rpt = merge(load_state(loc), rep, reclassify=args.reclassify)
            if args.write:
                if loc["tier"] == "paste":
                    raise ValidationError(
                        "Nowhere writable. Print the state and have the user keep it: "
                        "run without --write and save the JSON.")
                os.makedirs(loc["path"], exist_ok=True)
                with open(state_path(loc), "w", encoding="utf-8") as fh:
                    fh.write(dumps(st))
                write_anchor(loc)
                rpt["written_to"] = state_path(loc)
                rpt["backup"] = backup_state(st)
            else:
                rpt["state"] = st
            rpt["location"] = loc
            print(dumps(rpt))
            sys.exit(0)

        if args.cmd == "render":
            out_dir = args.out or loc["path"]
            if not out_dir:
                raise ValidationError("Nowhere writable — render needs a directory. Pass --out.")
            print(dumps(render(load_state(loc), out_dir, window=args.window, min_n=args.min_n)))
            sys.exit(0)

        if args.cmd == "purge":
            st, rpt = purge(load_state(loc), args.before, redact=args.redact)
            if loc["tier"] != "paste":
                with open(state_path(loc), "w", encoding="utf-8") as fh:
                    fh.write(dumps(st))
                rpt["written_to"] = state_path(loc)
            print(dumps(rpt))
            sys.exit(0)

    except ValidationError as e:
        sys.stderr.write("REFUSED: %s\n" % e)
        sys.exit(2)
    except json.JSONDecodeError as e:
        sys.stderr.write("REFUSED: input is not valid JSON (%s).\n" % e)
        sys.exit(2)


if __name__ == "__main__":
    main()
