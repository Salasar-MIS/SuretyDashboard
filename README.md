# Surety Dashboard

A centralized web platform to manage, monitor, and analyze surety bond performance across branches and Relationship Managers (RMs). Built for underwriters, agents, and brokers.

**Live:** [suretydashboard.streamlit.app](https://suretydashboard.streamlit.app)

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| Database | MongoDB Atlas (pymongo) |

---

## Dashboard Hierarchy (17 views)

- **Summary** (read-only) — aggregates the 4 top-level branches
- **Delhi (NCR) / Ahmedabad / Mumbai** — RM-level data entry
- **Naveen Aggarwal** (read-only) — aggregates 12 sub-branches
  - Bangalore, Bhubaneswar, Guwahati, Hyderabad, Indore, Jamshedpur, Kanpur, Kolkata, Mayank Shukla, Nagpur, Raipur, Ranchi — RM-level data entry

Each data-entry dashboard has 3 sections:
1. **Month Wise Branch Revenue** (APR–MAR per RM)
2. **Revenue in Lakhs** (Target per RM + auto-computed Achievement)
3. **Month Wise Proposal Conversions** (Proposals & Converted per RM per month)

---

## Project Structure

```
SuretyDashboard/
├── main.py                      # Streamlit Cloud entry point + nav + auto-seed
├── seed.py                      # Populates branches & RMs (auto-runs on first boot)
├── requirements.txt
├── app/
│   ├── components/              # section_revenue / lakhs / proposals
│   ├── pages/                   # branch_dashboard, naveen_aggarwal, summary
│   └── utils/                   # db, queries, transforms, styles
├── PROJECT_DESCRIPTION.md
└── ARCHITECTURE.md
```

---

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create `.streamlit/secrets.toml` (or `.env`) with:
   ```toml
   MONGO_URI = "your-mongodb-atlas-uri"
   ```
3. Run:
   ```bash
   streamlit run main.py
   ```

The database auto-seeds on first launch if the `branches` collection is empty.

---

## Deployment (Streamlit Cloud)

- Entry point: `main.py`
- Add `MONGO_URI` under **Settings → Secrets**
- Ensure MongoDB Atlas **Network Access** allows `0.0.0.0/0`

---

## Configuration Notes

- **RMs** are managed per branch via the in-app Admin panel (add / rename / remove)
- **Target** is entered per RM; branch Grand Total Target = sum of all RM targets
- **Achievement** is auto-computed from the 12 monthly revenue figures
- Financial Year: **FY 2026-27**
- Authentication is open access (Phase 1); login planned for Phase 2
