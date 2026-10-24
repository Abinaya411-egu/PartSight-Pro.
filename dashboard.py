import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

if load_dotenv is not None:
    load_dotenv(PROJECT_ROOT / ".env")

st.set_page_config(
    page_title="PartSight Pro",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

from pages.history import render_history_page
from pages.inspect_page import render_inspect_page
from services.ai_service import describe_model_status
from services.database import get_inspection_counts, init_db
from services.status_policy import load_policy_config

init_db()

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(128, 128, 128, 0.25);
        }
        .main-heading {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.3rem;
        }
        .sub-heading {
            color: #777;
            margin-bottom: 1.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_dashboard():
    counts = get_inspection_counts()
    model_status = describe_model_status()
    policy = load_policy_config()

    st.markdown(
        '<div class="main-heading">🔍 PartSight Pro</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="sub-heading">AI-assisted metal surface inspection for hackathon demonstration</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Upload a metal-part image, run the configured model, assign a prototype "
        "PASS / FAIL / REVIEW status, and keep a SQLite history. Dashboard counts "
        "come from the local database, not from sample records."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total inspections", counts["total"])
    c2.metric("PASS", counts["PASS"])
    c3.metric("FAIL", counts["FAIL"])
    c4.metric("REVIEW", counts["REVIEW"])

    if model_status["ready"]:
        st.success(model_status["message"])
    else:
        st.warning(model_status["message"])

    st.caption(
        "Prototype policy: "
        f"ALLOW_PASS={policy['allow_pass']}, "
        f"defect classes={policy['defect_classes'] or 'not configured'}, "
        f"FAIL confidence={policy['fail_confidence']:.2f}. "
        "These are not validated engineering thresholds."
    )

    st.divider()
    st.subheader("Inspection workflow")
    step1, step2, step3 = st.columns(3)
    with step1:
        st.markdown("### 1. Upload image")
        st.write("Select a JPG, JPEG, or PNG photo of a metal component.")
    with step2:
        st.markdown("### 2. Run AI inspection")
        st.write("Click **Run AI Inspection** once. Predictions are shown only if a real model runs.")
    with step3:
        st.markdown("### 3. Review history")
        st.write("Saved records persist in `data/inspections.db` after the app restarts.")

    st.divider()
    st.subheader("Open a page")
    nav1, nav2, nav3 = st.columns(3)
    with nav1:
        if st.button("🔎 Inspect Image", use_container_width=True):
            st.session_state["selected_page"] = "Inspect Image"
            st.rerun()
    with nav2:
        if st.button("📋 History", use_container_width=True):
            st.session_state["selected_page"] = "History"
            st.rerun()
    with nav3:
        if st.button("ℹ️ About", use_container_width=True):
            st.session_state["selected_page"] = "About"
            st.rerun()


def render_about():
    st.title("About PartSight Pro")
    st.write(
        "PartSight Pro is a local Streamlit prototype for visual inspection of metal "
        "components. It is intended as an affordable hackathon demonstration, not a "
        "replacement for industrial machine-vision systems."
    )
    st.subheader("What is implemented")
    st.markdown(
        """
        - Streamlit dashboard with inspection and history pages
        - SQLite inspection records that survive restarts
        - Local YOLO inference when `models/best.pt` (or `PARTSIGHT_MODEL_PATH`) exists
        - Optional Roboflow hosted inference when API credentials are set
        - Conservative PASS / FAIL / REVIEW policy with prototype labels
        """
    )
    st.subheader("What is not claimed")
    st.markdown(
        """
        - Missing weights are not replaced with a generic COCO detector
        - Empty predictions are not treated as proof a part is safe
        - Confidence thresholds are prototype settings until validated
        """
    )


with st.sidebar:
    st.title("🔍 PartSight Pro")
    st.caption("Metal surface inspection")
    st.divider()
    page_options = ["Dashboard", "Inspect Image", "History", "About"]
    if st.session_state.get("selected_page") not in page_options:
        st.session_state["selected_page"] = "Dashboard"
    selected_page = st.radio("Navigation", page_options, key="selected_page")
    st.divider()
    st.caption("Hackathon prototype · Innowah Coders")


if selected_page == "Dashboard":
    render_dashboard()
elif selected_page == "Inspect Image":
    render_inspect_page()
elif selected_page == "History":
    render_history_page()
elif selected_page == "About":
    render_about()
