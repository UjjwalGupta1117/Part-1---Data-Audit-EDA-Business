"""Find 10 specific customers for manual_review_cases.md"""
import pandas as pd

df = pd.read_csv('segments.csv')

def get_customers(condition, limit=2):
    return df[condition].head(limit)

print("=== Type 1: Boundary Straddle ===")
# At-Risk, recency_days 130-145, complaint_score near zero, frequency >= 3
c1 = get_customers((df['segment'] == 'At-Risk Customers') & (df['recency_days'].between(130, 145)) & (df['complaint_score'] < 0.1) & (df['frequency'] >= 3))
print(c1[['customer_id', 'recency_days', 'complaint_score', 'frequency']])

print("\n=== Type 2: Signal Conflict ===")
# RFM_score >= 12, complaint_score >= 0.20
c2 = get_customers((df['RFM_score'] >= 12) & (df['complaint_score'] >= 0.20))
print(c2[['customer_id', 'RFM_score', 'complaint_score', 'segment']])

print("\n=== Type 3: High LTV + Actual Churn ===")
# monetary >= 5000, At-Risk, churn_next_60d == 1
c3 = get_customers((df['monetary'] >= 5000) & (df['segment'] == 'At-Risk Customers') & (df['churn_next_60d'] == 1))
if len(c3) < 2:
    # Relax segment if needed
    c3 = get_customers((df['monetary'] >= 4000) & (df['churn_next_60d'] == 1) & (df['segment'].isin(['At-Risk Customers', 'Loyal Customers'])))
print(c3[['customer_id', 'monetary', 'segment', 'churn_next_60d']])

print("\n=== Type 4: Dormant But Re-Engaging ===")
# Dormant, sessions_30d > 0
c4 = get_customers((df['segment'] == 'Dormant Customers') & (df['sessions_30d'] > 0))
print(c4[['customer_id', 'segment', 'sessions_30d', 'last_visit_days_ago']])

print("\n=== Type 5: Loyal Discount Buyer ===")
# Discount Dependents, frequency >= 3
c5 = get_customers((df['segment'] == 'Discount Dependents') & (df['frequency'] >= 3))
print(c5[['customer_id', 'segment', 'frequency', 'return_rate', 'avg_discount']])
