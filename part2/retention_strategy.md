# Retention Strategy — D2C Churn Capstone Part 2
Snapshot date: 2025-09-30 | Total campaign budget: ₹50,000

---

## Segmentation Logic

Six segments defined using rules applied to RFM quintile scores (1–5) plus two composite signals.

### RFM Scoring
Each dimension is scored 1–5 using quintile bins (equal-frequency):
- **R_score**: inverse rank of `recency_days` — score 5 = purchased most recently
- **F_score**: rank of `frequency` — score 5 = most orders
- **M_score**: rank of `monetary` — score 5 = highest spend

Quintiles are used (not equal-width bins) because distributions are right-skewed.

### Additional Signal 1 — complaint_score (0–1)
```
complaint_score = 0.4 × ticket_count_norm + 0.4 × neg_ticket_rate + 0.2 × pct_reopened
```
Higher = worse support experience = higher churn risk.

### Additional Signal 2 — engagement_score (0–1)
```
engagement_score = 0.35 × sessions_norm + 0.20 × cart_adds_norm
                 + 0.20 × visit_recency_inv + 0.15 × email_opens_norm
                 + 0.10 × campaign_clicks_norm
```
Higher = more active in app/web right now = lower churn risk.

### Segment Rules (applied in priority order)

| Priority | Segment | Rule | Rationale |
|---|---|---|---|
| 1 | Champions | R≥4 AND F≥4 AND M≥4 | Top quintile on all three — brand advocates |
| 2 | Dormant Customers | recency > 196d OR frequency = 0 | Deeply lapsed — evaluated before At-Risk to avoid misclassification |
| 3 | At-Risk Customers | freq ≥ 2 AND (recency > 129d OR complaint_score ≥ 0.25) | Active base sliding away — still within recovery window |
| 4 | Loyal Customers | F≥3 AND M≥3 AND recency ≤ 130d | Consistent, moderate-to-high value buyers |
| 5 | Discount Dependents | avg_discount ≥ 0.35 AND freq ≥ 2 | Buy primarily during promotions |
| 6 | Promising Risers | freq ≤ 2 AND recency ≤ 30d AND engagement ≥ 0.35 | New/low-freq but actively engaged right now |

Thresholds set from actual data quantiles: recency P75 = 129d, P90 = 196d.

---

## Retention Actions Per Segment

| Priority | Segment | Recommended Action | Cost/Customer | Rationale |
|---|---|---|---|---|
| 1 | At-Risk Customers | Personalised re-engagement email + 15% one-time coupon | ₹18 | Highest churn rate among recoverable segments; meaningful past spend; still within window |
| 2 | Dormant Customers | Win-back: new product launch highlight + 20% discount (top-200 by historical LTV only) | ₹30 | Low ROI broadly — filter to high-LTV subset only to justify cost |
| 3 | Promising Risers | Free shipping on next order + loyalty programme enrolment prompt | ₹12 | Low cost to convert; moves customer into habit-forming repeat-purchase zone |
| 4 | Discount Dependents | Loyalty points double-up event + free sample bundle (no direct discount) | ₹15 | Avoid reinforcing discount dependency; shift motivation to loyalty programme value |
| 5 | Loyal Customers | Loyalty tier upgrade notification + early access to new launch | ₹8 | Low churn risk; recognition action is low cost and maintains relationship |
| 6 | Champions | Exclusive brand ambassador invite + personalised thank-you reward | ₹5 | Lowest churn risk; discounts are unnecessary and erode margin |

---

## Budget Allocation (Total: ₹50,000)

| Segment | Budget Share | Allocated (INR) | Est. Customers Reached | Priority Logic |
|---|---|---|---|---|
| At-Risk Customers | 35% | ₹17,500 | ~972 | Highest ROI — high churn × meaningful LTV × recoverable |
| Dormant Customers | 20% | ₹10,000 | ~333 (top-LTV only) | Low success rate broadly; restrict to high-value subset |
| Promising Risers | 20% | ₹10,000 | ~833 | Cheapest conversion; highest future LTV upside |
| Discount Dependents | 15% | ₹7,500 | ~500 | Behavioural shift campaign — no cash discount |
| Loyal Customers | 8% | ₹4,000 | ~500 | Maintenance; low spend needed |
| Champions | 2% | ₹1,000 | ~200 | Recognition only — no promotional spend required |

### Why At-Risk Customers are Priority 1

1. They have the highest churn rate among segments that are still recoverable.
2. Their historical monetary value is material — each saved customer represents significant LTV.
3. They are still within the recovery window. Dormant customers have already psychologically disengaged, making intervention less effective.
4. The intervention cost (₹18/customer) is lower than Dormant (₹30/customer), giving better expected ROI.

### Expected Value Calculation (At-Risk)
```
Budget allocated : ₹17,500
Customers reached: ~972
Assumed save rate : 15-20% of flagged (industry benchmark for personalised email)
Customers saved  : ~145–194
Avg monetary 180d: ~₹2,000 (estimated from segment profile)
Retention value  : ₹290,000–₹388,000
Cost             : ₹17,500
ROI              : ~16–22x on campaign spend
```

---

## What NOT to Do

1. **Do not blanket-discount Champions or Loyal Customers.** This trains high-value customers to wait for promotions, depressing margins without improving retention.
2. **Do not run a broad Dormant win-back campaign.** At ₹30/customer across hundreds of deeply lapsed customers, the math does not support it. Filter strictly to historical LTV > ₹5,000.
3. **Do not run any campaign without a holdout group.** Without a control, it is impossible to isolate the campaign's incremental effect from natural retention.
4. **Do not use discount as the only lever for Discount Dependents.** More discounts deepen the dependency. The goal is to shift their purchase motivation to loyalty programme value.
