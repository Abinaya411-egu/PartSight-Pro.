# PartSight Pro

AI-assisted metal surface inspection for a college hackathon. The app runs locally on Windows through VS Code using Streamlit, SQLite, and a real configured model when one is available.

Team: **Innowah Coders** (Hindusthan College of Technology, Salem).

## What works without model weights

- Dashboard, Inspect, History, and About pages
- Image upload and validation (JPG / JPEG / PNG)
- SQLite history that survives Streamlit restarts
- Conservative REVIEW status when inference cannot run
- Unit tests for the database and AI service

## What still requires a real model

Place trained YOLO weights at `models/best.pt`, or set Roboflow credentials in `.env`. Until then, the inspect page will show a setup message and save **REVIEW** records. The app never invents detections.

If you use weights that were **not** trained on metal defects, label that run as a technical smoke test. Do not present those classes as validated scratch/dent/crack findings.

## Windows setup in VS Code

Open this folder as the workspace root: `partsight-pro`.

In the VS Code terminal (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
streamlit run dashboard.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`).

CPU inference is the default (`PARTSIGHT_DEVICE=cpu`). A GPU is not required.

## Prototype PASS / FAIL policy

Copy `.env.example` to `.env` if you need to change policy:

| Variable | Default | Meaning |
| --- | --- | --- |
| `PARTSIGHT_ALLOW_PASS` | `false` | PASS is allowed only when this is true **and** inference succeeded |
| `PARTSIGHT_DEFECT_CLASSES` | empty | Comma-separated class names that may trigger FAIL |
| `PARTSIGHT_FAIL_CONFIDENCE` | `0.50` | Prototype confidence gate for FAIL |

Empty predictions are not treated as proof the part is safe. If defect classes are not configured, detections stay in **REVIEW** instead of becoming FAIL.

## Project layout

```text
partsight-pro/
├── dashboard.py
├── requirements.txt
├── pages/
│   ├── inspect_page.py
│   └── history.py
├── services/
│   ├── ai_service.py
│   ├── database.py
│   └── status_policy.py
├── utils/image_utils.py
├── models/
├── data/
└── tests/
```
