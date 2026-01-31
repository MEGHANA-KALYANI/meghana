# 🛡 SOC Artifact Analysis Dashboard

A SOC-style interactive dashboard built using **Streamlit** to analyze host forensic artifacts and identify security risks related to **persistence mechanisms, EDR gaps, browser compromise, and collector integrity**.

This project simulates how a blue team analyst evaluates endpoint artifacts during an incident response or security audit.

---

## 🎯 Objectives

The dashboard answers the following security questions:

- **Any persistence hooks?**  
  (Scheduled tasks, auto-start services)

- **Was EDR absent or tampered?**  
  (Detection of common endpoint security products)

- **Browser-based compromise or data exfiltration?**  
  (Cookies, tokens, credential artifacts)

- **Collector integrity and completeness?**  
  (Errors, metadata availability)

---

## 🗂 Project Structure

```
├── sgui.py
├── app.py                        # Streamlit SOC dashboard
├── data/
├── analysis_reports/            # Generated per-artifact reports
└── README.md
```

--

## 🎯 Risk Scoring & Severity

Risk score range: 0–100

Severity levels:

LOW (< 40)

MEDIUM (40–69)

HIGH (≥ 70)

Risk scoring is explainable and derived from artifact-specific indicators.

--

## 🎯 MITRE ATT&CK Mapping

Each artifact is mapped to relevant MITRE ATT&CK techniques, such as:

T1053 – Scheduled Task

T1543 – Create or Modify System Process

T1562 – Impair Defenses

T1056 – Input Capture

This helps align findings with industry-standard adversary techniques.

--

## 📊 Dashboard Features

🎯 Risk Gauge (per artifact)

🔥 Artifact Risk Comparison Bar Chart

🧬 Persistence Analysis

🛡 EDR Gap Detection

🌐 Browser Compromise Detection

📦 Collector Integrity Checks

🎯 MITRE ATT&CK Technique Mapping

📄 Downloadable Markdown Analysis Report
