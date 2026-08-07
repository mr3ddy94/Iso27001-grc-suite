"""
Generates data/crosswalk.csv — a curated ISO/IEC 27001:2022 (Annex A) <->
NIST CSF 2.0 <-> CIS Controls v8 crosswalk.

STORAGE FORMAT: long/normalized, one row per (iso_control, target_framework,
target_control) mapping:

    iso_control_id, target_framework, target_id, target_title, confidence, notes

This is deliberately normalized rather than wide (one column pair per
framework) so that adding a new framework later — COBIT, PCI DSS, SOC 2,
GDPR, DORA, NIS2 — is just appending more rows with a new target_framework
value, with no schema/column changes and no app code changes needed.

IMPORTANT — sourcing note:
This mapping is a thematic best-effort crosswalk built for a portfolio /
demo project, based on general understanding of overlapping control intent
across the three frameworks. It is NOT a reproduction of any single vendor's
official mapping table (e.g. CIS's or NIST's own published crosswalk docs),
and mapping strength is necessarily approximate — many controls map
many-to-many rather than 1:1. Confidence is labelled Strong / Partial / Weak.

Before relying on this for a real audit, cross-check against:
  - NIST CSF 2.0 reference tool / Informative References
  - CIS Controls v8 "Controls to ISO 27001:2022" mapping documentation
  - Your own control narrative and SoA

Run: python data/generate_crosswalk.py
"""
import csv

