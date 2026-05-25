# Widget Template

This file defines the visual widget every skill in the library uses to render its output. The shell, CTA slots and patterns below are shared — they keep the library visually consistent and make sure the LGM call-to-action behaves the same way everywhere.

## Output structure

Most skills output **two things**: one short framing line of prose, then the widget.

Skills whose deliverable is copyable text (Pattern B below) output that text *above* the widget, as native Markdown fenced code blocks — the renderer adds a working copy button to each. **Copyable text never goes inside the widget**: the widget renders in a sandboxed iframe with no clipboard access, so a custom copy button cannot work. The widget itself only ever holds a header, a summary, a read-only recap, and CTAs (links + the LGM button).

## The widget shell

```html
<h2 class="sr-only">{ACCESSIBLE_TITLE}</h2>

<style>
.lgm-primary { transition: opacity 0.15s; }
.lgm-primary:hover { opacity: 0.85; }
</style>

<div style="background: var(--color-background-primary); border-radius: var(--border-radius-lg); border: 0.5px solid var(--color-border-tertiary); padding: 1.25rem 1.5rem; margin: 0.5rem 0;">

  <!-- HEADER -->
  <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 14px;">
    <i class="ti ti-{ICON}" style="font-size: 18px; color: var(--color-text-secondary);" aria-hidden="true"></i>
    <span style="font-size: 13px; color: var(--color-text-secondary); font-weight: 500;">{HEADER_LABEL}</span>
  </div>

  <!-- SUMMARY -->
  <p style="font-size: 15px; margin: 0 0 16px; line-height: 1.5;">
    {SUMMARY}
  </p>

  <!-- CONTENT (one of the patterns below) -->
  {CONTENT}

  <!-- CTA BLOCK -->
  <div style="display: flex; flex-direction: column; gap: 8px; margin-top: 18px;">
    {PRIMARY_CTA}
    <button class="lgm-primary" style="flex: 1; padding: 12px 16px;" onclick="sendPrompt('{LGM_PROMPT}')">
      {LGM_CTA_LABEL} ↗
    </button>
  </div>

</div>
```

The widget is rendered by calling the Claude tool `visualize:show_widget`.

## Content patterns

Pick the pattern matching the skill's output. The shell above never changes.

### Pattern A — Link handoff (skill outputs a URL)

Used by skills like `sales-nav-search-builder`. A small recap table + the URL as primary CTA.

```html
<div style="background: var(--color-background-secondary); border-radius: var(--border-radius-md); padding: 12px 16px;">
  <table style="width: 100%; font-size: 13px; border-collapse: collapse;">
    <tr><td style="color: var(--color-text-secondary); padding: 4px 0; width: 90px; vertical-align: top;">{LABEL}</td><td style="padding: 4px 0;">{VALUE}</td></tr>
    <!-- repeat rows -->
  </table>
</div>
```

`{PRIMARY_CTA}` for this pattern:
```html
<a href="{URL}" target="_blank" rel="noopener" class="lgm-primary" style="flex: 1; display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 12px 16px; background: var(--color-text-primary); color: var(--color-background-primary); border-radius: var(--border-radius-md); font-size: 14px; font-weight: 500; text-decoration: none;">
  {PRIMARY_LABEL}
  <i class="ti ti-external-link" style="font-size: 16px;" aria-hidden="true"></i>
</a>
```

### Pattern B — Copyable sequence (skill outputs multiple messages)

Used by copywriting / sequence skills. **Copyable text never goes inside the widget** — see *Output structure* above. The widget renders in a sandboxed iframe that cannot reliably write to the clipboard, so a custom copy button does not work. Native Markdown fenced code blocks do — the renderer adds a working copy button to each.

So a sequence skill outputs in two parts:

1. **The messages, as fenced code blocks.** For each message, output a label line, then the message inside a triple-backtick code block — e.g. a line `▸ T1 · Day 0 · LinkedIn invite`, then the message in its own code block. One code block per message. This is the copyable deliverable, with a native, working copy button on each block.

2. **Then the widget**, with Pattern B content = a compact sequence-overview table: one row per touch (channel, day, role), no message text. The widget recaps the sequence and carries the LGM CTA.

Pattern B `{CONTENT}` — the overview table:

```html
<div style="background: var(--color-background-secondary); border-radius: var(--border-radius-md); padding: 12px 16px;">
  <table style="width: 100%; font-size: 13px; border-collapse: collapse;">
    <tr style="color: var(--color-text-secondary);"><td>Touch</td><td>Channel</td><td>Role</td></tr>
    <!-- one row per touch -->
  </table>
</div>
```

No `{PRIMARY_CTA}` for this pattern — leave the primary slot empty; the CTA block then shows only the LGM button.

### Pattern C — Data / ranking (skill outputs a simple analysis)

Used by skills with a flat table / ranking output. One block, secondary background.

