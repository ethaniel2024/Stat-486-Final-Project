"""
models.py — Broadway gross-revenue ML pipeline
STAT 486 Final Project

Reads:  data/processed/Broadway_Data_Clean.csv
Writes: results/model_results.md
        results/model_predictions.csv

Run from the repository root:
    python analysis/models.py
"""

from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "Broadway_Data_Clean.csv"
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------
# 1. Load cleaned data
# ---------------------------------------------------------------------------
df = pd.read_csv(DATA_PATH, parse_dates=["Week Ending"])
df = df.sort_values(["Show", "Week Ending"]).reset_index(drop=True)

# ---------------------------------------------------------------------------
# 2. Feature engineering — lag-1 features (all use prior week only → no leakage)
# ---------------------------------------------------------------------------
grp = df.groupby("Show")

df["Lag1_Gross"]    = grp["This Week Gross"].shift(1)
df["Lag2_Gross"]    = grp["This Week Gross"].shift(2)
df["Lag1_Avg_Ticket"] = grp["Avg Ticket"].shift(1)
df["Lag1_Pct_Cap"]  = grp["Pct Cap"].shift(1)
df["Lag1_Perfs"]    = grp["Perfs"].shift(1)

# Confirm prior observation is exactly 7 days earlier
df["Prev_Week"]  = grp["Week Ending"].shift(1)
df["Days_Between"] = (df["Week Ending"] - df["Prev_Week"]).dt.days

# Tony flag as int
df["Tony_Flag"] = df["Tony Nominated Musical"].fillna(False).astype(int)

# Week-of-year (seasonal signal)
df["Week_Of_Year"] = df["Week Ending"].dt.isocalendar().week.astype(int)

# ---------------------------------------------------------------------------
# 3. Keep only rows with a valid 7-day lag
# ---------------------------------------------------------------------------
df = df[df["Days_Between"] == 7].copy()

FEATURES = [
    "Lag1_Gross",
    "Lag1_Pct_Cap",
    "Lag1_Perfs",
    "Tony_Flag",
    "Week_Of_Year",
]
OPTIONAL_FEATURES = [
    "Lag2_Gross",
    "Lag1_Avg_Ticket",
]
TARGET = "This Week Gross"

# Drop rows missing any required feature or target
df_model = df.dropna(subset=FEATURES + [TARGET]).copy()

# Fill optional features with their median where available, else drop them
for col in OPTIONAL_FEATURES:
    if col in df_model.columns and df_model[col].notna().sum() > 100:
        df_model[col] = df_model[col].fillna(df_model[col].median())
        FEATURES.append(col)
    # else skip — not enough coverage

# ---------------------------------------------------------------------------
# 4. Chronological train / test split  (train = pre-2026, test = 2026)
# ---------------------------------------------------------------------------
train = df_model[df_model["Week Ending"] < "2026-01-01"].copy()
test  = df_model[df_model["Week Ending"] >= "2026-01-01"].copy()

X_train, y_train = train[FEATURES], train[TARGET]
X_test,  y_test  = test[FEATURES],  test[TARGET]

print(f"Train rows: {len(train):,}  |  Test rows: {len(test):,}")
print(f"Test period: {test['Week Ending'].min().date()} – {test['Week Ending'].max().date()}")

# ---------------------------------------------------------------------------
# 5. Persistence baseline (reference — same test set)
# ---------------------------------------------------------------------------
baseline_preds = test["Lag1_Gross"]
baseline_mae   = mean_absolute_error(y_test, baseline_preds)
baseline_rmse  = np.sqrt(mean_squared_error(y_test, baseline_preds))

# ---------------------------------------------------------------------------
# 6. Ridge regression
# ---------------------------------------------------------------------------
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

ridge = Ridge(alpha=1.0)
ridge.fit(X_train_sc, y_train)
ridge_preds = ridge.predict(X_test_sc)
ridge_mae   = mean_absolute_error(y_test, ridge_preds)
ridge_rmse  = np.sqrt(mean_squared_error(y_test, ridge_preds))

