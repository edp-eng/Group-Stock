import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# Page Configuration for widescreen layout
st.set_page_config(layout="wide", page_title="Live Vahan Reg. Data Dashboard", page_icon="⚡")

# Custom CSS styling for polished cards
st.markdown("""
    <style>
    .main-title { font-size:32px !important; font-weight: 700 !important; color: #1E3A8A; margin-bottom: 20px; }
    .metric-box { background-color: #F3F4F6; padding: 15px; border-radius: 8px; border-left: 5px solid #3B82F6; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ Real-Time Team Lead Master Stock Tracker</div>', unsafe_allow_html=True)

# 🔄 NATIVE REAL-TIME AUTOREFRESH: Reloads the page safely every 2 seconds without session errors
st_autorefresh(interval=2000, key="vahan_data_refresh")

# Target Google Sheet ID from your latest Vahan Reg. Data sheet script configuration
GOOGLE_SHEET_ID = "1ftmnwcv9uPI85Srz5_fu-kWbjCyVVi7uREOppal3zrk"
SHEET_NAME = "Vahan Reg. Data"
CSV_URL = f"https://google.com{GOOGLE_SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

# Fetch data directly from Google servers with cache lifetime set to 1 second
@st.cache_data(ttl=1)
def load_live_stock_data():
    df = pd.read_csv(CSV_URL)
    return df

try:
    master_df = load_live_stock_data()
    
    # Strip any hidden whitespaces from column headers automatically
    master_df.columns = master_df.columns.str.strip()

    # --- AUTOMATED SCORECARDS PANEL ---
    total_cars = len(master_df)
    
    # Safe fallback validation for "Billing Status" column variations
    billing_col = None
    for col in master_df.columns:
        if col.lower() in ["billing status", "status", "billing_status"]:
            billing_col = col
            break

    if billing_col:
        billed_count = len(master_df[master_df[billing_col].astype(str).str.lower() == "billed"])
        pending_count = len(master_df[master_df[billing_col].astype(str).str.lower() == "pending"])
    else:
        billed_count, pending_count = 0, 0

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-box">➡️ <b>Total Stock Allocation:</b><br><span style="font-size:24px; font-weight:bold;">{total_cars} Units</span></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-box">🟢 <b>Billed Count:</b><br><span style="font-size:24px; font-weight:bold; color:green;">{billed_count} Units</span></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-box"> echelon 🟡 <b>Pending Billing:</b><br><span style="font-size:24px; font-weight:bold; color:#D97706;">{pending_count} Units</span></div>', unsafe_allow_html=True)

    st.write("---")

    # --- TEAM LEAD SELECTION DROPDOWN ---
    # Find the correct TL Name column automatically even if spelled slightly differently
    tl_col = None
    for col in master_df.columns:
        if col.lower() in ["tl name", "team lead", "tl_name", "tl"]:
            tl_col = col
            break

    if tl_col:
        all_tls = ["ALL TEAM LEADS"] + list(master_df[tl_col].dropna().unique())
        selected_tl = st.selectbox("🎯 Filter Dashboard by Team Lead Profile:", all_tls)
        
        if selected_tl != "ALL TEAM LEADS":
            filtered_df = master_df[master_df[tl_col] == selected_tl]
        else:
            filtered_df = master_df
    else:
        st.warning("⚠️ 'TL Name' column not found in Google Sheet. Displaying raw data master view.")
        selected_tl = "Master View"
        filtered_df = master_df

    # --- LIVE DATA GRID ---
    st.markdown(f"### 📋 Current Active Rows for: **{selected_tl}**")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

except Exception as e:
    st.error("📡 Connecting to Google Cloud Pipeline...")
    st.info("💡 Ensure your Google Sheet sharing permission is set to 'Anyone with the link can view' so the app can pull rows.")
