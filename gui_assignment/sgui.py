import streamlit as st
from pathlib import Path
import csv, json
import plotly.graph_objects as go

# =========================================================
# CONFIG
# =========================================================

HOST_DIR = Path("data/host-001")
REPORT_DIR = Path("analysis_reports")
REPORT_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="SOC Artifact Analysis Dashboard",
    layout="wide",
    page_icon="🛡️"
)

# =========================================================
# SAFE FILE READERS
# =========================================================

@st.cache_data(show_spinner=False)
def read_text(path: Path):
    try:
        return path.read_text(errors="ignore").splitlines()
    except Exception:
        return []

@st.cache_data(show_spinner=False)
def read_csv(path: Path):
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            return list(csv.DictReader(f))
    except Exception:
        return []

@st.cache_data(show_spinner=False)
def read_json_safe(path: Path):
    try:
        raw = path.read_text().strip()
        if not raw:
            return {}
        return json.loads(raw)
    except Exception:
        return {}

# =========================================================
# ARTIFACT DISCOVERY
# =========================================================

def discover_artifacts():
    items = []
    for p in HOST_DIR.iterdir():
        prefix = "[DIR]" if p.is_dir() else "[FILE]"
        items.append(f"{prefix} {p.name}")
    return sorted(items)

# =========================================================
# RISK / SEVERITY
# =========================================================

def severity(score: int):
    if score >= 70:
        return "HIGH"
    if score >= 40:
        return "MEDIUM"
    return "LOW"

def risk_gauge(score: int):
    return go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Overall Risk Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {
                    "color": "#ef4444" if score >= 70
                    else "#f59e0b" if score >= 40
                    else "#22c55e"
                }
            }
        )
    ).update_layout(height=260, margin=dict(t=10, b=10))

# =========================================================
# ARTIFACT ANALYSIS (FIXED)
# =========================================================

def analyze_artifact(name: str):
    findings = []
    mitre = []
    score = 0

    if name == "persistence":
        tasks = read_text(HOST_DIR / "scheduled_tasks_verbose.txt")
        services = read_csv(HOST_DIR / "services_running.csv")

        suspicious_tasks = [l for l in tasks if "powershell" in l.lower() or "cmd.exe" in l.lower()]
        suspicious_services = [
            s for s in services
            if s.get("StartType", "").upper() == "AUTO"
            and "system32" not in s.get("PathName", "").lower()
        ]

        findings += [
            f"Total scheduled tasks: {len(tasks)}",
            f"Suspicious scheduled tasks: {len(suspicious_tasks)}",
            f"Suspicious auto-start services: {len(suspicious_services)}"
        ]

        mitre += ["T1053 – Scheduled Task", "T1543 – Create or Modify System Process"]
        score = 70 if suspicious_tasks or suspicious_services else 30

    elif name == "scheduled_tasks_verbose.txt":
        lines = read_text(HOST_DIR / name)
        suspicious = [l for l in lines if "powershell" in l.lower() or "cmd.exe" in l.lower()]
        findings += [
            f"Total scheduled tasks: {len(lines)}",
            f"Suspicious task entries: {len(suspicious)}"
        ]
        mitre.append("T1053 – Scheduled Task")
        score = 60 if suspicious else 25

    elif name == "services_running.csv":
        rows = read_csv(HOST_DIR / name)
        auto = [r for r in rows if r.get("StartType", "").upper() == "AUTO"]
        findings += [
            f"Total services: {len(rows)}",
            f"Auto-start services: {len(auto)}"
        ]
        mitre.append("T1543 – Create or Modify System Process")
        score = 55 if len(auto) > 20 else 30

    elif name == "edr_candidates_present.txt":
        text = " ".join(read_text(HOST_DIR / name)).lower()
        products = ["defender", "crowdstrike", "sentinel", "carbon"]
        found = [p for p in products if p in text]
        findings.append(f"EDR products detected: {found if found else 'NONE'}")
        mitre.append("T1562 – Impair Defenses")
        score = 80 if not found else 20

    elif name == "browsers":
        indicators = 0
        for f in (HOST_DIR / "browsers").rglob("*.txt"):
            indicators += sum(
                1 for l in read_text(f)
                if "cookie" in l.lower() or "token" in l.lower() or "password" in l.lower()
            )
        findings.append(f"Credential/session indicators found: {indicators}")
        mitre.append("T1056 – Input Capture")
        score = 70 if indicators else 20

    elif name == "collector_runlog.txt":
        errors = [l for l in read_text(HOST_DIR / name) if "error" in l.lower()]
        findings.append(f"Collector execution errors: {len(errors)}")
        score = 60 if errors else 10

    elif name == "run_metadata.json":
        meta = read_json_safe(HOST_DIR / name)
        findings.append(f"Metadata fields present: {len(meta)}")
        score = 15 if meta else 35

    else:
        findings.append("No specialized parser for this artifact")
        score = 30

    return min(score, 100), findings, mitre

# =========================================================
# HOST-WIDE RISK COMPARISON
# =========================================================

def compute_all_artifact_risks():
    risks = {}
    for item in discover_artifacts():
        name = item.replace("[DIR] ", "").replace("[FILE] ", "")
        score, _, _ = analyze_artifact(name)
        risks[name] = score
    return risks

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🧭 Analyst Panel")

artifact_label = st.sidebar.selectbox("Select Artifact", discover_artifacts())
run = st.sidebar.button("▶ Analyze Artifact")

# =========================================================
# MAIN UI
# =========================================================

st.title("🛡 SOC Artifact Analysis Dashboard")

if not run:
    st.info("Select an artifact and click **Analyze Artifact**.")
    st.stop()

artifact = artifact_label.replace("[DIR] ", "").replace("[FILE] ", "")
risk, findings, mitre = analyze_artifact(artifact)

# =========================================================
# EXEC SUMMARY
# =========================================================

row = st.columns([1.2, 2, 1])

with row[0]:
    st.plotly_chart(risk_gauge(risk), use_container_width=True)

with row[1]:
    st.markdown(f"### Artifact\n**{artifact}**")
    st.markdown(f"### Risk Score\n**{risk}**")
    st.markdown(f"### Severity\n**{severity(risk)}**")

with row[2]:
    st.metric("High Risk", "YES" if risk >= 70 else "NO")

st.divider()

# =========================================================
# DETAILS
# =========================================================

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### 🔍 Findings")
    for f in findings:
        st.markdown(f"- {f}")

with c2:
    st.markdown("### 🎯 MITRE ATT&CK")
    for m in mitre or ["None inferred"]:
        st.markdown(f"- {m}")

with c3:
    st.markdown("### 🔥 Artifact Risk Comparison")
    risks = compute_all_artifact_risks()
    fig = go.Figure(go.Bar(x=list(risks.keys()), y=list(risks.values())))
    fig.update_layout(yaxis=dict(range=[0, 100]), height=300)
    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# REPORT DOWNLOAD
# =========================================================

report_md = f"# Analysis Report – {artifact}\n\n" + "\n".join(f"- {f}" for f in findings)
st.download_button("⬇ Download Analysis Report (Markdown)", report_md)
