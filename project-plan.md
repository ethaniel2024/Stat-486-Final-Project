# STAT 486 Project Plan

**Due:** Tuesday, October 27, 2026, at 11:59 PM Mountain Time  
**Team:** Scott, Monte, Ethan  
**Repository:** https://github.com/ethaniel2024/Stat-486-Final-Project.git  
**Date updated:** 10/27/2026

## Project question and purpose

**What specific question do you want to investigate?**

Can we use historical Broadway box-office data to predict a show's gross revenue in a subsequent week? We will compare a simple baseline with machine-learning models to determine whether additional show characteristics and historical performance improve predictions.

**Why does this question interest your team, and what might someone learn from answering it?**

We are interested in Broadway and in applying machine learning to a real-world dataset. Shows vary in ticket prices, theater capacity, attendance, and number of performances, and their financial performance can change from week to week. This project will let us explore how much these factors, combined with a show's recent performance, can tell us about its future revenue. It will also give us experience building a dataset and taking it through a reproducible machine-learning pipeline.

**What claim or expectation could your evidence support, challenge, or leave uncertain?**

We expect recent gross revenue to be a useful predictor of the following week's revenue, and we expect that adding other relevant features may improve prediction accuracy. We will also investigate whether a nonlinear model performs better than a simpler regression model. Our results may show that more complex models offer little improvement over a basic baseline. Any relationships we identify will be predictive, not necessarily causal.

**What does one observation represent in the data you expect to use?**

One observation represents one Broadway show during one reporting week, identified by the show's name and the week-ending date.

## Chosen route

- [ ] **A. Develop something new** in an ML method or system
- [ ] **B. Kaggle competition** with two meaningfully different pipelines
- [x] **C. Build a dataset** and use it in a reproducible ML pipeline

**Why this route:**

We are building a custom Broadway dataset and already have a preliminary CSV to use as a starting point. Route C lets us focus on making the collection and processing reproducible, then using the resulting dataset to investigate a concrete forecasting question. Our contribution will be the dataset, the processing pipeline, and the evaluation of multiple predictive approaches.

## Data source and access

**What data will you use? Give the dataset, competition, API, or source name and a direct link if available.**

We will use a custom-collected dataset of weekly Broadway box-office statistics. The current CSV contains approximately 4,353 records and 11 columns. We will provide a link to the repository containing our scraper as part of next week's data checkpoint assignment, when the acquisition code is ready to share.

**What does each row or record represent, and which fields are relevant to the question?**

Each row represents a show-week observation. Relevant fields include show name, weekly gross, gross change, average ticket price, attendance, theater capacity, number of performances and previews, percentage of capacity sold, week-ending date, Tony-related information, and theater name. We will verify the definitions of the existing fields before using them in the analysis.

**How will the team obtain the data? Note access requirements, collection dates or versions, and any expected size or compute needs.**

We will use our custom scraper to collect the data and modify or rerun it as needed. We will document the collection date and the weeks covered by the final dataset. The current dataset is small enough to process with standard Python tools on a personal computer, and we do not expect to need specialized computing resources.

**What license, competition rules, privacy, ethical, or other use limits apply? Could any data be restricted or identifying?**

The dataset concerns Broadway show and box-office performance rather than individual people, so we do not expect it to contain personal identifying information. We will document the underlying source and review applicable access, collection, and redistribution terms before sharing the dataset. If redistribution is restricted, we will provide the processing code and instructions for rebuilding the dataset where permitted, and share only data or outputs that we are authorized to distribute.

**What data quality issues might affect the investigation?**

The preliminary CSV contains some concatenated column names and values, including fields that appear to combine ticket-price measures, attendance and theater capacity, and performance counts. We will investigate and correct these issues before modeling. Other potential issues include missing values, duplicate show-week observations, inconsistent show or theater names, unusual values, and changes in reporting over time. We will also verify the meaning and consistency of the Tony-related field.

## Route-specific plan

### Route C: New dataset and ML pipeline

**What useful dataset will you create, and what question will the ML analysis investigate?**

