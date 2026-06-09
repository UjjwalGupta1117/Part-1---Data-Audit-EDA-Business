# Manual Review Cases — Part 2
10 customers selected at segment decision boundaries or where signals conflict.

Five ambiguity types covered:
1. **Boundary straddle** — just crossed a threshold into a different segment
2. **Signal conflict** — good RFM but bad support, or bad RFM but high engagement
3. **High LTV + high churn risk** — the most costly false-negative scenario
4. **Dormant but re-engaging now** — rules say dormant but behaviour says otherwise
5. **Loyal discount buyer** — discount pattern may be acquisition hook, not ongoing crutch

---

## How to Read These Cases
Each case shows:
- The segment the rules assigned
- The CRM team's manual priority label (from `intervention_history.csv`)
- Key RFM and signal values
- The ambiguity type and a concrete recommendation

For cases where the notebook generates the actual customer IDs at runtime, the patterns below represent the types of customers that will appear and how to reason about them.

---

## Ambiguity Type 1: Boundary Straddle (2 cases: CUST00116, CUST00296)

### Pattern
Customers crossed into **At-Risk** purely because `recency_days` is 132–143 (e.g., CUST00296: 132 days, CUST00116: 143 days) — just above the P75 threshold of 129 days. However:
- `complaint_score` is 0.0 (no negative support history)
- `frequency` ≥ 4 (CUST00296 has 4 orders, CUST00116 has 6 orders — repeat buyers with established habits)
- `engagement_score` may still be moderate

### Why it's ambiguous
The recency-based rule is a hard boundary. A customer with `recency_days = 130` is At-Risk; one with `recency_days = 128` is Loyal — despite being nearly indistinguishable in actual churn risk.

### Recommendation
Do **not** immediately send a discount. Send a soft re-engagement email (product recommendation, new launch notification). Monitor for 30 days. If no purchase, escalate to the full At-Risk intervention. This avoids training a borderline-loyal customer to expect discounts.

---

## Ambiguity Type 2: Signal Conflict — High RFM + High Complaint (2 cases: CUST00014, CUST00030)

### Pattern
Customer has `RFM_score ≥ 13` (e.g., CUST00030: RFM 14 (Champions), CUST00014: RFM 13 (At-Risk)) but `complaint_score ≥ 0.33`, indicating recent negative support interactions with possible re-opened tickets.

### Why it's ambiguous
RFM says this customer is highly valuable and engaged. The support signal says they are dissatisfied. Sending a promotional offer to a customer who feels mistreated may feel tone-deaf and could accelerate churn rather than prevent it.

### Recommendation
**Service-recovery first, promotion second.** Route to a senior CRM agent for a personal outreach acknowledging the support experience. Only after a positive resolution response should a promotional offer be introduced. The offer should be framed as appreciation, not compensation.

---

## Ambiguity Type 3: High LTV + Actual Churn (2 cases: CUST00088, CUST00116)

### Pattern
Customer is in the top 10% by `monetary_180d` (CUST00088: ₹6,774.5, CUST00116: ₹5,635.9) and is flagged by the model as At-Risk — but actually churned in the 60-day target window.

### Why it's ambiguous
This represents the most costly false-negative type: a high-value customer the model scored but not strongly enough to trigger the most aggressive intervention, or who was not reached in time.

### Recommendation
For customers matching this profile at scoring time:
- Apply a **lower threshold** (0.35 instead of 0.40) for customers with `monetary_180d > P75`
- Escalate to personal outreach (WhatsApp / phone call), not just email
- Offer a high-perceived-value intervention: early access, exclusive product, or bundle — not a generic discount
- Flag in the post-campaign analysis to refine the threshold rule

---

## Ambiguity Type 4: Dormant But Re-Engaging (2 cases: CUST00016, CUST00017)

### Pattern
Customer was assigned to **Dormant Customers** because `recency_days > 196` OR `frequency = 0`. However, current web behaviour shows:
- `sessions_30d ≥ 2` (CUST00016: 2 sessions, CUST00017: 4 sessions)
- `last_visit_days_ago ≤ 47` (CUST00016: 32 days, CUST00017: 47 days)

This customer has been absent for months but is actively browsing right now.

### Why it's ambiguous
The rules segment on historical purchase behaviour. But the customer's current web activity is indistinguishable from a Promising Riser — they are showing purchase intent signals today. Treating them as deeply dormant and ignoring the engagement signal wastes a real-time opportunity.

### Recommendation
Override the Dormant classification for this specific case. Treat as **Promising Riser**: send a 'welcome back' offer (free shipping, new product highlight) within 24–48 hours while intent is hot. Do not send a win-back campaign (heavy discount) — the customer is already re-engaging without one.

---

## Ambiguity Type 5: Loyal Discount Buyer (2 cases: CUST00150, CUST00217)

### Pattern
Customer is classified as **Discount Dependents** because `avg_discount ≥ 0.35` (CUST00150: 0.39, CUST00217: 0.35). However:
- `frequency ≥ 3` (both have 3 orders)
- `return_rate < 0.10` (both have 0.0 return rate — they actually use what they buy)
- Order history spans multiple product categories

### Why it's ambiguous
The Discount Dependents segment assumes discounts are the primary purchase driver. But for a customer with 5+ orders and low returns, the discount may have been the *acquisition* hook — not an ongoing crutch. Their category diversity and return behaviour suggest genuine product affinity.

### Recommendation
Run a **discount removal test** for this customer type: send loyalty-points reward (no cash discount) for the next 2 campaigns. If purchase frequency holds, reclassify as Loyal Customer. If it drops, acknowledge the discount dependency and maintain the Discount Dependents strategy. This test costs nothing extra and provides valuable signal for future segmentation.
