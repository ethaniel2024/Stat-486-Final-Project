# STAT 486 Final Project — Broadway Box Office Forecasting

**Team:** Scott, Monte, and Ethan  
**Course:** BYU STAT 486 — Fall 2026  
**Project Route:** C — Build a Dataset and Develop an ML Pipeline

## Project Overview

Our project investigates whether historical Broadway box-office performance can predict a show's gross revenue in a subsequent week. We are building a custom dataset of weekly Broadway show-level box-office observations and will compare a simple previous-week baseline with more advanced predictive models.

Our goal is to determine whether additional historical information and show characteristics improve forecasting accuracy. Our primary evaluation metric is Mean Absolute Error (MAE), with Root Mean Squared Error (RMSE) as a secondary metric.

## October 27, 2026 — Project Plan Checkpoint

### Research question and motivation

Can historical Broadway box-office data be used to predict a show's gross revenue in a subsequent week?

We chose this question because Broadway shows vary in ticket prices, attendance, theater capacity, and number of performances. Their weekly financial performance can also change over time. We want to investigate how much these factors, combined with recent performance, can help predict future revenue.

### Data and project approach

We selected **Route C: Build a Dataset and Develop an ML Pipeline**. Our team is collecting weekly Broadway box-office statistics and organizing them into a reproducible dataset.

Each observation represents one Broadway show during one reporting week. Potentially useful variables include show name, theater, weekly gross, ticket prices, attendance, theater capacity, performance counts, percentage of capacity sold, week-ending date, and Tony-related information.

### Proposed modeling approach

We proposed comparing a simple persistence baseline—which predicts a show's next week's gross using its most recent gross—with more advanced regression and machine-learning methods. Potential models include regularized linear regression and random forest regression.

### Evaluation plan

We planned to use a chronological training and testing split, evaluating models on later weeks that were not used for training. MAE will be our primary metric because it communicates prediction error in dollars. RMSE will provide a secondary measure that places greater weight on large errors.

We will avoid data leakage by ensuring that predictors use only information available before the week being predicted. Our comparisons will use the same held-out period and metrics.

## November 5, 2026 — Data and Reference Result Checkpoint

### Data acquisition and preparation

We collected weekly Broadway box-office data using a custom Python web-scraping notebook that retrieves weekly show-level statistics from Playbill. We also incorporated Tony Award for Best Musical nomination information and extracted show and theater names into separate fields.

- [Acquisition notebook](acquisition/PlaybillScrape.ipynb)
- [Original collected data](data/raw/Uncleaned_Broadway_Data.csv)
- [Processed dataset](data/processed/Broadway_Data.csv)

The current processed dataset contains **7,371 show-week observations across 11 columns**, representing **207 distinct show names and 253 reporting weeks**. The date range is January 2, 2022, through November 1, 2026.

Initial data inspection identified 24 missing values in the Show column and 24 in the Theater column. Some fields also contain concatenated values, particularly average and top ticket prices and seats sold and theater capacity. These fields require additional cleaning before they can be used reliably as model predictors.

The current baseline uses the show identifier, reporting date, and weekly gross, so these remaining cleaning issues do not prevent us from establishing an initial reference result.

### Evaluation plan

We are predicting a show's gross revenue for the following reporting week. We reserved 2026 observations for testing and use a rolling one-week-ahead evaluation.

The persistence baseline predicts a show's gross using its actual gross from exactly one week earlier. Each prediction uses information available before the target week; actual prior-week observations may come from earlier in 2026. This avoids using future observations to predict earlier outcomes.

Our primary metric is Mean Absolute Error (MAE), with Root Mean Squared Error (RMSE) as a secondary metric. Future models will be compared against this baseline using the same evaluation period and metrics.

### First runnable result: Persistence baseline

We implemented and ran a persistence baseline that predicts each show's weekly gross using its gross from the immediately preceding week. Only observations with a prior record for the same show exactly seven days earlier were included.

**Results:**

| Measure | Result |
|---|---:|
| Test observations | 1,346 |
| Test period | January 4 – November 1, 2026 |
| MAE | $138,700.66 |
| RMSE | $222,494.50 |
| Duplicate show-week observations | 0 |

The MAE represents an average absolute prediction error of approximately $138,701 per show-week observation. RMSE is higher because it gives greater weight to larger prediction errors.

This baseline establishes a reference point for evaluating more advanced forecasting models. A future model will need to improve on this result using the same test observations and evaluation metrics to demonstrate predictive value.

- [Baseline results and interpretation](results/baseline_results.md)
- [Baseline implementation](analysis/baseline.py)
- [Individual baseline predictions](results/baseline_predictions.csv)

To reproduce the baseline from the repository root:

```bash
python analysis/baseline.py
```

### Next steps

1. Continue cleaning and validating the dataset, particularly the concatenated ticket-price and seating fields.
2. Investigate missing show and theater identifiers.
3. Develop additional historical and show-level predictors.
4. Implement regularized regression and random forest models.
5. Compare their performance against the persistence baseline using the same chronological evaluation period.

## Repository Organization

```text
Stat-486-Final-Project/
├── README.md
├── project-plan.md
├── acquisition/
│   └── PlaybillScrape.ipynb
├── data/
│   ├── raw/
│   │   └── Uncleaned_Broadway_Data.csv
│   └── processed/
│       └── Broadway_Data.csv
├── analysis/
│   └── baseline.py
└── results/
    ├── baseline_results.md
    └── baseline_predictions.csv
```

## Sources and Acknowledgments

- [Playbill weekly Broadway grosses](https://playbill.com/grosses) — source for weekly box-office data.
- [pandas documentation](https://pandas.pydata.org/docs/) — data acquisition, cleaning, and analysis.
- [scikit-learn documentation](https://scikit-learn.org/stable/) — planned reference for machine-learning models and evaluation.

We will document additional sources, code contributions, and data-use considerations as the project develops.
