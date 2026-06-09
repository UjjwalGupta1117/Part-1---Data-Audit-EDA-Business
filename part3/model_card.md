# Model Card — D2C Customer Churn Prediction Model
**Version:** 1.0
**Date:** 2025-09-30
**Model type:** XGBoost Binary Classifier
**Owner:** Data Team

---

## 1. Model Details

| Property | Value |
|---|---|
| Algorithm | XGBoost (gradient boosted trees) |
| Task | Binary classification — churn vs no-churn |
| Output | Probability score [0, 1] + binary label at threshold 0.40 |
| Features | 27 features across 5 categories (see Section 3) |
| Training data | 2,400 customers, snapshot 2025-09-30 |
| Framework | xgboost 2.0.3, scikit-learn 1.4.2, Python 3.10 |

**Key hyperparameters:**
- `n_estimators`: 300
- `max_depth`: 5
- `learning_rate`: 0.05
- `subsample`: 0.8
- `colsample_bytree`: 0.8
- `scale_pos_weight`: neg_count / pos_count (handles class imbalance)
- `reg_alpha`: 0.1 (L1), `reg_lambda`: 1.0 (L2)

---

## 2. Intended Use

### Intended use cases
- Score customers on their 60-day churn probability at the monthly snapshot date
- Prioritise which customers receive a retention intervention (email, coupon, personal outreach)
- Allocate campaign budget across RFM segments based on predicted risk level
- Flag high-LTV customers at HIGH risk for escalated personal CRM contact

### Intended users
- CRM / retention team
- Marketing operations
- Customer success managers reviewing high-priority accounts

### Out-of-scope uses
- **Do not use** for customer-facing communications or pricing decisions
- **Do not use** as the sole basis for any punitive action (cancelling accounts, restricting service)
- **Do not use** for customers with `days_since_signup < 90` — insufficient history for reliable scoring
- **Do not use** in real-time (< 1 second) scoring contexts — model is designed for batch monthly runs

---

## 3. Training Data

### Source
`rfm_modeling_snapshot.csv` — pre-built, leakage-free feature table as of 2025-09-30.

### Feature categories

| Category | Features |
|---|---|
| Transactional (RFM) | recency_days, frequency_180d, monetary_180d |
| Behavioural | return_rate_180d, avg_discount_pct_180d, avg_rating_180d, category_diversity_180d |
| Support quality | ticket_count_90d, negative_ticket_rate_90d, avg_resolution_hours_90d |
| Web engagement | sessions_30d, product_views_30d, cart_adds_30d, wishlist_adds_30d, abandoned_carts_30d, email_opens_30d, campaign_clicks_30d, last_visit_days_ago |
| Demographic | city_tier, age_group, acquisition_channel, loyalty_tier, preferred_category, marketing_consent, days_since_signup |
| Engineered | is_loyalty_member (from loyalty_tier null), has_rated (from avg_rating_180d null) |

### Target variable
`churn_next_60d` = 1 if customer made no purchase between 2025-10-01 and 2025-11-29.

### Class distribution
- Overall churn rate: ~47%
- Near-balanced — handled via `scale_pos_weight` in XGBoost

### Leakage prevention
- All features represent state at or before 2025-09-30
- Post-snapshot order rows filtered out before any feature computation
- Pre-assigned `split` column used — no re-splitting that could leak target distribution

### Data splits
| Split | Usage |
|---|---|
| train | Model training |
| validation | Hyperparameter selection, threshold sweep |
| test | Final unbiased evaluation (touched once, after all decisions) |

---

## 4. Performance

*Actual values populated when `churn_model.ipynb` is run.*

| Metric | Validation | Test |
|---|---|---|
| AUC-ROC | 0.8745 | 0.8608 |
| F1 | 0.7723 | 0.8000 |
| Recall | 0.7959 | 0.8571 |
| Precision | 0.7500 | 0.7500 |
| Threshold | 0.40 | 0.40 |

### Threshold justification
Default threshold of 0.50 was lowered to 0.40 because:
- **False Negative cost**: a missed churner represents ~₹2,000+ in lost LTV
- **False Positive cost**: a wasted intervention is ~₹18
- Cost ratio of ~100:1 justifies biasing toward higher recall
- Threshold sweep (Precision-Recall-F1 vs threshold plot) confirms 0.40 as a reasonable operating point

