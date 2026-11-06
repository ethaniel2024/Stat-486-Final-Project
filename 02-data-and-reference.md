# Data and Reference Result

**Checkpoint:** November 5, 2026  
**Team:** Scott, Monte, and Ethan  
**Date:** November 5, 2026

## Data

### Where did the data come from, and how did you obtain or prepare it?

We collected weekly Broadway box-office data from Playbill using a custom Python web scraper. The acquisition notebook retrieves weekly show-level box-office statistics. We extended the original collection period through November 1, 2026, and incorporated Tony Award for Best Musical nomination information. We also separated the combined show and theater field into individual variables.

- Acquisition code: `acquisition/PlaybillScrape.ipynb`
- Original collected data: `data/raw/Uncleaned_Broadway_Data.csv`
- Processed data: `data/processed/Broadway_Data.csv`

### What data are available to your team now? What remains to be collected or cleaned?

Our current processed dataset contains 7,371 observations and 11 columns, covering January 2, 2022, through November 1, 2026. It includes 207 distinct show names and 253 reporting weeks.

The available variables include show name, weekly gross, gross change, average and top ticket prices, seats sold and theater capacity, performance counts, percentage of capacity sold, week-ending date, Tony nomination status, and theater name.

Initial inspection identified 24 missing values in the Show column and 24 in the Theater column. Several fields also contain concatenated values, particularly average and top ticket prices and seats sold and theater capacity. These fields need additional parsing and validation before they can be used reliably as predictors.

The current baseline only requires show name, week-ending date, and weekly gross, allowing us to establish an initial reference result while additional cleaning continues.

### Route C: What does your first collected and cleaned sample contain?

Our first processed sample contains 7,371 show-week observations across 11 columns. Each row represents one Broadway show during one reporting week. The data cover 207 distinct shows and 253 reporting weeks, from January 2, 2022, through November 1, 2026.

The processed dataset is suitable for an initial forecasting baseline using weekly gross and historical show-level observations. Additional cleaning and validation will be necessary before incorporating all available variables into more advanced models.

## Evaluation Plan

### What comparison, split, metric, or diagnostic will help answer your question? Why?

We are investigating whether historical Broadway performance can predict a show's gross revenue in a subsequent week.

We use a chronological holdout, reserving 2026 observations for testing. Our first reference model is a persistence baseline that predicts a show's gross using its actual gross from exactly one week earlier.

Our primary evaluation metric is Mean Absolute Error (MAE), which communicates the typical absolute prediction error in dollars. We also report Root Mean Squared Error (RMSE), which places greater weight on larger prediction errors.

The baseline evaluation includes 1,346 show-week observations from January 4 through November 1, 2026.

### How will you avoid data leakage or another misleading comparison?

We construct historical predictors by sorting observations by show and week-ending date, then using the previous observation for the same show. For the persistence baseline, we require that the previous observation occurred exactly seven days before the prediction week.

This is a rolling one-week-ahead evaluation: each prediction uses the actual gross from the preceding week, including when that preceding week falls within 2026. No future observations are used to predict earlier weeks.

Future models will be evaluated on the same test observations and metrics to ensure a fair comparison.

## First Runnable Result

### What baseline or other reference did you run? What did it produce?

We implemented a persistence baseline that predicts each show's gross for a given week using that show's actual gross from the previous week.

The baseline produced the following results:

| Measure | Result |
|---|---:|
| Test observations | 1,346 |
| Test period | January 4 – November 1, 2026 |
| Mean Absolute Error (MAE) | $138,700.66 |
| Root Mean Squared Error (RMSE) | $222,494.50 |
| Duplicate show-week observations | 0 |

The MAE indicates an average absolute prediction error of approximately $138,701 per show-week observation. The higher RMSE indicates that larger prediction errors have a greater influence on that metric.

### Where are the code and output? Include the command needed to rerun the result if available.

The relevant files are organized in our repository:

- Acquisition notebook: `acquisition/PlaybillScrape.ipynb`
- Processed dataset: `data/processed/Broadway_Data.csv`
- Baseline implementation: `analysis/baseline.py`
- Baseline results: `results/baseline_results.md`
- Individual predictions: `results/baseline_predictions.csv`

From the repository root, the baseline can be reproduced using:

```bash
python analysis/baseline.py
```

### What did this first result suggest, and what will you try next?

The persistence baseline gives us a concrete reference point for evaluating more advanced forecasting approaches. It provides a simple benchmark based on the assumption that a show's recent weekly gross is informative about its next week's gross.

Our next steps are to finish cleaning the ticket-price and seating variables, investigate missing show and theater identifiers, and develop additional historical and show-level predictors. We then plan to compare regularized regression and random forest models against the persistence baseline using the same chronological evaluation period and metrics.

Our goal is to determine whether the additional complexity and information in these models meaningfully improve predictive accuracy over the simple baseline.