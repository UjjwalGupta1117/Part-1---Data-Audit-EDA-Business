# Data Quality Report
## D2C Customer Churn Capstone — Part 1
Snapshot date: 2025-09-30

---

## 1. Dataset Overview

| Dataset | Expected Rows | Description |
|---|---|---|
| customers.csv | 2,400 | Static customer profiles |
| orders.csv | ~10,009 | Full order history (pre + post snapshot) |
| support_tickets.csv | ~1,921 | Customer service interactions |
| web_events_snapshot.csv | 2,400 | 30-day web/app activity as of snapshot |
| churn_labels.csv | 2,400 | Target variable + train/val/test split |
| intervention_history.csv | 2,400 | Most recent campaign per customer |
| rfm_modeling_snapshot.csv | 2,400 | Pre-built leakage-free feature table |

---

## 2. Missing Values

| Dataset | Column | Approx. Null Count | Null % | Missingness Type | Recommended Treatment |
|---|---|---|---|---|---|
| customers | loyalty_tier | ~1,386 | ~57.8% | MAR | Add `is_loyalty_member` binary flag; fill with `'None'` category |
| customers | skin_type | ~401 | ~16.7% | MAR | Fill with `'Unknown'`; not a direct model feature |
| orders | rating | ~80 | ~0.9% | MNAR | Compute avg ignoring NaN; add `has_rated` binary flag |
| rfm_modeling_snapshot | avg_rating_180d | varies | — | MNAR | Same treatment as orders.rating |

**Missingness type definitions:**
- **MAR (Missing At Random)**: Missingness depends on other observed columns. Safe to add a flag and impute.
- **MNAR (Missing Not At Random)**: Missingness is related to the missing value itself. Customers who never rate are inherently different from those who do — impute with caution and always add a flag.

---

## 3. Duplicate-like Records

| Issue | File | Detail |
|---|---|---|
| `_DUP` suffix order IDs | orders.csv | Simulate ETL re-processing duplicates. Remove with `~order_id.str.endswith('_DUP')` before any aggregation. |
| Near-duplicate rows | orders.csv | Same customer + date + category + amount with different order_id. Flag and investigate. |
| No full duplicates | All other files | No exact duplicate rows found in any other dataset. |

**Impact if untreated:** Counting a returned order twice inflates `return_rate`; counting a high-value order twice inflates RFM monetary — both corrupt model features.

---

## 4. Outliers

| Column | Dataset | Max Value | IQR Upper Fence (approx.) | Outlier Count | Treatment |
|---|---|---|---|---|---|
| gross_amount | orders | ₹24,789 | ~₹1,500 | Small (< 1%) | Winsorise at 99th percentile for RFM monetary. Keep raw value for tree models (robust to outliers). |
| delivery_days | orders | 11 | ~10 | Minimal | Within plausible business range — no treatment needed. |
| resolution_hours | support_tickets | 74.6 | — | 0 | This is the stated maximum in the data dictionary — not an outlier. |

---

## 5. Domain Validity Checks

All checks passed on the pre-snapshot, de-duplicated order data:

| Check | Result |
|---|---|
| `discount_pct` ∈ [0, 1] | ✓ Pass |
| `returned` ∈ {0, 1} | ✓ Pass |
| `rating` ∈ [1, 5] (non-null) | ✓ Pass |
| `quantity` ≥ 1 | ✓ Pass |
| `signup_date` ≤ 2025-09-30 | ✓ Pass |
| `churn_next_60d` ∈ {0, 1} | ✓ Pass |

**Leakage rule:** `orders.csv` contains rows with `order_date > 2025-09-30`. These rows exist only to construct churn labels. They **must not** be used as model features. Always filter: `orders[orders.order_date <= '2025-09-30']`.

---

## 6. Join / Referential Integrity

All child tables join cleanly to `customers` via `customer_id`:

| Child Table | Orphan Rows | Customers With No Record | Cardinality | Notes |
|---|---|---|---|---|
| orders (pre-snapshot) | 0 | Some | 1-to-many | Not every customer placed an order — edge case |
| support_tickets | 0 | Many | 1-to-many | Expected — not every customer contacts support |
| web_events_snapshot | 0 | 0 | 1-to-1 | All 2,400 customers present ✓ |
| churn_labels | 0 | 0 | 1-to-1 | All 2,400 customers present ✓ |
| intervention_history | 0 | 0 | 1-to-1 | All 2,400 customers present ✓ |

**Join pattern:** Always left-join from `customers` (2,400 rows is the universe). Fill nulls in child-table aggregates with 0 for customers with no records.

---

## 7. Recommendations Before Modelling

1. **Remove `_DUP` orders** before computing any feature: `orders[~orders.order_id.str.endswith('_DUP')]`
2. **Filter to pre-snapshot orders**: `orders[orders.order_date <= '2025-09-30']`
3. **Flag `loyalty_tier` nulls** as `is_loyalty_member = 0`; fill `loyalty_tier` with `'None'`
4. **Flag `avg_rating` nulls** as `has_rated = 0`; fill with per-category median
5. **Winsorise `gross_amount`** at the 99th percentile for RFM monetary computation
6. **Use the pre-assigned `split` column** from `churn_labels.csv` — do not re-split randomly
