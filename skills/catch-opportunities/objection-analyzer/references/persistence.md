# Persistence — where the playbook lives and how it accumulates

## Why this is not simply "a file in the skill folder"

The obvious answer is to keep the playbook next to the skill. It does not survive
contact with how skills are actually installed:

- Installed skills are frequently **symlinks into a package cache**. Writing "into the
  skill folder" writes into that cache.
- `npx skills add` **replaces the skill directory** on update. A playbook stored there
  is one routine update away from gone.
- In a sandboxed session (an uploaded skill, an ephemeral container), **nothing
  persists at all** between conversations. Not the home directory, not the skill
  folder, nothing.

So the skill folder is the **anchor**, not the storage. `analyze.py` locates itself
through `os.path.dirname(__file__)`, resolves where the data should live, and records
the answer in `playbook/LOCATION` so every later run agrees. The bytes live somewhere
that survives.

## The ladder

`analyze.py doctor` walks it top to bottom, takes the first writable tier, and prints
which one it took and why. Run it first, every session, and tell the user the answer
in one line. Silent accumulation into a directory that is about to be wiped is the one
failure mode worth being loud about.

| Tier | Path | Chosen when |
|---|---|---|
| `env` | `$OBJECTION_PLAYBOOK_DIR` | Set. Point a whole team at one synced or Git-tracked folder. |
| `home` | `${XDG_DATA_HOME}/objection-analyzer` or `~/.gtm-skills/objection-analyzer` | **Default.** Survives a skill reinstall. |
| `skill` | `<skill folder>/playbook/` | Home not writable. A skill update can erase this, and `doctor` says so. |
| `cwd` | `./.objection-playbook/` | Nothing else is writable. Same shape as the dot-directory the dashboard skills use for their snapshots. |
| `paste` | none | Sandboxed, or no code execution at all. |

Nothing in the data layout carries a vendor name. The skill works without La Growth
Machine, so the user's own files should not imply otherwise.

## The `paste` tier

No disk and no script means no engine, and that has consequences worth stating plainly
rather than hiding:

1. Classify and analyze in-session as usual.
2. **Label every number as estimated**, because the model computed it. Drop the
   recovery rate entirely below n=10 rather than showing a soft one.
3. Emit the full `state.json` in a fenced code block: *"this is your playbook, save it
   and paste it back at the start of the next run"*.
4. Accept a pasted state as input on the next run and merge in-session.

Accumulation still works. It is just manual, and slower to trust.

## Layout

```
<resolved path>/
├── state.json               # the ledger: every instance, every run, the authored prose
├── playbook.md              # human index: ranked objections, reply mix, segmentation
└── cards/<type>.md          # one battle card per objection type
```

## `state.json`

```jsonc
{
  "state_version": 1,
  "created_at": "2026-06-02", "updated_at": "2026-08-18",
  "runs": [ {"run_id","as_of","source","threads_in","new_instances","totals"} ],
  "instances": {
    "<thread_id>#<msg_index>": {
      "type": "price_budget", "objection_at": "…", "campaign_id": "…",
      "identity_id": "…", "channel": "linkedin", "lead_ref": "J. L. · Acme",
      "verbatim": "…", "is_first_touch": true, "smokescreen": false,
      "outcome": "recovered|dead|pending|unhandled", "rubric_total": 24,
      "should_have": "…", "first_seen_run": "…", "reclassified_from": null
    }
  },
  "reply_mix_runs": [ … ],      // last 12, for the reply-mix trend
  "seen_thread_ids": [ … ],     // skip-list: never re-read a thread
  "cards": { "<type>": {"means","handling_angle","what_not_to_say","edited_by_user"} },
  "not_computed": [ … ]
}
```

**Counts are derived from `instances`, never incremented.** That single choice is what
makes everything else safe:

- **Re-running is free.** Merging the same report twice produces a byte-identical
  state. Nothing double-counts.
- **Merging is commutative.** Two reps' states union in either order for the same
  numbers, so a team can point `$OBJECTION_PLAYBOOK_DIR` at a shared folder and merge
  freely.
- **The dedup key is `instance_id`** = `<thread_id>#<objection_msg_index>`. A recurring
  objection inside one thread counts once, so a chatty prospect cannot inflate the
  ranking.

## Outcomes re-mature, types do not

An outcome is a function of time. A `pending` instance matures, and a lead can answer on day
20 after being written off on day 8. So on merge, a non-recovered instance has its
time-dependent fields refreshed from the newer report, and the merge report counts them as
`rematured`. Without that, the headline rate carries a structural downward bias and the tail
is permanently truncated.

A `recovered` outcome is terminal: re-merging an older report can never walk it back. And
re-merging the same report after a re-maturation is still a no-op, so the idempotency
guarantee holds.

## Classification drift

The same thread can read as `price_budget` in one run and `value_doubt` in the next.
On merge, an existing instance **keeps its original type** unless `--reclassify` is
passed, and the merge report always carries `reclassified` and `conflicts[]`. Drift
becomes visible instead of silently resolving itself one way or the other.

## Ranking is windowed, accumulation is not

Lifetime counts only grow, so ranking on them would keep a solved objection at number
one forever. `render --window 90` ranks on the recent window and keeps the lifetime
count in a secondary column. Both numbers are true and they answer different questions.

## Backup, restore, purge

Every `merge --write` mirrors the state to `~/.gtm-skills/objection-analyzer/backup/`
(last 10 kept) and reports the path. Before updating the skill, or any time the user
wants a copy:

```bash
python3 scripts/analyze.py doctor --export > my-objection-playbook.json
```

The playbook holds prospect words, so it is subject to the same retention discipline as
a CRM:

```bash
python3 scripts/analyze.py purge --before 2026-01-01            # drop old instances
python3 scripts/analyze.py purge --before 2026-01-01 --redact   # keep counts, drop the words
```

`lead_ref` is initials plus company and nothing more. Full message bodies never enter
the pipeline: only the short verbatim you selected, truncated to 200 characters.

## What a card contains

`render` writes one file per objection type, sections in this order:

1. **Title** — the label, the id, the family, the rank and the frequency in scope vs lifetime.
2. **The numbers** — share, recovery rate, never-answered, median response, median handling
   score, first-touch share, smokescreen share. Every rate carries its `n`, and a suppressed
   rate prints `n=3 — too few to rate` rather than a percentage.
3. **From your own data** — the reply to clone, quoted in a code block with the objection it
   answered, promoted only at 22/27 or above. Below that the card says so and promotes
   nothing. A second reply is shown as "worth redoing" only when it is a different one and
   scored under the floor: a lone 27/27 is an exemplar, never also the weakest.
4. **Response template** — present once mode 5 has written one, with its provenance line.
5. **Baseline playbook** — the shipped body from `baseline-playbook.md`, always present.

With zero conversations, all nine cards still render: the numbers table reads *"No data yet
— baseline only"*, sections 3 and 4 are explicit empty states, and section 5 carries the
full best-practice content. That is what makes run one useful with no account and no data.

## Hand-edited cards

Every rendered card ends with an HTML comment stamp. If a card exists without that
stamp, someone wrote it by hand, and `render` **skips it and reports it** rather than
overwriting. A team's own battle card always outranks a generated one.
