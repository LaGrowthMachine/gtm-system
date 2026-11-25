# La Growth Machine MCP · what was checked on a real account

Facts verified on a real La Growth Machine workspace. Each line has its date. Anything not listed here is not verified.

## Pushing leads (`create_lead`), 2026-11-17

Tested with one fake lead in a test audience, attached to no campaign.

| Fact | Result |
|---|---|
| An audience name that does not exist | **The audience is created**, with no warning. A typo in the name creates a new audience. |
| Custom attributes | Stored as written, apostrophe, ampersand and angle brackets included. How they render in a message is not tested. |
| Pushing the same lead again, identified by first name + last name + company | **Ignored**: "Lead is a duplicate & has been ignored". The custom attributes are **not** updated. |
| Pushing the same lead again with its `leadId` | **Updated**: "Lead is a duplicate & has been merged". The custom attributes are replaced. |
| Reading back | `get_audience_leads` with `include: ["customAttributes", "audiences"]` returns the lead, its values and its audiences. |
| `search_lead` on a lead that is in an audience | Finds the lead and its custom attributes. **`audiencesWithName` came back empty**, although the lead was in the audience. Do not rely on it to know which audience a lead is in. |

What follows for a push:

1. Look the lead up with `search_lead`. If it exists, push with its `leadId`, otherwise the attributes are not written.
2. To know who is already in the audience, read the audience with `get_audience_leads`. Do not ask `search_lead`.
3. Copy the audience name from `get_campaign`. Never type it.

Not verified yet: the same test with a LinkedIn URL or an email as the identifier, `involvedCampaigns` on a lead that
is in a campaign, the status values returned by `get_campaign`, `excludeContactedLeads` on a lead that was contacted.

## Importing a search (`create_audience_from_linkedin_url`), 2026-11-17

| Fact | Result |
|---|---|
| A Sales Navigator URL with a company filter and a boolean title filter | Works. The company goes in as `urn:li:organization:<LinkedIn company id>`. |
| Time | The call returns at once with an empty audience. 17 people were in it about 4 minutes later, 6 to 20 minutes in later runs. Check with `get_audience`. |
| The URL encoding | The values inside the query must be encoded twice (`urn%253Ali%253Aorganization%253A<id>`). Encoded once, the import returns nobody, with no error. The pattern is in the `find-contacts` skill. |
| An import into an audience that exists | The people are added to it. A working audience grows run after run: 33 to 190 people in one day of tests. |
| `list_audiences` | Returns every audience of the workspace, about 80 KB. Search the audience name in the full text to get its id. |
| What comes back | First name, last name, company, exact job title, LinkedIn URL, location. No email. |
| A person already in the workspace | Reused, not duplicated: it came back with its existing id and its email. |
| A LinkedIn event URL | The tool description says it imports the attendees, if the identity is registered to the event. Not tested. |

## Campaigns, 2026-11-17

| Fact | Result |
|---|---|
| `list_public_campaigns` (type `recommended`) | Returns 9 catalog templates, each with an id that `duplicate_campaign` accepts |
| `get_campaign_steps` on a catalog template id | 404. A template can only be read after it is duplicated. |
| `duplicate_campaign` with the id of a shared campaign link (`campaigns_shared/<id>`), 2026-11-17 | Works: the copy lands in the current workspace as a draft (READY). **It keeps the audience, the identity, the language and the CRM sync of the source**: set the audience and the identity right after. |
| `edit_campaign_message` with `<p><var name="customAttribute2"/></p>`, 2026-11-17 | Accepted on email and LinkedIn steps. For an email step in the same thread, pass `subjectNewHtml` as `<p/>`. |
| Creating an empty audience | Not possible. `create_lead` with a new audience name creates it with that lead in it. |
| Pushing a lead that exists, with its `leadId`, its email and 10 custom attributes, into the audience of a draft campaign, 2026-11-17 | "Merged. Added to existing audience." Read back with `get_audience_leads`: the email and the 10 values are there, `<br>` kept as written. The campaign stays READY. |
| A custom attribute with a label in the workspace, 2026-11-17 | The app shows the label instead of the number: for example custom attribute 1 can be displayed as `{{pageVisited}}`. The MCP still reads and writes it as `customAttribute1`. A label means another campaign uses that attribute: a lead that sits in both campaigns would have its value overwritten. |
| `enrich_lead` on a lead that exists (2026-11-18) | 5 credits per lead, announced before a confirmation. The email is written on the lead and readable with `search_lead`. The custom attributes are not touched. |
| `get_audience_leads` with `include: ["customAttributes"]` | The attributes come back flat on the lead (`customAttribute1`, `customAttribute2`…), not in a nested object. |
| The email status | It can go from pending to valid between the enrichment and the push. Read it again before a launch. |
| The name of a copy, 2026-11-18 | `duplicate_campaign` adds a number at the end of the name ("… 489"). Rename it with `rename_campaign`. |
| `set_campaign_audience` on a copy, 2026-11-18 | Returns the audience and its size. The source campaign keeps its own audience: checked on both with `get_campaign`. |
| `get_enrich_result`, 2026-11-18 | Can stay pending for about 3 minutes. Wait and read again before deciding the email was not found. |
| The email domain | It can differ from the website of the company (a site on one domain, the emails on another). Not a sign of a wrong match by itself. |
| `remove_lead_from_audience` | Needs one identifier of the lead: an email, a LinkedIn URL or a CRM id. A lead that has none cannot be removed through the MCP. |
| Adding a step, a delay or a condition | No tool does it. `add_campaign_step_message` fills an empty step that already exists. |

## Building from a catalog template, 2026-11-25

| Fact | Result |
|---|---|
| A copy of a catalog template | No audience (`get_campaign` shows no audience field until `set_campaign_audience`), the identity may be disconnected, language French, CRM sync on |
| `get_campaign` on the catalog template id | 404 |
| `get_campaign_messages` on a fresh catalog copy | 0 messages: fill the steps with `add_campaign_step_message` |
| `get_campaign_steps` | Lists the message steps only. The LinkedIn invitation step is not listed and its note cannot be written |
| `<var name="customAttribute1" default="..."/>` | Accepted: the default text is used when the lead has no value |
| `get_campaign_stats` | Large payload: it carries the HTML of every step |

