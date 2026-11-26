"""
Streamlit Web Dashboard for RoadPulse:
Interactive decision-support map for monitoring macro-scale road damage and flood submergence in Bangladesh.
"""
import streamlit as st
from src.config import PILOT_UPAZILAS, CONDITION_CLASSES

st.set_page_config(
    page_title="RoadPulse - Bangladesh Road Damage Detection",
    page_icon="🛰️",
    layout="wide",
)

st.title("🛰️ RoadPulse: Macro-Scale Road Damage & Submergence Monitoring")
st.markdown(
    """
    **Monitoring Macro-Scale Road Surface Degradation and Seasonal Flood Submergence Across Bangladesh 
    Using Sentinel-2 Multi-Spectral Imagery and OpenStreetMap.**
    """
)

# Sidebar Controls
st.sidebar.header("🕹️ Regional Selection & Filters")
pilot_keys = list(PILOT_UPAZILAS.keys())
selected_key = st.sidebar.selectbox(
    "Select Pilot Upazila:",
    options=pilot_keys,
    format_func=lambda k: f"{PILOT_UPAZILAS[k]['name']} ({PILOT_UPAZILAS[k]['district']})",
)

pilot_meta = PILOT_UPAZILAS[selected_key]
st.sidebar.info(
    f"**District:** {pilot_meta['district']}\n\n"
    f"**Division:** {pilot_meta['division']}\n\n"
    f"**UTM Projection:** `{pilot_meta['utm_crs']}`\n\n"
    f"**Bounding Box:** `{pilot_meta['bbox']}`"
)

# Metrics Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Selected Upazila", pilot_meta["name"])
col2.metric("🟢 Intact Corridors", "--")
col3.metric("🟡 Degraded Corridors", "--")
col4.metric("🔴 Submerged / Washed Out", "--")

# Condition Class Legend
st.markdown("### 🏷️ Condition Legend")
legend_cols = st.columns(3)
for i, (cls_id, info) in enumerate(CONDITION_CLASSES.items()):
    with legend_cols[i]:
        st.markdown(
            f"<div style='background-color:{info['color']}; padding:10px; border-radius:5px; color:white; font-weight:bold; text-align:center;'>"
            f"Class {cls_id}: {info['label']}"
            f"</div>",
            unsafe_allow_html=True,
        )

st.markdown("---")
st.info(
    "💡 **Phase 1 Local Environment Ready**: Run `python -m src.data_ingestion` or open the exploratory notebook to begin Phase 2 data fetching."
)