# columns: iso_control_id, nist_csf_function, nist_csf_category, cis_control_id,
#          cis_control_title, confidence, notes
ROWS = [
("A.5.1","GV","GV.PO — Policy","CIS 14","Security Awareness and Skills Training","Strong","Top-level ISMS policy governance"),
("A.5.2","GV","GV.RR — Roles, Responsibilities & Authorities","CIS 14","Security Awareness and Skills Training","Strong","Defined security roles/accountability"),
("A.5.3","GV","GV.OC — Organizational Context","CIS 6","Access Control Management","Partial","Segregation of duties supports access governance"),
("A.5.4","GV","GV.RR — Roles, Responsibilities & Authorities","CIS 14","Security Awareness and Skills Training","Partial","Management commitment to security"),
("A.5.5","GV","GV.OC — Organizational Context","CIS 17","Incident Response Management","Partial","Liaison with regulators/law enforcement"),
("A.5.6","ID","ID.RA — Risk Assessment","CIS 17","Incident Response Management","Weak","Threat/industry information sharing"),
("A.5.7","ID","ID.RA — Risk Assessment","CIS 17","Incident Response Management","Strong","Threat intelligence feeds risk assessment"),
("A.5.8","GV","GV.SC — Cybersecurity Supply Chain Risk Mgmt","CIS 16","Application Software Security","Partial","Security embedded in project lifecycle"),
("A.5.9","ID","ID.AM — Asset Management","CIS 1","Inventory and Control of Enterprise Assets","Strong","Core asset inventory control"),
("A.5.9","ID","ID.AM — Asset Management","CIS 2","Inventory and Control of Software Assets","Strong","Software asset inventory"),
("A.5.10","PR","PR.AA — Identity Mgmt, Auth & Access Control","CIS 3","Data Protection","Partial","Acceptable use governs data handling"),
("A.5.11","PR","PR.PS — Platform Security","CIS 1","Inventory and Control of Enterprise Assets","Partial","Asset return on offboarding"),
("A.5.12","ID","ID.AM — Asset Management","CIS 3","Data Protection","Strong","Data classification scheme"),
("A.5.13","ID","ID.AM — Asset Management","CIS 3","Data Protection","Strong","Labelling supports classification"),
("A.5.14","PR","PR.DS — Data Security","CIS 3","Data Protection","Strong","Secure information transfer"),
("A.5.15","PR","PR.AA — Identity Mgmt, Auth & Access Control","CIS 6","Access Control Management","Strong","Core access control policy"),
("A.5.16","PR","PR.AA — Identity Mgmt, Auth & Access Control","CIS 5","Account Management","Strong","Identity lifecycle management"),
("A.5.17","PR","PR.AA — Identity Mgmt, Auth & Access Control","CIS 6","Access Control Management","Strong","Authentication information/credentials"),
("A.5.18","PR","PR.AA — Identity Mgmt, Auth & Access Control","CIS 5","Account Management","Strong","Access rights provisioning/review"),
("A.5.19","GV","GV.SC — Cybersecurity Supply Chain Risk Mgmt","CIS 15","Service Provider Management","Strong","Supplier security requirements"),
("A.5.20","GV","GV.SC — Cybersecurity Supply Chain Risk Mgmt","CIS 15","Service Provider Management","Strong","Contractual security clauses"),
("A.5.21","GV","GV.SC — Cybersecurity Supply Chain Risk Mgmt","CIS 15","Service Provider Management","Strong","ICT supply chain risk"),
("A.5.22","GV","GV.SC — Cybersecurity Supply Chain Risk Mgmt","CIS 15","Service Provider Management","Strong","Ongoing supplier monitoring"),
("A.5.23","PR","PR.PS — Platform Security","CIS 3","Data Protection","Partial","Cloud service security posture"),
("A.5.24","RS","RS.MA — Incident Management","CIS 17","Incident Response Management","Strong","Incident response planning"),
("A.5.25","RS","RS.AN — Incident Analysis","CIS 17","Incident Response Management","Strong","Triage/assessment of events"),
("A.5.26","RS","RS.MA — Incident Management","CIS 17","Incident Response Management","Strong","Active incident response"),
("A.5.27","RC","RC.IM — Improvements","CIS 17","Incident Response Management","Strong","Post-incident lessons learned"),
("A.5.28","RS","RS.AN — Incident Analysis","CIS 17","Incident Response Management","Partial","Forensic evidence collection"),
("A.5.29","RC","RC.RP — Recovery Plan Execution","CIS 11","Data Recovery","Partial","Continuity of security during disruption"),
("A.5.30","RC","RC.RP — Recovery Plan Execution","CIS 11","Data Recovery","Strong","ICT/DR readiness"),
("A.5.31","GV","GV.OC — Organizational Context","CIS 14","Security Awareness and Skills Training","Weak","Legal/regulatory compliance tracking"),
("A.5.32","GV","GV.OC — Organizational Context","CIS 3","Data Protection","Weak","IP rights protection"),
("A.5.33","PR","PR.DS — Data Security","CIS 3","Data Protection","Partial","Records retention/protection"),
("A.5.34","PR","PR.DS — Data Security","CIS 3","Data Protection","Strong","Privacy/PII protection"),
("A.5.35","GV","GV.OV — Oversight","CIS 18","Penetration Testing","Partial","Independent ISMS review"),
("A.5.36","GV","GV.OV — Oversight","CIS 14","Security Awareness and Skills Training","Partial","Policy compliance monitoring"),
("A.5.37","PR","PR.PS — Platform Security","CIS 4","Secure Configuration of Enterprise Assets","Weak","Documented operating procedures"),
("A.6.1","PR","PR.AA — Identity Mgmt, Auth & Access Control","CIS 6","Access Control Management","Partial","Pre-employment screening"),
("A.6.2","GV","GV.RR — Roles, Responsibilities & Authorities","CIS 14","Security Awareness and Skills Training","Weak","Employment T&Cs incl. security"),
("A.6.3","PR","PR.AT — Awareness and Training","CIS 14","Security Awareness and Skills Training","Strong","Security awareness program"),
("A.6.4","GV","GV.RR — Roles, Responsibilities & Authorities","CIS 14","Security Awareness and Skills Training","Weak","Disciplinary process for violations"),
("A.6.5","PR","PR.AA — Identity Mgmt, Auth & Access Control","CIS 5","Account Management","Strong","Deprovisioning on termination"),
("A.6.6","GV","GV.OC — Organizational Context","CIS 14","Security Awareness and Skills Training","Weak","NDAs/confidentiality agreements"),
("A.6.7","PR","PR.PS — Platform Security","CIS 12","Network Infrastructure Management","Partial","Remote working security"),
("A.6.8","DE","DE.AE — Adverse Event Analysis","CIS 17","Incident Response Management","Strong","Employee security event reporting"),
("A.7.1","PR","PR.PS — Platform Security","CIS 12","Network Infrastructure Management","Weak","Physical perimeter security"),
("A.7.2","PR","PR.AA — Identity Mgmt, Auth & Access Control","CIS 6","Access Control Management","Partial","Physical entry controls"),
("A.7.3","PR","PR.PS — Platform Security","CIS 4","Secure Configuration of Enterprise Assets","Weak","Securing offices/facilities"),
("A.7.4","DE","DE.CM — Continuous Monitoring","CIS 13","Network Monitoring and Defense","Weak","Physical security monitoring/CCTV"),
("A.7.5","PR","PR.IR — Technology Infrastructure Resilience","CIS 11","Data Recovery","Weak","Environmental threat protection"),
("A.7.6","PR","PR.PS — Platform Security","CIS 4","Secure Configuration of Enterprise Assets","Weak","Secure-area working practices"),
("A.7.7","PR","PR.AA — Identity Mgmt, Auth & Access Control","CIS 4","Secure Configuration of Enterprise Assets","Partial","Clear desk / clear screen"),
("A.7.8","PR","PR.PS — Platform Security","CIS 1","Inventory and Control of Enterprise Assets","Weak","Equipment siting/protection"),
("A.7.9","PR","PR.PS — Platform Security","CIS 1","Inventory and Control of Enterprise Assets","Partial","Off-premises asset security"),
("A.7.10","PR","PR.DS — Data Security","CIS 3","Data Protection","Strong","Storage media handling"),
("A.7.11","PR","PR.IR — Technology Infrastructure Resilience","CIS 11","Data Recovery","Weak","Supporting utilities/power"),
("A.7.12","PR","PR.PS — Platform Security","CIS 12","Network Infrastructure Management","Weak","Cabling security"),
("A.7.13","PR","PR.PS — Platform Security","CIS 4","Secure Configuration of Enterprise Assets","Weak","Equipment maintenance"),
("A.7.14","PR","PR.DS — Data Security","CIS 3","Data Protection","Strong","Secure disposal/reuse of equipment"),
("A.8.1","PR","PR.PS — Platform Security","CIS 1","Inventory and Control of Enterprise Assets","Strong","Endpoint device management"),
("A.8.2","PR","PR.AA — Identity Mgmt, Auth & Access Control","CIS 5","Account Management","Strong","Privileged access management"),
("A.8.3","PR","PR.AA — Identity Mgmt, Auth & Access Control","CIS 3","Data Protection","Strong","Access restriction enforcement"),
("A.8.4","PR","PR.AA — Identity Mgmt, Auth & Access Control","CIS 16","Application Software Security","Strong","Source code access control"),
("A.8.5","PR","PR.AA — Identity Mgmt, Auth & Access Control","CIS 6","Access Control Management","Strong","MFA/secure authentication"),
("A.8.6","PR","PR.IR — Technology Infrastructure Resilience","CIS 12","Network Infrastructure Management","Weak","Capacity management"),
("A.8.7","DE","DE.CM — Continuous Monitoring","CIS 10","Malware Defenses","Strong","Anti-malware controls"),
("A.8.8","ID","ID.RA — Risk Assessment","CIS 7","Continuous Vulnerability Management","Strong","Vulnerability management"),
("A.8.9","PR","PR.PS — Platform Security","CIS 4","Secure Configuration of Enterprise Assets","Strong","Configuration management/hardening"),
("A.8.10","PR","PR.DS — Data Security","CIS 3","Data Protection","Strong","Secure information deletion"),
("A.8.11","PR","PR.DS — Data Security","CIS 3","Data Protection","Strong","Data masking"),
("A.8.12","PR","PR.DS — Data Security","CIS 3","Data Protection","Strong","Data leakage prevention"),
("A.8.13","PR","PR.DS — Data Security","CIS 11","Data Recovery","Strong","Backup management"),
("A.8.14","PR","PR.IR — Technology Infrastructure Resilience","CIS 11","Data Recovery","Strong","Processing facility redundancy"),
("A.8.15","DE","DE.CM — Continuous Monitoring","CIS 8","Audit Log Management","Strong","Security logging"),
("A.8.16","DE","DE.CM — Continuous Monitoring","CIS 13","Network Monitoring and Defense","Strong","SOC monitoring activities"),
("A.8.17","DE","DE.CM — Continuous Monitoring","CIS 8","Audit Log Management","Partial","Clock synchronization for log integrity"),
("A.8.18","PR","PR.AA — Identity Mgmt, Auth & Access Control","CIS 5","Account Management","Partial","Privileged utility program control"),
("A.8.19","PR","PR.PS — Platform Security","CIS 2","Inventory and Control of Software Assets","Strong","Controlled software installation"),
("A.8.20","PR","PR.IR — Technology Infrastructure Resilience","CIS 12","Network Infrastructure Management","Strong","Network security architecture"),
("A.8.21","PR","PR.IR — Technology Infrastructure Resilience","CIS 12","Network Infrastructure Management","Strong","Security of network services"),
("A.8.22","PR","PR.IR — Technology Infrastructure Resilience","CIS 12","Network Infrastructure Management","Strong","Network segmentation"),
("A.8.23","DE","DE.CM — Continuous Monitoring","CIS 9","Email and Web Browser Protections","Strong","Web filtering"),
("A.8.24","PR","PR.DS — Data Security","CIS 3","Data Protection","Strong","Cryptography/encryption"),
("A.8.25","PR","PR.PS — Platform Security","CIS 16","Application Software Security","Strong","Secure development lifecycle"),
("A.8.26","PR","PR.PS — Platform Security","CIS 16","Application Software Security","Strong","Application security requirements"),
("A.8.27","PR","PR.PS — Platform Security","CIS 16","Application Software Security","Strong","Secure architecture principles"),
("A.8.28","PR","PR.PS — Platform Security","CIS 16","Application Software Security","Strong","Secure coding practices"),
("A.8.29","ID","ID.RA — Risk Assessment","CIS 18","Penetration Testing","Strong","Security testing (SAST/DAST/pen test)"),
("A.8.30","GV","GV.SC — Cybersecurity Supply Chain Risk Mgmt","CIS 16","Application Software Security","Partial","Outsourced development oversight"),
("A.8.31","PR","PR.PS — Platform Security","CIS 4","Secure Configuration of Enterprise Assets","Strong","Dev/test/prod separation"),
("A.8.32","PR","PR.PS — Platform Security","CIS 4","Secure Configuration of Enterprise Assets","Strong","Change management"),
("A.8.33","PR","PR.DS — Data Security","CIS 3","Data Protection","Partial","Test data protection"),
("A.8.34","ID","ID.RA — Risk Assessment","CIS 18","Penetration Testing","Partial","Protecting systems during audit testing"),
]

def main():
    fieldnames = [
        "iso_control_id", "target_framework", "target_id", "target_title",
        "confidence", "notes",
    ]
    long_rows = []
    for iso_id, nist_fn, nist_cat, cis_id, cis_title, confidence, notes in ROWS:
        long_rows.append({
            "iso_control_id": iso_id,
            "target_framework": "NIST CSF 2.0",
            "target_id": nist_fn,
            "target_title": nist_cat,
            "confidence": confidence,
            "notes": notes,
        })
        long_rows.append({
            "iso_control_id": iso_id,
            "target_framework": "CIS Controls v8",
            "target_id": cis_id,
            "target_title": cis_title,
            "confidence": confidence,
            "notes": notes,
        })

    with open("data/crosswalk.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(long_rows)
    print(f"Wrote {len(long_rows)} crosswalk rows (long format) to data/crosswalk.csv")
    print(f"Source mappings: {len(ROWS)} ISO controls x 2 target frameworks")

if __name__ == "__main__":
    main()
