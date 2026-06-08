"""
Pure aggregation and computation helpers — no DB calls here.
All functions work on plain dicts returned by queries.py.
"""
from .queries import MONTHS


def branch_revenue_table(rms: list, revenue_data: dict) -> list:
    """
    Build rows for Section 1 (Month Wise Revenue).

    Returns a list of dicts:
      [{"rm_id": ..., "rm_name": ..., "April": 0.0, ..., "March": 0.0, "total": 0.0}, ...]
    Plus a final Grand Total row.
    """
    rows = []
    grand = {m: 0.0 for m in MONTHS}
    grand["total"] = 0.0

    for rm in rms:
        rm_rev = revenue_data.get(rm["_id"], {})
        row = {"rm_id": rm["_id"], "rm_name": rm["rm_name"]}
        row_total = 0.0
        for m in MONTHS:
            val = rm_rev.get(m, 0.0)
            row[m] = val
            row_total += val
            grand[m] += val
        row["total"] = row_total
        grand["total"] += row_total
        rows.append(row)

    grand["rm_name"] = "Grand Total"
    grand["rm_id"] = None
    rows.append(grand)
    return rows


def branch_lakhs_table(rms: list, revenue_data: dict, target_data: dict) -> list:
    """
    Build rows for Section 2 (Revenue in Lakhs).

    Returns:
      [{"rm_id": ..., "rm_name": ..., "target": 0.0, "achievement": 0.0}, ...]
    Plus Grand Total row.
    """
    rows = []
    grand_target = 0.0
    grand_achievement = 0.0

    for rm in rms:
        rm_rev = revenue_data.get(rm["_id"], {})
        achievement = sum(rm_rev.get(m, 0.0) for m in MONTHS)
        target = target_data.get(rm["_id"], 0.0)
        grand_target += target
        grand_achievement += achievement
        rows.append({
            "rm_id":       rm["_id"],
            "rm_name":     rm["rm_name"],
            "target":      target,
            "achievement": achievement,
        })

    rows.append({
        "rm_id":       None,
        "rm_name":     "Grand Total",
        "target":      grand_target,
        "achievement": grand_achievement,
    })
    return rows


def branch_proposals_table(rms: list, proposals_data: dict) -> list:
    """
    Build rows for Section 3 (Month Wise Proposal Conversions).

    Returns:
      [{"rm_id": ..., "rm_name": ..., "April_p": 0, "April_c": 0, ..., "March_p": 0, "March_c": 0}, ...]
    Plus Grand Total row.
    """
    rows = []
    grand = {f"{m}_p": 0 for m in MONTHS}
    grand.update({f"{m}_c": 0 for m in MONTHS})

    for rm in rms:
        rm_prop = proposals_data.get(rm["_id"], {})
        row = {"rm_id": rm["_id"], "rm_name": rm["rm_name"]}
        for m in MONTHS:
            month_data = rm_prop.get(m, {})
            p = month_data.get("proposals", 0)
            c = month_data.get("converted", 0)
            row[f"{m}_p"] = p
            row[f"{m}_c"] = c
            grand[f"{m}_p"] += p
            grand[f"{m}_c"] += c
        rows.append(row)

    grand["rm_name"] = "Grand Total"
    grand["rm_id"] = None
    rows.append(grand)
    return rows


def aggregate_grand_totals(branch_tables: list) -> dict:
    """
    Given a list of branch Grand Total rows (one per branch),
    produce the Summary Grand Total row by summing across branches.

    Each item in branch_tables must be a dict with month keys and
    optional target/achievement keys.
    """
    summary = {m: 0.0 for m in MONTHS}
    summary["total"] = 0.0
    summary["target"] = 0.0
    summary["achievement"] = 0.0

    for row in branch_tables:
        for m in MONTHS:
            summary[m] += row.get(m, 0.0)
        summary["total"] += row.get("total", 0.0)
        summary["target"] += row.get("target", 0.0)
        summary["achievement"] += row.get("achievement", 0.0)

    return summary
