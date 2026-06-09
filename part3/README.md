# Part 3 — Churn Prediction Model & Model Card

## Objective
Build, evaluate, and explain a churn prediction model. Train a Logistic Regression baseline, Random Forest, and XGBoost. Select a business-justified decision threshold. Perform error analysis on specific customers. Produce a model card.

## Folder Structure
```
part3/
├── churn_model.ipynb     # Main notebook — run this
├── requirements.txt
├── error_analysis.md     # Static analysis document
├── model_card.md         # Static model card
├── metrics.json          # Static metrics snapshot
├── README.md
└── outputs/              # Generated on notebook run
    ├── model.pkl
    ├── feature_cols.json
    ├── metrics.json       (also saved here by notebook)
    ├── error_analysis.md  (also saved here by notebook)
    ├── model_card.md      (also saved here by notebook)
    ├── chart_p3_01_roc_threshold.png
    ├── chart_p3_02_confusion_matrix.png
    ├── chart_p3_03_feature_importance.png
    └── chart_p3_04_error_distribution.png
```

## Setup & Run
```bash
pip install -r requirements.txt

# Place all 7 CSVs in ../data/ then:
jupyter lab churn_model.ipynb
# Run All Cells (Kernel → Restart Kernel and Run All Cells)
```

## Data Required
All 7 CSVs in `../data/`. The notebook uses `rfm_modeling_snapshot.csv` as the primary feature table.

## Models Trained

| Model | Type | Notes |
|---|---|---|
| Logistic Regression | Baseline | StandardScaler pipeline; class_weight='balanced' |
| Random Forest | Stronger | 200 trees, max_depth=8, class_weight='balanced' |
| XGBoost | Final / Selected | 300 trees, scale_pos_weight, L1/L2 regularisation |

## Decision Threshold
**Threshold = 0.40** (lowered from default 0.50)

Rationale: False Negative cost (lost LTV ~₹2,000+) >> False Positive cost (wasted campaign spend ~₹18). Lowering the threshold increases recall — we flag more churners — at a controlled precision cost. Threshold is swept and justified with a precision-recall-F1 plot in the notebook.

## Leakage Prevention
- Features: only columns from `rfm_modeling_snapshot.csv` at or before 2025-09-30
- Split: pre-assigned `split` column used — no re-splitting
- Post-snapshot order rows: never used as features