# ---------------------------------------------------------------------------
# 7. Random Forest
# ---------------------------------------------------------------------------
rf = RandomForestRegressor(n_estimators=300, max_features="sqrt",
                           random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
rf_preds = rf.predict(X_test)
rf_mae   = mean_absolute_error(y_test, rf_preds)
rf_rmse  = np.sqrt(mean_squared_error(y_test, rf_preds))

# ---------------------------------------------------------------------------
# 8. Print results
# ---------------------------------------------------------------------------
print("\n=== Model Comparison ===")
print(f"{'Model':<20} {'MAE':>14} {'RMSE':>14}")
print("-" * 50)
print(f"{'Persistence baseline':<20} ${baseline_mae:>13,.2f} ${baseline_rmse:>13,.2f}")
print(f"{'Ridge regression':<20} ${ridge_mae:>13,.2f} ${ridge_rmse:>13,.2f}")
print(f"{'Random Forest':<20} ${rf_mae:>13,.2f} ${rf_rmse:>13,.2f}")

# ---------------------------------------------------------------------------
# 9. Feature importance (Random Forest)
# ---------------------------------------------------------------------------
feat_imp = pd.Series(rf.feature_importances_, index=FEATURES).sort_values(ascending=False)
print("\nRandom Forest feature importances:")
print(feat_imp.round(4).to_string())

# ---------------------------------------------------------------------------
# 10. Save predictions CSV
# ---------------------------------------------------------------------------
out = test[["Show", "Week Ending", TARGET, "Lag1_Gross"]].copy()
out["Persistence_Pred"] = baseline_preds.values
out["Ridge_Pred"]       = ridge_preds
out["RF_Pred"]          = rf_preds
out["Persistence_AE"]   = (out[TARGET] - out["Persistence_Pred"]).abs()
out["Ridge_AE"]         = (out[TARGET] - out["Ridge_Pred"]).abs()
out["RF_AE"]            = (out[TARGET] - out["RF_Pred"]).abs()
out.to_csv(RESULTS_DIR / "model_predictions.csv", index=False)
print(f"\nSaved predictions → {RESULTS_DIR / 'model_predictions.csv'}")

# ---------------------------------------------------------------------------
# 11. Actual vs Predicted plot (Random Forest — best model)
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(test["Week Ending"].values, y_test.values,
        label="Actual", linewidth=1.2, alpha=0.8)
ax.plot(test["Week Ending"].values, rf_preds,
        label="Random Forest", linewidth=1.0, alpha=0.8, linestyle="--")
ax.plot(test["Week Ending"].values, baseline_preds.values,
        label="Persistence baseline", linewidth=0.8, alpha=0.5, linestyle=":")
ax.set_title("Broadway Weekly Gross: Actual vs Predicted (2026 test period)")
ax.set_xlabel("Week Ending")
ax.set_ylabel("Weekly Gross ($)")
ax.legend()
ax.yaxis.set_major_formatter(
    matplotlib.ticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M")
)
plt.tight_layout()
plot_path = RESULTS_DIR / "actual_vs_predicted.png"
fig.savefig(plot_path, dpi=150)
plt.close()
print(f"Saved plot → {plot_path}")

# ---------------------------------------------------------------------------
# 12. Write model_results.md
# ---------------------------------------------------------------------------
md = f"""# Model Results — Working Investigation

## Evaluation Setup

- **Train period:** pre-2026 (all weeks before January 1, 2026)
- **Test period:** January 2026 – November 2026 ({len(test):,} observations)
- **Target:** Weekly gross revenue (`This Week Gross`)
- **Primary metric:** Mean Absolute Error (MAE)
- **Secondary metric:** Root Mean Squared Error (RMSE)

## Features Used

| Feature | Description |
|---|---|
| `Lag1_Gross` | Show's gross from exactly one week prior |
| `Lag2_Gross` | Show's gross from two weeks prior |
| `Lag1_Avg_Ticket` | Average ticket price from one week prior |
| `Lag1_Pct_Cap` | Percent of capacity sold from one week prior |
| `Lag1_Perfs` | Number of performances from one week prior |
| `Tony_Flag` | Tony Award for Best Musical nomination (0/1) |
| `Week_Of_Year` | ISO week number (seasonal signal) |

## Results

| Model | MAE | RMSE | vs. Baseline MAE |
|---|---:|---:|---:|
| Persistence baseline | ${baseline_mae:,.2f} | ${baseline_rmse:,.2f} | — |
| Ridge regression | ${ridge_mae:,.2f} | ${ridge_rmse:,.2f} | {((ridge_mae - baseline_mae) / baseline_mae * 100):+.1f}% |
| Random Forest | ${rf_mae:,.2f} | ${rf_rmse:,.2f} | {((rf_mae - baseline_mae) / baseline_mae * 100):+.1f}% |

## Random Forest Feature Importances

| Feature | Importance |
|---|---:|
""" + "\n".join(
    f"| `{feat}` | {imp:.4f} |"
    for feat, imp in feat_imp.items()
) + f"""

## Interpretation

The persistence baseline (MAE \\${baseline_mae:,.2f}) remains the reference.
Ridge regression {"improved" if ridge_mae < baseline_mae else "did not improve"} on the baseline,
and Random Forest {"improved" if rf_mae < baseline_mae else "did not improve"} on it.

The gap between MAE and RMSE across all models reflects the presence of large
prediction errors — likely driven by holiday weeks, closing-week spikes, or
shows with high revenue variance.

## Outputs

- Code: `analysis/models.py`
- Predictions: `results/model_predictions.csv`
- Plot: `results/actual_vs_predicted.png`

To reproduce:

```bash
python analysis/clean.py
python analysis/models.py
```
"""

(RESULTS_DIR / "model_results.md").write_text(md)
print(f"Saved results summary → {RESULTS_DIR / 'model_results.md'}")

