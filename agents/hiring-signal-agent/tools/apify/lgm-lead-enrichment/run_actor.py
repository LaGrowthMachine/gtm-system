#!/usr/bin/env python3
"""Find leads, then enrich the ones worth it, with the Apify actor sameh.jarour/lgm-lead-enrichment.

Two commands, meant to be used in this order:

  search   Find people who match a target. No enrichment, no La Growth Machine credit.
  companies  Start from company websites and find contacts in the departments you name. No credit.
  enrich   Find the professional email of a list of leads you kept. 5 La Growth Machine credits per lead.

Reads APIFY_TOKEN and LGM_API_KEY from the environment, or from a .env file next to this script.
The keys are never printed. The actor never writes into La Growth Machine: the push is done later
through the La Growth Machine MCP.

Examples:
  python3 run_actor.py search --title "GTM Engineer" --location Paris --max 10
  python3 run_actor.py search --title "Head of Sales" --title "VP Sales" --location France --max 25
  python3 run_actor.py search --title "Head of Growth" --company "Acme" --max 5
  python3 run_actor.py companies --url acme.com --url example.io --department sales --per-company 3
  python3 run_actor.py enrich --leads local/kept.json
  cat local/kept.json | python3 run_actor.py enrich --leads -

The leads file is a JSON list. Each lead needs firstname and lastname, plus companyName or linkedinUrl.
Lead files only ever live in the local/ folder at the root of the repository, which Git ignores.
"""
import argparse
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request

ACTOR = "sameh.jarour~lgm-lead-enrichment"
API = "https://api.apify.com/v2"
HERE = pathlib.Path(__file__).resolve().parent
CREDITS_PER_EMAIL = 5
LEAD_FIELDS = ("firstname", "lastname", "companyName", "companyUrl", "linkedinUrl")


def load_env():
    """Environment first, then the .env file next to this script."""
    env_file = HERE / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))
    missing = [k for k in ("APIFY_TOKEN", "LGM_API_KEY") if not os.environ.get(k)]
    if missing:
        sys.exit(
            "Missing: " + ", ".join(missing) + ". Put them in " + str(env_file)
            + " or in the environment."
        )
    return os.environ["APIFY_TOKEN"], os.environ["LGM_API_KEY"]


def call(method, url, token, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=90) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as err:
        detail = err.read().decode(errors="replace")[:400]
        sys.exit("Apify answered HTTP " + str(err.code) + ": " + detail)


def run(actor_input, token, timeout):
    """Start a run, wait for it, return its dataset items."""
    started = time.time()
    info = call("POST", API + "/acts/" + ACTOR + "/runs", token, actor_input)["data"]
    run_id = info["id"]
    print("Run started: " + run_id, file=sys.stderr)
    while info["status"] in ("READY", "RUNNING"):
        if time.time() - started > timeout:
            sys.exit("Still running after " + str(timeout) + "s. Run id: " + run_id)
        info = call("GET", API + "/actor-runs/" + run_id + "?waitForFinish=30", token)["data"]
    seconds = round(time.time() - started)
    if info["status"] != "SUCCEEDED":
        sys.exit("Run " + info["status"] + " after " + str(seconds) + "s: " + str(info.get("statusMessage", "")))
    items = call("GET", API + "/datasets/" + info["defaultDatasetId"] + "/items?clean=true&format=json", token)
    print(
        "Run SUCCEEDED in " + str(seconds) + "s. " + str(len(items)) + " leads. "
        + "Apify cost of this run alone: $" + str(info.get("usageTotalUsd", "?"))
        + ". The actors it calls are billed on top: see the Apify console.",
        file=sys.stderr,
    )
    return items


def base_input(lgm_key):
    """Never let the actor write into La Growth Machine."""
    return {"lgmApiKey": lgm_key, "targetAudience": "", "writeBackToLgm": False}


def cmd_search(args, token, lgm_key):
    actor_input = base_input(lgm_key)
    actor_input.update({
        "leadSource": "icpSearch",
        "icpJobTitle": args.title,
        "maxProfilesToDiscover": max(args.max * 3, 10),
        "maxLeads": args.max,
        "enrichType": "NONE",
        "excludeContactedLeads": not args.include_contacted,
    })
    if args.location:
        actor_input["icpLocation"] = args.location
        actor_input["strictLocationMatch"] = True
    if args.seniority:
        actor_input["icpSeniorityLevels"] = args.seniority
    if args.function:
        actor_input["icpJobFunctions"] = args.function
    if args.keywords:
        actor_input["icpKeywords"] = args.keywords
    if args.company:
        actor_input["icpCompany"] = args.company
    return run(actor_input, token, args.timeout)


