# Tested queries

Each query below ran on a real workspace on 2026-11-25 and returned numbers checked against the campaign stats. Start
from the closest one and adapt it: change the window, add a `campaignId` or `identityId` filter, change the grouping.
Keep its structure.

Two limits of the server shape every query:

- **A query may scan 20 GB at most.** On a busy workspace, a query that joins several steps over a year is refused
  ("Query would scan ... above the limit"). Use 90 days by default. When the user asks for a longer period and the
  server refuses, move the start date forward one month at a time until it passes, and say the period you could read.
- **A partition filter on `date` in every `FROM logs`**, subqueries included.

## 0. The campaigns that weigh most

For questions that need "the main campaigns" (step loss, a test on the biggest campaigns).

```sql
SELECT campaignId,
  COUNT(DISTINCT IF(status = 'SUCCESS' AND type IN ('LINKEDIN_ADD_CONTACT','LINKEDIN_DIRECT_MESSAGE',
    'LINKEDIN_DIRECT_VOICE','GOOGLE_SEND_EMAIL'), leadId, NULL)) AS leads_reached,
  MIN(date) AS first_activity
FROM logs
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) AND campaignId IS NOT NULL
GROUP BY campaignId
ORDER BY leads_reached DESC
LIMIT 5
```

## 1. Which messages get the most replies

A reply is credited to the last message the lead received from that campaign before replying. Run it twice, `DESC`
for the best and `ASC` for the weakest: the answer names both ends. `messages_kept` gives the total.

```sql
WITH sends AS (
  SELECT campaignId, leadId, templateId, type, createdAt FROM logs
  WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) AND status = 'SUCCESS' AND templateId IS NOT NULL
    AND campaignId IS NOT NULL
    AND type IN ('LINKEDIN_ADD_CONTACT','LINKEDIN_DIRECT_MESSAGE','LINKEDIN_DIRECT_VOICE','GOOGLE_SEND_EMAIL')
),
replies AS (
  SELECT campaignId, leadId, MIN(createdAt) AS replied_at FROM logs
  WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) AND type IN ('LINKEDIN_HAS_REPLY','GOOGLE_REPLY')
    AND campaignId IS NOT NULL
  GROUP BY campaignId, leadId
),
credited AS (
  SELECT r.campaignId, r.leadId, ARRAY_AGG(s.templateId ORDER BY s.createdAt DESC LIMIT 1)[OFFSET(0)] AS templateId
  FROM replies r JOIN sends s ON s.campaignId = r.campaignId AND s.leadId = r.leadId AND s.createdAt <= r.replied_at
  GROUP BY r.campaignId, r.leadId
)
SELECT s.campaignId, s.templateId, ANY_VALUE(s.type) AS step_type,
  COUNT(DISTINCT s.leadId) AS leads_sent,
  COUNT(DISTINCT c.leadId) AS replies_credited,
  ROUND(100 * SAFE_DIVIDE(COUNT(DISTINCT c.leadId), COUNT(DISTINCT s.leadId)), 1) AS reply_rate,
  COUNT(*) OVER () AS messages_kept
FROM sends s
LEFT JOIN credited c ON c.campaignId = s.campaignId AND c.leadId = s.leadId AND c.templateId = s.templateId
GROUP BY s.campaignId, s.templateId
HAVING leads_sent >= 30
ORDER BY reply_rate DESC, leads_sent DESC
LIMIT 10
```

Then:
- Name each campaign with `get_campaign` and read its `objective`. **Warm campaigns (reactivation, signups,
  webinar registrants) reply far more than cold ones:** split the ranking by objective, or at least mark each row
  warm or cold, before anyone compares a message to another.
- Show the text of the best and the weakest messages: `get_campaign_stats` of the campaign, `templates[]` where
  `templateId` matches (`name`, `position`, `newHtml`). A template that is only `<var name="customAttributeN"/>` was
  written per lead: say so, its text differs for each lead.

## 2. Where the leads stop (one campaign)

Run it on the campaigns of query 0, one by one.

```sql
SELECT
  IF(type = 'LINKEDIN_ADD_CONTACT', 'invitation', COALESCE(templateId, 'unknown')) AS step,
  ANY_VALUE(type) AS step_type,
  MAX(IF(type = 'LINKEDIN_ADD_CONTACT' AND templateId IS NOT NULL, 1, 0)) AS invitation_with_note,
  MIN(createdAt) AS first_sent,
  COUNT(DISTINCT leadId) AS leads_reached
FROM logs
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) AND campaignId = '<campaignId>' AND status = 'SUCCESS'
  AND type IN ('LINKEDIN_ADD_CONTACT','LINKEDIN_DIRECT_MESSAGE','LINKEDIN_DIRECT_VOICE','GOOGLE_SEND_EMAIL')
GROUP BY step
ORDER BY first_sent
```

And the acceptance of the same campaign:

