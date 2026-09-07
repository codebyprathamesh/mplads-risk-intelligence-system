# MPLADS Risk Intelligence System

**A triage support tool for reviewing MPLADS public works data — built for Smart India Hackathon 2026 (Problem Statement SIH26102), Ministry of Statistics and Programme Implementation (MoSPI).**

> ⚠️ This system does not detect fraud or replace human investigation. It helps government officers identify which MPLADS works need attention first, so limited review capacity is spent where it matters most.

---

## The Problem

The Members of Parliament Local Area Development Scheme (MPLADS) generates lakhs of public works records every year across constituencies. Officers reviewing this data manually have no way to prioritize — every work looks the same until someone opens the file.

This system processes over **100,000 works records** from the eSAKSHI portal and surfaces a ranked, explainable risk view so reviewers know where to look first.

---

## What It Does

- **Risk Scoring Engine** — A transparent, rule-based scoring system that flags works against known MPLADS scheme guidelines (e.g. sanction and completion timelines, cost outliers, missing documentation). Every point on every score is traceable to a plain-language reason — no black-box output.
- **Risk Tiers** — Works are grouped into No Risk / Low / Medium / High / Critical tiers, calibrated against a fixed scale so the system doesn't need recalibration as data grows year over year.
- **Anomaly Detection** — An unsupervised ML layer (Isolation Forest) flags statistically unusual works that rule-based scoring alone might miss.
- **Duplicate/Template Detection** — Text-similarity analysis flags works with near-identical descriptions, surfaced for human review rather than treated as automatic fraud signals.
- **Interactive Dashboard** — A Streamlit app for exploring risk distribution, drilling into the highest-risk works, inspecting anomalies, and filtering geographically.

🔗 **Live demo:** [mplads-risk-intelligence-system.streamlit.app](https://mplads-risk-intelligence-system.streamlit.app/)

---

## Why This Approach

Most "AI for governance" tools either overpromise (claiming to detect fraud outright) or are too opaque for an officer to trust and act on. This system is built around two constraints instead:

1. **Explainability first.** Every risk point ties back to a named rule someone can check. If a work scores high, an officer can see exactly why in plain language.
2. **Human-in-the-loop by design.** Flags — including duplicates and anomalies — are framed as "review this" signals, not verdicts. The system narrows the search space; people make the call.

---

## Tech Stack

| Layer | Tools |
|---|---|
| Data pipeline | Python, pandas |
| Risk scoring | Custom rule-based engine |
| Anomaly detection | scikit-learn (Isolation Forest) |
| Duplicate detection | TF-IDF + cosine similarity |
| Dashboard | Streamlit, Plotly |
| Data source | eSAKSHI API (MoSPI) |

**Scope note:** Currently covers Lok Sabha constituencies; the pipeline schema is compatible with future Rajya Sabha extension.

---

## Team

Built by a 6-member team for SIH 2026:
- ML / Data Pipeline & Presentation
- Dashboard Development
- Manual Data Validation
- Data Quality Documentation
- Research Support
- Presentation & Demo Design

---

## Status

This project was built and presented for the SIH 2026 internal round.

---

