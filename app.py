import streamlit as st
import pandas as pd
import time

# 🖥️ WIDESCREEN DASHBOARD THEME CONFIGURATION
st.set_page_config(layout="wide", page_title="Live Dealership Master Stock Dashboard", page_icon="🏆")

# High-end corporate look styling configurations
st.markdown("""
    <style>
    .main-title { font-size:32px !important; font-weight: 700 !important; color: #0F172A; margin-bottom: 25px; font-family: 'Segoe UI', sans-serif; }
    .metric-box { background-color: #F8FAFC; padding: 18px; border-radius: 10px; border-top: 4px solid #2563EB; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    /* Block default streamlit running indicator flickering */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 Live Dealership Master Stock Dashboard</div>', unsafe_allow_html=True)

# 📍 DECODED REAL TARGET SHEET DATA COORDINATES
GOOGLE_SHEET_ID = "1xA07_7KUH_z9m7eaIRGbT8asNYLlMgOI1N3SgXnaMtw"
TARGET_GID = "1892903891"

# 🛡️ THE PERFECT ENGINE URL: Targets the explicit GID to bypass tab name mismatches completely
CSV_URL = f"https://google.com{GOOGLE_SHEET_ID}/export?format=csv&gid={TARGET_GID}"

# 🕒 SMART TIME CACHE ENGINE: Keeps a clean 3-second data pool in background memory 
# to protect the user interface from continuous looping or flickering.
@st.cache_data(ttl=3)
def fetch_live_cloud_matrix():
    df = pd.read_csv(CSV_URL)
    return df

try:
    master_df = fetch_live_cloud_matrix()
    
    # Strip spaces from header strings automatically
    master_df.columns = master_df.columns.str.strip()

    # --- AUTOMATED SCORECARDS PANEL ---
    total_records = len(master_df)
    
    # Dynamically find status fields across possible entry columns
    status_field = next((col for col in master_df.columns if col.lower() in ["billing status", "status", "vehicle status", "booking status"]), None)

    if status_field:
        allocated_units = len(master_df[master_df[status_field].astype(str).str.upper().str.contains("ALLOCATED|HOLD", na=False)])
        free_units = len(master_df[master_df[status_field].astype(str).str.upper().str.contains("FREE", na=False)])
    else:
        allocated_units, free_units = 0, 0

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-box"><span style="color:#64748B; font-weight:600; text-transform:uppercase; font-size:12px;">Total Available Stock</span><br><span style="font-size:28px; font-weight:700; color:#1E293B;">{total_records} Units</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-box"><span style="color:#16A34A; font-weight:600; text-transform:uppercase; font-size:12px;">Allocated / Hold Booking</span><br><span style="font-size:28px; font-weight:700; color:#16A34A;">{allocated_units} Units</span></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-box"><span style="color:#D97706; font-weight:600; text-transform:uppercase; font-size:12px;">Free Stock Volume</span><br><span style="font-size:28px; font-weight:700; color:#D97706;">{free_units} Units</span></div>', unsafe_allow_html=True)

    st.write("##")

    # --- INTERACTIVE SEARCH FIELD BAR ---
    search_query = st.text_input("🔍 Quick Locate: Search by VIN Number or Customer Name:", "").strip()

    # --- INTERACTIVE TEAM FILTER CONTROLLER ---
    tl_field = next((col for col in master_df.columns if col.lower() in ["tl name", "team lead", "tl_name", "tl"]), None)

    if tl_field:
        unique_leads = ["SHOW ALL TEAMS"] + list(master_df[tl_field].dropna().unique())
        selected_lead = st.selectbox("🎯 Filter View by Manager/Team Lead Name:", unique_leads)
        
        if selected_lead != "SHOW ALL TEAMS":
            display_df = master_df[master_df[tl_field] == selected_lead]
        else:
            display_df = master_df
    else:
        st.warning("⚠️ Column Tracking Tag not found in headers grid. Displaying Master View.")
        selected_lead = "Master View"
        display_df = master_df

    # Apply search text queries live if inputted by users
    if search_query:
        search_lower = search_query.lower()
        search_mask = (
            display_df.astype(str).apply(lambda x: x.str.lower().str.contains(search_lower)).any(axis=1)
        )
        display_df = display_df[search_mask]

    # --- LIVE DATA VIEW MATRIX ---
    st.markdown(f"### 📋 Current Active Rows ({selected_lead})")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

except Exception as error_msg:
    st.error("📡 Connecting to Google Cloud Data Handshake...")
    st.info("🔄 Reconnecting shortly. Please verify that your Google Sheet's Share setting is set to 'Anyone with the link can view'.")

# 🔄 STABLE REAL-TIME BACKGROUND REFRESH: 
# Pauses cleanly for 5 seconds before pulling data, ending the infinite blinking loop completely.
time.sleep(5)
st.rerun()
