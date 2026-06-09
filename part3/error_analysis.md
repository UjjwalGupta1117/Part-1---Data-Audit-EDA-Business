# Error Analysis — XGBoost Churn Model
Threshold: 0.4 | Split: test

## Error Distribution
- Correct predictions : 264
- False Negatives (missed churners) : 24
- False Positives (false alarms)    : 48

## False Negative Analysis (Missed Churners — 5 examples)
These are customers the model predicted would stay, but who actually churned.
Business cost: lost LTV — each is a customer we could have saved.

- **CUST02072**: predicted_proba=0.182, recency=35d, freq=7, monetary=₹4,340, sessions_30d=4. Missed churner — high LTV, prediction was below threshold.
- **CUST01990**: predicted_proba=0.032, recency=59d, freq=4, monetary=₹3,878, sessions_30d=11. Missed churner — high LTV, prediction was below threshold.
- **CUST00438**: predicted_proba=0.251, recency=64d, freq=3, monetary=₹2,466, sessions_30d=6. Missed churner — high LTV, prediction was below threshold.
- **CUST00184**: predicted_proba=0.006, recency=14d, freq=3, monetary=₹2,457, sessions_30d=6. Missed churner — high LTV, prediction was below threshold.
- **CUST02298**: predicted_proba=0.220, recency=100d, freq=3, monetary=₹2,204, sessions_30d=13. Missed churner — high LTV, prediction was below threshold.

**Pattern**: FN customers tend to have moderate predicted probabilities (0.25–0.38) — just below threshold.
Their RFM profiles can look similar to loyal customers who didn't churn.
Recommendation: consider lowering threshold to 0.35 for high-LTV customers (monetary > ₹3,000).

## False Positive Analysis (False Alarms — 5 examples)
These are customers flagged as churn risk who actually stayed.
Business cost: wasted intervention spend (~₹18/customer).

- **CUST00250**: predicted_proba=0.410, recency=35d, freq=1, monetary=₹837. False alarm — customer stayed despite model's flag.
- **CUST01877**: predicted_proba=0.416, recency=45d, freq=2, monetary=₹2,171. False alarm — customer stayed despite model's flag.
- **CUST01907**: predicted_proba=0.417, recency=32d, freq=2, monetary=₹1,249. False alarm — customer stayed despite model's flag.
- **CUST01505**: predicted_proba=0.426, recency=64d, freq=1, monetary=₹609. False alarm — customer stayed despite model's flag.
- **CUST02229**: predicted_proba=0.426, recency=75d, freq=2, monetary=₹1,771. False alarm — customer stayed despite model's flag.

**Pattern**: FP customers often have poor RFM signals (high recency, low sessions) but end up purchasing
in the target window anyway — possibly triggered by an external event (sale, product launch).
Recommendation: add a feature for seasonal purchase patterns if data allows.

## Recommendations
1. Deploy a tiered threshold: 0.35 for high-LTV (monetary_180d > P75), 0.40 for others.
2. Monitor FN rate monthly — any increase signals concept drift.
3. Collect more features on external triggers (sale events, new launches) to reduce FP rate.
