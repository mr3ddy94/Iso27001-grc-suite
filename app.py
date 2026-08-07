import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent))
from utils.data_loader import (
    STATUS_COLORS,
    THEME_ORDER,
    compliance_summary,
    load_controls,
)

st.set_page_config(
    page_title="ISO 27001 Compliance Dashboard",
    page_icon="🛡️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .metric-card {
        background: #F7F8FA;
        border: 1px solid #E4E7EB;
        border-radius: 10px;
        padding: 18px 20px;
        text-align: center;
    }
    .metric-card h2 { margin: 4px 0 0 0; font-size: 30px; }
    .metric-card p { margin: 0; color: #5A6472; font-size: 13px; text-transform: uppercase; letter-spacing: .04em; }
    </style>
    """,
    unsafe_allow_html=True,
)

df = load_controls()
summary = compliance_summary(df)

st.title("🛡️ ISO/IEC 27001:2022 Compliance Dashboard")
st.caption("Sample GRC portfolio project — Annex A controls (93), mock ISMS data")

# ---- Top metrics row ----
c1, c2, c3 = st.columns([1.3, 1, 1])
with c1:
    st.markdown(
        f"""<div class="metric-card"><p>Overall Compliance</p>
        <h2 style="color:#1A6FA8">{summary['overall_pct']}%</h2></div>""",
        unsafe_allow_html=True,
    )
with c2:
    st.markdown(
        f"""<div class="metric-card"><p>High Priority Gaps</p>
        <h2 style="color:#D64545">{summary['high_priority_gaps']}</h2></div>""",
        unsafe_allow_html=True,
    )
with c3:
    st.markdown(
        f"""<div class="metric-card"><p>Overdue Evidence</p>
        <h2 style="color:#E0A32C">{summary['overdue_evidence']}</h2></div>""",
        unsafe_allow_html=True,
    )

st.write("")

# ---- Status breakdown row ----
s1, s2, s3, s4 = st.columns(4)
status_map = [
    ("Implemented", summary["implemented"], s1),
    ("Partially Implemented", summary["partial"], s2),
    ("Not Implemented", summary["not_implemented"], s3),
    ("Not Applicable", summary["not_applicable"], s4),
]
for label, val, col in status_map:
    with col:
        st.markdown(
            f"""<div class="metric-card"><p>{label}</p>
            <h2 style="color:{STATUS_COLORS[label]}">{val}</h2></div>""",
            unsafe_allow_html=True,
        )

st.write("")
st.divider()

# ---- Charts ----
left, right = st.columns([1, 1.4])

with left:
    st.subheader("Status Breakdown")
    status_counts = df["status"].value_counts().reindex(
        ["Implemented", "Partially Implemented", "Not Implemented", "Not Applicable"]
    ).fillna(0)
    fig = go.Figure(
        go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=0.55,
            marker=dict(colors=[STATUS_COLORS[s] for s in status_counts.index]),
            textinfo="value+percent",
        )
    )
    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=340, showlegend=True,
                       legend=dict(orientation="h", y=-0.15))
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.subheader("Compliance by Theme")
    theme_status = (
        df.groupby(["theme", "status"], observed=True).size().reset_index(name="count")
    )
    fig2 = go.Figure()
    for status in ["Implemented", "Partially Implemented", "Not Implemented", "Not Applicable"]:
        sub = theme_status[theme_status["status"] == status]
        fig2.add_bar(
            x=THEME_ORDER,
            y=[sub[sub["theme"] == t]["count"].sum() for t in THEME_ORDER],
            name=status,
            marker_color=STATUS_COLORS[status],
        )
    fig2.update_layout(
        barmode="stack", height=340, margin=dict(t=10, b=10, l=10, r=10),
        legend=dict(orientation="h", y=-0.2),
    )
    st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ---- Attention lists ----
a1, a2 = st.columns(2)
with a1:
    st.subheader("🔴 High Priority Gaps")
    gaps = df[
        (df["status"].isin(["Not Implemented", "Partially Implemented"])) & (df["risk"] == "High")
    ][["control_id", "requirement", "status", "owner"]]
    if gaps.empty:
        st.success("No high-priority gaps outstanding.")
    else:
        st.dataframe(gaps, hide_index=True, use_container_width=True)

with a2:
    st.subheader("🟠 Overdue Evidence Review")
    today = pd.Timestamp.today()
    overdue = df[(df["next_review"] < today) & (df["status"] != "Not Applicable")][
        ["control_id", "requirement", "owner", "next_review"]
    ].sort_values("next_review")
    overdue["next_review"] = overdue["next_review"].dt.date
    if overdue.empty:
        st.success("No overdue evidence reviews.")
    else:
        st.dataframe(overdue, hide_index=True, use_container_width=True)

st.divider()
st.page_link("pages/1_Control_Drilldown.py", label="➡️ Drill into individual controls", icon="🔍")
st.page_link("pages/2_Framework_Crosswalk.py", label="➡️ Explore the Framework Crosswalk tool", icon="🔗")

st.caption(
    "Demo dataset · Control structure follows ISO/IEC 27001:2022 Annex A · "
    "Status, owners, dates and evidence are fictional sample data for portfolio purposes."
)
