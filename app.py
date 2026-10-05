import streamlit as st
import pandas as pd
import time

# Page Configuration for modern dashboard widescreen
st.set_page_config(layout="wide", page_title="Live Dealership Master Stock", page_icon="⚡")

# Custom CSS styling to add a professional header frame
st.markdown("""
    <style>
    .main-title { font-size:32px !important; font-weight: 700 !important; color: #1E3A8A; margin-bottom: 20px; }
    .metric-box { background-color: #F3F4F6; padding: 15px; border-radius: 8px; border-left: 5px solid #3B82F6; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ Real-Time Team Lead Master Stock Tracker</div>', unsafe_allow_html=True)

# Target Google Sheet ID from your Google Apps Script configuration
GOOGLE_SHEET_ID = "1xA07_7KUH_z9m7eaIRGbT8asNYLlMgOI1N3SgXnaMtw"
SHEET_NAME = "Group Stock"
CSV_URL = f"https://google.com{GOOGLE_SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

# Setup a background 1-second auto-reload trigger loop
if "refresh_counter" not in st.session_state:
    st.session_state.refresh_counter = 0

# Set a strict 1-second time-to-live cache refresh rule
@st.cache_data(ttl=1)
def load_live_stock_data():
    # Fetch data direct from the Google Sheets engine backend
    df = pd.read_csv(CSV_URL)
    return df

try:
    master_df = load_live_stock_data()
    
    # Clean up column spaces if any exist in the source sheet strings
    master_df.columns = master_df.columns.str.strip()

    # --- TOP METRIC CARDS PANEL ---
    # Calculates summary values automatically in real time based on active records
    total_cars = len(master_df)
    
    # Safe check for Billing Status column
    if "Billing Status" in master_df.columns:
        billed_count = len(master_df[master_df["Billing Status"].astype(str).str.lower() == "billed"])
        pending_count = len(master_df[master_df["Billing Status"].astype(str).str.lower() == "pending"])
    else:
        billed_count, pending_count = 0, 0

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-box">➡️ <b>Total Group Stock:</b><br><span style="font-size:24px; font-weight:bold;">{total_cars} Units</span></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-box">🟢 <b>Billed Count:</b><br><span style="font-size:24px; font-weight:bold; color:green;">{billed_count} Units</span></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-box">🟡 <b>Pending Billing:</b><br><span style="font-size:24px; font-weight:bold; color:#D97706;">{pending_count} Units</span></div>', unsafe_allow_html=True)

    st.write("---")

    # --- TEAMS DROPDOWN CONTROLLER ---
    # Dynamically extract modern Team Lead headers straight from your live rows
    tl_column = "TL Name" if "TL Name" in master_df.columns else master_df.columns[11] # fallback to column position
    
    all_tls = ["ALL TEAM LEADS"] + list(master_df[tl_column].dropna().unique())
    selected_tl = st.selectbox("🎯 Filter Dashboard by Team Lead Profile:", all_tls)
    
    if selected_tl != "ALL TEAM LEADS":
        filtered_df = master_df[master_df[tl_column] == selected_tl]
    else:
        filtered_df = master_df

    # --- LIVE DATA GRID ---
    st.markdown(f"### 📋 Current Active Rows for: **{selected_tl}**")
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)

except Exception as e:
    st.error(f"Connecting to Google Cloud Pipeline... Please verify link sharing permissions on your Google Sheet.")
    st.info("Ensure the column headers exactly match: 'TL Name', 'Billing Status', etc.")

# Pause for 1 second, then rerun the dashboard page seamlessly
time.sleep(1)
st.session_state.refresh_counter += 1
st.rerun()
