# Part 1 — Data Audit, EDA & Business Understanding

## Objective
Load, inspect, and audit all six raw datasets. Perform exploratory analysis, identify churn-risk hypotheses, and write a business memo for leadership.

## Folder Structure
```
part1/
├── eda_audit.ipynb          # Main notebook — run this
├── requirements.txt
├── data_quality_report.md   # Detailed report (static)
├── business_memo.md         # Detailed report (static)
├── README.md
└── outputs/                 # All charts saved here on run
    ├── chart_01_missing_values.png
    ├── chart_02_outlier_boxplots.png
    ├── chart_03_churn_distribution.png
    ├── chart_04_churn_by_demographics.png
    ├── chart_05_rfm_distributions.png
    ├── chart_06_support_tickets.png
    ├── chart_07_web_activity.png
    ├── chart_08_correlation_heatmap.png
    ├── chart_09_hypothesis_h1_h2_h5.png
    └── chart_10_hypothesis_h3_h4.png
```

## Setup & Run
```bash
pip install -r requirements.txt

# Place all 7 CSVs in ../data/ then:
jupyter lab eda_audit.ipynb
# Run All Cells (Kernel → Restart Kernel and Run All Cells)
```

## Data Required
Place these files in `../data/` before running:
- `customers.csv`
- `orders.csv`
- `support_tickets.csv`
- `web_events_snapshot.csv`
- `churn_labels.csv`
- `intervention_history.csv`
- `rfm_modeling_snapshot.csv`

## Outputs Produced
| File | Description |
|---|---|
| `outputs/data_quality_report.md` | Five-pillar DQ audit with treatment recommendations |
| `outputs/business_memo.md` | Non-technical memo for leadership |
| `outputs/chart_01_*.png` through `chart_10_*.png` | 10 charts covering missing values, outliers, churn distributions, RFM, support tickets, web activity, correlation heatmap, and hypothesis evidence |

## Key Findings
1. `loyalty_tier` is null for ~58% of customers — add `is_loyalty_member` flag before modelling.
2. `orders.csv` contains `_DUP` suffix rows and post-snapshot rows — must be removed before feature engineering.
3. `gross_amount` has intentional outliers up to ₹24,789 — Winsorise at 99th percentile for RFM monetary.
4. Five churn-risk hypotheses supported by evidence: recency, single-purchase, support sentiment, web disengagement, loyalty non-enrolment.
