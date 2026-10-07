import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# Widescreen browser dashboard window parameters initialization
st.set_page_config(layout="wide", page_title="Live Dealership Master Stock Dashboard", page_icon="🏆")

# High-end corporate look custom styling injects
st.markdown("""
    <style>
    .main-title { font-size:32px !important; font-weight: 700 !important; color: #0F172A; margin-bottom: 25px; font-family: 'Segoe UI', sans-serif; }
    .metric-box { background-color: #F8FAFC; padding: 18px; border-radius: 10px; border-top: 4px solid #2563EB; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 Live Dealership Master Stock Dashboard</div>', unsafe_allow_html=True)

# 🔄 RUN LIVE PAGE BACKGROUND REFRESH LOOP EVERY 2 SECONDS
st_autorefresh(interval=2000, key="vahan_master_stock_loop")

# 📍 DIRECT MATCH MAP FOR YOUR EXACT GOOGLE SHEET SPECIFICATIONS
GOOGLE_SHEET_ID = "1__GyepUvDrq6F6lJIYfU1EAqYv1TLIpntU2W1284ZAE"
GID_ID = "856894043"  # Your exact GID decoded from the sheet URL

# 🛡️ THE PERFECT ENGINE URL: Targets the explicit GID to bypass tab name mismatches completely
CSV_URL = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv&gid={GID_ID}"

@st.cache_data(ttl=1)
def fetch_live_cloud_matrix():
    df = pd.read_csv(CSV_URL)
    return df

try:
    master_df = fetch_live_cloud_matrix()
    
    # Strip spaces from header strings automatically
    master_df.columns = master_df.columns.str.strip()

    # --- AUTOMATED BUSINESS KPI SCORECARDS ---
    total_records = len(master_df)
    
    # Map column mapping from your sheet: "Vehicle Status" holds ALLOCATED / HOLD keys
    status_field = next((col for col in master_df.columns if col.lower() in ["vehicle status", "status", "billing status"]), None)

    if status_field:
        allocated_units = len(master_df[master_df[status_field].astype(str).str.upper().str.contains("ALLOCATED", na=False)])
        hold_units = len(master_df[master_df[status_field].astype(str).str.upper().str.contains("HOLD", na=False)])
    else:
        allocated_units, hold_units = 0, 0

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-box"><span style="color:#64748B; font-weight:600; text-transform:uppercase; font-size:12px;">Total Available Stock</span><br><span style="font-size:28px; font-weight:700; color:#1E293B;">{total_records} Units</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-box"><span style="color:#16A34A; font-weight:600; text-transform:uppercase; font-size:12px;">Allocated Allocation</span><br><span style="font-size:28px; font-weight:700; color:#16A34A;">{allocated_units} Units</span></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-box"><span style="color:#D97706; font-weight:600; text-transform:uppercase; font-size:12px;">Hold Pipeline</span><br><span style="font-size:28px; font-weight:700; color:#D97706;">{hold_units} Units</span></div>', unsafe_allow_html=True)

    st.write("##")

    # --- INTERACTIVE TEAM FILTER CONTROLLER ---
    # Maps precisely to column header "Team" from your live sheet structure
    tl_field = next((col for col in master_df.columns if col.lower() in ["team", "tl name", "team lead"]), None)

    if tl_field:
        unique_leads = ["SHOW ALL TEAMS"] + list(master_df[tl_field].dropna().unique())
        selected_lead = st.selectbox("🎯 Filter View by Team Profile Name:", unique_leads)
        
        if selected_lead != "SHOW ALL TEAMS":
            display_df = master_df[master_df[tl_field] == selected_lead]
        else:
            display_df = master_df
    else:
        st.warning("⚠️ Column 'Team' not found in row 1 headers. Displaying Master View.")
        selected_lead = "Master View"
        display_df = master_df

    # --- LIVE DATA VIEW MATRIX ---
    st.markdown(f"### 📋 Current Stock Status Grid ({selected_lead})")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

except Exception as error_msg:
    st.error("📡 Connecting to Google Cloud Data Handshake...")
    st.info("🔄 Reconnecting shortly. Please verify that your Google Sheet's Share setting is set to 'Anyone with the link can view'.")
