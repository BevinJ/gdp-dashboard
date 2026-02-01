import streamlit as st
from collections import defaultdict
import random

st.set_page_config(page_title="Agentic Support AI", layout="wide")

st.title("🧠 Agentic AI – Self-Healing Support System")
st.caption("Problem 1: Hosted → Headless Migration")

# -------------------------------
# Simulated Support Tickets
# -------------------------------

tickets = [
    {"merchant": "M1", "error": "CHECKOUT_500", "migrated": True, "stage": "checkout"},
    {"merchant": "M2", "error": "CHECKOUT_500", "migrated": True, "stage": "checkout"},
    {"merchant": "M3", "error": "CHECKOUT_500", "migrated": True, "stage": "checkout"},
    {"merchant": "M4", "error": "API_KEY_INVALID", "migrated": False, "stage": "api"},
    {"merchant": "M5", "error": "WEBHOOK_MISSING", "migrated": True, "stage": "webhook"},
]

st.subheader("📥 Incoming Signals (Support Tickets)")
st.table(tickets)

# -------------------------------
# Observation Layer
# -------------------------------

error_groups = defaultdict(list)
for t in tickets:
    error_groups[t["error"]].append(t)

# -------------------------------
# Reasoning Layer
# -------------------------------

hypotheses = []

for error, group in error_groups.items():
    merchants = set(t["merchant"] for t in group)
    migrated = [t for t in group if t["migrated"]]
    stages = set(t["stage"] for t in group)

    # 1. Merchant Misconfiguration
    if len(merchants) == 1:
        hypotheses.append({
            "type": "Merchant Misconfiguration",
            "confidence": 0.85,
            "reason": "Issue isolated to a single merchant",
            "action": "Guide merchant to fix configuration"
        })

    # 2. Platform Regression
    if len(merchants) >= 3:
        hypotheses.append({
            "type": "Platform Regression",
            "confidence": 0.8,
            "reason": "Same error across multiple merchants",
            "action": "Escalate to engineering immediately"
        })

    # 3. Documentation Gap
    if len(migrated) >= 2:
        hypotheses.append({
            "type": "Documentation Gap",
            "confidence": 0.75,
            "reason": "Repeated errors after migration",
            "action": "Update docs + notify merchants"
        })

    # 4. Migration Step Mismatch
    if len(stages) == 1:
        hypotheses.append({
            "type": "Migration Step Mismatch",
            "confidence": 0.7,
            "reason": f"Failures concentrated at stage: {list(stages)[0]}",
            "action": "Pause migration at this step"
        })

# -------------------------------
# Decision Layer
# -------------------------------

st.subheader("🧠 Agent Reasoning (Multiple Hypotheses)")

for h in hypotheses:
    with st.expander(f"🔎 {h['type']} (confidence {h['confidence']})"):
        st.write("**Why:**", h["reason"])
        st.write("**Proposed Action:**", h["action"])
        if h["confidence"] > 0.75:
            st.success("Safe to act autonomously")
        else:
            st.warning("Requires human approval")

# -------------------------------
# Action Layer
# -------------------------------

st.subheader("⚙️ Agent Actions (Simulated)")

for h in hypotheses:
    st.write(f"➡️ **{h['action']}**")

# -------------------------------
# Learning Layer
# -------------------------------

st.subheader("📈 Learning & Memory Update")

st.info(
    "Agent will track whether these actions reduce repeat tickets "
    "and adjust confidence for future incidents."
)