"""
history_page.py  -  PartSight Pro | Inspection History page (frontend only)

Usage from dashboard.py (no edits needed in this file):

    from history_page import render_history_page
    render_history_page()

Run standalone to preview:

    streamlit run history_page.py

NOTE: This page uses TEMPORARY SAMPLE DATA (see SAMPLE_INSPECTIONS below).
There is no database or backend connection. To connect real data later,
pass a list of records to render_history_page(records=...) using the same
keys as the sample data, or replace get_inspection_records().
"""

from datetime import datetime
from html import escape
from typing import Dict, List, Optional

import streamlit as st

# --------------------------------------------------------------------------
# TEMPORARY SAMPLE DATA  (dummy records - not real inspections)
# --------------------------------------------------------------------------
SAMPLE_INSPECTIONS: List[Dict] = [
    {"id": "INS-1001", "image": "gear_housing_001.jpg",   "timestamp": datetime(2026, 10, 23, 9, 12),  "status": "PASS",   "defect": "None"},
    {"id": "INS-1002", "image": "gear_housing_002.jpg",   "timestamp": datetime(2026, 10, 23, 9, 18),  "status": "FAIL",   "defect": "Crack"},
    {"id": "INS-1003", "image": "brake_disc_014.png",     "timestamp": datetime(2026, 10, 23, 9, 41),  "status": "REVIEW", "defect": "Surface scratch"},
    {"id": "INS-1004", "image": "brake_disc_015.png",     "timestamp": datetime(2026, 10, 23, 10, 5),  "status": "PASS",   "defect": "None"},
    {"id": "INS-1005", "image": "piston_ring_207.jpg",    "timestamp": datetime(2026, 10, 22, 15, 30), "status": "FAIL",   "defect": "Deformation"},
    {"id": "INS-1006", "image": "piston_ring_208.jpg",    "timestamp": datetime(2026, 10, 22, 15, 36), "status": "PASS",   "defect": "None"},
    {"id": "INS-1007", "image": "valve_body_330.jpeg",    "timestamp": datetime(2026, 10, 22, 11, 2),  "status": "REVIEW", "defect": "Porosity"},
    {"id": "INS-1008", "image": "valve_body_331.jpeg",    "timestamp": datetime(2026, 10, 22, 11, 9),  "status": "FAIL",   "defect": "Corrosion"},
    {"id": "INS-1009", "image": "shaft_coupling_048.jpg", "timestamp": datetime(2026, 10, 21, 16, 47), "status": "PASS",   "defect": "None"},
    {"id": "INS-1010", "image": "shaft_coupling_049.jpg", "timestamp": datetime(2026, 10, 21, 16, 52), "status": "FAIL",   "defect": "Missing hole"},
    {"id": "INS-1011", "image": "bearing_cap_512.png",    "timestamp": datetime(2026, 10, 21, 10, 20), "status": "REVIEW", "defect": "Dent"},
    {"id": "INS-1012", "image": "bearing_cap_513.png",    "timestamp": datetime(2026, 10, 21, 10, 26), "status": "PASS",   "defect": "None"},
]

STATUS_OPTIONS = ["All", "PASS", "FAIL", "REVIEW"]

# Status colours: (text, background, dot)
STATUS_COLORS = {
    "PASS":   ("#116b3a", "#e3f4ea", "#1f9d55"),
    "FAIL":   ("#9b1c1c", "#fde8e8", "#d93030"),
    "REVIEW": ("#8a5a00", "#fff3d6", "#e0a100"),
}

