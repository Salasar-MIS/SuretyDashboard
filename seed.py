"""
Run once to populate the branches and relationship_managers collections.
Usage: python seed.py
"""
from app.utils.db import get_db

# ── Branch definitions ────────────────────────────────────────────────────────

BRANCHES = [
    # Top-level summary is not a branch — it is derived at runtime.

    # Main branches (data-entry, RM-level)
    {"branch_code": "ncr",       "branch_name": "Delhi (NCR)", "branch_type": "main",         "parent_code": None, "display_order": 1},
    {"branch_code": "ahmedabad", "branch_name": "Ahmedabad",   "branch_type": "main",         "parent_code": None, "display_order": 2},
    {"branch_code": "mumbai",    "branch_name": "Mumbai",       "branch_type": "main",         "parent_code": None, "display_order": 3},

    # Naveen Aggarwal — aggregation node (no RMs of its own)
    {"branch_code": "naveen_aggarwal", "branch_name": "Naveen Aggarwal", "branch_type": "aggregate_l1", "parent_code": None, "display_order": 4},

    # 12 sub-branches under Naveen Aggarwal (data-entry, RM-level)
    {"branch_code": "bangalore",    "branch_name": "Bangalore",    "branch_type": "sub", "parent_code": "naveen_aggarwal", "display_order": 1},
    {"branch_code": "bhubaneswar",  "branch_name": "Bhubaneswar",  "branch_type": "sub", "parent_code": "naveen_aggarwal", "display_order": 2},
    {"branch_code": "guwahati",     "branch_name": "Guwahati",     "branch_type": "sub", "parent_code": "naveen_aggarwal", "display_order": 3},
    {"branch_code": "hyderabad",    "branch_name": "Hyderabad",    "branch_type": "sub", "parent_code": "naveen_aggarwal", "display_order": 4},
    {"branch_code": "indore",       "branch_name": "Indore",       "branch_type": "sub", "parent_code": "naveen_aggarwal", "display_order": 5},
    {"branch_code": "jamshedpur",   "branch_name": "Jamshedpur",   "branch_type": "sub", "parent_code": "naveen_aggarwal", "display_order": 6},
    {"branch_code": "kanpur",       "branch_name": "Kanpur",       "branch_type": "sub", "parent_code": "naveen_aggarwal", "display_order": 7},
    {"branch_code": "kolkata",      "branch_name": "Kolkata",      "branch_type": "sub", "parent_code": "naveen_aggarwal", "display_order": 8},
    {"branch_code": "mayank_shukla","branch_name": "Mayank Shukla","branch_type": "sub", "parent_code": "naveen_aggarwal", "display_order": 9},
    {"branch_code": "nagpur",       "branch_name": "Nagpur",       "branch_type": "sub", "parent_code": "naveen_aggarwal", "display_order": 10},
    {"branch_code": "raipur",       "branch_name": "Raipur",       "branch_type": "sub", "parent_code": "naveen_aggarwal", "display_order": 11},
    {"branch_code": "ranchi",       "branch_name": "Ranchi",       "branch_type": "sub", "parent_code": "naveen_aggarwal", "display_order": 12},
]

# Placeholder RMs — replace names with real ones via the admin panel later.
# Format: { branch_code: [rm_name, ...] }
INITIAL_RMS = {
    "ncr":          ["RM 1", "RM 2", "RM 3"],
    "ahmedabad":    ["RM 1", "RM 2", "RM 3"],
    "mumbai":       ["RM 1", "RM 2", "RM 3"],
    "bangalore":    ["RM 1", "RM 2"],
    "bhubaneswar":  ["RM 1", "RM 2"],
    "guwahati":     ["RM 1", "RM 2"],
    "hyderabad":    ["RM 1", "RM 2"],
    "indore":       ["RM 1", "RM 2"],
    "jamshedpur":   ["RM 1", "RM 2"],
    "kanpur":       ["RM 1", "RM 2"],
    "kolkata":      ["RM 1", "RM 2"],
    "mayank_shukla":["RM 1", "RM 2"],
    "nagpur":       ["RM 1", "RM 2"],
    "raipur":       ["RM 1", "RM 2"],
    "ranchi":       ["RM 1", "RM 2"],
}


def seed():
    db = get_db()

    # ── Seed branches ─────────────────────────────────────────────────────────
    branches_col = db["branches"]

    # First pass: insert branches without parent_id resolution
    code_to_id = {}
    for b in BRANCHES:
        existing = branches_col.find_one({"branch_code": b["branch_code"]})
        if existing:
            code_to_id[b["branch_code"]] = existing["_id"]
            print(f"  Branch already exists: {b['branch_name']}")
            continue
        doc = {
            "branch_code":   b["branch_code"],
            "branch_name":   b["branch_name"],
            "branch_type":   b["branch_type"],
            "parent_id":     None,
            "display_order": b["display_order"],
        }
        result = branches_col.insert_one(doc)
        code_to_id[b["branch_code"]] = result.inserted_id
        print(f"  Inserted branch: {b['branch_name']}")

    # Second pass: set parent_id for sub-branches
    for b in BRANCHES:
        if b["parent_code"]:
            branches_col.update_one(
                {"branch_code": b["branch_code"]},
                {"$set": {"parent_id": code_to_id[b["parent_code"]]}}
            )

    # ── Seed RMs ──────────────────────────────────────────────────────────────
    rms_col = db["relationship_managers"]

    for branch_code, rm_names in INITIAL_RMS.items():
        branch_id = code_to_id.get(branch_code)
        if not branch_id:
            print(f"  WARNING: branch_code '{branch_code}' not found, skipping RMs")
            continue
        for order, rm_name in enumerate(rm_names, start=1):
            existing = rms_col.find_one({"branch_id": branch_id, "rm_name": rm_name})
            if existing:
                print(f"  RM already exists: {branch_code} / {rm_name}")
                continue
            rms_col.insert_one({
                "branch_id":     branch_id,
                "rm_name":       rm_name,
                "is_active":     True,
                "display_order": order,
            })
            print(f"  Inserted RM: {branch_code} / {rm_name}")

    # ── Indexes ───────────────────────────────────────────────────────────────
    db["monthly_revenue"].create_index(
        [("rm_id", 1), ("financial_year", 1), ("month", 1)], unique=True
    )
    db["rm_targets"].create_index(
        [("rm_id", 1), ("financial_year", 1)], unique=True
    )
    db["proposal_conversions"].create_index(
        [("rm_id", 1), ("financial_year", 1), ("month", 1)], unique=True
    )
    print("\nIndexes ensured.")
    print("\nSeed complete.")


if __name__ == "__main__":
    seed()
