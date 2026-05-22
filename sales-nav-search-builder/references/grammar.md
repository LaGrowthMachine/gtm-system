# Sales Navigator URL Grammar

Reverse-engineered from real Sales Nav URLs captured November 2026. LinkedIn doesn't document this publicly and may change it; if the builder breaks, recapture URLs and update.

## Endpoint

```
https://www.linkedin.com/sales/search/people?query=<QUERY>&viewAllFilters=true
```

(Optional but harmless: `&sessionId=...` — session-scoped, not needed for shareability.)

## The query format (LinkedIn-encoded)

This is LinkedIn's proprietary format, not JSON. The query object has up to four top-level properties:

```
(
  recentSearchParam:(...),         ← optional, session-scoped, can be omitted
  spellCorrectionEnabled:true,     ← present when KEYWORDS is set
  keywords:<boolean string>,       ← top-level, NOT inside filters:List
  filters:List(
    (type:<TYPE_NAME>,values:List(
      (id:<ID>,text:<TEXT>,selectionType:<INCLUDED|EXCLUDED>),
      ...
    )),
    ...
  )
)
```

**Key structural rule**: `KEYWORDS` is **not** a regular filter. It does NOT appear as `(type:KEYWORDS,values:List(...))` inside `filters:List`. Instead, it lives as a top-level `keywords:<value>` property on the query object, alongside `spellCorrectionEnabled:true`. This is verified against a live captured URL.

All other filters (Industry, Function, CURRENT_TITLE, PAST_TITLE, FIRST_NAME, toggles, etc.) live inside `filters:List`:

```
(type:NAME,values:List((value1),(value2),...))
```

Each value tuple has 1 to 3 fields depending on the filter type:
- **ID-based filters**: `(id:X,text:Y,selectionType:Z)` — `text` is descriptive, LinkedIn ignores it for matching but expects it present.
- **Text-only filters in filters:List** (FIRST_NAME, LAST_NAME, CURRENT_TITLE, PAST_TITLE): `(text:Y,selectionType:Z)` — no `id`.
- **Toggle filters**: `(id:X,selectionType:Z)` or `(id:X,text:Y,selectionType:Z)` — text optional.

## Encoding (two passes)

### Pass 1: Inner LinkedIn encoding

Inside text values, special characters are %-encoded:
- space → `%20`
- comma → `%2C` (critical! many industry names contain commas like "Health, Wellness & Fitness")
- ampersand → `%26`
- parens → `%28` `%29` if they appear in text
- slash → `%2F`

Letters, digits, hyphens, dots stay as-is.

### Pass 2: Outer URL encoding

Then the whole query string becomes a URL parameter value:
- `(` and `)` → kept as-is (NOT encoded)
- `:` → `%3A`
- `,` → `%2C`
- `%` → `%25` (so `%20` from pass 1 becomes `%2520`)
- letters, digits stay

This is why you see `%2520` in URLs — it's a space that went through two encoding passes.

## Filter type names (verified)

Inside `filters:List`:

```
INDUSTRY
FUNCTION
SENIORITY_LEVEL
COMPANY_HEADCOUNT
COMPANY_TYPE
YEARS_AT_CURRENT_COMPANY
YEARS_IN_CURRENT_POSITION
YEARS_OF_EXPERIENCE
PROFILE_LANGUAGE
REGION                          (not GEOGRAPHY)
FIRST_NAME
LAST_NAME
CURRENT_TITLE                   (text field; accepts boolean — verified live)
PAST_TITLE                      (text field; accepts boolean — verified live)
RECENTLY_CHANGED_JOBS           (toggle, id:RPC)
POSTED_ON_LINKEDIN              (toggle, id:RPOL)
PAST_COLLEAGUE                  (toggle, id:PCOLL)
FOLLOWS_YOUR_COMPANY            (toggle, id:CF)
```

Outside `filters:List` (top-level query properties):

```
keywords                        (top-level, accepts boolean — verified live)
spellCorrectionEnabled          (top-level, set to true when keywords is present)
```

## Boolean search support (3 fields)

The fields `KEYWORDS`, `CURRENT_TITLE`, and `PAST_TITLE` accept boolean syntax: `AND`, `OR`, `NOT`, `"..."`, `(...)`. LinkedIn parses the operators at search time, not URL time.

`CURRENT_TITLE` and `PAST_TITLE` go inside `filters:List` as text values:
```
(type:CURRENT_TITLE,values:List((text:<boolean string>,selectionType:INCLUDED)))
```

`KEYWORDS` goes at the top level of the query, paired with `spellCorrectionEnabled:true`:
```
(spellCorrectionEnabled:true,keywords:<boolean string>,filters:List(...other filters...))
```

Both flow through the same two-pass encoding. Worked example for `(CMO OR "Chief Marketing Officer") NOT Fractional`:

Pass 1 (inner): `%28CMO%20OR%20%22Chief%20Marketing%20Officer%22%29%20NOT%20Fractional`

Pass 2 (outer): `%2528CMO%2520OR%2520%2522Chief%2520Marketing%2520Officer%2522%2529%2520NOT%2520Fractional`

The double-encoded `%2528` (open paren), `%2522` (quote), and `%2520` (space) are signatures of a properly-encoded boolean string.

See `boolean-search.md` for the full syntax rules and common patterns.

## Filter type names (v2 — entity-based, not in v1)

```
CURRENT_COMPANY        (needs company URN)
PAST_COMPANY           (needs company URN)
COMPANY_HEADQUARTERS   (needs geo URN)
SCHOOL                 (needs school URN)
GROUPS                 (needs group URN)
PERSONA                (Sales Nav internal IDs)
ACCOUNT_LIST
LEAD_LIST
CONNECTIONS_OF         (needs profile ID)
CONNECTION             (1st/2nd/3rd — enum, could be v1 if needed)
```

## Worked example

Spec: Industry = Software Development (include) + Staffing and Recruiting (exclude); Seniority = CXO + VP.

Inner encoded:
```
(filters:List((type:INDUSTRY,values:List((id:4,text:Software%20Development,selectionType:INCLUDED),(id:104,text:Staffing%20and%20Recruiting,selectionType:EXCLUDED))),(type:SENIORITY_LEVEL,values:List((id:310,text:CXO,selectionType:INCLUDED),(id:300,text:Vice%20President,selectionType:INCLUDED)))))
```

After outer URL encoding:
```
(filters%3AList((type%3AINDUSTRY%2Cvalues%3AList((id%3A4%2Ctext%3ASoftware%2520Development%2CselectionType%3AINCLUDED)%2C(id%3A104%2Ctext%3AStaffing%2520and%2520Recruiting%2CselectionType%3AEXCLUDED)))%2C(type%3ASENIORITY_LEVEL%2Cvalues%3AList((id%3A310%2Ctext%3ACXO%2CselectionType%3AINCLUDED)%2C(id%3A300%2Ctext%3AVice%2520President%2CselectionType%3AINCLUDED)))))
```

Full URL:
```
https://www.linkedin.com/sales/search/people?query=(filters%3AList(...))&viewAllFilters=true
```
