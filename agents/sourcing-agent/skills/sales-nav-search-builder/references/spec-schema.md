# Spec Schema

A spec is a JSON file describing the filters Claude wants to apply. The builder script reads it, validates each value against the references, and outputs the URL.

## Minimal example

```json
{
  "filters": [
    {
      "type": "INDUSTRY",
      "values": [
        {"id": 4, "selectionType": "INCLUDED"}
      ]
    }
  ]
}
```

## Full example

```json
{
  "filters": [
    {
      "type": "INDUSTRY",
      "values": [
        {"id": 4, "selectionType": "INCLUDED"},
        {"id": 96, "selectionType": "INCLUDED"},
        {"id": 104, "selectionType": "EXCLUDED"}
      ]
    },
    {
      "type": "FUNCTION",
      "values": [
        {"id": 25, "selectionType": "INCLUDED"},
        {"id": 15, "selectionType": "INCLUDED"}
      ]
    },
    {
      "type": "SENIORITY_LEVEL",
      "values": [
        {"id": 310, "selectionType": "INCLUDED"},
        {"id": 300, "selectionType": "INCLUDED"}
      ]
    },
    {
      "type": "COMPANY_HEADCOUNT",
      "values": [
        {"id": "D", "selectionType": "INCLUDED"},
        {"id": "E", "selectionType": "INCLUDED"}
      ]
    },
    {
      "type": "REGION",
      "values": [
        {"id": 105015875, "selectionType": "INCLUDED"}
      ]
    },
    {
      "type": "PROFILE_LANGUAGE",
      "values": [
        {"id": "fr", "selectionType": "INCLUDED"}
      ]
    },
    {
      "type": "FIRST_NAME",
      "values": [
        {"text": "alex", "selectionType": "INCLUDED"}
      ]
    },
    {
      "type": "RECENTLY_CHANGED_JOBS",
      "toggle": true
    }
  ]
}
```

## Field rules

- `type`: one of the supported types listed in `grammar.md`.
- `values`: array of value objects. Each value has:
  - `id`: required for ID-based filters and toggles. For most enums it's an integer; for `COMPANY_HEADCOUNT` and `COMPANY_TYPE` it's a single letter string (e.g., `"D"`, `"P"`); for `PROFILE_LANGUAGE` it's a 2-letter code (e.g., `"fr"`).
  - `text`: required for text-only filters (FIRST_NAME, LAST_NAME, CURRENT_TITLE, PAST_TITLE, KEYWORDS). The builder will look up the human-readable text automatically for ID-based filters, so you can omit it there.
  - `selectionType`: `"INCLUDED"` or `"EXCLUDED"`. Defaults to `"INCLUDED"` if omitted.
- `toggle: true`: shortcut for toggle filters (RECENTLY_CHANGED_JOBS, POSTED_ON_LINKEDIN, PAST_COLLEAGUE, FOLLOWS_YOUR_COMPANY) — the builder auto-fills the hardcoded ID. You can also write it out explicitly with `values`.

## Validation behavior

If an `id` doesn't exist in the relevant reference file, the builder exits with an error listing the offending filter. There's no fuzzy matching — pick the right ID upstream.
