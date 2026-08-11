import sys
from pathlib import Path

import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.data_loader import get_working_controls, load_crosswalk

st.set_page_config(page_title="Framework Crosswalk", page_icon="🔗", layout="wide")
st.title("🔗 Framework Crosswalk Tool")
st.caption("Map ISO/IEC 27001:2022 Annex A controls to other security frameworks")

st.info(
    "This is a curated, best-effort thematic mapping built for demonstration purposes — "
    "not a reproduction of any framework owner's official crosswalk. Confidence is labelled "
    "**Strong / Partial / Weak** for each row. Validate against official NIST/CIS/ISO "
    "documentation before using in a real audit.",
    icon="ℹ️",
)

controls = get_working_controls()
crosswalk = load_crosswalk()

available_frameworks = sorted(crosswalk["target_framework"].unique().tolist())

# ---- Framework selectors ----
fA, fB, fC = st.columns(3)
with fA:
    st.markdown("**Framework A** *(base)*")
    st.selectbox("Base framework", ["ISO 27001:2022"], disabled=True, key="fw_a")
with fB:
    st.markdown("**Framework B**")
    default_b = available_frameworks.index("NIST CSF 2.0") if "NIST CSF 2.0" in available_frameworks else 0
    fw_b = st.selectbox("Compare to", available_frameworks, index=default_b, key="fw_b")
with fC:
    st.markdown("**Framework C**")
    remaining = [f for f in available_frameworks if f != fw_b] or available_frameworks
    fw_c = st.selectbox("Compare to", remaining, index=0, key="fw_c")

st.caption(
    f"Currently loaded target frameworks: {', '.join(available_frameworks)}. "
    "Add more (COBIT, PCI DSS, SOC 2, GDPR, DORA, NIS2...) by appending rows to "
    "data/crosswalk.csv — no code changes required."
)

st.divider()

mode = st.radio("View", ["Single control lookup", "Full crosswalk table"], horizontal=True)

if mode == "Single control lookup":
    control_options = controls["control_id"] + " — " + controls["requirement"]
    choice = st.selectbox("Select an ISO 27001 control", control_options.tolist())
    iso_id = choice.split(" — ")[0]
    iso_row = controls[controls["control_id"] == iso_id].iloc[0]

    def mapping_rows(framework):
        return crosswalk[(crosswalk["iso_control_id"] == iso_id) & (crosswalk["target_framework"] == framework)]

    rows_b = mapping_rows(fw_b)
    rows_c = mapping_rows(fw_c)

    st.write("")
    d1, d2, d3 = st.columns([1, 1, 1])
    with d1:
        st.markdown("#### ISO 27001")
        st.markdown(f"**{iso_row['control_id']}**")
        st.write(iso_row["requirement"])
    with d2:
        st.markdown(f"#### {fw_b}")
        if rows_b.empty:
            st.caption("No mapping in current dataset")
        for _, r in rows_b.iterrows():
            st.markdown(f"**{r['target_id']}**")
            st.write(r["target_title"])
    with d3:
        st.markdown(f"#### {fw_c}")
        if rows_c.empty:
            st.caption("No mapping in current dataset")
        for _, r in rows_c.iterrows():
            st.markdown(f"**{r['target_id']}**")
            st.write(r["target_title"])

    if not rows_b.empty:
        target_str = " / ".join(rows_b["target_id"].tolist())
        arrow_c = " → " + "/".join(rows_c["target_id"].tolist()) if not rows_c.empty else ""
        st.markdown(
            f"<div style='text-align:center;font-size:20px;margin:18px 0;'>"
            f"{iso_row['control_id']} → {target_str}{arrow_c}"
            f"</div>",
            unsafe_allow_html=True,
        )
        conf_color = {"Strong": "#1A9E5C", "Partial": "#E0A32C", "Weak": "#D64545"}
        for _, r in rows_b.iterrows():
            c = conf_color.get(r["confidence"], "#5A6472")
            st.markdown(
                f"<div style='text-align:center;'><span style='background:{c}22;color:{c};"
                f"padding:4px 12px;border-radius:12px;font-weight:600;'>"
                f"{fw_b} confidence: {r['confidence']}</span></div>",
                unsafe_allow_html=True,
            )
        st.write("")
        st.markdown("**Mapping rationale**")
        st.write(rows_b.iloc[0]["notes"])

else:
    c1, c2, c3 = st.columns(3)
    with c1:
        fw_filter = st.multiselect("Target framework", available_frameworks, default=[])
    with c2:
        conf_filter = st.multiselect("Confidence", ["Strong", "Partial", "Weak"], default=[])
    with c3:
        search = st.text_input("Search ISO control / requirement / target", "")

    merged = crosswalk.merge(
        controls[["control_id", "requirement"]],
        left_on="iso_control_id", right_on="control_id", how="left",
    )
    view = merged.copy()
    if fw_filter:
        view = view[view["target_framework"].isin(fw_filter)]
    if conf_filter:
        view = view[view["confidence"].isin(conf_filter)]
    if search:
        s = search.lower()
        view = view[
            view["iso_control_id"].str.lower().str.contains(s)
            | view["requirement"].fillna("").str.lower().str.contains(s)
            | view["target_title"].str.lower().str.contains(s)
        ]

    st.caption(f"Showing {len(view)} of {len(merged)} mapped rows")
    st.dataframe(
        view[[
            "iso_control_id", "requirement", "target_framework", "target_id",
            "target_title", "confidence", "notes",
        ]].rename(columns={
            "iso_control_id": "ISO 27001",
            "requirement": "ISO Requirement",
            "target_framework": "Target Framework",
            "target_id": "Target ID",
            "target_title": "Target Title",
            "confidence": "Confidence",
            "notes": "Notes",
        }),
        hide_index=True,
        use_container_width=True,
        height=520,
    )
    st.download_button(
        "⬇️ Export crosswalk (CSV)",
        view.to_csv(index=False).encode("utf-8"),
        file_name="framework_crosswalk_export.csv",
        mime="text/csv",
    )
