import streamlit as st
from collections import defaultdict
import hashlib
import time
import random

st.set_page_config(page_title="Agentic Support AI", layout="wide")

st.title("🧠 Agentic AI – Self-Healing Support System")
st.caption("Problem 1: Hosted → Headless Migration")

# --------------------------------
# AGENT MEMORY
# --------------------------------
if "incident_memory" not in st.session_state:
    st.session_state.incident_memory = {}

if "tickets" not in st.session_state:
    st.session_state.tickets = []

# --------------------------------
# CONTROLS (SIMULATE REALITY)
# --------------------------------
st.subheader("🎛️ Simulate New Incidents")

incident_type = st.selectbox(
    "Choose incident type",
    [
        "Platform Regression",
        "Merchant Misconfiguration",
        "Documentation Gap",
        "Migration Step Mismatch",
    ],
)

if st.button("➕ Generate New Error Logs"):
    new_tickets = []

    if incident_type == "Platform Regression":
        for i in range(3):
            new_tickets.append({
                "merchant": f"M{random.randint(1,20)}",
                "error": "CHECKOUT_500",
                "migrated": True,
                "stage": "checkout",
            })

    elif incident_type == "Merchant Misconfiguration":
        new_tickets.append({
            "merchant": f"M{random.randint(1,20)}",
            "error": "API_KEY_INVALID",
            "migrated": False,
            "stage": "api",
        })

    elif incident_type == "Documentation Gap":
        for i in range(2):
            new_tickets.append({
                "merchant": f"M{random.randint(1,20)}",
                "error": "WEBHOOK_MISSING",
                "migrated": True,
                "stage": "webhook",
            })

    elif incident_type == "Migration Step Mismatch":
        for i in range(2):
            new_tickets.append({
                "merchant": f"M{random.randint(1,20)}",
                "error": "SCHEMA_MISMATCH",
                "migrated": True,
                "stage": "checkout",
            })

    st.session_state.tickets.extend(new_tickets)

# --------------------------------
# SHOW LIVE SIGNALS
# --------------------------------
st.subheader("📥 Live Incoming Signals")

if not st.session_state.tickets:
    st.info("No incidents yet. Generate some above.")
else:
    st.table(st.session_state.tickets)

# --------------------------------
# OBSERVATION & REASONING
# --------------------------------
error_groups = defaultdict(list)
for t in st.session_state.tickets:
    error_groups[t["error"]].append(t)

st.subheader("🧠 Agent Reasoning")

for error, group in error_groups.items():
    merchants = set(t["merchant"] for t in group)
    migrated = [t for t in group if t["migrated"]]
    stages = set(t["stage"] for t in group)

    signature = hashlib.md5(
        f"{error}-{sorted(merchants)}-{sorted(stages)}".encode()
    ).hexdigest()

    seen_before = signature in st.session_state.incident_memory

    hypotheses = []

    if len(merchants) == 1:
        hypotheses.append(("Merchant Misconfiguration", 0.85, "Guide merchant"))

    if len(merchants) >= 3:
        hypotheses.append(("Platform Regression", 0.8, "Escalate to engineering"))

    if len(migrated) >= 2:
        hypotheses.append(("Documentation Gap", 0.75, "Update docs & notify"))

    if len(stages) == 1:
        hypotheses.append(("Migration Step Mismatch", 0.7, f"Pause {list(stages)[0]} step"))

    final_hypotheses = []
    for h in hypotheses:
        confidence = h[1] + (0.1 if seen_before else 0)
        final_hypotheses.append((h[0], round(min(confidence, 0.95), 2), h[2]))

    st.session_state.incident_memory[signature] = {
        "error": error,
        "times_seen": st.session_state.incident_memory.get(signature, {}).get("times_seen", 0) + 1,
        "last_seen": time.strftime("%Y-%m-%d %H:%M:%S"),
    }

    with st.expander(f"🔎 Error Pattern: {error}"):
        if seen_before:
            st.warning("⚠️ Recurring issue detected")
        else:
            st.info("🆕 New issue detected")

        for h in final_hypotheses:
            st.write(f"**Hypothesis:** {h[0]}")
            st.write(f"Confidence: {h[1]}")
            st.write(f"Action: {h[2]}")
            st.divider()

# --------------------------------
# MEMORY VIEW
# --------------------------------
st.subheader("📈 Agent Memory")

for v in st.session_state.incident_memory.values():
    st.write(
        f"🧠 {v['error']} | Seen {v['times_seen']} times | Last seen: {v['last_seen']}"
    )