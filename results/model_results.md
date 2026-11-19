# Model Results — Working Investigation

## Evaluation Setup

- **Train period:** pre-2026 (all weeks before January 1, 2026)
- **Test period:** January 2026 – November 2026 (1,346 observations)
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
| Persistence baseline | $138,700.66 | $222,494.50 | — |
| Ridge regression | $135,061.38 | $213,089.77 | -2.6% |
| Random Forest | $134,419.15 | $208,541.73 | -3.1% |

## Random Forest Feature Importances

| Feature | Importance |
|---|---:|
| `Lag1_Gross` | 0.4203 |
| `Lag2_Gross` | 0.3046 |
| `Lag1_Avg_Ticket` | 0.1485 |
| `Lag1_Pct_Cap` | 0.0714 |
| `Week_Of_Year` | 0.0323 |
| `Lag1_Perfs` | 0.0132 |
| `Tony_Flag` | 0.0097 |

## Interpretation

The persistence baseline (MAE \$138,700.66) remains the reference.
Ridge regression improved on the baseline,
and Random Forest improved on it.

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
