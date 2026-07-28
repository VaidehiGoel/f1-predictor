# 🏎️ GridCast — F1 Race Prediction System

A full-stack machine learning system that predicts Formula 1 finishing order from real qualifying and historical data — built end-to-end from data collection through a deployed web app.

Not a toy notebook: this is a production-shaped pipeline with leakage prevention, cold-start handling for new drivers/teams, a real evaluation methodology, a FastAPI backend, and a React/TypeScript frontend.

---

## What it does

Given a race where qualifying has just completed, GridCast predicts the full finishing order for every driver on the grid — using a gradient-boosted ranking model trained on five seasons (2022–2026) of real F1 data via [FastF1](https://github.com/theOehrly/Fast-F1).

**Live demo:** 
**API docs:** 

---

## Why this is harder than it looks

- **2026 introduced major regulation changes** — pre-2026 data is structurally distinct and can't be blended in naively.
- **New teams (Cadillac, Audi) have zero history** — the model can't rely on team identity; it needs cold-start-safe, behavior-based features instead.
- **Predicting "finishing order" is a ranking problem, not a regression problem** — evaluated with per-race Spearman correlation, not just MAE.
- **DNFs are fundamentally unpredictable** from pre-race data alone, and meaningfully suppress any ranking metric — this is measured and reported honestly, not hidden.

---

## Architecture

```
f1-predictor/
├── src/
│   ├── data_collection.py      # FastF1 pulls, rate-limit + missing-session handling
│   ├── data_cleaning.py        # type fixes, leakage/redundant column removal
│   ├── eda.py                  # multi-season aggregation for exploration
│   ├── feature_engineering.py  # leakage-free rolling features, cold-start handling
│   ├── modeling.py             # train/test split, evaluation metrics
│   ├── train_baseline.py       # LinearRegression baseline
│   ├── train_ranker.py         # XGBRanker (production model)
│   ├── predict.py              # real-time prediction assembly
│   └── api.py                  # FastAPI backend
├── configs/config.py            # centralized paths & season list
├── data/                        # raw → processed (gitignored, regenerable)
├── models/                      # trained model + fitted preprocessing values (gitignored)
└── frontend/                    # React + TypeScript + Tailwind
```

---

## The pipeline

**1. Data collection** — Pulls Qualifying + Race results per season via FastF1, with graceful skipping of future/cancelled races and explicit handling of API rate limits (distinct from routine per-race failures).

**2. Cleaning** — Verifies `Position` is trustworthy even for DNFs (F1 classifies retirees by race distance completed), drops redundant/leakage columns (`Time`, `ClassifiedPosition`), converts lap times to numeric seconds while preserving originals.

**3. EDA** — Quantifies the grid-to-finish relationship (0.75 Spearman, excluding DNFs), finds team competitiveness drifts significantly year-over-year (motivating rolling features over static team identity), and investigates real anomalies (e.g., unusually low predictability at Las Vegas) with sample-size discipline throughout.

**4. Feature engineering** — All rolling features (`shift(1)` before rolling) are leakage-free by construction:
- Driver & team recent form (team form computed at the *round* level to avoid distorting rolling windows across two teammates)
- Circuit-specific historical performance
- Teammate gap (isolates driver skill from car performance)
- Team DNF rate
- Cold-start handling: every rolling feature has a paired `HasHistory` flag and a sensible neutral fill (population average or zero), verified against real new-team cases (Cadillac/Bottas)

**5. Modeling** — Baseline `LinearRegression` vs. `XGBRanker` (a true learning-to-rank model). Evaluated with:
- MAE / RMSE (regression sanity check)
- **Per-race Spearman correlation**, averaged across races — computed separately per race since ranking only means something within a competitive group
- A DNF-excluded variant of Spearman, to separate genuine ranking skill from unpredictable race chaos

**6. Prediction pipeline** — Reuses the exact same feature-engineering functions for live prediction by appending a synthetic "upcoming race" row (real qualifying data, unknown target) onto historical data, computing each driver's most recent rolling stats, and converting the ranker's raw relevance scores into a clean 1st–Nth order.

**7. API & frontend** — FastAPI serves predictions and a real-time "available races" list (checked live against FastF1 for the current season, cached at startup for completed seasons). React/TypeScript frontend with a race selector and a styled prediction table.

---

## Results (honest, not cherry-picked)

| Metric | Value |
|---|---|
| Spearman correlation (all races, 2025 test season) | 0.649 |
| Spearman correlation (DNF-excluded) | 0.771 |
| Grid position alone, for comparison | 0.752 (DNF-excluded) |

The model performs close to the ceiling set by grid position alone — the strongest single predictor available. This is expected: F1 outcomes have real, irreducible randomness (crashes, mechanical failures, weather) that no pre-race feature set can fully capture.

**Known limitations:**
- Requires completed qualifying data — does not forecast weeks in advance (grid position and qualifying pace are by far the strongest features, and don't exist before qualifying happens)
- DNFs are not predicted; they're the dominant source of remaining ranking error
- New teams/drivers rely on population-average fallbacks until they accumulate real history

---

## Tech stack

**ML/Backend:** Python, FastF1, pandas, scikit-learn, XGBoost, FastAPI
**Frontend:** React, TypeScript, Vite, Tailwind CSS, React Router
**Practices:** leakage-free time-series feature engineering, per-group ranking evaluation, cold-start handling, model persistence via joblib

---

## Running locally

```bash
# Backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\Activate.ps1 on Windows
pip install -r requirements.txt
python -m src.train_ranker        # trains and saves the model
uvicorn src.api:app --reload      # runs the API on :8000

# Frontend
cd frontend
npm install
npm run dev                        # runs on :5173
```

---

## What I'd build next

- Weather data as a feature (directly affects tire strategy and incident rate)
- A second, lower-confidence "pre-qualifying" prediction mode for weeks-ahead forecasts
- Automated periodic refresh of the current-season race-availability cache
