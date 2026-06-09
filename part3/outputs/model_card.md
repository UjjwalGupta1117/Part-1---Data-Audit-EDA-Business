# Model Card — D2C Churn Prediction Model
Version: 1.0 | Date: 2025-09-30 | Model: XGBoost Classifier

## Intended Use
- **Primary use**: Score customers on their probability of churning in the next 60 days.
- **Intended users**: CRM / retention team, using scores to prioritise intervention spend.
- **Out-of-scope**: The score should not be used for customer-facing communications, pricing decisions,
  or as a sole basis for cancelling accounts.

## Data
- **Training data**: 2,400 customers, snapshot date 2025-09-30.
- **Features**: 27 features across transactional, behavioural, support, web engagement, and demographic categories.
- **Target**: `churn_next_60d` — 1 if no purchase between 2025-10-01 and 2025-11-29.
- **Data leakage prevention**: All features use data at or before 2025-09-30 only.

## Performance (Test Set)
| Metric | Value |
|---|---|
| AUC-ROC | 0.8608 |
| F1 | 0.8 |
| Recall | 0.8571 |
| Precision | 0.75 |
| Threshold | 0.4 |

## Limitations
1. **Concept drift**: Customer behaviour changes with seasons, promotions, and market conditions.
   The model should be retrained quarterly or when AUC drops below 0.70 on held-out recent data.
2. **New customers**: Customers with < 30 days tenure have no purchase history features.
   Model performance is lower for this group; do not act on scores for sub-30-day customers.
3. **Intervention bias**: If the CRM team acts on model scores, future training data will be
   confounded (the model's own predictions affect the outcome). Monitor with holdout control groups.
4. **Single-channel view**: The model does not capture offline purchases or call-centre interactions.

## Ethical Risks
1. **Disparate impact**: Retention interventions triggered by the model should not systematically
   favour customers from higher-tier cities or specific acquisition channels. Run fairness audits
   quarterly across city_tier, age_group, and acquisition_channel.
2. **Do not use for denial of service**: A high churn score is NOT a signal to downgrade, restrict,
   or otherwise penalise a customer. It is solely a signal to offer a retention incentive.
3. **Transparency**: If a customer asks why they received a promotional offer, the team should be
   able to give a general explanation (e.g., 'we noticed you hadn't visited recently') without
   exposing the model or score.

## Monitoring Needs
- Track AUC and recall on a monthly rolling basis.
- Monitor input feature distributions (PSI — Population Stability Index) for drift.
- Alert if predicted churn rate deviates more than ±10pp from baseline for 2 consecutive weeks.
- Retrain trigger: AUC < 0.70 OR PSI > 0.2 on any top-5 feature OR 3+ months since last retrain.