```sql
SELECT
  COUNT(DISTINCT IF(status = 'SUCCESS' AND type = 'LINKEDIN_ADD_CONTACT', leadId, NULL)) AS invited,
  COUNT(DISTINCT IF(type = 'LINKEDIN_NEW_RELATION_ADDED', leadId, NULL)) AS new_connections,
  COUNT(DISTINCT IF(type IN ('LINKEDIN_HAS_REPLY','GOOGLE_REPLY'), leadId, NULL)) AS replied
FROM logs
WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) AND campaignId = '<campaignId>'
```

How to read it:
- The invitation step counts every invitation, with or without a note.
- **A campaign is not a straight line.** Leads who do not accept the invitation are often sent to an email branch,
  leads who reply leave the sequence. A count that goes back up after a step is a branch, not an error. Read the
  steps in the order of `first_sent`, not of `position` (`position` is the order of the template list, not of the
  flow).
- In most LinkedIn campaigns the biggest stop is the invitation that is not accepted: `invited` against
  `new_connections`. Say it with both numbers.

## 3. Does an invitation note get more replies

Grouped per campaign and lead, so a lead invited in two campaigns is counted in each, and the reply belongs to the
same campaign. Invitations of the last 14 days are left out: they have not had time to be accepted.

```sql
WITH inv AS (
  SELECT campaignId, leadId, MAX(IF(templateId IS NOT NULL, 1, 0)) AS with_note, MIN(createdAt) AS invited_at
  FROM logs
  WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 180 DAY) AND date < DATE_SUB(CURRENT_DATE(), INTERVAL 14 DAY)
    AND status = 'SUCCESS' AND type = 'LINKEDIN_ADD_CONTACT' AND campaignId IS NOT NULL
  GROUP BY campaignId, leadId
),
acc AS (
  SELECT campaignId, leadId, MIN(createdAt) AS accepted_at FROM logs
  WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 180 DAY) AND type = 'LINKEDIN_NEW_RELATION_ADDED'
    AND campaignId IS NOT NULL
  GROUP BY campaignId, leadId
),
rep AS (
  SELECT campaignId, leadId, MIN(createdAt) AS replied_at FROM logs
  WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 180 DAY) AND type = 'LINKEDIN_HAS_REPLY' AND campaignId IS NOT NULL
  GROUP BY campaignId, leadId
)
SELECT inv.with_note,
  COUNT(*) AS invited,
  COUNT(DISTINCT inv.campaignId) AS campaigns,
  COUNTIF(acc.accepted_at >= inv.invited_at) AS accepted,
  COUNTIF(rep.replied_at >= inv.invited_at) AS replied_on_linkedin,
  ROUND(100 * SAFE_DIVIDE(COUNTIF(acc.accepted_at >= inv.invited_at), COUNT(*)), 1) AS acceptance_rate,
  ROUND(100 * SAFE_DIVIDE(COUNTIF(rep.replied_at >= inv.invited_at), COUNT(*)), 1) AS reply_rate
FROM inv LEFT JOIN acc USING (campaignId, leadId) LEFT JOIN rep USING (campaignId, leadId)
GROUP BY inv.with_note
```

Use `LINKEDIN_NEW_RELATION_ADDED` for an acceptance: `LINKEDIN_ACCEPT_REQUEST` and `LINKEDIN_NEW_RELATION` also count
leads who were already connected and inflate the rate (83% instead of 44% in the test). When one group comes from a
few campaigns, group by `campaignId` too and say which campaigns weigh: a note is often used on warmer leads, and the
two groups rarely target the same people. The fair test is an A/B inside one campaign.

## 4. Which replies never reached the CRM

A reply reached the CRM when the CRM received an update of the lead after the reply. `HUBSPOT_CRM_INIT` does not count:
it fires when the lead starts the campaign, before any reply.

```sql
WITH rep AS (
  SELECT campaignId, leadId, MIN(createdAt) AS replied_at FROM logs
  WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) AND type IN ('LINKEDIN_HAS_REPLY','GOOGLE_REPLY')
    AND campaignId IS NOT NULL
  GROUP BY campaignId, leadId
),
crm AS (
  SELECT leadId, MAX(createdAt) AS last_crm_at FROM logs
  WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
    AND type IN ('HUBSPOT_CRM_UPDATE_LEAD','HUBSPOT_CRM_UPDATE_LEAD_LIFECYCLE','HUBSPOT_CRM_UPDATE_LEAD_TIMELINE',
                 'PIPEDRIVE_CRM_UPDATE_LEAD','PIPEDRIVE_CRM_UPDATE_LEAD_LIFECYCLE','PIPEDRIVE_CRM_UPDATE_LEAD_TIMELINE')
  GROUP BY leadId
)
SELECT rep.campaignId,
  COUNT(*) AS replied_leads,
  COUNTIF(crm.last_crm_at IS NULL OR crm.last_crm_at < rep.replied_at) AS reply_not_synced
FROM rep LEFT JOIN crm USING (leadId)
GROUP BY rep.campaignId
HAVING reply_not_synced > 0
ORDER BY reply_not_synced DESC
LIMIT 10
```

