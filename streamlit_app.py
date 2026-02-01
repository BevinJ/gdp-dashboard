import streamlit as st
from collections import defaultdict
import hashlib
import time

st.set_page_config(page_title="Agentic Support AI", layout="wide")

st.title("🧠 Agentic AI – Self-Healing Support System")
st.caption("Problem 1: Hosted → Headless Migration")

# --------------------------------
# AGENT MEMORY (PERSISTENT)
# --------------------------------
if "incident_memory" not in st.session_state:
    st.session_state.incident_memory = {}

# --------------------------------
# SIMULATED SUPPORT TICKETS
# --------------------------------
tickets = [
    {"merchant": "M1", "error": "CHECKOUT_500", "migrated": True, "stage": "checkout"},
    {"merchant": "M2", "error": "CHECKOUT_500", "migrated": True, "stage": "checkout"},
    {"merchant": "M3", "error": "CHECKOUT_500", "migrated": True, "stage": "checkout"},
    {"merchant": "M4", "error": "API_KEY_INVALID", "migrated": False, "stage": "api"},
    {"merchant": "M5", "error": "WEBHOOK_MISSING", "migrated": True, "stage": "webhook"},
]

st.subheader("📥 Incoming Signals (Support Tickets)")
st.table(tickets)

# --------------------------------
# OBSERVATION LAYER
# --------------------------------
error_groups = defaultdict(list)
for t in tickets:
    error_groups[t["error"]].append(t)

# --------------------------------
# REASONING LAYER (MULTI-HYPOTHESIS)
# --------------------------------
st.subheader("🧠 Agent Reasoning")

for error, group in error_groups.items():
    merchants = set(t["merchant"] for t in group)
    migrated = [t for t in group if t["migrated"]]
    stages = set(t["stage"] for t in group)

    # Create incident signature
    signature = hashlib.md5(
        f"{error}-{sorted(merchants)}-{sorted(stages)}".encode()
    ).hexdigest()

    seen_before = signature in st.session_state.incident_memory

    hypotheses = []

    # Merchant Misconfiguration
    if len(merchants) == 1:
        hypotheses.append(("Merchant Misconfiguration", 0.85, "Guide merchant"))

    # Platform Regression
    if len(merchants) >= 3:
        hypotheses.append(("Platform Regression", 0.8, "Escalate to engineering"))

    # Documentation Gap
    if len(migrated) >= 2:
        hypotheses.append(("Documentation Gap", 0.75, "Update docs & notify"))

    # Migration Step Mismatch
    if len(stages) == 1:
        hypotheses.append(("Migration Step Mismatch", 0.7, f"Pause {list(stages)[0]} step"))

    # Increase confidence if seen before
    final_hypotheses = []
    for h in hypotheses:
        confidence = h[1]
        if seen_before:
            confidence += 0.1
        final_hypotheses.append((h[0], round(min(confidence, 0.95), 2), h[2]))

    # Save memory
    st.session_state.incident_memory[signature] = {
        "error": error,
        "times_seen": st.session_state.incident_memory.get(signature, {}).get("times_seen", 0) + 1,
        "last_seen": time.strftime("%Y-%m-%d %H:%M:%S"),
        "hypotheses": final_hypotheses,
    }

    # --------------------------------
    # UI OUTPUT
    # --------------------------------
    with st.expander(f"🔎 Error Pattern: {error}"):
        if seen_before:
            st.warning("⚠️ This issue has occurred before")
            st.write("**Agent Insight:** Previous mitigation likely applies.")
        else:
            st.info("🆕 New issue detected")

        for h in final_hypotheses:
            st.write(f"**Hypothesis:** {h[0]}")
            st.write(f"Confidence: {h[1]}")
            st.write(f"Proposed Action: {h[2]}")
            if h[1] >= 0.8:
                st.success("Safe to act autonomously")
            else:
                st.warning("Requires human approval")
            st.divider()

# --------------------------------
# LEARNING & MEMORY VIEW
# --------------------------------
st.subheader("📈 Agent Memory")

for v in st.session_state.incident_memory.values():
    st.write(
        f"🧠 **{v['error']}** | Seen {v['times_seen']} times | Last seen: {v['last_seen']}"
    )