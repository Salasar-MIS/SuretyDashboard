"""
All MongoDB read/write operations.
Every function takes explicit parameters — no globals except db().
"""
from bson import ObjectId
from .db import get_db

MONTHS = ["April", "May", "June", "July", "August", "September",
          "October", "November", "December", "January", "February", "March"]


# ── Branch helpers ────────────────────────────────────────────────────────────

def get_all_branches():
    return list(get_db()["branches"].find().sort("display_order", 1))

def get_branch_by_code(code: str):
    return get_db()["branches"].find_one({"branch_code": code})

def get_sub_branches(parent_id: ObjectId):
    """Return sub-branches under a given parent, ordered by display_order."""
    return list(get_db()["branches"].find(
        {"parent_id": parent_id, "branch_type": "sub"}
    ).sort("display_order", 1))

def get_main_branches():
    """Return the 4 top-level branches in display order."""
    return list(get_db()["branches"].find(
        {"branch_type": {"$in": ["main", "aggregate_l1"]}}
    ).sort("display_order", 1))


# ── RM helpers ────────────────────────────────────────────────────────────────

def get_rms(branch_id: ObjectId, active_only: bool = True):
    query = {"branch_id": branch_id}
    if active_only:
        query["is_active"] = True
    return list(get_db()["relationship_managers"].find(query).sort("display_order", 1))

def add_rm(branch_id: ObjectId, rm_name: str):
    col = get_db()["relationship_managers"]
    last = col.find_one({"branch_id": branch_id}, sort=[("display_order", -1)])
    order = (last["display_order"] + 1) if last else 1
    col.insert_one({
        "branch_id":     branch_id,
        "rm_name":       rm_name,
        "is_active":     True,
        "display_order": order,
    })

def deactivate_rm(rm_id: ObjectId):
    get_db()["relationship_managers"].update_one(
        {"_id": rm_id}, {"$set": {"is_active": False}}
    )

def rename_rm(rm_id: ObjectId, new_name: str):
    get_db()["relationship_managers"].update_one(
        {"_id": rm_id}, {"$set": {"rm_name": new_name}}
    )


# ── Revenue ───────────────────────────────────────────────────────────────────

def upsert_revenue(rm_id: ObjectId, branch_id: ObjectId, fy: str, month: str, amount: float):
    get_db()["monthly_revenue"].update_one(
        {"rm_id": rm_id, "financial_year": fy, "month": month},
        {"$set": {"revenue_amount": amount, "branch_id": branch_id}},
        upsert=True,
    )

def get_revenue_for_branch(branch_id: ObjectId, fy: str) -> dict:
    """Return {rm_id: {month: amount}} for all RMs in a branch."""
    rows = get_db()["monthly_revenue"].find({"branch_id": branch_id, "financial_year": fy})
    result = {}
    for r in rows:
        result.setdefault(r["rm_id"], {})[r["month"]] = r["revenue_amount"]
    return result


# ── Targets ───────────────────────────────────────────────────────────────────

def upsert_target(rm_id: ObjectId, branch_id: ObjectId, fy: str, amount: float):
    get_db()["rm_targets"].update_one(
        {"rm_id": rm_id, "financial_year": fy},
        {"$set": {"target_amount": amount, "branch_id": branch_id}},
        upsert=True,
    )

def get_targets_for_branch(branch_id: ObjectId, fy: str) -> dict:
    """Return {rm_id: target_amount}."""
    rows = get_db()["rm_targets"].find({"branch_id": branch_id, "financial_year": fy})
    return {r["rm_id"]: r["target_amount"] for r in rows}


# ── Proposals ─────────────────────────────────────────────────────────────────

def upsert_proposals(rm_id: ObjectId, branch_id: ObjectId, fy: str, month: str,
                     proposals: int, converted: int):
    get_db()["proposal_conversions"].update_one(
        {"rm_id": rm_id, "financial_year": fy, "month": month},
        {"$set": {"proposals_count": proposals, "converted_count": converted,
                  "branch_id": branch_id}},
        upsert=True,
    )

def get_proposals_for_branch(branch_id: ObjectId, fy: str) -> dict:
    """Return {rm_id: {month: {"proposals": int, "converted": int}}}."""
    rows = get_db()["proposal_conversions"].find({"branch_id": branch_id, "financial_year": fy})
    result = {}
    for r in rows:
        result.setdefault(r["rm_id"], {})[r["month"]] = {
            "proposals": r["proposals_count"],
            "converted": r["converted_count"],
        }
    return result
