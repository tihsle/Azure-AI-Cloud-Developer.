### Processing JSON Data with T-SQL

#### Scenario

You are a SQL AI Developer at CarbonOps.

Your ESG platform now:

1) Receives data from APIs in JSON format
2) Stores semi-structured ESG metadata
3) Needs to generate JSON responses for frontend + AI systems

You must process JSON directly in SQL


#### Store JSON Data

Add JSON Column to Companies:
```sql
ALTER TABLE ESG.Companies
ADD COLUMN ESG_Metadata JSONB;
```

Insert JSON Data:
```sql
UPDATE ESG.Companies
SET ESG_Metadata =
CASE CompanyID

WHEN 1 THEN
'{
    "rating":"A",
    "esgScore":85,
    "audits":{
        "lastAuditYear":2024,
        "passed":true
    }
}'::jsonb

WHEN 2 THEN
'{
    "rating":"B",
    "esgScore":72,
    "audits":{
        "lastAuditYear":2023,
        "passed":true
    }
}'::jsonb

WHEN 3 THEN
'{
    "rating":"C",
    "esgScore":60,
    "audits":{
        "lastAuditYear":2022,
        "passed":false
    }
}'::jsonb

WHEN 4 THEN
'{
    "rating":"A",
    "esgScore":90,
    "audits":{
        "lastAuditYear":2024,
        "passed":true
    }
}'::jsonb

ELSE NULL

END;
```

#### Extract Data from JSON

Extract scalar values:
```sql
SELECT
    CompanyID,
    CompanyName,

    ESG_Metadata->>'rating' AS ESG_Rating,

    (ESG_Metadata->>'esgScore')::INT AS ESG_Score

FROM ESG.Companies;
```

Extract nested json metadata fields
```sql
SELECT
    CompanyID,
    CompanyName,

    ESG_Metadata->'audits' AS AuditInfo

FROM ESG.Companies;
```

#### Access Nested Properties

Access nested properties using the following query:
```sql
SELECT
    CompanyName,

    ESG_Metadata->'audits'->>'lastAuditYear'
        AS LastAuditYear,

    ESG_Metadata->'audits'->>'passed'
        AS AuditPassed

FROM ESG.Companies;
```

#### Parse JSON Arrays

Declare a JSON Variable:
```sql
SELECT '
[
    {
        "year":2023,
        "emissions":1000
    },
    {
        "year":2024,
        "emissions":800
    }
]
'::jsonb AS emissions_json;
```

Parse into rows:
```sql
SELECT *

FROM jsonb_to_recordset(
'
[
    {
        "year":2023,
        "emissions":1000
    },
    {
        "year":2024,
        "emissions":800
    }
]
'::jsonb
)

AS x(
    year INT,
    emissions INT
);
```

### Construct JSON Objects

Construct JSON Objects from table values:
```sql
SELECT
    json_build_object(
        'company',
        CompanyName,

        'country',
        Country
    ) AS CompanyJson

FROM ESG.Companies;
```

Construct a simple JSON Array:
```sql
SELECT json_build_array(
    'ESG',
    'AI',
    'Sustainability'
) AS Tags;
```

### Aggregate Rows into JSON Arrays:

use the following query to build JSON aggregates:
```sql
SELECT
    CompanyID,

    json_agg(
        CO2_Emissions
    ) AS EmissionHistory

FROM ESG.EmissionRecords

GROUP BY CompanyID;
```

