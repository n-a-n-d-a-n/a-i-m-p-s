# AI Model Performance Simulator

> A full-stack ML deployment tool that stress-tests classification models under controlled real-world data degradation — noise, drift, imbalance, missing values, label noise, outliers, and feature corruption.

**Stack:** FastAPI · React · Vite · Tailwind CSS · scikit-learn · Plotly.js · Render

---

## Streamlit SaaS Dashboard

The Streamlit application has been refactored from a single page into a polished multipage AI dashboard platform. It preserves the original simulator logic from `backend/core/` while adding reusable UI components, session state management, Plotly dashboards, saved-run analytics, dataset profiling, system status, and settings screens.

### Run The Streamlit App

```bash
python3 -m pip install -r requirements.txt
python3 -m streamlit run Dashboard.py
```

Local app URL:

```text
http://localhost:8501
```

### Streamlit Folder Structure

```text
AI-Model-Performance-Simulator/
├── Dashboard.py
├── pages/
│   ├── 2_Model_Simulator.py
│   ├── 3_Results_Analytics.py
│   ├── 4_Model_Comparison.py
│   ├── 5_Dataset_Info.py
│   ├── 6_About_Project.py
│   ├── 7_System_Status.py
│   ├── 8_Settings.py
│   └── 9_Simulation_History.py
├── components/
│   ├── cards.py
│   ├── charts.py
│   ├── metrics.py
│   ├── navbar.py
│   └── theme.py
├── utils/
│   ├── data.py
│   ├── simulator.py
│   └── state.py
├── assets/
│   ├── animations/
│   ├── backgrounds/
│   ├── css/
│   └── icons/
└── requirements.txt
```

### What Each Area Does

| Area | Purpose |
|---|---|
| `Dashboard.py` | Main dashboard entrypoint with KPI cards, hero, recent runs, and performance overview. |
| `pages/2_Model_Simulator.py` | Preserves and upgrades the original simulator workflow: dataset input, model selection, distortion controls, run/save/export. |
| `pages/3_Results_Analytics.py` | Reliability horizons, degradation tables, per-distortion analysis, confusion matrix artifacts, recommendation output. |
| `pages/4_Model_Comparison.py` | Multi-model leaderboard, aggregate metrics, robustness ranking, and radar comparison. |
| `pages/5_Dataset_Info.py` | Built-in dataset profiling and custom CSV preprocessing diagnostics. |
| `pages/6_About_Project.py` | Visual project overview, objectives, architecture diagram, future scope. |
| `pages/7_System_Status.py` | CPU, memory, uptime, run count, runtime diagnostics, operational log panel. |
| `pages/8_Settings.py` | Theme preference, default model preferences, reliability threshold, settings export/import. |
| `pages/9_Simulation_History.py` | Full saved-run archive with expanded charts, artifact images, and CSV-backed result tables. |
| `components/` | Reusable UI blocks for theme, cards, metrics, navigation, and Plotly charts. |
| `utils/` | Shared session state, data loading, saved-run helpers, and centralized simulator orchestration. |

### Preserved Core Functionality

- 7 supported models: Random Forest, Logistic Regression, SVM, Decision Tree, KNN, Gradient Boosting, XGBoost.
- Built-in datasets and custom CSV classification uploads.
- 8 distortion types: Gaussian noise, covariate drift, distribution shift, class imbalance, missing values, label noise, outliers, feature corruption.
- Metrics: accuracy, precision, recall, F1, ROC-AUC, confidence.
- Reliability horizons, degradation summaries, confusion matrices, recommendation scoring, saved run artifacts, CSV exports.

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────┐
│                   React Frontend                     │
│   Vite · Tailwind CSS · Zustand · Plotly.js          │
│                                                      │
│   Step 1     Step 2     Step 3     Step 4            │
│   Dataset  → Config   → Run     → Results            │
│                                                      │
│   Step 5     Step 6     Step 7                       │
│   Analysis → Recommend → History                     │
└───────────────────────┬──────────────────────────────┘
                        │ REST + SSE
