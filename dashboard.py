import streamlit as st

st.set_page_config(
    page_title="PartSight Pro | Dashboard",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Theme ----------
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
      html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
      .stApp { background: #f7faf9; color: #12243a; }
      [data-testid="stSidebar"] {
        background: #102a43;
        border-right: 1px solid #203d56;
      }
      [data-testid="stSidebar"] * { color: #edf7f3 !important; }
      .brand {
        display:flex; align-items:center; gap:12px;
        padding: 10px 4px 26px 4px;
      }
      .brand-icon {
        width:44px; height:44px; border-radius:13px;
        display:flex; align-items:center; justify-content:center;
        background:#19a875; color:white; font-size:23px; font-weight:800;
      }
      .brand-name { font-size:20px; font-weight:800; letter-spacing:-.5px; }
      .brand-sub { font-size:11px; color:#b8c9d8; margin-top:3px; }
      .nav-label { color:#9eb2c5 !important; font-size:11px; font-weight:700;
                   letter-spacing:1.4px; margin:8px 0 8px 5px; }
      .eyebrow { color:#16845f; font-size:12px; font-weight:800;
                 text-transform:uppercase; letter-spacing:1.6px; }
      .page-title { font-size:32px; font-weight:800; letter-spacing:-1.2px;
                    color:#102a43; margin:4px 0 4px 0; }
      .page-subtitle { color:#64748b; font-size:14px; margin-bottom:22px; }
      .status-pill { display:inline-block; padding:7px 12px; border-radius:999px;
                     background:#e5f7ef; color:#08744c; font-size:12px;
                     font-weight:700; border:1px solid #c7efdc; }
      .metric-card {
        background:white; border:1px solid #e4ece8; border-radius:18px;
        padding:21px 22px 19px 22px; min-height:148px;
        box-shadow:0 5px 18px rgba(16,42,67,.035);
      }
      .metric-top { display:flex; justify-content:space-between; align-items:center; }
      .metric-label { color:#607286; font-size:13px; font-weight:600; }
      .metric-icon { width:39px; height:39px; border-radius:12px;
                     display:flex; align-items:center; justify-content:center;
                     font-size:19px; }
      .metric-value { font-size:32px; font-weight:800; color:#102a43;
                      letter-spacing:-1px; margin-top:15px; }
      .metric-note { color:#7b8b9b; font-size:12px; margin-top:3px; }
      .section-card { background:white; border:1px solid #e4ece8; border-radius:18px;
                      padding:22px; box-shadow:0 5px 18px rgba(16,42,67,.03); }
      .section-heading { color:#102a43; font-size:17px; font-weight:750; }
      .section-caption { color:#718096; font-size:12px; margin-top:4px; }
      .empty-state { text-align:center; padding:34px 12px 22px 12px; }
      .empty-icon { font-size:36px; margin-bottom:12px; }
      .empty-title { color:#102a43; font-size:16px; font-weight:700; }
      .empty-copy { color:#718096; font-size:13px; margin-top:6px; line-height:1.6; }
      .footer { color:#94a3b8; font-size:11px; padding-top:25px; text-align:center; }
      div.stButton > button {
        border-radius:10px; border:0; background:#13845f; color:white;
        font-weight:700; padding: .65rem 1rem;
      }
      div.stButton > button:hover { background:#0d6d4d; color:white; }
      [data-testid="stMetric"] { background:white; padding:16px; border-radius:14px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown(
        """
        <div class="brand">
          <div class="brand-icon">P</div>
          <div>
            <div class="brand-name">PartSight Pro</div>
            <div class="brand-sub">QUALITY INSPECTION SYSTEM</div>
          </div>
        </div>
        <div class="nav-label">WORKSPACE</div>
        """,
        unsafe_allow_html=True,
    )
    selected_page = st.radio(
        "Navigation",
        ["Dashboard", "Inspect Image", "History", "About"],
        index=0,
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown(
        """
        <div style="background:#183750;border:1px solid #2a4b63;padding:15px;border-radius:13px;margin-top:12px;">
          <div style="font-size:11px;color:#a9c0d2;letter-spacing:1px;font-weight:700;">SYSTEM STATUS</div>
          <div style="display:flex;align-items:center;gap:8px;margin-top:10px;">
            <span style="height:8px;width:8px;background:#35d39a;border-radius:50%;display:inline-block;"></span>
            <span style="font-size:13px;font-weight:600;">Dashboard ready</span>
          </div>
          <div style="font-size:11px;color:#b8c9d8;margin-top:7px;">Demo interface · Sample metrics</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="position:fixed;bottom:18px;color:#9eb2c5;font-size:11px;">PartSight Pro · Hackathon Demo</div>',
        unsafe_allow_html=True,
    )

# Dashboard is the only implemented page; the other navigation entries are placeholders.
if selected_page != "Dashboard":
    st.markdown('<div class="eyebrow">PARTSIGHT PRO</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-title">{selected_page}</div>', unsafe_allow_html=True)
    st.info(
        f"The {selected_page} page is a navigation placeholder. "
        "This file implements the Home Dashboard only."
    )
    st.stop()

# ---------- Main dashboard ----------
left, right = st.columns([5, 1.4], vertical_alignment="center")
with left:
    st.markdown('<div class="eyebrow">MANUFACTURING INTELLIGENCE</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-title">Home Dashboard</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="page-subtitle">Monitor part quality, track inspections, and review potential defects.</div>',
        unsafe_allow_html=True,
    )
with right:
    st.markdown('<div style="text-align:right;margin-bottom:24px;"><span class="status-pill">● System Online</span></div>', unsafe_allow_html=True)

# Sample numbers are clearly marked as demo data.
cards = [
    ("Total Inspections", "128", "All images checked in this demo", "▣", "#e7f2ff", "#2563a6"),
    ("Defects Found", "24", "Parts flagged with possible defects", "⌕", "#e4f8ee", "#12805c"),
    ("Review Required", "7", "Parts waiting for human review", "◷", "#fff3df", "#b7791f"),
]
columns = st.columns(3, gap="medium")
for col, (label, value, note, icon, icon_bg, icon_color) in zip(columns, cards):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
              <div class="metric-top">
                <div class="metric-label">{label}</div>
                <div class="metric-icon" style="background:{icon_bg};color:{icon_color};">{icon}</div>
              </div>
              <div class="metric-value">{value}</div>
              <div class="metric-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.write("")
main_col, side_col = st.columns([1.55, 1], gap="medium")

with main_col:
    st.markdown(
        """
        <div class="section-card">
          <div class="section-heading">Inspection overview</div>
          <div class="section-caption">A quick snapshot of the sample inspection data</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    chart_data = {
        "Category": ["Passed", "Defect found", "Review required"],
        "Parts": [97, 24, 7],
    }
    st.bar_chart(chart_data, x="Category", y="Parts", color="#16845f", height=250)
    st.caption("Demo data for dashboard preview. Connect the inspection pipeline to show live results.")

with side_col:
    st.markdown(
        """
        <div class="section-card">
          <div class="section-heading">Quick start</div>
          <div class="section-caption">Your quality workflow at a glance</div>
          <div style="margin-top:22px;display:flex;gap:12px;align-items:flex-start;">
            <div style="background:#e5f7ef;color:#12805c;border-radius:10px;padding:9px 11px;font-weight:800;">1</div>
            <div><div style="font-weight:700;color:#102a43;font-size:13px;">Choose a part image</div>
            <div style="color:#718096;font-size:12px;margin-top:4px;">Start with a clear photo of the metal part.</div></div>
          </div>
          <div style="margin-top:17px;display:flex;gap:12px;align-items:flex-start;">
            <div style="background:#e7f2ff;color:#2563a6;border-radius:10px;padding:9px 11px;font-weight:800;">2</div>
            <div><div style="font-weight:700;color:#102a43;font-size:13px;">Run the inspection</div>
            <div style="color:#718096;font-size:12px;margin-top:4px;">Check for scratches and visible defects.</div></div>
          </div>
          <div style="margin-top:17px;display:flex;gap:12px;align-items:flex-start;">
            <div style="background:#fff3df;color:#b7791f;border-radius:10px;padding:9px 11px;font-weight:800;">3</div>
            <div><div style="font-weight:700;color:#102a43;font-size:13px;">Review flagged parts</div>
            <div style="color:#718096;font-size:12px;margin-top:4px;">Confirm uncertain results before decisions.</div></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    if st.button("＋  Start an inspection", use_container_width=True):
        st.info("Inspect Image is a placeholder in this dashboard-only build. The image inspection page can be added separately.")

st.markdown(
    '<div class="footer">PartSight Pro · Manufacturing quality dashboard · Sample values shown for demo purposes</div>',
    unsafe_allow_html=True,
)