Give the total first (replied leads, replies not synced), then the campaigns where it happens. Only the native
HubSpot and Pipedrive syncs leave a trace in the logs: a CRM fed by Zapier, Make, the API or Clay is invisible here,
and a campaign with the CRM sync off shows every reply as not synced. Check the sync of a campaign before calling it a
problem. To list the leads, select `leadId` for one campaign, then name them with `search_lead`, only when the user
asks.

## 5. Compare the sender identities

Split by channel by default: the email and LinkedIn rates of one identity can differ by 10 to 18 points. A reply
counts only when it comes from a lead this identity contacted in the same campaign and on the same channel.

```sql
WITH contacted AS (
  SELECT identityId, campaignId, leadId, IF(STARTS_WITH(type, 'LINKEDIN_'), 'LINKEDIN', 'EMAIL') AS channel
  FROM logs
  WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) AND status = 'SUCCESS' AND identityId IS NOT NULL
    AND campaignId IS NOT NULL
    AND ((type = 'LINKEDIN_ADD_CONTACT' AND templateId IS NOT NULL)
      OR type IN ('LINKEDIN_DIRECT_MESSAGE','LINKEDIN_DIRECT_VOICE','GOOGLE_SEND_EMAIL'))
  GROUP BY identityId, campaignId, leadId, channel
),
replied AS (
  SELECT DISTINCT campaignId, leadId, IF(type = 'LINKEDIN_HAS_REPLY', 'LINKEDIN', 'EMAIL') AS channel
  FROM logs
  WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) AND type IN ('LINKEDIN_HAS_REPLY','GOOGLE_REPLY')
    AND campaignId IS NOT NULL
)
SELECT c.identityId, c.channel,
  COUNT(DISTINCT c.leadId) AS contacted_leads,
  COUNT(DISTINCT r.leadId) AS replied_leads,
  ROUND(100 * SAFE_DIVIDE(COUNT(DISTINCT r.leadId), COUNT(DISTINCT c.leadId)), 1) AS reply_rate
FROM contacted c
LEFT JOIN replied r ON r.campaignId = c.campaignId AND r.leadId = c.leadId AND r.channel = c.channel
GROUP BY c.identityId, c.channel
HAVING contacted_leads >= 30
ORDER BY c.channel, reply_rate DESC
```

Name the identities with `list_identities`. Identities run different campaigns on different targets: say it before
anyone reads the ranking as a ranking of people. An email reply rate near 0 on hundreds of emails can be a logging gap
(the mailbox does not report replies) as much as a real result: say both, and suggest checking one thread in the
inbox.

## 6. How long leads take to reply

Medians, not averages: a few late replies pull the average far up.

```sql
WITH first_contact AS (
  SELECT campaignId, leadId, IF(STARTS_WITH(type, 'LINKEDIN_'), 'LINKEDIN', 'EMAIL') AS ch, MIN(createdAt) AS contacted_at
  FROM logs
  WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) AND status = 'SUCCESS'
    AND ((type = 'LINKEDIN_ADD_CONTACT' AND templateId IS NOT NULL)
      OR type IN ('LINKEDIN_DIRECT_MESSAGE','LINKEDIN_DIRECT_VOICE','GOOGLE_SEND_EMAIL'))
    AND campaignId IS NOT NULL AND leadId IS NOT NULL
  GROUP BY campaignId, leadId, ch
),
first_reply AS (
  SELECT campaignId, leadId, IF(type = 'LINKEDIN_HAS_REPLY', 'LINKEDIN', 'EMAIL') AS ch, MIN(createdAt) AS replied_at
  FROM logs
  WHERE date >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY) AND type IN ('LINKEDIN_HAS_REPLY','GOOGLE_REPLY')
    AND campaignId IS NOT NULL AND leadId IS NOT NULL
  GROUP BY campaignId, leadId, ch
),
pairs AS (
  SELECT fc.campaignId, fc.ch, TIMESTAMP_DIFF(fr.replied_at, fc.contacted_at, MINUTE) / 60 AS hours
  FROM first_contact fc JOIN first_reply fr
    ON fc.campaignId = fr.campaignId AND fc.leadId = fr.leadId AND fc.ch = fr.ch AND fr.replied_at >= fc.contacted_at
)
SELECT ch AS channel, COUNT(*) AS replied_leads,
  ROUND(APPROX_QUANTILES(hours, 100)[OFFSET(50)], 1) AS median_hours,
  ROUND(100 * SAFE_DIVIDE(COUNTIF(hours <= 24), COUNT(*)), 1) AS pct_within_24h
FROM pairs
GROUP BY ch
```

Add `campaignId` to the final grouping (with `HAVING replied_leads >= 10`) for the split by campaign. A campaign whose
invitations carry a note starts the clock at the invitation, so its time includes waiting for the acceptance: say it
when campaigns are compared.

## More

`get_bigquery_logs_guide` has ready-made queries for the funnel of each campaign, the email funnel and the daily
activity. Use them as they are.
