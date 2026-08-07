"""
Generates data/controls.csv — the full ISO/IEC 27001:2022 Annex A control set
(93 controls across the 4 themes) populated with representative mock GRC data
(status, owner, evidence, review dates, risk, gaps, remediation).

This is SAMPLE / DEMO data for a portfolio project. Control IDs and titles are
the real ISO/IEC 27001:2022 Annex A structure; status, owners, evidence and
dates are fictional and generated deterministically (seeded) so the dashboard
numbers are stable and reproducible.

Run: python data/generate_controls.py
"""
import csv
import random
from datetime import date, timedelta

random.seed(42)
TODAY = date(2026, 8, 5)

# (control_id, theme, requirement) -- ISO/IEC 27001:2022 Annex A, 93 controls
CONTROLS = [
    # A.5 Organizational controls (37)
    ("A.5.1", "Organizational", "Policies for information security"),
    ("A.5.2", "Organizational", "Information security roles and responsibilities"),
    ("A.5.3", "Organizational", "Segregation of duties"),
    ("A.5.4", "Organizational", "Management responsibilities"),
    ("A.5.5", "Organizational", "Contact with authorities"),
    ("A.5.6", "Organizational", "Contact with special interest groups"),
    ("A.5.7", "Organizational", "Threat intelligence"),
    ("A.5.8", "Organizational", "Information security in project management"),
    ("A.5.9", "Organizational", "Inventory of information and other associated assets"),
    ("A.5.10", "Organizational", "Acceptable use of information and other associated assets"),
    ("A.5.11", "Organizational", "Return of assets"),
    ("A.5.12", "Organizational", "Classification of information"),
    ("A.5.13", "Organizational", "Labelling of information"),
    ("A.5.14", "Organizational", "Information transfer"),
    ("A.5.15", "Organizational", "Access control"),
    ("A.5.16", "Organizational", "Identity management"),
    ("A.5.17", "Organizational", "Authentication information"),
    ("A.5.18", "Organizational", "Access rights"),
    ("A.5.19", "Organizational", "Information security in supplier relationships"),
    ("A.5.20", "Organizational", "Addressing information security within supplier agreements"),
    ("A.5.21", "Organizational", "Managing information security in the ICT supply chain"),
    ("A.5.22", "Organizational", "Monitoring, review and change management of supplier services"),
    ("A.5.23", "Organizational", "Information security for use of cloud services"),
    ("A.5.24", "Organizational", "Information security incident management planning and preparation"),
    ("A.5.25", "Organizational", "Assessment and decision on information security events"),
    ("A.5.26", "Organizational", "Response to information security incidents"),
    ("A.5.27", "Organizational", "Learning from information security incidents"),
    ("A.5.28", "Organizational", "Collection of evidence"),
    ("A.5.29", "Organizational", "Information security during disruption"),
    ("A.5.30", "Organizational", "ICT readiness for business continuity"),
    ("A.5.31", "Organizational", "Legal, statutory, regulatory and contractual requirements"),
    ("A.5.32", "Organizational", "Intellectual property rights"),
    ("A.5.33", "Organizational", "Protection of records"),
    ("A.5.34", "Organizational", "Privacy and protection of PII"),
    ("A.5.35", "Organizational", "Independent review of information security"),
    ("A.5.36", "Organizational", "Compliance with policies, rules and standards for information security"),
    ("A.5.37", "Organizational", "Documented operating procedures"),
    # A.6 People controls (8)
    ("A.6.1", "People", "Screening"),
    ("A.6.2", "People", "Terms and conditions of employment"),
    ("A.6.3", "People", "Information security awareness, education and training"),
    ("A.6.4", "People", "Disciplinary process"),
    ("A.6.5", "People", "Responsibilities after termination or change of employment"),
    ("A.6.6", "People", "Confidentiality or non-disclosure agreements"),
    ("A.6.7", "People", "Remote working"),
    ("A.6.8", "People", "Information security event reporting"),
    # A.7 Physical controls (14)
    ("A.7.1", "Physical", "Physical security perimeters"),
    ("A.7.2", "Physical", "Physical entry"),
    ("A.7.3", "Physical", "Securing offices, rooms and facilities"),
    ("A.7.4", "Physical", "Physical security monitoring"),
    ("A.7.5", "Physical", "Protecting against physical and environmental threats"),
    ("A.7.6", "Physical", "Working in secure areas"),
    ("A.7.7", "Physical", "Clear desk and clear screen"),
    ("A.7.8", "Physical", "Equipment siting and protection"),
    ("A.7.9", "Physical", "Security of assets off-premises"),
    ("A.7.10", "Physical", "Storage media"),
    ("A.7.11", "Physical", "Supporting utilities"),
    ("A.7.12", "Physical", "Cabling security"),
    ("A.7.13", "Physical", "Equipment maintenance"),
    ("A.7.14", "Physical", "Secure disposal or re-use of equipment"),
    # A.8 Technological controls (34)
    ("A.8.1", "Technological", "User endpoint devices"),
    ("A.8.2", "Technological", "Privileged access rights"),
    ("A.8.3", "Technological", "Information access restriction"),
    ("A.8.4", "Technological", "Access to source code"),
    ("A.8.5", "Technological", "Secure authentication"),
    ("A.8.6", "Technological", "Capacity management"),
    ("A.8.7", "Technological", "Protection against malware"),
    ("A.8.8", "Technological", "Management of technical vulnerabilities"),
    ("A.8.9", "Technological", "Configuration management"),
    ("A.8.10", "Technological", "Information deletion"),
    ("A.8.11", "Technological", "Data masking"),
    ("A.8.12", "Technological", "Data leakage prevention"),
    ("A.8.13", "Technological", "Information backup"),
    ("A.8.14", "Technological", "Redundancy of information processing facilities"),
    ("A.8.15", "Technological", "Logging"),
    ("A.8.16", "Technological", "Monitoring activities"),
    ("A.8.17", "Technological", "Clock synchronization"),
    ("A.8.18", "Technological", "Use of privileged utility programs"),
    ("A.8.19", "Technological", "Installation of software on operational systems"),
    ("A.8.20", "Technological", "Networks security"),
    ("A.8.21", "Technological", "Security of network services"),
    ("A.8.22", "Technological", "Segregation of networks"),
    ("A.8.23", "Technological", "Web filtering"),
    ("A.8.24", "Technological", "Use of cryptography"),
    ("A.8.25", "Technological", "Secure development life cycle"),
    ("A.8.26", "Technological", "Application security requirements"),
    ("A.8.27", "Technological", "Secure system architecture and engineering principles"),
    ("A.8.28", "Technological", "Secure coding"),
    ("A.8.29", "Technological", "Security testing in development and acceptance"),
    ("A.8.30", "Technological", "Outsourced development"),
    ("A.8.31", "Technological", "Separation of development, test and production environments"),
    ("A.8.32", "Technological", "Change management"),
    ("A.8.33", "Technological", "Test information"),
    ("A.8.34", "Technological", "Protection of information systems during audit testing"),
]

