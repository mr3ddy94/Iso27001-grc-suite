import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.data_loader import RISK_COLORS, STATUS_COLORS, THEME_ORDER, load_controls

st.set_page_config(page_title="Control Drilldown", page_icon="🔍", layout="wide")
st.title("🔍 Control Drilldown")
st.caption("Filter and inspect individual ISO/IEC 27001:2022 Annex A controls")

df = load_controls()

# ---- Filters ----
f1, f2, f3, f4 = st.columns(4)
with f1:
    theme_filter = st.multiselect("Theme", THEME_ORDER, default=[])
with f2:
    status_filter = st.multiselect(
        "Status",
        ["Implemented", "Partially Implemented", "Not Implemented", "Not Applicable"],
        default=[],
    )
with f3:
    owner_filter = st.multiselect("Owner", sorted(df["owner"].unique()), default=[])
with f4:
    risk_filter = st.multiselect("Risk", ["High", "Medium", "Low", "N/A"], default=[])

search = st.text_input("Search control ID or requirement text", "")

filtered = df.copy()
if theme_filter:
    filtered = filtered[filtered["theme"].isin(theme_filter)]
if status_filter:
    filtered = filtered[filtered["status"].isin(status_filter)]
if owner_filter:
    filtered = filtered[filtered["owner"].isin(owner_filter)]
if risk_filter:
    filtered = filtered[filtered["risk"].isin(risk_filter)]
if search:
    s = search.lower()
    filtered = filtered[
        filtered["control_id"].str.lower().str.contains(s)
        | filtered["requirement"].str.lower().str.contains(s)
    ]

st.caption(f"Showing {len(filtered)} of {len(df)} controls")

# ---- Table + selection ----
table_col, detail_col = st.columns([1.1, 1.4])

with table_col:
    st.dataframe(
        filtered[["control_id", "requirement", "theme", "status", "owner", "risk"]],
        hide_index=True,
        use_container_width=True,
        height=520,
    )
    options = filtered["control_id"].tolist()
    selected_id = st.selectbox("Select a control to view full detail", options) if options else None

with detail_col:
    if selected_id:
        row = df[df["control_id"] == selected_id].iloc[0]
        status_color = STATUS_COLORS.get(row["status"], "#5A6472")
        risk_color = RISK_COLORS.get(row["risk"], "#5A6472")

        st.markdown(f"### {row['control_id']} — {row['requirement']}")
        badge1, badge2 = st.columns(2)
        with badge1:
            st.markdown(
                f"<span style='background:{status_color}22;color:{status_color};"
                f"padding:4px 10px;border-radius:12px;font-weight:600;'>{row['status']}</span>",
                unsafe_allow_html=True,
            )
        with badge2:
            st.markdown(
                f"<span style='background:{risk_color}22;color:{risk_color};"
                f"padding:4px 10px;border-radius:12px;font-weight:600;'>Risk: {row['risk']}</span>",
                unsafe_allow_html=True,
            )

        st.write("")
        st.markdown(f"**Theme:** {row['theme']}")
        st.markdown(f"**Control Owner:** {row['owner']}")
        st.markdown(f"**Last Review:** {row['last_review'].date()}")
        st.markdown(f"**Next Review:** {row['next_review'].date()}")
        st.markdown("**Evidence**")
        st.info(row["evidence"])
        st.markdown("**Gap**")
        if row["gap"] == "None identified":
            st.success(row["gap"])
        else:
            st.warning(row["gap"])
        st.markdown("**Remediation Action**")
        st.write(row["remediation_action"])
    else:
        st.info("No controls match the current filters.")

st.divider()
st.download_button(
    "⬇️ Export filtered controls (CSV)",
    filtered.to_csv(index=False).encode("utf-8"),
    file_name="iso27001_controls_export.csv",
    mime="text/csv",
)
