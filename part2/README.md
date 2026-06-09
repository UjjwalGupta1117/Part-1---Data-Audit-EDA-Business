# Part 2 — RFM Segmentation & Retention Strategy

## Objective
Build RFM customer segments from order data, enrich with support and web engagement signals, assign retention actions, allocate a limited budget, and manually review 10 ambiguous customer cases.

## Folder Structure
```
part2/
├── rfm_segmentation.ipynb    # Main notebook — run this
├── requirements.txt
├── retention_strategy.md     # Static strategy document
├── manual_review_cases.md    # Static manual review document
├── README.md
└── outputs/                  # Generated on notebook run
    ├── segments.csv
    ├── chart_p2_01_rfm_score_dist.png
    ├── chart_p2_02_segments_overview.png
    ├── chart_p2_03_rfm_scores.png
    ├── chart_p2_04_additional_signals.png
    ├── chart_p2_05_scatter.png
    └── chart_p2_06_budget_allocation.png
```

## Setup & Run
```bash
pip install -r requirements.txt

# Place all 7 CSVs in ../data/ then:
jupyter lab rfm_segmentation.ipynb
# Run All Cells (Kernel → Restart Kernel and Run All Cells)
```

## Data Required
All 7 CSVs in `../data/` (same folder used by Part 1).

## Outputs Produced
| File | Description |
|---|---|
| `outputs/segments.csv` | customer_id, segment_name, RFM scores, and all key features |
| `outputs/retention_strategy.md` | Action + cost per segment, budget breakdown |
| `outputs/manual_review_cases.md` | 10 ambiguous customers with reasoning |
| Charts | Segment size, churn rates, RFM profiles, budget allocation, scatter |

## Segmentation Logic Summary

6 segments defined via rules on RFM quintile scores + 2 composite signals:

| Segment | Core Rule |
|---|---|
| Champions | R≥4 AND F≥4 AND M≥4 |
| Dormant Customers | recency > 196d OR frequency = 0 |
| At-Risk Customers | freq ≥ 2 AND (recency > 129d OR complaint_score ≥ 0.25) |
| Loyal Customers | F≥3 AND M≥3 AND recency ≤ 130d |
| Discount Dependents | avg_discount ≥ 0.35 AND freq ≥ 2 |
| Promising Risers | freq ≤ 2 AND recency ≤ 30d AND engagement_score ≥ 0.35 |

**Additional signals:**
- `complaint_score` = 40% ticket_count_norm + 40% neg_ticket_rate + 20% pct_reopened
- `engagement_score` = 35% sessions + 20% cart_adds + 20% visit_recency_inv + 15% email_opens + 10% campaign_clicks