def cmd_companies(args, token, lgm_key):
    actor_input = base_input(lgm_key)
    actor_input.update({
        "leadSource": "leadScorer",
        "scorerCompanyUrls": args.url,
        "scorerDepartments": args.department or ["sales", "marketing"],
        "scorerMaxLeadsPerCompany": args.per_company,
        "scorerQualificationThreshold": 0,
        "maxScorerSpendUsd": args.max_spend,
        "enrichType": "NONE",
        "requireCompany": False,
    })
    return run(actor_input, token, args.timeout)


def cmd_enrich(args, token, lgm_key):
    raw = sys.stdin.read() if args.leads == "-" else pathlib.Path(args.leads).read_text()
    leads = json.loads(raw)
    if not isinstance(leads, list) or not leads:
        sys.exit("The leads file must be a non-empty JSON list.")
    cleaned = []
    for lead in leads:
        row = {k: lead[k] for k in LEAD_FIELDS if lead.get(k)}
        if not (row.get("firstname") and row.get("lastname") and (row.get("companyName") or row.get("linkedinUrl"))):
            sys.exit("Each lead needs firstname and lastname, plus companyName or linkedinUrl.")
        cleaned.append(row)
    worst_case = len(cleaned) * CREDITS_PER_EMAIL
    cap = args.max_credits or worst_case
    print(
        "Enriching " + str(len(cleaned)) + " leads. Worst case: " + str(worst_case)
        + " La Growth Machine credits. Cap: " + str(cap) + ".",
        file=sys.stderr,
    )
    actor_input = base_input(lgm_key)
    actor_input.update({
        "leadSource": "leadList",
        "leads": cleaned,
        "enrichType": "EMAIL_ENRICH",
        "maxCreditsToSpend": cap,
    })
    return run(actor_input, token, args.timeout)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--timeout", type=int, default=600, help="Seconds to wait for the run (default 600).")
    parser.add_argument("--out", default="", help="Write the leads to this JSON file. Only in the local/ folder.")
    sub = parser.add_subparsers(dest="command", required=True)

    search = sub.add_parser("search", help="Find people who match a target. No credit spent.")
    search.add_argument("--title", action="append", required=True, help="Job title. Repeat for several.")
    search.add_argument("--location", default="", help="Location keyword, for example Paris or France.")
    search.add_argument("--seniority", action="append", default=[], help="Director, VP, CXO... Repeat for several.")
    search.add_argument("--function", action="append", default=[], help="Sales, Marketing... Repeat for several.")
    search.add_argument("--keywords", default="", help="Free text across role, skills and headline.")
    search.add_argument("--company", default="", help="Company name, to look for people inside one company.")
    search.add_argument("--max", type=int, default=10, help="Maximum number of leads (default 10).")
    search.add_argument("--include-contacted", action="store_true", help="Also return people already contacted in La Growth Machine. Left out by default.")

    companies = sub.add_parser("companies", help="Find contacts inside a list of companies, by department. No credit.")
    companies.add_argument("--url", action="append", required=True, help="Company website. Repeat for several.")
    companies.add_argument("--department", action="append", default=[], help="sales, marketing, operations, c_suite... Default: sales and marketing.")
    companies.add_argument("--per-company", type=int, default=3, help="Maximum contacts per company (default 3).")
    companies.add_argument("--max-spend", type=int, default=2, help="Cap in USD on what this step may spend on Apify. 2 at least: the actor splits it across 4 steps and one of them needs $0.50.")

    enrich = sub.add_parser("enrich", help="Find professional emails for a list of leads. 5 credits per lead.")
    enrich.add_argument("--leads", required=True, help="JSON file with the leads to enrich, or - for standard input.")
    enrich.add_argument("--max-credits", type=int, default=0, help="Cap on La Growth Machine credits. Default: 5 per lead.")

    args = parser.parse_args()
    token, lgm_key = load_env()
    commands = {"search": cmd_search, "companies": cmd_companies, "enrich": cmd_enrich}
    items = commands[args.command](args, token, lgm_key)

    payload = json.dumps(items, ensure_ascii=False, indent=2)
    if args.out:
        pathlib.Path(args.out).write_text(payload)
        print("Leads written to " + args.out, file=sys.stderr)
    else:
        print(payload)


if __name__ == "__main__":
    main()