assert len(CONTROLS) == 93, len(CONTROLS)

OWNERS = [
    "CISO", "Head of IT Operations", "SOC Manager", "Compliance Manager",
    "HR Director", "Facilities Manager", "Head of Engineering",
    "IAM Lead", "Network Engineering Lead", "DPO", "Procurement Lead",
    "Business Continuity Manager", "Application Security Lead",
]

RISK_LEVELS = ["Low", "Medium", "High"]

GAP_TEMPLATES = {
    "Partially Implemented": [
        "Control is defined but not consistently enforced across all business units.",
        "Policy exists but supporting procedure/tooling is not fully rolled out.",
        "Implemented for core systems only; coverage gap on legacy/third-party systems.",
        "Manual process in place; lacks automation and consistent monitoring.",
        "Control operating but evidence collection is ad hoc rather than scheduled.",
    ],
    "Not Implemented": [
        "No formal control currently in place; identified during internal audit.",
        "Requirement acknowledged but not yet resourced or scheduled.",
        "Previously informal practice; no documented control or ownership assigned.",
        "Dependent on a tooling/platform decision not yet finalized.",
    ],
}

REMEDIATION_TEMPLATES = {
    "Partially Implemented": [
        "Extend control coverage to remaining systems and formalize monitoring cadence.",
        "Automate evidence collection and assign quarterly control-owner attestation.",
        "Close tooling gap and align procedure documentation with actual practice.",
        "Run a coverage audit and remediate exceptions within next review cycle.",
    ],
    "Not Implemented": [
        "Assign control owner, draft procedure, and target implementation next quarter.",
        "Raise as remediation item in ISMS improvement register with target date.",
        "Procure/configure required tooling and pilot before full rollout.",
        "Escalate to management review for resourcing and prioritization.",
    ],
}