# --------------------------------------------------------------------------
# Styling
# --------------------------------------------------------------------------
_CSS = """
<style>
.psh-title { font-size: 2rem; font-weight: 700; color: #14213d; margin: 0 0 .15rem 0; }
.psh-sub   { color: #5b6577; margin: 0 0 1.1rem 0; font-size: .95rem; }

.psh-sample-note {
    background: #eef3ff; border: 1px solid #c9d8ff; color: #23407a;
    border-radius: 8px; padding: .55rem .85rem; font-size: .85rem; margin-bottom: 1.1rem;
}

.psh-cards { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-bottom: 1.4rem; }
.psh-card {
    background: #ffffff; border: 1px solid #e3e8ef; border-radius: 10px;
    padding: 14px 18px; border-left-width: 5px;
}
.psh-card .psh-card-label { color: #5b6577; font-size: .85rem; margin-bottom: 2px; }
.psh-card .psh-card-value { color: #14213d; font-size: 1.9rem; font-weight: 700; line-height: 1.2; }
.psh-card.total  { border-left-color: #14213d; }
.psh-card.pass   { border-left-color: #1f9d55; }
.psh-card.fail   { border-left-color: #d93030; }
.psh-card.review { border-left-color: #e0a100; }

.psh-count { color: #5b6577; font-size: .85rem; margin: .2rem 0 .5rem 0; }

.psh-table-wrap { border: 1px solid #e3e8ef; border-radius: 10px; overflow-x: auto; background: #fff; }
table.psh-table { width: 100%; border-collapse: collapse; font-size: .92rem; }
table.psh-table thead th {
    background: #f4f6fa; color: #33405a; text-align: left; font-weight: 600;
    padding: 11px 16px; border-bottom: 1px solid #e3e8ef; white-space: nowrap;
}
table.psh-table tbody td {
    padding: 11px 16px; border-bottom: 1px solid #eef1f6; color: #1f2937; vertical-align: middle;
}
table.psh-table tbody tr:last-child td { border-bottom: none; }
table.psh-table tbody tr:hover td { background: #f8faff; }
.psh-id   { font-weight: 600; color: #14213d; white-space: nowrap; }
.psh-file { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: .85rem; }
.psh-muted { color: #8a93a3; }

.psh-badge {
    display: inline-flex; align-items: center; gap: 6px; padding: 3px 11px;
    border-radius: 999px; font-size: .78rem; font-weight: 600; white-space: nowrap;
}
.psh-badge .psh-dot { width: 7px; height: 7px; border-radius: 50%; display: inline-block; }

.psh-empty {
    border: 1px dashed #c4ccd9; border-radius: 10px; background: #fafbfd;
    padding: 2.4rem 1rem; text-align: center; color: #5b6577;
}
.psh-empty .psh-empty-title { font-size: 1.05rem; font-weight: 600; color: #33405a; margin-bottom: .25rem; }

@media (max-width: 760px) {
    .psh-cards { grid-template-columns: repeat(2, 1fr); }
}
</style>
"""


# --------------------------------------------------------------------------
# Data helpers
# --------------------------------------------------------------------------
def get_inspection_records() -> List[Dict]:
    """Return the records shown on the page.

    Currently returns TEMPORARY SAMPLE DATA. Replace this body later when a
    real data source is available.
    """
    return SAMPLE_INSPECTIONS


def _count_by_status(records: List[Dict]) -> Dict[str, int]:
    counts = {"PASS": 0, "FAIL": 0, "REVIEW": 0}
    for rec in records:
        status = str(rec.get("status", "")).upper()
        if status in counts:
            counts[status] += 1
    return counts


def _filter_records(records: List[Dict], query: str, status: str) -> List[Dict]:
    query = query.strip().lower()
    result = []
    for rec in records:
        if status != "All" and str(rec.get("status", "")).upper() != status:
            continue
        if query and query not in str(rec.get("image", "")).lower():
            continue
        result.append(rec)
    # newest first
    return sorted(result, key=lambda r: r.get("timestamp") or datetime.min, reverse=True)


# --------------------------------------------------------------------------
# HTML builders
# --------------------------------------------------------------------------
def _summary_cards_html(total: int, counts: Dict[str, int]) -> str:
    items = [
        ("total", "Total inspections", total),
        ("pass", "PASS", counts["PASS"]),
        ("fail", "FAIL", counts["FAIL"]),
        ("review", "REVIEW", counts["REVIEW"]),
    ]
    cards = "".join(
        f'<div class="psh-card {cls}">'
        f'<div class="psh-card-label">{label}</div>'
        f'<div class="psh-card-value">{value}</div></div>'
        for cls, label, value in items
    )
    return f'<div class="psh-cards">{cards}</div>'


