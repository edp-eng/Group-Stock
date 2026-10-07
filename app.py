import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# Widescreen browser dashboard configuration
st.set_page_config(layout="wide", page_title="Live Dealership Master Stock Tracker", page_icon="⚡")

# Custom UI styling configurations
st.markdown("""
    <style>
    .main-title { font-size:32px !important; font-weight: 700 !important; color: #1E3A8A; margin-bottom: 20px; }
    .metric-box { background-color: #F3F4F6; padding: 15px; border-radius: 8px; border-left: 5px solid #3B82F6; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ Real-Time Team Lead Master Stock Tracker</div>', unsafe_allow_html=True)

# 🔄 NATIVE REAL-TIME AUTOREFRESH: Reruns every 2 seconds smoothly without memory glitches
st_autorefresh(interval=2000, key="group_stock_refresh")

# 📍 CORRECT TARGET SHEET ID DETECTED
GOOGLE_SHEET_ID = "1xA07_7KUH_z9m7eaIRGbT8asNYLlMgOI1N3SgXnaMtw"
SHEET_NAME = "Group Stock"

# Google Visualization API endpoint to query rows cleanly bypassing corporate walls
CSV_URL = f"https://google.com{GOOGLE_SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

@st.cache_data(ttl=1)
def load_live_stock_data():
    df = pd.read_csv(CSV_URL)
    return df

try:
    master_df = load_live_stock_data()
    
    # Strip spaces from header strings automatically
    master_df.columns = master_df.columns.str.strip()

    # --- TOP KPI SCORECARDS ---
    total_cars = len(master_df)
    
    # Locate Vehicle/Billing Status dynamically
    status_col = next((col for col in master_df.columns if col.lower() in ["vehicle status", "billing status", "status", "booking status"]), None)

    if status_col:
        billed_count = len(master_df[master_df[status_col].astype(str).str.lower().str.contains("billed|fitmentdone", na=False)])
        pending_count = len(master_df[master_df[status_col].astype(str).str.lower().str.contains("pending", na=False)])
    else:
        billed_count, pending_count = 0, 0

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-box">➡️ <b>Total Stock Allocation:</b><br><span style="font-size:24px; font-weight:bold;">{total_cars} Rows</span></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-box">🟢 <b>Active / Billed Count:</b><br><span style="font-size:24px; font-weight:bold; color:green;">{billed_count} Units</span></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-box">🟡 <b>Pending Pipeline:</b><br><span style="font-size:24px; font-weight:bold; color:#D97706;">{pending_count} Units</span></div>', unsafe_allow_html=True)

    st.write("---")

    # --- TEAM LEAD SELECTION DROPDOWN ---
    tl_col = next((col for col in master_df.columns if col.lower() in ["tl name", "team lead", "tl_name", "tl", "team lead name"]), None)

    if tl_col:
        all_tls = ["ALL TEAM LEADS"] + list(master_df[tl_col].dropna().unique())
        selected_tl = st.selectbox("🎯 Filter Dashboard by Team Lead Profile:", all_tls)
        
        if selected_tl != "ALL TEAM LEADS":
            filtered_df = master_df[master_df[tl_col] == selected_tl]
        else:
            filtered_df = master_df
    else:
        st.warning("⚠️ Team Lead tracking column not found in Google Sheet. Displaying raw data master view.")
        selected_tl = "Master View"
        filtered_df = master_df

    # --- LIVE DATA GRID ---
    st.markdown(f"### 📋 Current Active Rows for: **{selected_tl}**")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

except Exception as e:
    st.error("📡 Connecting to Google Cloud Pipeline...")
    st.info(f"Technical error context: {str(e)}")
    st.info("💡 Ensure your sheet tab is named exactly 'Group Stock' at the bottom tab options menu.")
