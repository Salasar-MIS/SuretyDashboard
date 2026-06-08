# Surety Dashboard — Project Description

**Last Updated:** 2026-06-08
**Status:** Architecture finalized — Ready for development

---

## Overview

The Surety Dashboard is a centralized web-based platform for managing, monitoring, and analyzing surety bonds. Built for underwriters, agents, and brokers, it provides real-time visibility into bond portfolios, revenue, and proposal conversions across branches and Relationship Managers (RMs).

All data is entered manually by authorized branch personnel via Streamlit forms and stored in MongoDB Atlas. No file uploads.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (Python-based UI) |
| Backend | Python |
| Database | MongoDB Atlas (pymongo) |

---

## Financial Year

**FY 2026-27** (April 2026 to March 2027)

---

## Dashboard Hierarchy

```
Summary Dashboard (read-only)
├── NCR Dashboard (data entry, RM-level)
├── Ahmedabad Dashboard (data entry, RM-level)
├── Mumbai Dashboard (data entry, RM-level)
└── Naveen Aggarwal (aggregation, read-only)
    ├── Bangalore (data entry, RM-level)
    ├── Bhubaneswar (data entry, RM-level)
    ├── Guwahati (data entry, RM-level)
    ├── Hyderabad (data entry, RM-level)
    ├── Indore (data entry, RM-level)
    ├── Jamshedpur (data entry, RM-level)
    ├── Kanpur (data entry, RM-level)
    ├── Kolkata (data entry, RM-level)
    ├── Mayank Shukla (data entry, RM-level)
    ├── Nagpur (data entry, RM-level)
    ├── Raipur (data entry, RM-level)
    └── Ranchi (data entry, RM-level)
```

**Total dashboards:** 1 Summary + 3 main branches + 1 Naveen Aggarwal aggregation + 12 sub-branches = **17 views**

---

## Branch Types

| Type | Dashboards | Behaviour |
|---|---|---|
| `main` | NCR, Ahmedabad, Mumbai | Data entry at RM level |
| `aggregate_l1` | Naveen Aggarwal | Read-only; aggregates 12 sub-branches |
| `sub` | 12 under Naveen Aggarwal | Data entry at RM level |

---

## Dashboard Structure (all data-entry dashboards share this layout)

### Section 1 — Month Wise Branch Revenue

| Column | Content |
|---|---|
| Name | RM names (rows) |
| April–March | Monthly revenue entered per RM |
| Grand Total | Auto-computed: column-wise sum of all RMs |

### Section 2 — Revenue in Lakhs (FY 2026-27)

| Column | Content |
|---|---|
| Name | RM names (rows) |
| Target | Manually entered per RM |
| Achievement | Auto-computed: sum of 12 months for that RM |
| Grand Total | Target = sum of all RM targets; Achievement = sum of all RM achievements |

### Section 3 — Month Wise Proposal Conversions

| Column | Content |
|---|---|
| Name | RM names (rows) |
| April…March | Each month: 2 sub-columns — Proposals (entered) and Converted (entered) |
| Grand Total | Auto-computed: column-wise sum per sub-column |

---

## Summary Dashboard (read-only)

Same 3 sections. Rows are the 4 top-level branches:
- Naveen Aggarwal, NCR, Ahmedabad, Mumbai + Grand Total

Values pulled from the Grand Total row of each branch/aggregate dashboard.

### Naveen Aggarwal Dashboard (read-only)

Same 3 sections. Rows are the 12 sub-branches.
Values pulled from the Grand Total row of each sub-branch dashboard.

---

## RM Management (Admin)

- RMs are dynamically configurable per branch (add/remove)
- Each branch has its own RM count (not fixed to 6)
- Admin can manage RMs without code changes

---

## Authentication

- **Phase 1 (current):** Open access — no login required
- **Phase 2 (future):** Login/authentication per user to be implemented later

---

## Coding Guidelines

- Keep the entire app **low code**
- Emphasize **high quality coding**
- Provide **simple comments** over code blocks for human readability
- Handle **edge cases** carefully
- Do **not** create unnecessary code
- Always ask before coding any **unspecified logic blocks**
