"""
Databricks Apps: Supply Chain Operations & Expedite Cockpit
Direct replacement for Palantir Workshop & Slate applications.
Hosted natively on Databricks serverless compute with Unity Catalog SSO & OAuth tokens.
Enables business users to visualize order digital twins and trigger kinetic ERP write-backs.
"""

import streamlit as st
import pandas as pd
import datetime
import json
import os
import requests

# Page setup - Enterprise Cockpit
st.set_page_config(
    page_title="Supply Chain Command Center (Databricks Apps)",
    page_icon="📦",
    layout="wide"
)

# Custom Styling to match operational executive cockpit standards
st.markdown("""
<style>
    .metric-card {
        background-color: #0F2C59;
        color: white;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    .status-alert {
        color: #D9534F;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("📦 Global Supply Chain Command Center")
st.caption("Databricks Lakehouse Operational Cockpit (Migrated from Palantir Workshop)")

# Top KPI Metric Bar
col1, col2, col3, col4 = st.columns(4)
col1.metric("Critical Shortage Orders", "14 Orders", delta="-3 today", delta_color="inverse")
col2.metric("Revenue at Risk", "$1,420,500", delta="+ $180k", delta_color="inverse")
col3.metric("Avg Expedite Fulfillment", "18.4 Hours", delta="-4.2 hrs")
col4.metric("Mosaic Agent Actions", "92 Completed", delta="100% policy pass")

st.divider()

# Left Column: Worklist | Right Column: Digital Twin & Kinetic Action
col_left, col_right = st.columns([1, 1.2])

with col_left:
    st.subheader("🚨 Disrupted Orders Worklist")
    
    # Mock data representing Unity Catalog query: SELECT * FROM enterprise_operations.gold.fact_supply_order WHERE stock_shortage_flag = true
    mock_orders = pd.DataFrame([
        {"Order ID": "ORD-89201", "Customer": "AeroTech Dynamics", "SKU": "SKU-TURBINE-09", "Amount ($)": 284000.0, "Risk": "CRITICAL"},
        {"Order ID": "ORD-89244", "Customer": "Nordic Marine Logistics", "SKU": "SKU-VALVE-44", "Amount ($)": 94500.0, "Risk": "HIGH"},
        {"Order ID": "ORD-89302", "Customer": "Global Energy Corp", "SKU": "SKU-SENSOR-12", "Amount ($)": 42000.0, "Risk": "MEDIUM"},
        {"Order ID": "ORD-89350", "Customer": "Pacifica Manufacturing", "SKU": "SKU-ALLOY-88", "Amount ($)": 18200.0, "Risk": "LOW"}
    ])
    
    selected_order_id = st.selectbox(
        "Select Order for Triage & Inspection:",
        options=mock_orders["Order ID"].tolist()
    )
    
    st.dataframe(mock_orders, use_container_width=True, hide_index=True)

with col_right:
    st.subheader(f"🔍 Operational Digital Twin: {selected_order_id}")
    
    order_info = mock_orders[mock_orders["Order ID"] == selected_order_id].iloc[0]
    
    st.info(f"**Customer:** {order_info['Customer']} | **SKU:** {order_info['SKU']} | **Value:** ${order_info['Amount ($)']:,.2f}")
    
    st.markdown("### 🤖 Mosaic AI Recommendation & Action Trigger")
    st.write(
        "**AI Analysis:** Stock shortage detected at primary warehouse (WH-CHICAGO). "
        "Alternative safety inventory (45 units) located at **WH-ATLANTA**. "
        "Transit impact: +8 hours. Air-freight premium: $1,250.00."
    )
    
    with st.form("action_writeback_form"):
        st.write("**Operational Action Parameters (Kinetic Write-Back to SAP ERP):**")
        source_wh = st.selectbox("Source Warehouse:", ["WH-ATLANTA", "WH-DALLAS", "WH-ROTTERDAM"])
        dest_wh = st.text_input("Destination Facility:", "WH-CHICAGO-PLANT-1")
        quantity = st.number_input("Reallocation Quantity:", min_value=1.0, value=25.0)
        expedite_reason = st.text_area("Audit Justification / Expedite Reason:", "Customer SLA contract penalty threshold active.")
        
        submitted = st.form_submit_button("🚀 Approve & Execute Operational Write-Back")
        
        if submitted:
            # Simulate Kinetic Action writeback and Unity Catalog audit logging
            st.success(f"✅ Action Executed Successfully for {selected_order_id}!")
            st.json({
                "action": "reallocateInventoryAndExpedite",
                "order_id": selected_order_id,
                "source_warehouse": source_wh,
                "units_reallocated": quantity,
                "audit_timestamp": datetime.datetime.utcnow().isoformat(),
                "unity_catalog_audit_id": "act_884fbc91",
                "erp_status": "SAP_DELIVERY_EXPEDITED_CONFIRMED"
            })
