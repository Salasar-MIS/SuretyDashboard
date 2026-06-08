# Surety Dashboard — Architecture

**Last Updated:** 2026-06-08
**Status:** Finalized — Ready for development

---

## High-Level Architecture

```
[ User (Browser) ]
       │
       ▼
[ Streamlit App ]
  - Navigation sidebar
  - Data entry forms (branch/sub-branch dashboards)
  - Read-only display tables (summary/aggregate dashboards)
       │
       ▼
[ Python Backend Layer ]
  - Query helpers (queries.py)
  - Data transformation / aggregation (transforms.py)
  - MongoDB connection (db.py)
       │
       ▼
[ MongoDB Atlas ]
  - branches
  - relationship_managers
  - monthly_revenue
  - rm_targets
  - proposal_conversions
```

---

## MongoDB Collections

### `branches`
Stores all branches and sub-branches.

```json
{
  "_id": "ObjectId",
  "branch_code": "string (slug, e.g. 'ncr', 'ahmedabad', 'bangalore')",
  "branch_name": "string (display name)",
  "branch_type": "string ('main' | 'sub' | 'aggregate_l1')",
  "parent_id": "ObjectId | null",
  "display_order": "int"
}
```

- `branch_type = 'main'` → NCR, Ahmedabad, Mumbai (data-entry, RM-level)
- `branch_type = 'aggregate_l1'` → Naveen Aggarwal (read-only, aggregates sub-branches)
- `branch_type = 'sub'` → 12 sub-branches under Naveen Aggarwal (data-entry, RM-level)
- `parent_id` → null for top-level branches; Naveen Aggarwal's `_id` for sub-branches

---

### `relationship_managers`
Stores RMs per branch. Variable count per branch, admin-configurable.

```json
{
  "_id": "ObjectId",
  "branch_id": "ObjectId",
  "rm_name": "string",
  "is_active": "bool",
  "display_order": "int"
}
```

---

### `monthly_revenue`
Monthly revenue entered per RM per month.

```json
{
  "_id": "ObjectId",
  "rm_id": "ObjectId",
  "branch_id": "ObjectId",
  "financial_year": "string (e.g. '2026-27')",
  "month": "string (e.g. 'April')",
  "revenue_amount": "float"
}
```

Compound unique index: `(rm_id, financial_year, month)`

---

### `rm_targets`
Individual annual target per RM per FY. Branch Grand Total Target = sum of all RM targets.

```json
{
  "_id": "ObjectId",
  "rm_id": "ObjectId",
  "branch_id": "ObjectId",
  "financial_year": "string",
  "target_amount": "float"
}
```

Compound unique index: `(rm_id, financial_year)`

---

### `proposal_conversions`
Monthly proposals submitted and converted per RM.

```json
{
  "_id": "ObjectId",
  "rm_id": "ObjectId",
  "branch_id": "ObjectId",
  "financial_year": "string",
  "month": "string",
  "proposals_count": "int",
  "converted_count": "int"
}
```

Compound unique index: `(rm_id, financial_year, month)`

---

## Derived / Computed Values (Not Stored)

| Value | Derivation |
|---|---|
| RM Achievement | Sum of 12 months from `monthly_revenue` for that RM |
| Branch Grand Total (Revenue) | Sum of all RM revenues per month |
| Branch Grand Total Target | Sum of all RM targets |
| Branch Grand Total Achievement | Sum of all RM achievements |
| Naveen Aggarwal row (in Summary) | Grand Totals from Naveen Aggarwal's 12 sub-branches |
| Summary Grand Total | Column-wise sum of all 4 main branches |

---

## Navigation (Streamlit Sidebar)

```
Summary
NCR
Ahmedabad
Mumbai
Naveen Aggarwal
  └── Naveen Aggarwal Dashboard
  └── Bangalore
  └── Bhubaneswar
  └── Guwahati
  └── Hyderabad
  └── Indore
  └── Jamshedpur
  └── Kanpur
  └── Kolkata
  └── Mayank Shukla
  └── Nagpur
  └── Raipur
  └── Ranchi
```

Clicking "Naveen Aggarwal" in the top-level menu expands to show the Naveen Aggarwal aggregation view and its 12 sub-branch links.

---

## Folder Structure

```
Surety-Dashboard-Claude/
│
├── app/
│   ├── main.py                      # Streamlit entry point + sidebar navigation
│   ├── pages/
│   │   ├── summary.py               # Top-level summary (read-only)
│   │   ├── branch_dashboard.py      # Reusable data-entry dashboard (NCR, Ahmedabad, Mumbai, sub-branches)
│   │   └── naveen_aggarwal.py       # Naveen Aggarwal aggregation view (read-only)
│   ├── components/
│   │   ├── section_revenue.py       # Section 1: Month Wise Revenue table
│   │   ├── section_lakhs.py         # Section 2: Revenue in Lakhs table
│   │   └── section_proposals.py    # Section 3: Proposal Conversions table
│   └── utils/
│       ├── db.py                    # MongoDB Atlas connection (pymongo)
│       ├── queries.py               # All read/write DB operations
│       └── transforms.py           # Aggregation and computation helpers
│
├── PROJECT_DESCRIPTION.md
├── ARCHITECTURE.md
└── requirements.txt
```

---

## Key Design Decisions

- **Single reusable dashboard component:** `branch_dashboard.py` handles all 15 data-entry dashboards (NCR, Ahmedabad, Mumbai + 12 sub-branches) — branch identity passed as a parameter.
- **Computed at runtime:** All Grand Totals, Achievements, and aggregations are derived at query time, never stored.
- **RM management via DB:** Adding/removing RMs requires no code changes — admin updates `relationship_managers` collection.
- **Naveen Aggarwal is a pure aggregator:** It never holds its own RM data; it reads sub-branch Grand Totals only.
- **Open auth now, pluggable later:** No auth layer in Phase 1; session state and route guards can be added in Phase 2 without restructuring the app.
