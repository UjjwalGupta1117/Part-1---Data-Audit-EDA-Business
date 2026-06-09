# Retention Strategy
Snapshot date: 2025-09-30 | Total budget: ₹50,000

## Segmentation Logic
Six segments defined using RFM quintile scores plus two composite signals:
- complaint_score = 40% ticket_count_norm + 40% neg_ticket_rate + 20% pct_reopened
- engagement_score = 35% sessions + 20% cart_adds + 20% visit_recency_inv + 15% email_opens + 10% campaign_clicks
Thresholds from actual data quantiles: recency P75=129d, P90=196d; frequency P25=1, P75=5.

## Retention Actions
| Priority | Segment | Action | Cost/Customer |
|---|---|---|---|
| 1 | At-Risk | Personalised email + 15% one-time coupon | ₹18 |
| 2 | Dormant | Win-back: new launch + 20% discount (top-LTV only) | ₹30 |
| 3 | Promising Risers | Free shipping + loyalty enrolment prompt | ₹12 |
| 4 | Discount Dependents | Loyalty points double-up + free sample | ₹15 |
| 5 | Loyal | Tier upgrade notification + early access | ₹8 |
| 6 | Champions | Ambassador invite + thank-you reward | ₹5 |

## Budget Breakdown
| Segment | Budget Share | Allocated | Est. Reach |
|---|---|---|---|
| At-Risk | 35% | ₹17,500 | ~972 |
| Dormant | 20% | ₹10,000 | ~333 |
| Promising Risers | 20% | ₹10,000 | ~833 |
| Discount Dependents | 15% | ₹7,500 | ~500 |
| Loyal | 8% | ₹4,000 | ~500 |
| Champions | 2% | ₹1,000 | ~200 |

## Why At-Risk is Priority 1
1. Highest churn rate among recoverable segments.
2. Meaningful historical monetary value — each saved customer is material LTV.
3. Still within recovery window (Dormant customers have already disengaged psychologically).
4. Lower intervention cost (₹18) than Dormant (₹30).

## What NOT to Do
- Do not blanket-discount Champions or Loyal — trains them to wait for deals.
- Do not run broad Dormant win-back — filter to top-LTV only; math does not support wide spend.
- Always measure incremental lift against a holdout group per segment.
