import streamlit as st
from pathlib import Path
import csv, json
import plotly.graph_objects as go

# =========================
# Config
# =========================

BASE_DIR = Path("data/host-001")

st.set_page_config(
    page_title="SOC Artifact Analysis Dashboard",
    layout="wide",
    page_icon="🛡️"
)

# =========================
# Cached File Readers
# =========================

@st.cache_data(show_spinner=False)
def read_text(path: Path):
    return path.read_text(errors="ignore").splitlines() if path.exists() else []

@st.cache_data(show_spinner=False)
def read_csv(path: Path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        return list(csv.DictReader(f))

@st.cache_data(show_spinner=False)
def read_json(path: Path):
    return json.loads(path.read_text(errors="ignore"))

# =========================
# Analysis Functions
# =========================

def analyze_tasks():
    lines = read_text(BASE_DIR / "scheduled_tasks_verbose.txt")
    suspicious = [l for l in lines if "powershell" in l.lower() or "cmd.exe" in l.lower()]
    return len(lines), suspicious

def analyze_services():
    rows = read_csv(BASE_DIR / "services_running.csv")
    suspicious = [
        r for r in rows
        if r.get("StartType", "").upper() == "AUTO"
        and "system32" not in r.get("PathName", "").lower()
    ]
    return rows, suspicious

def analyze_edr():
    text = " ".join(read_text(BASE_DIR / "edr_candidates_present.txt")).lower()
    products = ["defender", "crowdstrike", "sentinel", "carbon"]
    found = [p for p in products if p in text]
    return found

def analyze_browser():
    count = 0
    browser_dir = BASE_DIR / "browsers"
    if browser_dir.exists():
        for f in browser_dir.glob("*.txt"):
            lines = read_text(f)
            count += sum(1 for l in lines if "cookie" in l.lower() or "token" in l.lower())
    return count

def analyze_collector():
    lines = read_text(BASE_DIR / "collector_runlog.txt")
    errors = [l for l in lines if "error" in l.lower() or "fail" in l.lower()]
    return errors

# =========================
# Risk Calculation
# =========================

def calculate_risk(persistence, edr, browser, collector):
    score = 0
    score += 25 if persistence else 0
    score += 25 if not edr else 0
    score += 25 if browser else 0
    score += 25 if collector else 0
    return score

def risk_gauge(score):
    return go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "Overall Risk Score"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {
                    "color": "red" if score >= 75 else
                             "orange" if score >= 40 else
                             "green"
                }
            }
        )
    ).update_layout(height=260, margin=dict(t=20, b=20))

# =========================
# Sidebar
# =========================

st.sidebar.title("🧭 Analyst Panel")

artifact_options = [
    "scheduled_tasks_verbose.txt",
    "services_running.csv",
    "edr_candidates_present.txt",
    "browser_artifacts",
    "collector_runlog.txt"
]

selected = st.sidebar.multiselect(
    "Select Artifacts to Analyze",
    artifact_options
)

run = st.sidebar.button("▶ Analyze Selected Artifacts")

# =========================
# Main
# =========================

st.title("🛡 SOC Artifact Analysis Dashboard")
st.caption("Persistence • EDR • Browser Threats • Collector Integrity")

if not run or not selected:
    st.info("Select artifacts and click **Analyze Selected Artifacts**.")
    st.stop()

# =========================
# Run Selected Analyses
# =========================

persistence_flag = False
edr_flag = False
browser_flag = False
collector_flag = False

st.markdown("## 📊 Executive Summary")

col1, col2 = st.columns([1, 3])

with col2:
    m1, m2, m3, m4 = st.columns(4)

# ---------- Persistence ----------
if "scheduled_tasks_verbose.txt" in selected:
    task_count, suspicious_tasks = analyze_tasks()
    persistence_flag = bool(suspicious_tasks)

    st.markdown("## 🧬 Scheduled Tasks")
    st.metric("Total Tasks", task_count)
    if suspicious_tasks:
        st.error("Suspicious scheduled tasks detected")
        with st.expander("View suspicious tasks"):
            st.code("\n".join(suspicious_tasks[:10]))
    else:
        st.success("No suspicious scheduled tasks")

if "services_running.csv" in selected:
    _, suspicious_services = analyze_services()
    persistence_flag |= bool(suspicious_services)

    st.markdown("## 🧬 Services")
    st.metric("Suspicious Services", len(suspicious_services))
    if suspicious_services:
        st.error("Suspicious auto-start services detected")
        with st.expander("View services"):
            st.json(suspicious_services)
    else:
        st.success("No suspicious services")

# ---------- EDR ----------
if "edr_candidates_present.txt" in selected:
    edr_found = analyze_edr()
    edr_flag = bool(edr_found)

    st.markdown("## 🛡 EDR Status")
    if edr_found:
        st.success(f"EDR detected: {', '.join(edr_found)}")
    else:
        st.error("No EDR detected or possible tampering")

# ---------- Browser ----------
if "browser_artifacts" in selected:
    browser_count = analyze_browser()
    browser_flag = browser_count > 0

    st.markdown("## 🌐 Browser-Based Threats")
    if browser_count:
        st.error(f"{browser_count} suspicious browser indicators detected")
        fig = go.Figure(go.Bar(x=["Indicators"], y=[browser_count]))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("No browser-based compromise detected")

# ---------- Collector ----------
if "collector_runlog.txt" in selected:
    errors = analyze_collector()
    collector_flag = bool(errors)

    st.markdown("## 📦 Collector Integrity")
    if errors:
        st.error("Collector execution issues detected")
        with st.expander("View errors"):
            st.code("\n".join(errors))
    else:
        st.success("Collector ran successfully without errors")

# =========================
# Risk Score
# =========================

risk = calculate_risk(
    persistence_flag,
    edr_flag,
    browser_flag,
    collector_flag
)

with col1:
    st.plotly_chart(risk_gauge(risk), use_container_width=True)

with col2:
    m1.metric("Persistence Hooks", "YES" if persistence_flag else "NO")
    m2.metric("EDR Detected", "YES" if edr_flag else "NO")
    m3.metric("Browser Threats", "YES" if browser_flag else "NO")
    m4.metric("Collector Issues", "YES" if collector_flag else "NO")
