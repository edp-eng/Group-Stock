import streamlit as st
import pandas as pd
import datetime

# 🖥️ STABLE CORPORATE LAYOUT THEME CONFIGURATION
st.set_page_config(layout="wide", page_title="Live Dealership Master Stock Dashboard", page_icon="🏆")

# Advanced styling injects to maximize data stability and hide system flickering elements
st.markdown("""
    <style>
    .main-title { font-size:32px !important; font-weight: 700 !important; color: #0F172A; margin-bottom: 5px; font-family: 'Segoe UI', sans-serif; }
    .sync-timestamp { color: #64748B; font-size: 14px; margin-bottom: 25px; }
    .metric-box { background-color: #F8FAFC; padding: 18px; border-radius: 10px; border-top: 4px solid #2563EB; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    div[data-testid="stNotification"] { border-radius: 8px !important; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 Live Dealership Master Stock Dashboard</div>', unsafe_allow_html=True)

# 📍 DECODED SYSTEM LINK PARAMETERS
GOOGLE_SHEET_ID = "1xA07_7KUH_z9m7eaIRGbT8asNYLlMgOI1N3SgXnaMtw"
TARGET_GID = "1892903891"

# Target the clean cloud download channel directly
CSV_URL = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv&gid={TARGET_GID}"

# 🕒 CACHE MECHANISM: Holds a clean 10-minute safe memory pool to prevent background blinking loops
@st.cache_data(ttl=600)
def fetch_live_cloud_matrix():
    df = pd.read_csv(CSV_URL)
    return df

# Initialize clean workspace state memories
if "last_updated" not in st.session_state:
    st.session_state.last_updated = datetime.datetime.now().strftime("%I:%M:%S %p")

# --- TOP UTILITY BAR: CLEAR AND MANUAL SYNC ---
col_title, col_btn = st.columns([5, 1])
with col_title:
    st.markdown(f'<div class="sync-timestamp">⏱️ Live Cache Protected • Last verified at: <b>{st.session_state.last_updated}</b></div>', unsafe_allow_html=True)
with col_btn:
    # Manual button allows users to force a fresh pull directly without running flashing loop timers
    if st.button("🔄 Sync Fresh Data", use_container_width=True):
        st.cache_data.clear()
        st.session_state.last_updated = datetime.datetime.now().strftime("%I:%M:%S %p")
        st.rerun()

try:
    master_df = fetch_live_cloud_matrix()
    
    # Strip spaces from header strings automatically
    master_df.columns = master_df.columns.str.strip()

    # --- AUTOMATED SCORECARDS PANEL ---
    total_records = len(master_df)
    
    # Track Billing Status safely across possible formatting adjustments
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

    # --- INTERACTIVE CONTROLS BAR ---
    f1, f2 = st.columns([2, 4])
    with f1:
        # Team Lead Filter
        tl_field = next((col for col in master_df.columns if col.lower() in ["tl name", "team lead", "tl_name", "tl"]), None)
        if tl_field:
            unique_leads = ["SHOW ALL TEAMS"] + list(master_df[tl_field].dropna().unique())
            selected_lead = st.selectbox("🎯 Filter View by Manager/Team Lead:", unique_leads)
            if selected_lead != "SHOW ALL TEAMS":
                display_df = master_df[master_df[tl_field] == selected_lead]
            else:
                display_df = master_df
        else:
            st.warning("⚠️ Column 'TL Name' not found in row 1 headers grid.")
            selected_lead = "Master View"
            display_df = master_df

    with f2:
        # Global Search input box
        search_query = st.text_input("🔍 Quick Search: Type VIN Number, Model, or Customer Name:", "").strip()

    # Process search query conditions
    if search_query:
        search_lower = search_query.lower()
        search_mask = display_df.astype(str).apply(lambda x: x.str.lower().str.contains(search_lower)).any(axis=1)
        display_df = display_df[search_mask]

    # --- LIVE DATA VIEW MATRIX ---
    st.markdown(f"### 📋 Current Active Rows ({selected_lead})")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

except Exception as error_msg:
    st.error("📡 Connecting to Google Cloud Data Handshake...")
    st.info("💡 Ensure your Google Sheet's Share settings are set to 'Anyone with the link can view' so the app can pull rows.")