We will create a cleaned, analysis-ready dataset of weekly Broadway show performance. The ML analysis will investigate whether historical performance and other information available before a reporting week can predict that week's gross revenue.

**What source or sources will you combine or collect? Are collection and redistribution permitted?**

We will use our custom scraper to collect weekly Broadway box-office data. If additional show or theater information would materially improve the analysis, we may incorporate supplementary data after verifying that it can be collected and used appropriately. We will document the underlying sources and applicable terms before distributing the resulting dataset.

**What does one observation represent, and what will the dataset schema contain?**

One observation will represent one show during one reporting week. The cleaned schema will include:

- **Identifiers:** show name, theater, and week-ending date.
- **Target:** weekly gross revenue.
- **Historical predictors:** prior-week gross and, where available, prior-week attendance or capacity utilization.
- **Show and schedule characteristics:** theater, Tony-related information, and performance counts when their timing makes them appropriate predictors.
- **Documentation:** field definitions, source information, and notes on cleaning and transformations.

We will retain original fields as needed to validate the cleaning process.

**How will you collect, integrate, clean, or label the data? Which scripts will reproduce these steps?**

We will use our scraper as the starting point and organize the workflow into data acquisition, cleaning, feature engineering, and modeling steps. We will correct malformed fields, convert currency and percentage values to numeric types, standardize dates and identifiers, and check for duplicate observations. We will create lagged variables by ordering records by show and date, ensuring that predictors use only information available before the target week. We will document any exclusions and assumptions.

**How will you record source locations, access or license terms, collection dates or versions, and transformations?**

The repository will identify the scraper and underlying data sources, provide links where available, document the collection date and date coverage, and summarize applicable access or licensing restrictions. The processing code will record the transformations applied to the original data, and the project documentation will explain the resulting fields and assumptions.

**What quality checks will you run?**

We will check for duplicate show-week records, missing or invalid dates, incorrect data types, implausible values, inconsistent identifiers, and missingness in important fields. We will verify that reconstructed fields are consistent with the source wherever possible and that lagged variables are aligned to the correct show and week. We will also check whether the dataset's coverage or reporting conventions change over time.

**Can you preserve a permitted snapshot or small fixture? If raw data cannot be shared, how can an authorized reader rebuild or verify the cleaned data?**

We will preserve a dataset snapshot or small test fixture if permitted by the applicable terms. If the full dataset cannot be redistributed, we will provide the processing code, source references, and instructions for rebuilding the dataset where access permits. A small authorized fixture or synthetic example can demonstrate the cleaning and modeling workflow without sharing restricted records.

**What reference ML method will use the cleaned dataset, and what evidence will show both dataset fitness and ML usefulness?**

We will compare a simple previous-week-gross baseline with regression-based ML methods, likely regularized linear regression and random forest regression. Dataset fitness will be assessed through data-quality checks and verification that the predictors are correctly constructed. ML usefulness will be assessed by comparing predictive performance on later weeks that were not used for training.

## Initial reference and proposed contribution

**What is the simplest credible baseline, reference method, or comparison for your question?**

Our baseline will predict the next week's gross using the show's most recently observed weekly gross. This provides a simple reference point for determining whether additional features and more sophisticated models improve predictions.

**What will your team design, build, collect, or investigate beyond that reference?**

We will develop a reproducible pipeline that takes the acquired data through cleaning, feature engineering, modeling, and evaluation. We will investigate whether additional historical performance measures and show characteristics improve prediction accuracy, and whether a nonlinear model offers a meaningful advantage over a simpler regression model.

**Which choices, code, data, papers, notebooks, packages, or pretrained models will come from others, and how will you credit them?**

We will document the development of our scraper and credit any external resources used in its construction. We expect to use standard Python packages, including pandas and scikit-learn. We will distinguish our own acquisition, cleaning, feature engineering, modeling, and evaluation work from any reused code or external resources. We do not currently plan to use pretrained models.

## Evaluation and evidence

**What evaluation design fits the question and how the data were collected?**

