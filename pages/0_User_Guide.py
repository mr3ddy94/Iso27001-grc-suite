import streamlit as st

st.set_page_config(page_title="User Guide", page_icon="📖", layout="wide")
st.title("📖 User Guide")
st.caption("A 2-minute orientation for anyone testing this project")

st.markdown(
    """
This is a portfolio project built by **Edwin Acquah** — a mini GRC
(Governance, Risk & Compliance) management system covering ISO/IEC
27001:2022 compliance tracking and cross-framework mapping. It's designed
to actually be interacted with, not just screenshotted.
"""
)

st.info(
    "**Nothing you do here can break anything.** Edits are stored only in "
    "your own browser session — they never touch the underlying dataset, "
    "the GitHub repo, or any other visitor's view. Refresh the page or "
    "click **Reset to original sample data** in the sidebar at any time to "
    "start clean.",
    icon="🛡️",
)

st.divider()
st.subheader("What's in the app")

g1, g2, g3 = st.columns(3)
with g1:
    st.markdown("#### 🛡️ Dashboard")
    st.write(
        "Landing page. Overall compliance %, status breakdown, high-priority "
        "gaps and overdue evidence, plus charts by Annex A theme "
        "(Organizational / People / Physical / Technological)."
    )
with g2:
    st.markdown("#### 🔍 Control Drilldown")
    st.write(
        "All 93 ISO 27001:2022 Annex A controls. Filter by theme, status, "
        "owner, or risk. Select any control to see full detail — "
        "**and edit it live** (see below)."
    )
with g3:
    st.markdown("#### 🔗 Framework Crosswalk")
    st.write(
        "Maps each ISO control to its closest NIST CSF 2.0 and CIS "
        "Controls v8 equivalent, with a confidence rating and rationale "
        "for each mapping."
    )

st.divider()
st.subheader("🧪 Try the interactive part (recommended, ~30 seconds)")

st.markdown(
    """
1. Go to **Control Drilldown** in the sidebar.
2. Pick any control from the table — for example one that's currently
   *Implemented*.
3. Expand **✏️ Edit this control (live demo)**.
4. Change its **Status** to *Not Implemented* and **Risk** to *High*, then
   click **Save changes**.
5. Go back to the **Dashboard**. Notice:
   - Overall compliance % drops
   - The status counts and donut chart update
   - The control now appears in the **High Priority Gaps** table
6. When you're done, use **↩️ Reset to original sample data** in the
   sidebar (visible on the Dashboard or Control Drilldown page) to restore
   the sample dataset.
"""
)

st.divider()
st.subheader("A note on the data")
st.write(
    "Control statuses, owners, evidence, and review dates are fictional "
    "sample data generated for this demo — not a real ISMS record. The "
    "framework crosswalk is a curated, best-effort thematic mapping built "
    "for demonstration purposes, labelled with a confidence rating per "
    "row, and is not a reproduction of any framework owner's official "
    "mapping document."
)

st.divider()
st.subheader("Under the hood")
st.write(
    "Built with Streamlit, Pandas, and Plotly. Source code, the data "
    "generation scripts, and a CI pipeline that validates the dataset and "
    "smoke-tests the app on every push are all in the GitHub repo linked "
    "from the project README."
)

st.page_link("app.py", label="⬅️ Back to Dashboard", icon="🛡️")
