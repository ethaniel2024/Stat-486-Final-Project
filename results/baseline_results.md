# Persistence Baseline Results

## Evaluation Setup

The initial reference model uses a persistence approach: each show's predicted gross for a given week is equal to that show's gross from the previous week.

The evaluation uses a chronological holdout:
- **Test period:** 2026
- **Prediction requirement:** The show must have an observation exactly seven days before the prediction week.
- **Primary metric:** Mean Absolute Error (MAE)
- **Secondary metric:** Root Mean Squared Error (RMSE)

This is a rolling one-week-ahead evaluation. Each prediction uses the show's actual gross from the immediately preceding week, including when that preceding week is within 2026. No future observations are used to make predictions.

## Results

| Metric | Result |
|---|---:|
| Test observations | 1,346 |
| Test period | January 4, 2026 – November 1, 2026 |
| MAE | $138,700.66 |
| RMSE | $222,494.50 |
| Duplicate show-week observations | 0 |

## Interpretation

The baseline's MAE indicates an average absolute prediction error of approximately $138,701 per show-week observation.

The RMSE is higher than the MAE because it gives greater weight to larger prediction errors. This suggests that some predictions have substantially larger errors than others.

This result establishes a reference point for evaluating more advanced forecasting approaches. Future models should be evaluated on the same test period using the same metrics so their performance can be compared fairly.

## Next Steps

- Investigate and address missing show and theater names.
- Separate concatenated ticket-price and seating fields into their individual variables.
- Explore additional historical and show-level predictors.
- Develop and evaluate more advanced models against the persistence baseline.
