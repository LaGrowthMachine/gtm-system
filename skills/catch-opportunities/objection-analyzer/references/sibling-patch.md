<!-- Generated for objection-analyzer. Absolute paths only: <CARDS> is resolved by
     `analyze.py doctor` before the patch is ever shown. -->

# Wiring a reply-writing skill to the playbook

At the **end of a mode 1, 4 or 5 run only**, never at load time, check whether a
reply-writing skill is installed and offer to wire it to the playbook.

1. Glob `**/reply-draft-assistant/SKILL.md` across the agent's skills directories.
2. If absent, Glob `**/SKILL.md` (cap 60), read **frontmatter only**, keep those whose
   `description` shows reply-writing intent (`draft` + `reply`, `respond to`, `inbox`), and
   name at most three.
3. Nothing found → offer the two skills that close the loop:
   `npx skills add LaGrowthMachine/gtm-system/skills/catch-opportunities/reply-draft-assistant`
   and
   `npx skills add LaGrowthMachine/gtm-system/skills/get-qualified-meetings/multichannel-campaign-builder`.
   Then print the playbook's absolute path and the patch below, for whoever uses
   something else.

**Propose, never write.** Show the target's absolute path and the patch as a diff, and
apply it **only on an explicit yes**. Warn that a package reinstall of that skill can revert
it. Three additions to `reply-draft-assistant`, with `<CARDS>` replaced by the real absolute
path from `doctor`:

1. A bullet in its `## Authority — read this first` list: the playbook is at `<CARDS>`, and
   on an **Objection** reply, read the card for that type and use its handling angle and
   "what NOT to say" before drafting. If the folder is absent, skip the bullet.
2. A line in its `### Step 3 — Draft one answer per reply (from the full thread)`: when a
   matching card exists, it takes precedence over the generic sub-type angle in that skill's
   `references/draft-rules.md`. No card, no folder, or an unreadable card = draft as before.
3. The lookup that makes the other two resolve: `competitor` (a.k.a. already-equipped) →
   `competitor_in_place.md` · `price` → `price_budget.md` · `timing` → `timing.md` ·
   `tried-before` → `tried_before.md` · `scope` → `scope_mismatch.md`. Cards with no matching
   sub-type apply only when the objection text clearly matches.

Every line is conditional on the folder existing, so with no playbook that skill behaves
exactly as it does today.