┌───────────────────────▼──────────────────────────────┐
│                  FastAPI Backend                     │
│                                                      │
│   POST /api/simulate   ← SSE streaming               │
│   POST /api/analysis                                 │
│   POST /api/recommend                                │
│   GET  /api/history                                  │
└───────────────────────┬──────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────┐
│                  backend/core/                       │
│                                                      │
│   model.py                 → 7 sklearn models        │
│   distortions.py           → 8 distortion types      │
│   evaluation.py            → 6 metrics               │
│   distortion_analysis.py   → per-distortion engine   │
│   degradation_analysis.py  → robustness scoring      │
│   confusion_matrix_analysis.py                       │
│   reliability_analysis.py  → horizon tracker         │
│   recommendation_engine.py → composite scoring       │
│   run_logger.py            → save/load runs          │
└──────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
AI-Model-Performance-Simulator/
│
├── backend/
│   ├── main.py                      ← FastAPI app entry point
│   ├── routes/
│   │   ├── simulate.py              ← POST /api/simulate (SSE)
│   │   ├── analysis.py              ← POST /api/analysis
│   │   ├── recommend.py             ← POST /api/recommend
│   │   └── history.py               ← GET  /api/history
│   ├── core/
│   │   ├── model.py                 ← 7 models + dataset loading
│   │   ├── distortions.py           ← 8 distortion functions
│   │   ├── evaluation.py            ← 6 metrics
│   │   ├── distortion_analysis.py
│   │   ├── degradation_analysis.py
│   │   ├── confusion_matrix_analysis.py
│   │   ├── reliability_analysis.py
│   │   ├── recommendation_engine.py
│   │   └── run_logger.py
│   ├── results/                     ← saved runs (gitignored)
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                  ← step router
│   │   ├── api.js                   ← all fetch calls
│   │   ├── store.js                 ← Zustand global state
│   │   ├── pages/
│   │   │   ├── Step1_Dataset.jsx
│   │   │   ├── Step2_Config.jsx
│   │   │   ├── Step3_Run.jsx
│   │   │   ├── Step4_Results.jsx
│   │   │   ├── Step5_Analysis.jsx
│   │   │   ├── Step6_Recommend.jsx
│   │   │   └── Step7_History.jsx
│   │   └── components/
│   │       ├── StepNav.jsx
│   │       ├── MetricChart.jsx
│   │       ├── RadarChart.jsx
│   │       └── ConfusionMatrix.jsx
│   └── package.json
│
├── Dashboard.py                     ← Streamlit dashboard entrypoint
├── render.yaml                      ← Render deployment config
├── .gitignore
└── README.md
```

---

## 🚀 Local Development

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Swagger UI → `http://localhost:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App → `http://localhost:5173`

### Streamlit Dashboard

```bash
pip install -r requirements.txt
streamlit run Dashboard.py
```

---

## 🔌 API Reference

### `POST /api/simulate`

Streams progress via Server-Sent Events, then returns full results.

**Request:**
```json
{
  "dataset": "iris",
  "models": ["Random Forest", "Logistic Regression"],
  "distortion_type": "noise",
  "levels": [0.0, 0.1, 0.2, 0.3, 0.4]
}
```

**SSE stream:**
```
data: {"step": 1, "total": 5, "level": 0.0, "done": false}
data: {"step": 2, "total": 5, "level": 0.1, "done": false}
...
data: {"done": true, "results": [...]}
```

### `POST /api/analysis`

Returns per-distortion metrics, degradation %, and reliability scores.

```json
{ "results": [ ...simulate results array... ] }
```

### `POST /api/recommend`

Returns composite scores and the recommended model.

```json
{
  "results": [ ...simulate results array... ],
  "weights": { "accuracy": 0.4, "f1": 0.3, "robustness": 0.3 }
}
```

### `GET /api/history`

Returns all saved simulation runs from `backend/results/`.

---

## 🤖 Models

| Model | Details |
|---|---|
| Random Forest | 100 estimators |
| Logistic Regression | max_iter=2000 |
| SVM | RBF kernel, probability=True |
| Decision Tree | Default sklearn |
| KNN | 5 neighbors |
| Gradient Boosting | 100 estimators |
| XGBoost | 100 estimators, mlogloss eval metric |

---

## 📊 Metrics Tracked

| Metric | Description |
|---|---|
| Accuracy | Overall correct predictions |
| Precision (macro) | Avg precision across all classes |
| Recall (macro) | Avg recall across all classes |
| F1 Score (macro) | Harmonic mean of precision & recall |
| ROC-AUC | Discrimination ability across classes |
| Confidence | Mean max prediction probability |

---

## 💥 Distortion Types

