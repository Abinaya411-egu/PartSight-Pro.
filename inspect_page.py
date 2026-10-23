"""
inspect_page.py - PartSight Pro | Inspect Metal Part (frontend only)

Usage from dashboard.py (no edits needed in dashboard.py itself, just import and call):

    from inspect_page import render_inspect_page
    render_inspect_page()

Run standalone for preview:

    streamlit run inspect_page.py

AI MODEL STATUS
---------------
The AI model is NOT integrated yet. While MODEL_INTEGRATED is False, the page
shows "AI model not integrated yet" after Analyze Image and never shows a
result that looks like a real AI prediction.

To connect the model later:
  1. Implement _run_ai_model(image) below.
  2. Set MODEL_INTEGRATED = True.
"""

import streamlit as st
from PIL import Image, ImageDraw, UnidentifiedImageError

# ---------------------------------------------------------------- settings
ALLOWED_EXTENSIONS = ("jpg", "jpeg", "png")
MAX_FILE_MB = 10
MODEL_INTEGRATED = False  # set True only after _run_ai_model() is implemented

# ---------------------------------------------------------------- theme
GREEN = "#1E9E5A"
NAVY = "#0B2545"
LIGHT_BLUE = "#EEF2F8"
BORDER = "#D5DCE6"

STATUS_STYLE = {
    "PASS": {"color": "#1E9E5A", "bg": "#E8F6EE", "icon": "✅",
             "msg": "No defects found."},
    "FAIL": {"color": "#C0392B", "bg": "#FDECEA", "icon": "❌",
             "msg": "Defects found. Part rejected."},
    "REVIEW": {"color": "#D68910", "bg": "#FEF5E7", "icon": "⚠️",
               "msg": "Doubtful result. Send to human inspector."},
    "NOT INTEGRATED": {"color": "#5B6B82", "bg": "#EEF2F8", "icon": "🛠️",
                       "msg": "AI model not integrated yet. "
                              "No real analysis was performed."},
}

# SAMPLE data, used only when the person ticks "Show sample UI preview".
# box = (x1, y1, x2, y2) as fractions of image width/height.
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


# ---------------------------------------------------------------- AI hook
def _run_ai_model(image):
    """
    Hook for the real AI model (backend team).

    Must return a dict:
        {
          "status": "PASS" | "FAIL" | "REVIEW",
          "defects": [{"Defect Type": str, "Location": str, "Severity": str}, ...],
          "analysed_image": PIL.Image or None,
        }
    """
    raise NotImplementedError("AI model not integrated yet")


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


def _draw_sample_overlay(image, defects):
    """Draws SAMPLE boxes for UI preview only. Not real detection."""
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


def _load_image(uploaded):
    """Validates the upload. Returns (image, None) or (None, error_message)."""
    name = uploaded.name or ""
    ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""

    if ext not in ALLOWED_EXTENSIONS:
        shown = f".{ext}" if ext else "(no extension)"
        return None, (f"Invalid file type {shown}. "
                      "Please upload a JPG, JPEG or PNG image.")

    if uploaded.size == 0:
        return None, "The file is empty. Please upload a valid image."

    if uploaded.size > MAX_FILE_MB * 1024 * 1024:
        size_mb = uploaded.size / (1024 * 1024)
        return None, (f"File is too large ({size_mb:.1f} MB). "
                      f"Maximum allowed size is {MAX_FILE_MB} MB.")

    try:
        check = Image.open(uploaded)
        check.verify()
        uploaded.seek(0)
        image = Image.open(uploaded).convert("RGB")
    except (UnidentifiedImageError, OSError, ValueError, SyntaxError,
            Image.DecompressionBombError):
        return None, ("This file is not a valid image or it is corrupted. "
                      "Please upload a different JPG, JPEG or PNG file.")

    return image, None


def _render_result(status, defects, original, analysed, mode):
    """mode: 'real' | 'sample' | 'none' (AI model not integrated)."""
    _section("Analysis Result")

    if mode == "sample":
        st.warning("SAMPLE DATA for UI preview only. "
                   "This is NOT a real AI prediction.")
    _status_banner(status)

    _section("Defect Details")
    if mode == "none":
        st.info("No defect data available. AI model not integrated yet.")
    elif defects:
        rows = [{"#": i, "Defect Type": d["Defect Type"],
                 "Location": d["Location"], "Severity": d["Severity"]}
                for i, d in enumerate(defects, start=1)]
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.success("No defects to display.")

    _section("Compare: Original vs Analysed")
    c1, c2 = st.columns(2)
    with c1:
        st.image(original, caption="Original image", use_container_width=True)
    with c2:
        if analysed is not None:
            caption = ("Analysed image (sample overlay, not real AI)"
                       if mode == "sample" else "Analysed image")
            st.image(analysed, caption=caption, use_container_width=True)
        else:
            st.info("Analysed image will appear here once the AI model "
                    "is connected.")


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
        "Upload Image", type=list(ALLOWED_EXTENSIONS), key="ps_inspect_upload"
    )

    if uploaded is None:
        st.session_state["ps_analyzed"] = False
        st.info("Please upload a metal part image (JPG, JPEG or PNG) to begin.")
        return

    image, error = _load_image(uploaded)
    if error:
        st.session_state["ps_analyzed"] = False
        st.error(error)
        return

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

    # Optional UI preview (only while the AI model is not integrated)
    show_sample = False
    sample_status = "FAIL"
    if not MODEL_INTEGRATED:
        with st.expander("Demo settings (UI preview only)"):
            show_sample = st.checkbox(
                "Show sample UI preview (fake data, not real AI)",
                value=False,
                key="ps_show_sample",
            )
            if show_sample:
                sample_status = st.radio(
                    "Sample status to preview",
                    ["PASS", "FAIL", "REVIEW"],
                    index=1,
                    horizontal=True,
                    key="ps_demo_status",
                )

    # 5. Analyze button
    st.write("")
    if st.button("Analyze Image", key="ps_analyze_btn"):
        st.session_state["ps_analyzed"] = True

    if not st.session_state.get("ps_analyzed"):
        return

    # 6-8. Result, defect details, compare
    if MODEL_INTEGRATED:
        try:
            with st.spinner("Analyzing image..."):
                result = _run_ai_model(image)
        except Exception as exc:  # noqa: BLE001 - show any model failure clearly
            st.error(f"Analysis failed: {exc}")
            return
        _render_result(result["status"], result.get("defects", []), image,
                       result.get("analysed_image"), mode="real")
    elif show_sample:
        defects = SAMPLE_RESULTS[sample_status]["defects"]
        analysed = _draw_sample_overlay(image, defects)
        _render_result(sample_status, defects, image, analysed, mode="sample")
    else:
        _render_result("NOT INTEGRATED", [], image, None, mode="none")


# ---------------------------------------------------------------- standalone
if __name__ == "__main__":
    st.set_page_config(page_title="Inspect Metal Part | PartSight Pro",
                       page_icon="🔩", layout="wide")
    render_inspect_page()
