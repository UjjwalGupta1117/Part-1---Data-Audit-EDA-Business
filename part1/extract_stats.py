"""Extract exact statistics for business memo hypotheses."""
import pandas as pd
import numpy as np

# Load data
orders = pd.read_csv('../data/orders.csv')
customers = pd.read_csv('../data/customers.csv')
labels = pd.read_csv('../data/churn_labels.csv')
support = pd.read_csv('../data/support_tickets.csv')
web = pd.read_csv('../data/web_events_snapshot.csv')

# Filter pre-snapshot, non-dup orders
orders = orders[~orders['order_id'].str.endswith('_DUP')]
orders['order_date'] = pd.to_datetime(orders['order_date'])
orders_pre = orders[orders['order_date'] <= '2025-09-30']

# Merge labels
cust_labels = customers.merge(labels[['customer_id','churn_next_60d']], on='customer_id')

# --- Hypothesis 1: Single-purchase vs repeat ---
order_counts = orders_pre.groupby('customer_id').size().reset_index(name='order_count')
h1 = cust_labels.merge(order_counts, on='customer_id', how='left')
h1['order_count'] = h1['order_count'].fillna(0)
h1['buyer_type'] = np.where(h1['order_count'] <= 1, 'single_purchase', 'repeat')
h1_rates = h1.groupby('buyer_type')['churn_next_60d'].agg(['mean','count'])
print("=== H1: Single vs Repeat ===")
print(h1_rates)
single_rate = h1[h1['buyer_type']=='single_purchase']['churn_next_60d'].mean()
repeat_rate = h1[h1['buyer_type']=='repeat']['churn_next_60d'].mean()
single_n = (h1['buyer_type']=='single_purchase').sum()
repeat_n = (h1['buyer_type']=='repeat').sum()
print(f"Single-purchase: {single_rate:.1%} churn rate (n={single_n})")
print(f"Repeat:          {repeat_rate:.1%} churn rate (n={repeat_n})")

# --- Hypothesis 2: Loyalty enrolment ---
h2 = cust_labels.copy()
h2['is_loyalty'] = h2['loyalty_tier'].notna()
h2_rates = h2.groupby('is_loyalty')['churn_next_60d'].agg(['mean','count'])
print("\n=== H2: Loyalty Enrolment ===")
print(h2_rates)
non_enrolled_rate = h2[~h2['is_loyalty']]['churn_next_60d'].mean()
enrolled_rate = h2[h2['is_loyalty']]['churn_next_60d'].mean()
null_pct = h2['loyalty_tier'].isna().mean() * 100
print(f"Non-enrolled: {non_enrolled_rate:.1%} churn (n={(~h2['is_loyalty']).sum()}, {null_pct:.0f}% of base)")
print(f"Enrolled:     {enrolled_rate:.1%} churn (n={h2['is_loyalty'].sum()})")

# --- Hypothesis 3: High recency (>180 days) ---
last_order = orders_pre.groupby('customer_id')['order_date'].max().reset_index()
last_order['recency_days'] = (pd.Timestamp('2025-09-30') - last_order['order_date']).dt.days
h3 = cust_labels.merge(last_order[['customer_id','recency_days']], on='customer_id', how='left')
h3['recency_bucket'] = pd.cut(h3['recency_days'], bins=[0, 30, 90, 180, 9999],
                               labels=['0-30d','31-90d','91-180d','180d+'])
h3_rates = h3.groupby('recency_bucket', observed=False)['churn_next_60d'].agg(['mean','count'])
print("\n=== H3: Recency Buckets ===")
print(h3_rates)
high_rec = h3[h3['recency_days'] > 180]['churn_next_60d'].mean()
low_rec = h3[h3['recency_days'] <= 30]['churn_next_60d'].mean()
print(f"180d+ recency: {high_rec:.1%} churn")
print(f"0-30d recency: {low_rec:.1%} churn")

# --- Hypothesis 4: Support sentiment ---
print("\n=== Support columns ===")
print(support.columns.tolist())
print(support.dtypes)
print(support.head(2))

# Try different sentiment column names
sent_col = None
for c in ['sentiment_score', 'sentiment', 'csat_score', 'satisfaction']:
    if c in support.columns:
        sent_col = c
        break

if sent_col:
    print(f"\nUsing sentiment col: {sent_col}")
    print(support[sent_col].value_counts())
    # Check if numeric or categorical
    if support[sent_col].dtype in ['float64', 'int64', 'float32', 'int32']:
        neg_tickets = support[support[sent_col] < 0]
    else:
        neg_tickets = support[support[sent_col].str.lower().isin(['negative', 'neg'])]
    neg_custs = neg_tickets['customer_id'].unique()
    h4 = cust_labels.copy()
    h4['has_neg_ticket'] = h4['customer_id'].isin(neg_custs)
    h4_rates = h4.groupby('has_neg_ticket')['churn_next_60d'].agg(['mean','count'])
    print(f"\n=== H4: Negative Support Sentiment ===")
    print(h4_rates)
    neg_churn = h4[h4['has_neg_ticket']]['churn_next_60d'].mean()
    no_neg_churn = h4[~h4['has_neg_ticket']]['churn_next_60d'].mean()
    print(f"Has negative ticket: {neg_churn:.1%} churn (n={h4['has_neg_ticket'].sum()})")
    print(f"No negative ticket:  {no_neg_churn:.1%} churn (n={(~h4['has_neg_ticket']).sum()})")

# --- Hypothesis 5: Web disengagement ---
print("\n=== Web columns ===")
print(web.columns.tolist())

visit_col = None
for c in ['last_visit_days_ago', 'days_since_last_visit', 'last_visit_days']:
    if c in web.columns:
        visit_col = c
        break

if visit_col:
    h5 = cust_labels.merge(web[['customer_id', visit_col]], on='customer_id', how='left')
    h5['web_disengaged'] = h5[visit_col] >= 15
    h5_rates = h5.groupby('web_disengaged')['churn_next_60d'].agg(['mean','count'])
    print(f"\n=== H5: Web Disengagement ({visit_col} >= 15d) ===")
    print(h5_rates)
    disengaged_churn = h5[h5['web_disengaged']]['churn_next_60d'].mean()
    engaged_churn = h5[~h5['web_disengaged']]['churn_next_60d'].mean()
    print(f"Disengaged (>=15d): {disengaged_churn:.1%} churn (n={h5['web_disengaged'].sum()})")
    print(f"Active (<15d):      {engaged_churn:.1%} churn (n={(~h5['web_disengaged']).sum()})")

# Overall churn rate
overall = labels['churn_next_60d'].mean()
total_churned = labels['churn_next_60d'].sum()
print(f"\n=== Overall: {overall:.1%} churn rate ({total_churned}/{len(labels)}) ===")
