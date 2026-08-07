# ISO 27001 GRC Suite

A mini compliance management system combining an **ISO/IEC 27001:2022 Compliance
Dashboard** with a **Framework Crosswalk Tool** (ISO 27001 ↔ NIST CSF 2.0 ↔ CIS
Controls v8), built as a portfolio project with Streamlit.

**Live demo:** _add your Streamlit Community Cloud URL here once deployed_

![Python](https://img.shields.io/badge/python-3.11-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.37-red)
![License](https://img.shields.io/badge/license-MIT-green)
[![CI](https://github.com/<your-username>/iso27001-grc-suite/actions/workflows/ci.yml/badge.svg)](https://github.com/<your-username>/iso27001-grc-suite/actions/workflows/ci.yml)

---

## What it does

### 1. Compliance Dashboard (`app.py`)
- Overall weighted compliance % (Implemented + ½×Partial, over applicable controls)
- Status breakdown: Implemented / Partially Implemented / Not Implemented / Not Applicable
- High priority gaps and overdue evidence review counters
- Donut chart of status mix + stacked bar of compliance by Annex A theme
  (Organizational / People / Physical / Technological)
- "Needs attention" tables: high-risk gaps, overdue reviews

### 2. Control Drilldown (`pages/1_Control_Drilldown.py`)
Filterable register of all **93 ISO/IEC 27001:2022 Annex A controls**. For each
control:

| Field | |
|---|---|
| Control ID | e.g. `A.8.7` |
| Requirement | Control title/description |
| Status | Implemented / Partially Implemented / Not Implemented / Not Applicable |
| Control Owner | |
| Evidence | |
| Last Review / Next Review | |
| Risk | High / Medium / Low |
| Gap | |
| Remediation Action | |

Filter by theme, status, owner, risk, or free-text search; export the filtered
view to CSV.

### 3. Framework Crosswalk Tool (`pages/2_Framework_Crosswalk.py`)
Maps each ISO 27001 Annex A control to its closest **NIST CSF 2.0** function/category
and **CIS Controls v8** control, e.g.:

```
ISO 27001 A.5.15  →  NIST PR.AA  →  CIS Control 6
```

Framework A is fixed as ISO 27001 (the anchor); Framework B and C are chosen
from dropdowns populated dynamically from whatever target frameworks exist in
the data — so the picker doesn't need code changes as more frameworks are added.

Two views: a single-control lookup (with mapping rationale + confidence rating)
and a full searchable/exportable crosswalk table.

**Data format:** `data/crosswalk.csv` is stored **normalized/long**, one row per
`(iso_control_id, target_framework, target_id)` mapping, rather than one column
pair per framework. That means adding COBIT, PCI DSS, SOC 2, GDPR, DORA, or
NIS2 later is just appending rows with a new `target_framework` value — no
schema change and no app code change required.

> **Sourcing note:** the crosswalk is a curated, thematic best-effort mapping
> built for this project — not a reproduction of any framework owner's official
> mapping document. Each row is labelled with a confidence rating
> (**Strong / Partial / Weak**). Treat it as a study/demo aid and validate
> against the official NIST CSF Informative References and CIS Controls v8
> mapping documentation before relying on it for a real audit or SoA.

---

## Tech stack

- **Streamlit** (multi-page app) — UI
- **Pandas** — data handling
- **Plotly** — charts
- Data stored as version-controlled CSVs (`data/controls.csv`, `data/crosswalk.csv`),
  generated reproducibly by the scripts in `data/`

## Project structure

```
iso27001-grc-suite/
├── app.py                          # Dashboard (entry point)
├── pages/
│   ├── 1_Control_Drilldown.py
│   └── 2_Framework_Crosswalk.py
├── utils/
│   └── data_loader.py              # shared data loading + metrics
├── data/
│   ├── controls.csv                # 93 Annex A controls, mock GRC data
│   ├── crosswalk.csv               # ISO -> {NIST CSF, CIS Controls v8}, long format
│   ├── generate_controls.py        # reproducible generator (seeded)
│   ├── generate_crosswalk.py       # curated crosswalk generator
│   └── validate_data.py            # schema/integrity checks, used by CI
├── .github/workflows/ci.yml        # lint + data validation + smoke test on push/PR
├── .streamlit/config.toml          # theme
├── requirements.txt
└── README.md
```

## Run locally

```bash
git clone https://github.com/<your-username>/iso27001-grc-suite.git
cd iso27001-grc-suite
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Regenerate the sample data at any time with:

```bash
python data/generate_controls.py
python data/generate_crosswalk.py
```

Validate data integrity (also runs in CI on every push/PR):

```bash
python data/validate_data.py
```

## Roadmap / extension ideas

- [ ] Add COBIT, PCI DSS, SOC 2, GDPR, DORA, NIS2 to the crosswalk
      (append rows to `data/crosswalk.csv` with a new `target_framework` value)
- [ ] Persist control edits (SQLite/Supabase) instead of static CSV
- [ ] Auth + multi-tenant support for real ISMS use
- [ ] Evidence file upload per control
- [ ] Statement of Applicability (SoA) export as a formatted Word/PDF doc
- [ ] Trend view: compliance % over time (audit history)

## Disclaimer

This is a **portfolio/demo project**. Control statuses, owners, evidence, and
dates in `data/controls.csv` are fictional sample data, not a real ISMS record.
The crosswalk mappings are approximate and should be independently verified
before use in a compliance program. ISO/IEC 27001:2022 is a trademarked
standard of ISO/IEC — this project references its public Annex A control
structure for educational purposes and is not affiliated with or endorsed by
ISO, NIST, or CIS.

## License

MIT — see [LICENSE](LICENSE).