We will use a chronological training and test split, training on earlier weeks and evaluating on later weeks. If the available data support it, we will also use a validation period or expanding-window evaluation to compare model choices. We will ensure that all predictors use information available before the target week and that observations from the future do not leak into training. Records without sufficient history for the required lagged predictors will be handled explicitly.

**What metric or diagnostic will you use, and why does it match the question?**

Our primary metric will be mean absolute error (MAE), measured in dollars, because it communicates the typical size of a revenue-prediction error in an interpretable way. We may also report root mean squared error (RMSE), which places greater weight on large errors.

**How will you compare your work with a baseline or other reference? What would count as evidence against your initial expectation?**

All models will be evaluated on the same held-out weeks and compared against the previous-week-gross baseline. Our expectation would be challenged if the more complex models do not consistently reduce test error, perform worse than the baseline, or provide improvements too small to be practically meaningful.

**What informative error, failure, uncertainty, tradeoff, or limitation will you inspect?**

We will examine large prediction errors, performance differences between high- and low-grossing shows, and weeks with unusual revenue changes. We will consider whether the models perform differently across shows or periods and whether a small number of high-revenue observations disproportionately affects the results. The dataset may not capture important factors such as holidays, reviews, cast changes, or marketing activity, which could limit forecasting accuracy.

**What figures, tables, examples, or other outputs could make the results understandable?**

We expect to produce a summary of dataset size, date coverage, missingness, and cleaning decisions; a comparison table of baseline and model performance; a plot of actual versus predicted gross over time; and an analysis of prediction errors across shows or revenue levels. We may also include a feature-importance summary, with appropriate caution that predictive importance does not establish causation.

## Risks and backup scope

**What could prevent the plan from working?**

Potential risks include changes to the source website or scraper, restrictions on data redistribution, malformed or ambiguous fields, insufficient historical records for some shows, and limited project time. More complex models may also fail to improve meaningfully over the baseline.

**What smaller version would still let you answer a useful question if a risk occurs?**

If acquisition or cleaning proves difficult, we will use the existing CSV and focus on a smaller set of reliable fields. We can compare the previous-week-gross baseline with one additional model using gross revenue, show identifiers, dates, and valid lagged predictors. This would preserve the central research question without requiring a larger data collection effort.

**What evidence or feedback would lead you to pivot, and how would you document the reason?**

We will reconsider the scope if key fields cannot be reconstructed reliably, the available history is insufficient, or the source terms prevent our intended data-sharing plan. We may narrow the date range, reduce the number of predictors, or revise the modeling approach. Any significant change will be documented in the repository README and final report.

## Reproducibility and team contributions

**Where will code, configuration, data instructions, and results live in the repository?**

The project repository will contain the acquisition and processing code, modeling and evaluation scripts or notebooks, dependency information, data-access instructions, results, and documentation. The README will explain how to reproduce the workflow. Data will only be committed if the applicable terms permit it.

**What is the first small runnable result you aim to produce, and what will a reader need to reproduce it?**

Our first milestone will be a script or notebook that loads the current CSV, cleans the core fields, produces a basic data-quality summary, and evaluates a previous-week-gross baseline on a chronological split. A reader will need Python, the documented dependencies, and the permitted dataset or access to the original source.

**How will team members contribute substantively and review one another's work?**

Scott, Monte, and Ethan will divide responsibility across data acquisition and documentation, cleaning and feature engineering, and modeling and evaluation. We will review one another's code and analysis, jointly assess the model comparisons, and document individual contributions in the repository and final report.

**What support, approval, or early instructor feedback would help you proceed?**

We would appreciate confirmation that the proposed forecasting task and chronological evaluation design meet the project's expectations for Route C. We would also welcome feedback on whether the proposed baseline and model comparison provide sufficient ML depth and how best to handle data-sharing restrictions if the original records cannot be redistributed.

## Sources

- **Custom Broadway data scraper:** Repository link to be provided with next week's data checkpoint assignment, when the scraper is ready to share.
- [scikit-learn documentation](https://scikit-learn.org/stable/) — reference for implementing regression models and evaluating predictive performance.
- [pandas documentation](https://pandas.pydata.org/docs/) — reference for data cleaning, transformation, and analysis.