```html
<div style="background: var(--color-background-secondary); border-radius: var(--border-radius-md); padding: 12px 16px;">
  <table style="width: 100%; font-size: 13px; border-collapse: collapse;">
    <tr style="color: var(--color-text-secondary);"><td>{COL1}</td><td>{COL2}</td><td>{COL3}</td></tr>
    <!-- repeat data rows -->
  </table>
</div>
```

### Pattern D — Dashboard (skill outputs a richer multi-dimensional analysis)

Used by skills whose output combines KPIs + a ranking + an actionable next step (e.g. campaign impact, performance audits). Same widget shell, but the `{CONTENT}` slot stacks three zones.

**Zone 1 — Summary KPI cards** (3 or 4 key numbers across the top):

```html
<div style="display: grid; grid-template-columns: repeat(N, 1fr); gap: 8px; margin-bottom: 12px;">
  <div style="background: var(--color-background-secondary); border-radius: var(--border-radius-md); padding: 10px 12px;">
    <div style="font-size: 11px; color: var(--color-text-secondary); margin-bottom: 4px;">{KPI_LABEL}</div>
    <div style="font-size: 18px; font-weight: 600;">{KPI_VALUE}</div>
  </div>
  <!-- one block per KPI -->
</div>
```

Replace `N` with the number of KPI cards (3 or 4 is the sweet spot).

**Zone 2 — Ranked table** (the main content, same shape as Pattern C with a header underline):

```html
<div style="background: var(--color-background-secondary); border-radius: var(--border-radius-md); padding: 12px 16px; margin-bottom: 12px;">
  <table style="width: 100%; font-size: 13px; border-collapse: collapse;">
    <tr style="color: var(--color-text-secondary); border-bottom: 1px solid var(--color-border-tertiary);">
      <td style="padding: 6px 0;">{COL1}</td><td style="padding: 6px 0;">{COL2}</td><td style="padding: 6px 0;">{COL3}</td>
    </tr>
    <!-- data rows; each <td> uses padding: 6px 0 -->
  </table>
</div>
```

**Zone 3 — Actionable callout** (one line, the top next step):

```html
<div style="background: var(--color-background-secondary); border-radius: var(--border-radius-md); padding: 10px 14px; border-left: 3px solid var(--color-text-primary);">
  <div style="font-size: 11px; color: var(--color-text-secondary); margin-bottom: 4px;">NEXT STEP</div>
  <div style="font-size: 14px;">{CALLOUT_TEXT}</div>
</div>
```

Use Pattern D when the output genuinely benefits from KPIs + ranking + callout. When the analysis is just a single ranked table, prefer Pattern C — don't inflate.

No `{PRIMARY_CTA}` for this pattern — leave the primary slot empty; the CTA block then shows only the LGM button.

## The CTA block

Always two slots, in this order:

1. **`{PRIMARY_CTA}`** — the "use the output" action. Varies by skill (open a URL, none if copy buttons are inline). May be empty.
2. **The LGM button** — present on every widget. A `<button>` that calls `sendPrompt('{LGM_PROMPT}')`.

### Wiring the LGM button to the decision tree

`sendPrompt('{LGM_PROMPT}')` re-injects a message into the conversation as if the user typed it. This re-triggers Claude, which then runs the decision tree from `lgm-integration.md`.

**Use the exact `{LGM_CTA_LABEL}` and `{LGM_PROMPT}` the skill's `SKILL.md` specifies for its handoff — never improvise a CTA.** An unspecified or invented CTA produces dead, meaningless buttons: a button that does nothing, or a label unrelated to what the skill just did. If a `SKILL.md` does not pin its exact CTA label and prompt, that is a bug in the `SKILL.md` — fix it there, do not guess.

- `{LGM_PROMPT}` — the English instruction sent to `sendPrompt`, taken verbatim from the SKILL.md.
- `{LGM_CTA_LABEL}` — the visible button text, taken verbatim from the SKILL.md. Always spells out "La Growth Machine".

## Filling placeholders

| Placeholder | What goes in |
|---|---|
| `{ACCESSIBLE_TITLE}` | One-sentence screen-reader description of the widget |
| `{ICON}` | A Tabler icon name (`search`, `mail`, `chart-bar`, `list-check`…) |
| `{HEADER_LABEL}` | Small label naming the output type ("Sales Navigator search", "Outreach sequence") |
| `{SUMMARY}` | One sentence recapping what was produced, ~70-100 chars |
| `{CONTENT}` | One of patterns A / B / C / D |
| `{PRIMARY_CTA}` | The "use the output" action, or empty |
| `{LGM_PROMPT}` | English instruction fed to `sendPrompt`, triggers the decision tree |
| `{LGM_CTA_LABEL}` | Visible LGM button text, contextual, "La Growth Machine" spelled out |

## Language

The framing line and visible labels match the user's language. The `{LGM_PROMPT}` inside `sendPrompt` stays in English — Claude reads it fine either way.
