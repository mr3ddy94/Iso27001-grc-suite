"""
Validates data/controls.csv and data/crosswalk.csv for structural integrity.
Run manually with `python data/validate_data.py`, or via CI on every push.
Exits non-zero (and prints failures) if any check fails.
"""
import re
import sys
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent
ISO_ID_PATTERN = re.compile(r"^A\.(5|6|7|8)\.\d+$")

REQUIRED_CONTROL_COLUMNS = [
    "control_id", "theme", "requirement", "status", "owner", "evidence",
    "last_review", "next_review", "risk", "gap", "remediation_action",
]
VALID_STATUSES = {"Implemented", "Partially Implemented", "Not Implemented", "Not Applicable"}
VALID_THEMES = {"Organizational", "People", "Physical", "Technological"}
VALID_RISKS = {"High", "Medium", "Low", "N/A"}

REQUIRED_CROSSWALK_COLUMNS = [
    "iso_control_id", "target_framework", "target_id", "target_title", "confidence", "notes",
]
VALID_CONFIDENCE = {"Strong", "Partial", "Weak"}

failures = []


def check(condition: bool, message: str):
    if not condition:
        failures.append(message)


def validate_controls() -> pd.DataFrame:
    # keep_default_na=False: "risk" legitimately contains the literal string
    # "N/A" for Not Applicable controls; don't let pandas coerce it to NaN.
    df = pd.read_csv(DATA_DIR / "controls.csv", keep_default_na=False, na_values=[])

    check(list(df.columns) == REQUIRED_CONTROL_COLUMNS, "controls.csv: column set/order mismatch")
    check(len(df) == 93, f"controls.csv: expected 93 rows (Annex A 2022), found {len(df)}")
    check(df["control_id"].is_unique, "controls.csv: duplicate control_id values found")

    bad_ids = df[~df["control_id"].apply(lambda x: bool(ISO_ID_PATTERN.match(str(x))))]
    check(bad_ids.empty, f"controls.csv: malformed control_id values: {bad_ids['control_id'].tolist()}")

    check(set(df["status"].unique()) <= VALID_STATUSES, f"controls.csv: unexpected status values: {set(df['status'].unique()) - VALID_STATUSES}")
    check(set(df["theme"].unique()) <= VALID_THEMES, f"controls.csv: unexpected theme values: {set(df['theme'].unique()) - VALID_THEMES}")
    check(set(df["risk"].unique()) <= VALID_RISKS, f"controls.csv: unexpected risk values: {set(df['risk'].unique()) - VALID_RISKS}")

    for col in REQUIRED_CONTROL_COLUMNS:
        check(df[col].notna().all(), f"controls.csv: null values found in column '{col}'")

    dates_ok = pd.to_datetime(df["last_review"], errors="coerce").notna().all() and \
        pd.to_datetime(df["next_review"], errors="coerce").notna().all()
    check(dates_ok, "controls.csv: unparseable dates in last_review/next_review")

    return df


def validate_crosswalk(controls_df: pd.DataFrame):
    df = pd.read_csv(DATA_DIR / "crosswalk.csv", keep_default_na=False, na_values=[])

    check(list(df.columns) == REQUIRED_CROSSWALK_COLUMNS, "crosswalk.csv: column set/order mismatch")
    check(len(df) > 0, "crosswalk.csv: no rows found")

    unknown_iso = set(df["iso_control_id"].unique()) - set(controls_df["control_id"].unique())
    check(not unknown_iso, f"crosswalk.csv: iso_control_id values with no matching control: {unknown_iso}")

    check(set(df["confidence"].unique()) <= VALID_CONFIDENCE, f"crosswalk.csv: unexpected confidence values: {set(df['confidence'].unique()) - VALID_CONFIDENCE}")

    for col in ["iso_control_id", "target_framework", "target_id", "target_title", "confidence"]:
        check(df[col].notna().all(), f"crosswalk.csv: null values found in column '{col}'")

    # every ISO control should have at least one crosswalk mapping
    uncovered = set(controls_df["control_id"].unique()) - set(df["iso_control_id"].unique())
    if uncovered:
        print(f"WARNING: {len(uncovered)} ISO controls have no crosswalk mapping yet: {sorted(uncovered)}")


def main():
    controls_df = validate_controls()
    validate_crosswalk(controls_df)

    if failures:
        print(f"\n❌ {len(failures)} validation failure(s):")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)

    print("✅ All data validation checks passed.")
    print(f"   controls.csv: {len(controls_df)} rows")
    crosswalk_df = pd.read_csv(DATA_DIR / "crosswalk.csv", keep_default_na=False, na_values=[])
    print(f"   crosswalk.csv: {len(crosswalk_df)} rows, "
          f"{crosswalk_df['target_framework'].nunique()} target framework(s)")


if __name__ == "__main__":
    main()
