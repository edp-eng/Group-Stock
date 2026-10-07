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

# 📍 FRESH UPDATE: NEW TARGET GOOGLE SHEET ID ASSIGNED
GOOGLE_SHEET_ID = "1__GyepUvDrq6F6lJIYfU1EAqYv1TLIpntU2W1284ZAE"

# Direct download file endpoint configuration—bypasses link encoding bugs with spaces
CSV_URL = f"https://google.com{GOOGLE_SHEET_ID}/export?format=csv&sheet=Group+Stock"

@st.cache_data(ttl=1)
def fetch_live_cloud_matrix():
    # Read the direct CSV data array instantly
    df = pd.read_csv(CSV_URL)
    return df

try:
    master_df = fetch_live_cloud_matrix()
    
    # Clean up accidental space anomalies inside headers string arrays
    master_df.columns = master_df.columns.str.strip()

    # --- AUTOMATED BUSINESS KPI SCORECARDS ---
    total_records = len(master_df)
    
    # Look for status headers dynamically across system variations
    status_field = next((col for col in master_df.columns if col.lower() in ["vehicle status", "billing status", "status", "booking status"]), None)

    if status_field:
        billed_units = len(master_df[master_df[status_field].astype(str).str.lower().str.contains("billed|fitmentdone", na=False)])
        pending_units = len(master_df[master_df[status_field].astype(str).str.lower().str.contains("pending", na=False)])
    else:
        billed_units, pending_units = 0, 0

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="metric-box"><span style="color:#64748B; font-weight:600; text-transform:uppercase; font-size:12px;">Total Combined Stock</span><br><span style="font-size:28px; font-weight:700; color:#1E293B;">{total_records} Units</span></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="metric-box"><span style="color:#16A34A; font-weight:600; text-transform:uppercase; font-size:12px;">Billed / Fitment Done</span><br><span style="font-size:28px; font-weight:700; color:#16A34A;">{billed_units} Units</span></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="metric-box"><span style="color:#D97706; font-weight:600; text-transform:uppercase; font-size:12px;">Pending Pipeline</span><br><span style="font-size:28px; font-weight:700; color:#D97706;">{pending_units} Units</span></div>', unsafe_allow_html=True)

    st.write("##")

    # --- INTERACTIVE TEAM FILTER CONTROLLER ---
    tl_field = next((col for col in master_df.columns if col.lower() in ["tl name", "team lead", "tl_name", "tl", "team lead name"]), None)

    if tl_field:
        unique_leads = ["SHOW ALL TEAMS"] + list(master_df[tl_field].dropna().unique())
        selected_lead = st.selectbox("🎯 Filter View by Manager/Team Lead Name:", unique_leads)
        
        if selected_lead != "SHOW ALL TEAMS":
            display_df = master_df[master_df[tl_field] == selected_lead]
        else:
            display_df = master_df
    else:
        st.warning("⚠️ Column 'TL Name' not found in structural headers row. Displaying Master View.")
        selected_lead = "Master View"
        display_df = master_df

    # --- LIVE DATA VIEW MATRIX ---
    st.markdown(f"### 📋 Current Stock Status Grid ({selected_lead})")
    st.dataframe(display_df, use_container_width=True, hide_index=True)

except Exception as error_msg:
    st.error("📡 Establishing Google Cloud Data Handshake...")
    st.info("🔄 Reconnecting shortly. Verify the Google Sheet's General Access is set to 'Anyone with the link can view'.")