### Metric interpretation for this business
- **AUC-ROC**: Overall discrimination ability — how well the model separates churners from non-churners across all thresholds
- **Recall**: % of actual churners that the model catches — most important business metric
- **Precision**: % of flagged customers who actually churn — governs campaign budget efficiency
- **F1**: Harmonic mean of recall and precision — balanced view

---

## 5. Limitations

1. **Concept drift**: Customer behaviour changes with seasons, promotions, and competitive landscape. The model's training data reflects behaviour up to September 2025. Performance will degrade over time without retraining.

2. **New customers**: Customers with `days_since_signup < 90` have little or no purchase history. The model is poorly calibrated for this group. Do not use scores for sub-90-day customers; apply a separate new-customer onboarding flow.

3. **Intervention bias (feedback loop)**: If the CRM team acts on model scores, future training data becomes confounded. A customer who would have churned but received a retention offer and stayed will be labelled `churn = 0` in future training data — the model learns the intervened outcome, not the counterfactual. Mitigate with holdout control groups.

4. **Single-channel view**: The model does not capture offline purchases, in-store transactions, or call-centre interactions beyond what is in `support_tickets.csv`.

5. **Static categorical encoding**: Categorical features (city_tier, acquisition_channel, etc.) are label-encoded. If new categories appear in production (e.g., a new acquisition channel), the API will fail or produce incorrect scores. Re-encode and retrain when new categories are introduced.

6. **No temporal features**: The model does not capture purchase trends (increasing vs decreasing frequency over time). A customer on a downward trajectory may score lower risk than their trajectory warrants.

---

## 6. Ethical Risks

### Risk 1: Disparate impact across demographic groups
The model uses `age_group`, `city_tier`, and `acquisition_channel` as features. If the model learns that certain demographic groups churn at higher rates, it may systematically direct retention spend toward or away from those groups in ways that are discriminatory.

**Mitigation**: Run quarterly fairness audits. Compute predicted churn rate and intervention rate across `city_tier`, `age_group`, and `acquisition_channel`. If any group's predicted churn rate deviates more than 15 percentage points from the overall rate, investigate before the next campaign.

### Risk 2: Misuse for customer penalisation
A high churn score means "this customer may leave." It does not mean "this customer is less valuable" or "this customer deserves reduced service." The score must only trigger positive interventions.

**Mitigation**: Document explicitly in the retention team's operating procedures that churn scores must not be used to downgrade, restrict, or deprioritise service quality for any customer.

### Risk 3: Transparency and explainability
If a customer asks why they received a promotional offer, the team should be able to give a general and honest explanation (e.g., "we noticed it had been a while since your last order") without exposing the model's internal score or the customer's risk profile.

**Mitigation**: Prepare a standard customer-facing explanation template. Never expose raw probability scores to customers.

### Risk 4: Over-reliance on model scores
The model has measurable error rates. Human CRM knowledge about specific customers should always be able to override a model score. The model is a decision-support tool, not a decision-making authority.

---

## 7. Monitoring Needs

| What to monitor | How | Alert threshold |
|---|---|---|
| AUC on rolling 90-day cohort | Monthly batch evaluation | AUC < 0.70 |
| Recall on rolling 90-day cohort | Monthly batch evaluation | Recall < 0.60 |
| Input feature distributions (PSI) | Monthly PSI on top-5 features | PSI ≥ 0.20 on any feature |
| Predicted churn rate | Daily 7-day rolling mean | ±10pp from 0.47 baseline for 2 weeks |
| API error rate | Real-time APM | 5xx rate > 1% |

**Retraining triggers (any one sufficient):**
- AUC < 0.70 on recent cohort
- Recall < 0.60 on recent cohort
- PSI ≥ 0.20 on any top-5 feature
- Predicted churn rate deviation ±10pp for 2 consecutive weeks
- ≥ 3 months since last retrain
- Major product, pricing, or market change

---

## 8. How to Retrain

1. Collect new `rfm_modeling_snapshot.csv` with updated snapshot date
2. Run `part3/churn_model.ipynb` with updated `DATA_DIR` and `SNAPSHOT_DATE`
3. Review new metrics — ensure AUC ≥ 0.70 and Recall ≥ 0.60 on validation set
4. Update `part4/model/model.pkl` and `part4/model/feature_cols.json`
5. Restart the API: `uvicorn app.main:app --reload`
6. Update this model card with new version number and performance metrics
