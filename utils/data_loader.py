"""Shared data loading + metric helpers for the GRC Suite."""
from datetime import date
from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

STATUS_COLORS = {
    "Implemented": "#1A9E5C",
    "Partially Implemented": "#E0A32C",
    "Not Implemented": "#D64545",
    "Not Applicable": "#8A8F98",
}

RISK_COLORS = {"High": "#D64545", "Medium": "#E0A32C", "Low": "#1A9E5C", "N/A": "#8A8F98"}

THEME_ORDER = ["Organizational", "People", "Physical", "Technological"]


@st.cache_data
def load_controls() -> pd.DataFrame:
    # keep_default_na=False: the "risk" column legitimately contains the literal
    # string "N/A" (for Not Applicable controls) which pandas would otherwise
    # silently coerce to a real NaN.
    df = pd.read_csv(
        DATA_DIR / "controls.csv",
        parse_dates=["last_review", "next_review"],
        keep_default_na=False,
        na_values=[],
    )
    df["theme"] = pd.Categorical(df["theme"], categories=THEME_ORDER, ordered=True)
    return df


def get_working_controls() -> pd.DataFrame:
    """Session-scoped, editable copy of the controls dataset.

    This is what pages should call (instead of load_controls directly) so
    that live edits made through the Control Drilldown page are reflected
    everywhere in the app for that visitor's session — without ever writing
    back to the CSV on disk. Each browser session gets its own independent
    copy, so one visitor's edits never affect another's, and the underlying
    sample data in the repo is never modified.
    """
    if "controls_df" not in st.session_state:
        st.session_state["controls_df"] = load_controls().copy()
    return st.session_state["controls_df"]


def update_control(control_id: str, updates: dict) -> None:
    """Apply an in-session edit to a single control row."""
    df = get_working_controls()
    idx = df.index[df["control_id"] == control_id]
    if len(idx):
        for key, value in updates.items():
            df.loc[idx, key] = value
        st.session_state["controls_df"] = df


def reset_working_controls() -> None:
    """Discard session edits and restore the original sample dataset."""
    st.session_state["controls_df"] = load_controls().copy()


def has_session_edits() -> bool:
    if "controls_df" not in st.session_state:
        return False
    return not st.session_state["controls_df"].equals(load_controls())


@st.cache_data
def load_crosswalk() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "crosswalk.csv", keep_default_na=False, na_values=[])


def compliance_summary(df: pd.DataFrame) -> dict:
    counts = df["status"].value_counts().to_dict()
    implemented = counts.get("Implemented", 0)
    partial = counts.get("Partially Implemented", 0)
    not_impl = counts.get("Not Implemented", 0)
    na = counts.get("Not Applicable", 0)
    applicable_total = len(df) - na
    weighted = (implemented + 0.5 * partial) / applicable_total if applicable_total else 0
    high_priority_gaps = len(
        df[(df["status"].isin(["Not Implemented", "Partially Implemented"])) & (df["risk"] == "High")]
    )
    today = pd.Timestamp(date.today())
    overdue_evidence = len(df[(df["next_review"] < today) & (df["status"] != "Not Applicable")])
    return {
        "overall_pct": round(weighted * 100, 1),
        "implemented": implemented,
        "partial": partial,
        "not_implemented": not_impl,
        "not_applicable": na,
        "high_priority_gaps": high_priority_gaps,
        "overdue_evidence": overdue_evidence,
        "total": len(df),
    }
