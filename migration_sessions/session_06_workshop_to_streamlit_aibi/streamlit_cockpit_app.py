"""
Session 6: Palantir Workshop to Databricks Apps (Streamlit)
Rebuilds the interactive operational decision cockpit with Worklists, KPI metric bars,
and form-driven ERP write-back buttons.
"""

import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Supply Chain Command Center", layout="wide")

st.title("📦 Global Supply Chain Operational Command Center")
st.caption("Decoupled Databricks App replacing Palantir Workshop & Slate")

# Top KPI Bar
c1, c2, c3 = st.columns(3)
c1.metric("Shortage Orders", "14 Active", delta="-3", delta_color="inverse")
c2.metric("Revenue at Risk", "$1,420,500", delta="-$80k")
c3.metric("Fulfillment Latency", "18.4 Hours", delta="-4.2 hrs")

st.divider()

col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("🚨 Disrupted Orders Worklist")
    orders = pd.DataFrame([
        {"Order ID": "ORD-89201", "Customer": "AeroTech Dynamics", "Amount ($)": 284000.0, "Risk": "HIGH"},
        {"Order ID": "ORD-89244", "Customer": "Nordic Marine Logistics", "Amount ($)": 94500.0, "Risk": "MEDIUM"}
    ])
    selected = st.selectbox("Select Order for Inspection:", orders["Order ID"])
    st.dataframe(orders, hide_index=True)

with col_right:
    st.subheader(f"⚙️ Operational Write-Back Action: {selected}")
    with st.form("action_form"):
        wh = st.selectbox("Reallocate From Warehouse:", ["WH-ATLANTA", "WH-DALLAS"])
        qty = st.number_input("Units to Expedite:", min_value=1.0, value=25.0)
        reason = st.text_input("Operational Reason:", value="Customer SLA contract penalty threshold active.")
        
        if st.form_submit_button("🚀 Dispatch ERP Expedite Action"):
            st.success(f"Action dispatched successfully for {selected}!")
            st.json({
                "action": "reallocateInventoryAndExpedite",
                "order_id": selected,
                "source_warehouse": wh,
                "reallocated_units": qty,
                "erp_status": "SAP_EXPEDITE_CONFIRMED",
                "timestamp": datetime.datetime.utcnow().isoformat()
            })
