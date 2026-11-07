#!/usr/bin/env python3
"""
M2 Deliverable (deepseek-agent):
Florida Senior Relocation Dataset Validator & Carrying Cost Scorer
Converts src/data/florida_communities.csv -> src/data/communities.json
"""
import csv
import datetime
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "src" / "data" / "florida_communities.csv"
JSON_PATH = ROOT / "src" / "data" / "communities.json"


def compute_carrying_score(hoa_mo: int, cdd_mo: int, tax_ins_mo: int, zone: str) -> dict:
    total_monthly_carry = hoa_mo + cdd_mo + tax_ins_mo
    is_hvhz = "HVHZ" in zone.upper() or "COASTAL" in zone.upper()
    if total_monthly_carry < 850 and not is_hvhz:
        tier = "Low (Non-Coastal)"
        badge_color = "emerald"
    elif total_monthly_carry <= 1150 and not is_hvhz:
        tier = "Moderate"
        badge_color = "amber"
    else:
        tier = "High (Coastal Wind Zone)"
        badge_color = "rose"
    return {
        "total_monthly_carrying_cost_usd": total_monthly_carry,
        "carrying_cost_tier": tier,
        "badge_color": badge_color,
    }


def main():
    rows = []
    with CSV_PATH.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            hoa = int(r.get("hoa_monthly") or 0)
            cdd = int(r.get("cdd_monthly") or 0)
            tax_ins = int(r.get("est_tax_ins_monthly") or 0)
            scoring = compute_carrying_score(hoa, cdd, tax_ins, r.get("flood_hurricane_zone", ""))
            rows.append({
                **r,
                "median_price_min": int(r.get("median_price_min") or 0),
                "median_price_max": int(r.get("median_price_max") or 0),
                "hoa_monthly": hoa,
                "cdd_monthly": cdd,
                "est_tax_ins_monthly": tax_ins,
                "va_drive_mins": int(r.get("va_drive_mins") or 0),
                **scoring,
            })

    payload = {
        "site": "agentpulse.pro",
        "repo": "blogerr",
        "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "count": len(rows),
        "communities": rows,
    }
    JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    JSON_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"[validate_and_score] Validated {len(rows)} communities -> {JSON_PATH}")


if __name__ == "__main__":
    main()
