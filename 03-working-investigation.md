# Working Investigation

**Checkpoint:** November 12, 2026, by 11:59 PM Mountain Time  
**Team:** Scott, Monte, and Ethan  
**Route:** C — Build a Dataset and Develop an ML Pipeline  
**Date:** November 12, 2026

## Working code and evidence

### What part of your investigation runs now?

Two scripts now run end-to-end from the repository root:

1. **`analysis/clean.py`** — reads the processed CSV, parses all concatenated fields, drops 24 rows with missing identifiers, and writes a fully clean dataset to `data/processed/Broadway_Data_Clean.csv`.

2. **`analysis/models.py`** — reads the cleaned dataset, engineers lagged features, trains Ridge regression and Random Forest models on pre-2026 data, evaluates all models on the 2026 holdout, and writes results to `results/model_results.md`, `results/model_predictions.csv`, and `results/actual_vs_predicted.png`.

**Run commands (from the repository root, with the virtual environment activated):**

```bash
python analysis/clean.py
python analysis/models.py
```

A `uv`-managed virtual environment with all dependencies is specified in `pyproject.toml`. To set up:

```bash
uv venv
uv pip install -e .
source .venv/bin/activate
```

### What inputs and steps does the run use?

`clean.py` reads `data/processed/Broadway_Data.csv` (the scraper output from Checkpoint 2) and applies the following transformations:

- Renames all concatenated column headers to their intended names
- Extracts the first and second dollar amounts from the fused `Avg TicketTop Ticket` field into separate `Avg Ticket` and `Top Ticket` columns
- Splits the `Seats SoldSeats in Theatre` field into `Seats Sold` and `Seats In Theatre` using a digit-boundary regex
- Strips currency symbols and casts all numeric fields
- Drops 24 rows with missing `Show` or `Theater` values
- Checks for duplicate show-week records (none found)

`models.py` reads `data/processed/Broadway_Data_Clean.csv` and:

- Creates lag-1 and lag-2 gross features, lag-1 ticket price, lag-1 capacity utilization, and lag-1 performance count per show
- Requires that the prior observation is exactly seven days earlier (same constraint as the persistence baseline)
- Trains on all observations before January 1, 2026, and evaluates on 2026 observations
- Reports MAE and RMSE for the persistence baseline, Ridge regression, and Random Forest

### What comparison or diagnostic did you run?

We used the same chronological holdout (test = 2026, 1,346 observations, January 4 – November 1, 2026) and the same metrics (MAE, RMSE) established at Checkpoint 2.

| Model | MAE | RMSE |
|---|---:|---:|
| Persistence baseline | $138,700.66 | $222,494.50 |
| Ridge regression | $135,061.38 | $213,089.77 |
| **Random Forest** | **$134,421.03** | **$208,620.92** |

Both models outperform the baseline. Random Forest achieves the best result, reducing MAE by approximately $4,280 (−3.1%) and RMSE by approximately $13,874 (−6.2%) relative to persistence.

## Route C: New dataset and ML pipeline

### Where are the collection, cleaning, and integration scripts?

| Step | Script | Output |
|---|---|---|
| Acquisition | `acquisition/PlaybillScrape.ipynb` | `data/raw/Uncleaned_Broadway_Data.csv` |
| Initial processing | (scraper output) | `data/processed/Broadway_Data.csv` |
| Full cleaning | `analysis/clean.py` | `data/processed/Broadway_Data_Clean.csv` |
| Modeling | `analysis/models.py` | `results/model_results.md`, `results/model_predictions.csv`, `results/actual_vs_predicted.png` |

Run order: `PlaybillScrape.ipynb` → `clean.py` → `models.py`

Data cover weekly Broadway box-office reporting weeks from January 2, 2022, through November 1, 2026, collected from Playbill in October–November 2026.

### What does one cleaned observation represent?

One observation represents one Broadway show during one reporting week. The cleaned dataset contains 7,347 show-week observations across 207 distinct shows and 253 reporting weeks (January 2, 2022 – November 1, 2026).

**Quality checks:**

| Check | Result |
|---|---|
| Total rows after cleaning | 7,347 |
| Rows dropped (missing Show/Theater) | 24 |
| Duplicate show-week observations | 0 |
| Missing values — This Week Gross | 0 |
| Missing values — Avg Ticket | 0 |
| Missing values — Pct Cap | 0 |
| Missing values — Perfs | 0 |
| Missing values — Top Ticket | 226 (not used as a predictor) |

The cleaning step resolved 7,121 previously unparseable `Avg Ticket` entries by extracting the first dollar amount from the concatenated `$NNN.NN$NNN.NN` string format produced by the scraper. All other columns are fully populated after dropping missing-identifier rows.

A permissible sample of the cleaned dataset is available at `data/processed/Broadway_Data_Clean.csv`.

### What initial ML result did you obtain using the cleaned output?

Using the cleaned dataset with seven lagged and show-level features, Random Forest achieves an MAE of **$134,421** on the 2026 holdout — a reduction of approximately $4,280 (−3.1%) from the $138,701 persistence baseline. Ridge regression achieves an MAE of **$135,061** (−2.6%).

Random Forest feature importances:

| Feature | Importance |
|---|---:|
| `Lag1_Gross` (prior-week gross) | 41.9% |
| `Lag2_Gross` (two-weeks-prior gross) | 30.5% |
| `Lag1_Avg_Ticket` (prior-week avg ticket price) | 15.0% |
| `Lag1_Pct_Cap` (prior-week capacity utilization) | 7.1% |
| `Week_Of_Year` (seasonal signal) | 3.2% |
| `Lag1_Perfs` (prior-week performance count) | 1.3% |
| `Tony_Flag` (Tony nomination indicator) | 1.0% |

**What the result suggests:** Broadway weekly gross is close to a random walk — prior-week revenue explains the dominant share of variance (72% of feature importance from the two lag terms alone). The modest improvement over the naive baseline indicates that additional show characteristics and ticket-price information do add signal, but the effect is limited. Large individual prediction errors (reflected in the gap between MAE and RMSE) likely correspond to holiday weeks, closing-week spikes, or award-show timing that is not captured in the current feature set.

**Next to investigate:** show age or run-week number, explicit holiday week indicators, and a more careful examination of the highest-error observations.

- [Cleaning pipeline](analysis/clean.py)
- [Model pipeline](analysis/models.py)
- [Model results and interpretation](results/model_results.md)
- [Per-observation predictions](results/model_predictions.csv)
- [Actual vs. predicted plot](results/actual_vs_predicted.png)

## Next question

### Did your plan change since November 5?

The overall plan has not changed. We anticipated developing additional features and comparing regularized regression and random forest models, which we have now done. The main adjustment is that the full cleaning step was more involved than expected: the `Avg Ticket` field required regex extraction of the first dollar amount from concatenated strings, rather than a simple currency strip.

### What is uncertain or blocked?

The improvement over the baseline is real but modest. It is uncertain whether additional features (show age, holiday indicators, cast or marketing information not in the dataset) would produce a meaningfully larger improvement, or whether the revenue process is sufficiently close to a random walk that the ceiling is near the current result.

The `Seats In Theatre` field shows some implausible values (minimum of 1 seat), suggesting the seat-splitting regex may misparse some edge cases. This field is not currently used as a predictor but would require additional validation before use.

If further feature engineering does not reduce MAE meaningfully, we will focus the final report on characterizing the error distribution, identifying which shows and time periods are hardest to predict, and interpreting the feature-importance results rather than pursuing further model complexity.