EVIDENCE_BY_STATUS = {
    "Implemented": [
        "Policy document + approval record in document management system",
        "Signed procedure, sample logs, and quarterly attestation on file",
        "System configuration export + change log reference",
        "Training completion records (LMS report)",
        "Audit trail export from monitoring platform",
        "Signed contracts/DPAs on file with supplier register reference",
    ],
    "Partially Implemented": [
        "Policy in place; enforcement evidence incomplete for all business units",
        "Partial log coverage; automated alerting not yet configured",
        "Procedure drafted, pending sign-off from control owner",
        "Evidence exists for core environment only",
    ],
    "Not Implemented": [
        "No evidence available",
        "N/A — control not yet operational",
    ],
    "Not Applicable": [
        "Justification on file in Statement of Applicability (SoA)",
    ],
}

def random_date(start_days_ago, end_days_ago):
    d = random.randint(end_days_ago, start_days_ago)
    return TODAY - timedelta(days=d)

def build_row(control_id, theme, requirement, status):
    owner = random.choice(OWNERS)
    last_review = random_date(400, 20)
    # cadence: annual review for most, semi-annual for high-touch technical controls
    cadence_days = 365 if theme in ("Organizational", "People") else random.choice([180, 365])
    next_review = last_review + timedelta(days=cadence_days)

    if status == "Not Applicable":
        risk = "N/A"
        evidence = random.choice(EVIDENCE_BY_STATUS["Not Applicable"])
        gap = "Not applicable — excluded via Statement of Applicability"
        remediation = "None required"
    else:
        evidence = random.choice(EVIDENCE_BY_STATUS[status])
        if status == "Implemented":
            risk = random.choices(RISK_LEVELS, weights=[0.6, 0.3, 0.1])[0]
            gap = "None identified"
            remediation = "Maintain control; continue scheduled review cadence"
        else:
            risk = random.choices(RISK_LEVELS, weights=[0.15, 0.35, 0.5])[0]
            gap = random.choice(GAP_TEMPLATES[status])
            remediation = random.choice(REMEDIATION_TEMPLATES[status])

    return {
        "control_id": control_id,
        "theme": theme,
        "requirement": requirement,
        "status": status,
        "owner": owner,
        "evidence": evidence,
        "last_review": last_review.isoformat(),
        "next_review": next_review.isoformat(),
        "risk": risk,
        "gap": gap,
        "remediation_action": remediation,
    }

def main():
    # Target distribution tuned to land close to the ~74% weighted-compliance
    # example: Implemented + 0.5*Partial, over (total - Not Applicable).
    n_total = len(CONTROLS)
    n_na = 4
    n_not_impl = 11
    n_partial = 25
    n_impl = n_total - n_na - n_not_impl - n_partial  # 53

    statuses = (
        ["Implemented"] * n_impl
        + ["Partially Implemented"] * n_partial
        + ["Not Implemented"] * n_not_impl
        + ["Not Applicable"] * n_na
    )
    random.shuffle(statuses)

    rows = []
    for (cid, theme, req), status in zip(CONTROLS, statuses):
        rows.append(build_row(cid, theme, req, status))

    fieldnames = [
        "control_id", "theme", "requirement", "status", "owner", "evidence",
        "last_review", "next_review", "risk", "gap", "remediation_action",
    ]
    with open("data/controls.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} controls to data/controls.csv")
    print(f"Implemented={n_impl} Partial={n_partial} NotImpl={n_not_impl} N/A={n_na}")
    weighted = (n_impl + 0.5 * n_partial) / (n_total - n_na)
    print(f"Approx weighted compliance: {weighted*100:.1f}%")

if __name__ == "__main__":
    main()