| Type | Parameter | Effect |
|---|---|---|
| Gaussian Noise | `noise_level` | Random noise added to features |
| Data Drift | `drift_level` | Feature mean shift over time |
| Distribution Shift | `dist_shift_level` | Feature variance change |
| Missing Values | `missing_level` | Random NaN injection |
| Class Imbalance | `imbalance_level` | Minority class undersampling |
| Label Noise | `label_noise_level` | Random label flipping |
| Outliers | `outlier_level` | Extreme value injection |
| Feature Corruption | `corruption_level` | Feature columns zeroed out |

---

## 📉 Degradation Analysis

Tracks how fast each model degrades as distortion increases.

| Metric | Description |
|---|---|
| Baseline | Performance at zero distortion |
| Worst | Performance at max distortion |
| Abs Drop | Baseline minus Worst |
| % Drop | Percentage of baseline lost |
| Deg Rate/Level | Performance lost per distortion unit |
| Robustness Score | AUC under performance curve, 0–100 |

**Robustness tiers:**

| Score | Tier |
|---|---|
| 90–100 | Excellent |
| 75–89 | Good |
| 55–74 | Moderate |
| 0–54 | Fragile |

---

## ⏱️ Reliability Horizon

Identifies the exact distortion level at which each model becomes untrustworthy.

- Set a reliability threshold (e.g. accuracy ≥ 0.75)
- Simulator interpolates the precise crossing point per model
- Auto-suggests threshold at 80% of best model's clean baseline
- Models that never drop below threshold → **Always Reliable**

---

## 🏆 Recommendation Engine

Composite score combining three sub-scores with adjustable weights:

| Sub-score | What it measures | Default weight |
|---|---|---|
| Robustness Score | AUC under accuracy curve, 0–100 | 40% |
| Peak Accuracy | Best accuracy across all levels | 35% |
| Stability Score | 1 − std(accuracy) | 25% |

---

## 💾 Run History

Every simulation is saved to `backend/results/run_NNN/`:

```
results/
└── run_001/
    ├── run_001.json
    ├── per_distortion_analysis.csv
    ├── degradation_summary.csv
    ├── reliability_horizons.csv
    └── model_recommendation.csv
```

**JSON structure:**
```json
{
  "run_id": 1,
  "timestamp": "2026-05-01 14:32:00",
  "dataset": "iris",
  "settings": { "max_distortion_level": 0.4, "num_levels": 5 },
  "levels": [0.0, 0.1, 0.2, 0.3, 0.4],
  "results": {
    "Random Forest": [{ "accuracy": 0.95, "f1": 0.94, "roc_auc": 0.99 }]
  },
  "degradation": [{ "Model": "Random Forest", "Robustness Score": 91.2 }],
  "reliability": { "threshold": 0.75, "horizons": [] },
  "recommendation": [{ "Model": "Random Forest", "Composite Score": 0.934 }]
}
```

---

## 🧪 Tests

```bash
cd backend
pytest tests/test_simulator.py -v
```

---

## 📦 Requirements

```
fastapi
uvicorn
scikit-learn
numpy
pandas
matplotlib
xgboost
python-multipart
pydantic
```

---

## 🚢 Build Status

| Session | Status | What was built |
|---|---|---|
| Session 1 | ✅ Complete | FastAPI backend — all 4 routes, core wrappers |
| Session 2 | ✅ Complete | React frontend Steps 1–3, Tailwind dark theme, SSE progress bar |
| Session 3 | ⏳ Pending | Results charts, Analysis tabs, Recommend page |
| Session 4 | ⏳ Pending | History page, Render deployment |

---

## 🔑 Key Design Decisions

**Why SSE over polling for the progress bar?**
SSE streams each distortion level result as it completes, giving genuine real-time feedback. Polling would require a separate status endpoint and introduce latency between completion and UI update.

**Why area under the curve for robustness score?**
A model that degrades slowly is more robust than one that holds well then suddenly collapses. AUC captures the full trajectory, not just the endpoint.

**Why interpolate the reliability horizon?**
A coarse distortion grid means the true crossing point sits between two measured levels. Linear interpolation gives a precise horizon rather than just the last known good level.

**Why a composite score for recommendation?**
No single metric captures deployment readiness. High peak accuracy with poor stability is risky in production. The composite score balances robustness, accuracy, and stability — with user-adjustable weights.

**Why auto-suggest the reliability threshold?**
A fixed default of 0.75 fails on hard datasets where even the best model scores 0.50 at baseline. Auto-suggesting 80% of the best baseline always produces meaningful results.
