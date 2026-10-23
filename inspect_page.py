"""
inspect_page.py - PartSight Pro | Inspect Metal Part (frontend only)

Usage from dashboard.py (no edits needed in dashboard.py itself, just import and call):

    from inspect_page import render_inspect_page
    render_inspect_page()

Run standalone for preview:

    streamlit run inspect_page.py

NOTE: All analysis results here are SAMPLE / PLACEHOLDER data for UI demo only.
No real AI detection is performed.
"""

import streamlit as st
from PIL import Image, ImageDraw

# ---------------------------------------------------------------- theme
GREEN = "#1E9E5A"
NAVY = "#0B2545"
LIGHT_GREEN = "#E8F6EE"
LIGHT_BLUE = "#EEF2F8"
BORDER = "#D5DCE6"

STATUS_STYLE = {
    "PASS": {"color": "#1E9E5A", "bg": "#E8F6EE", "icon": "✅",
             "msg": "No defects found in this sample result."},
    "FAIL": {"color": "#C0392B", "bg": "#FDECEA", "icon": "❌",
             "msg": "Defects found in this sample result. Part rejected."},
    "REVIEW": {"color": "#D68910", "bg": "#FEF5E7", "icon": "⚠️",
               "msg": "Doubtful result. Send to human inspector."},
}

# Placeholder data. box = (x1, y1, x2, y2) as fractions of image width/height.
SAMPLE_RESULTS = {
    "PASS": {"defects": []},
    "FAIL": {
        "defects": [
            {"Defect Type": "Scratch", "Location": "Top-left area",
             "Severity": "High", "box": (0.10, 0.12, 0.40, 0.30)},
            {"Defect Type": "Dent", "Location": "Center",
             "Severity": "Medium", "box": (0.40, 0.42, 0.62, 0.64)},
        ]
    },
    "REVIEW": {
        "defects": [
            {"Defect Type": "Possible crack", "Location": "Bottom-right area",
             "Severity": "Low", "box": (0.60, 0.62, 0.90, 0.88)},
        ]
    },
}