def _status_badge_html(status: str) -> str:
    key = str(status).upper()
    text, bg, dot = STATUS_COLORS.get(key, ("#33405a", "#eceff4", "#8a93a3"))
    return (
        f'<span class="psh-badge" style="color:{text};background:{bg};">'
        f'<span class="psh-dot" style="background:{dot};"></span>{escape(key)}</span>'
    )


def _format_datetime(value: Optional[datetime]) -> str:
    if not isinstance(value, datetime):
        return "-"
    return value.strftime("%d %b %Y, %I:%M %p")


def _table_html(records: List[Dict]) -> str:
    rows = []
    for rec in records:
        defect = str(rec.get("defect", "") or "None")
        defect_cell = (
            f'<span class="psh-muted">{escape(defect)}</span>'
            if defect.lower() == "none"
            else escape(defect)
        )
        rows.append(
            "<tr>"
            f'<td class="psh-id">{escape(str(rec.get("id", "-")))}</td>'
            f'<td class="psh-file">{escape(str(rec.get("image", "-")))}</td>'
            f'<td>{_format_datetime(rec.get("timestamp"))}</td>'
            f'<td>{_status_badge_html(rec.get("status", ""))}</td>'
            f"<td>{defect_cell}</td>"
            "</tr>"
        )
    return (
        '<div class="psh-table-wrap"><table class="psh-table">'
        "<thead><tr>"
        "<th>Inspection ID</th><th>Image filename</th><th>Date and time</th>"
        "<th>Status</th><th>Defect type</th>"
        "</tr></thead>"
        f'<tbody>{"".join(rows)}</tbody></table></div>'
    )


def _empty_state_html(has_any_records: bool) -> str:
    if has_any_records:
        title = "No inspections match your search"
        hint = "Try a different filename or set the status filter to All."
    else:
        title = "No inspection records yet"
        hint = "Inspections will appear here once images have been checked."
    return (
        '<div class="psh-empty">'
        f'<div class="psh-empty-title">{title}</div>'
        f"<div>{hint}</div></div>"
    )


# --------------------------------------------------------------------------
# Public entry point
# --------------------------------------------------------------------------
def render_history_page(records: Optional[List[Dict]] = None) -> None:
    """Render the Inspection History page.

    Args:
        records: Optional list of dicts with keys
                 id, image, timestamp (datetime), status (PASS/FAIL/REVIEW), defect.
                 If omitted, TEMPORARY SAMPLE DATA is used.
    """
    using_sample = records is None
    data = get_inspection_records() if using_sample else records

    st.markdown(_CSS, unsafe_allow_html=True)

    # 1. Page title
    st.markdown('<div class="psh-title">Inspection History</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="psh-sub">Review past inspections, search by image filename and filter by result.</div>',
        unsafe_allow_html=True,
    )

    if using_sample:
        st.markdown(
            '<div class="psh-sample-note"><b>Sample data:</b> the records below are '
            "temporary dummy data for the frontend preview, not real inspections.</div>",
            unsafe_allow_html=True,
        )

    # 2. Summary cards (always based on all records)
    counts = _count_by_status(data)
    st.markdown(_summary_cards_html(len(data), counts), unsafe_allow_html=True)

    # 3 & 4. Search box + status filter
    col_search, col_status = st.columns([3, 1])
    with col_search:
        query = st.text_input(
            "Search by image filename",
            placeholder="Type a filename, e.g. brake_disc",
            key="history_search",
        )
    with col_status:
        status = st.selectbox("Status", STATUS_OPTIONS, key="history_status")

    filtered = _filter_records(data, query, status)

    # 5, 6, 7. Table with status labels, or empty state
    if filtered:
        st.markdown(
            f'<div class="psh-count">Showing {len(filtered)} of {len(data)} inspections</div>',
            unsafe_allow_html=True,
        )
        st.markdown(_table_html(filtered), unsafe_allow_html=True)
    else:
        st.markdown(_empty_state_html(bool(data)), unsafe_allow_html=True)


# Standalone preview: `streamlit run history_page.py`
if __name__ == "__main__":
    st.set_page_config(page_title="Inspection History | PartSight Pro", layout="wide")
    render_history_page()