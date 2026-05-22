# Geo Locations Reference

The `regions.json` file maps LinkedIn geo URN IDs to their human-readable names, used by the `REGION` filter in Sales Navigator search URLs.

## How LinkedIn geo IDs work

LinkedIn's location taxonomy is **Bing Geo** — a numeric URN namespace covering countries, regions, and cities. Each location has a unique ID in the form `urn:li:geo:<NNN>`. In Sales Navigator search URLs, the filter type is `REGION` and the bare numeric ID is passed.

LinkedIn migrated to Bing Geo around 2020-2021, deprecating the older ISO-style identifiers (`urn:li:country:us`). The Bing Geo namespace is shared across LinkedIn surfaces — the same numeric ID identifies a country in Sales Navigator URLs, in the LinkedIn API, and in LinkedIn Ads campaigns.

## What's in regions.json

The current file contains a curated set of countries — the COUNTRY_REGION level of the Bing Geo taxonomy. Cities, metropolitan areas, and sub-national subdivisions (US states, UK constituent countries, etc.) are not included in v1. For city-level or state-level targeting, the user can open the generated URL in Sales Navigator and refine the location filter manually in the UI.

Schema:

```json
[
  {"id": 105015875, "displayValue": "France"},
  {"id": 103644278, "displayValue": "United States"}
]
```

`displayValue` is used verbatim for the `text:` field in the Sales Nav URL. The pair (`id`, `displayValue`) is what LinkedIn expects.

## Adding a new region manually

If a location is missing, anyone can add it by capturing the URN from Sales Navigator:

1. Open Sales Navigator search in a browser
2. Apply only the geography filter, set to the location you want
3. Inspect the URL in the address bar — look for `type:REGION,values:List((id:NNNNNNNNN,text:...))`
4. The number after `id:` is the URN. Add an entry to `regions.json`:

```json
{"id": 123456789, "displayValue": "Your Location Name"}
```

5. Open a pull request

## Notes on special entries

Two entries have anomalously low IDs in the format LinkedIn returns:

- `Worldwide` (`92000000`) — meta-entity representing "no geographic restriction"
- `Palestinian Authority` (`93000000`) — special territorial entry

These are intentional LinkedIn meta-entries and work correctly in the `REGION` filter.

## Cross-surface validity

A geo URN obtained from any LinkedIn surface works on any other:

- Sales Navigator search URLs (`type:REGION` filter)
- LinkedIn Recruiter search
- LinkedIn Ads Manager campaigns (post-2021 Bing Geo migration)
- The official LinkedIn Marketing API (`urn:li:geo:<ID>`)

This is verifiable by spot-checking: e.g., France resolves to `105015875` everywhere it appears across LinkedIn.