# ---------------------------------------------------------------- styling
def _inject_css():
    st.markdown(
        f"""
        <style>
        .stApp {{ background-color: #FFFFFF; }}
        h1, h2, h3, h4, label, p, span, div {{ color: {NAVY}; }}
        .ps-title {{ font-size: 2.1rem; font-weight: 800; color: {NAVY};
                     border-left: 8px solid {GREEN}; padding-left: 14px;
                     margin-bottom: 0.2rem; }}
        .ps-sub {{ color: #5B6B82; margin-bottom: 1.2rem; padding-left: 22px; }}
        .ps-card {{ background: {LIGHT_BLUE}; border: 1px solid {BORDER};
                    border-radius: 12px; padding: 14px 18px; margin-bottom: 10px; }}
        .ps-label {{ font-size: 0.78rem; color: #5B6B82; text-transform: uppercase;
                     letter-spacing: 0.05em; }}
        .ps-value {{ font-size: 1.05rem; font-weight: 700; color: {NAVY}; }}
        .ps-section {{ font-size: 1.2rem; font-weight: 700; color: {NAVY};
                       border-bottom: 3px solid {GREEN}; display: inline-block;
                       margin: 18px 0 10px 0; padding-bottom: 2px; }}
        .ps-status {{ border-radius: 14px; padding: 18px 22px; border: 2px solid; }}
        .ps-status-big {{ font-size: 1.9rem; font-weight: 800; }}
        .ps-note {{ font-size: 0.8rem; color: #5B6B82; font-style: italic; }}
        div.stButton > button {{ background-color: {GREEN}; color: #FFFFFF;
                                 border: none; border-radius: 8px;
                                 font-weight: 700; padding: 0.6rem 1.4rem; }}
        div.stButton > button:hover {{ background-color: {NAVY}; color: #FFFFFF; }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------- helpers
def _info_card(label, value):
    st.markdown(
        f'<div class="ps-card"><div class="ps-label">{label}</div>'
        f'<div class="ps-value">{value}</div></div>',
        unsafe_allow_html=True,
    )


def _section(title):
    st.markdown(f'<div class="ps-section">{title}</div>', unsafe_allow_html=True)


def _status_banner(status):
    s = STATUS_STYLE[status]
    st.markdown(
        f"""
        <div class="ps-status" style="background:{s['bg']}; border-color:{s['color']};">
            <div class="ps-label">Inspection Status</div>
            <div class="ps-status-big" style="color:{s['color']};">{s['icon']} {status}</div>
            <div style="color:{NAVY};">{s['msg']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _draw_placeholder_overlay(image, defects):
    """Draws SAMPLE boxes only for UI preview. Not real detection."""
    out = image.copy().convert("RGB")
    draw = ImageDraw.Draw(out)
    w, h = out.size
    line = max(2, w // 200)
    for i, d in enumerate(defects, start=1):
        x1, y1, x2, y2 = d["box"]
        box = (int(x1 * w), int(y1 * h), int(x2 * w), int(y2 * h))
        draw.rectangle(box, outline="#E74C3C", width=line)
        draw.rectangle((box[0], box[1], box[0] + 28 + line, box[1] + 22),
                       fill="#E74C3C")
        draw.text((box[0] + 8, box[1] + 5), str(i), fill="#FFFFFF")
    return out


# ---------------------------------------------------------------- main page
def render_inspect_page():
    """Renders the Inspect Metal Part page. Call this from dashboard.py."""
    _inject_css()

    # 1. Page title
    st.markdown('<div class="ps-title">Inspect Metal Part</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="ps-sub">PartSight Pro · Upload a metal component image to inspect it</div>',
        unsafe_allow_html=True,
    )

    # 2. Upload button
    uploaded = st.file_uploader(
        "Upload Image", type=["jpg", "jpeg", "png"], key="ps_inspect_upload"
    )

    if uploaded is None:
        st.info("Please upload a metal part image (JPG, JPEG or PNG) to begin.")
        return

    image = Image.open(uploaded).convert("RGB")
    width, height = image.size
    file_key = f"{uploaded.name}_{uploaded.size}"

    # reset result when a new file is uploaded
    if st.session_state.get("ps_file_key") != file_key:
        st.session_state["ps_file_key"] = file_key
        st.session_state["ps_analyzed"] = False

    # 3 + 4. Preview, filename and dimensions
    _section("Uploaded Image")
    col_img, col_info = st.columns([3, 2])
    with col_img:
        st.image(image, caption="Uploaded metal part", use_container_width=True)
    with col_info:
        _info_card("File name", uploaded.name)
        _info_card("Image dimensions", f"{width} × {height} px")
        _info_card("File size", f"{uploaded.size / 1024:.1f} KB")

    # Sample state selector (for UI demo only)
    with st.expander("Demo settings (placeholder results only)"):
        demo_status = st.radio(
            "Preview which sample result?",
            ["PASS", "FAIL", "REVIEW"],
            index=1,
            horizontal=True,
            key="ps_demo_status",
        )
        st.caption("This only switches the sample UI state. No real AI model is used.")

    # 5. Analyze button
    st.write("")
    if st.button("Analyze Image", key="ps_analyze_btn"):
        with st.spinner("Analyzing image..."):
            st.session_state["ps_analyzed"] = True

    if not st.session_state.get("ps_analyzed"):
        return

    # 6. Analysis result
    status = st.session_state.get("ps_demo_status", "FAIL")
    defects = SAMPLE_RESULTS[status]["defects"]

    _section("Analysis Result")
    _status_banner(status)
    st.markdown(
        '<div class="ps-note">Sample / placeholder result for UI demo. '
        "Not a real AI detection.</div>",
        unsafe_allow_html=True,
    )

    # 7. Defect details
    _section("Defect Details")
    if defects:
        rows = [{"#": i, "Defect Type": d["Defect Type"],
                 "Location": d["Location"], "Severity": d["Severity"]}
                for i, d in enumerate(defects, start=1)]
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.success("No defects to display.")

    # 8. Original vs analysed comparison
    _section("Compare: Original vs Analysed")
    analysed = _draw_placeholder_overlay(image, defects)
    c1, c2 = st.columns(2)
    with c1:
        st.image(image, caption="Original image", use_container_width=True)
    with c2:
        st.image(analysed, caption="Analysed image (sample overlay)",
                 use_container_width=True)


# ---------------------------------------------------------------- standalone
if __name__ == "__main__":
    st.set_page_config(page_title="Inspect Metal Part | PartSight Pro",
                       page_icon="🔩", layout="wide")
    render_inspect_page()
