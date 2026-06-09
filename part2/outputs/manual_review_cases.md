# Manual Review Cases — Part 2
10 customers selected at segment decision boundaries or where signals conflict.
Five ambiguity types: boundary straddle, signal conflict, high-LTV churn, dormant-re-engaging, loyal discount buyer.

---

### CUST00116 | Segment: At-Risk Customers | CRM: high | Actual churn: 1
- RFM: recency=143d, freq=6, monetary=₹5,636
- Signals: discount=0.19, complaint=0.000, engagement=0.349, sessions=10, last_visit=26d
- Last campaign: new_launch
**Recommendation:** Boundary straddle — crossed At-Risk by recency only, no complaint history. Send soft re-engagement email; monitor 30 days before escalating spend.

---

### CUST00296 | Segment: At-Risk Customers | CRM: high | Actual churn: 1
- RFM: recency=132d, freq=4, monetary=₹1,990
- Signals: discount=0.20, complaint=0.000, engagement=0.145, sessions=2, last_visit=30d
- Last campaign: none
**Recommendation:** Boundary straddle — crossed At-Risk by recency only, no complaint history. Send soft re-engagement email; monitor 30 days before escalating spend.

---

### CUST00014 | Segment: At-Risk Customers | CRM: medium | Actual churn: 0
- RFM: recency=51d, freq=11, monetary=₹8,130
- Signals: discount=0.26, complaint=0.333, engagement=0.347, sessions=11, last_visit=17d
- Last campaign: bundle_discount
**Recommendation:** Signal conflict — high RFM but significant complaints. Service-recovery message first (apology + account review); no promotion until satisfaction is confirmed.

---

### CUST00030 | Segment: Champions | CRM: medium | Actual churn: 0
- RFM: recency=5d, freq=6, monetary=₹3,436
- Signals: discount=0.34, complaint=0.533, engagement=0.377, sessions=11, last_visit=3d
- Last campaign: free_shipping
**Recommendation:** Signal conflict — high RFM but significant complaints. Service-recovery message first (apology + account review); no promotion until satisfaction is confirmed.

---

### CUST00088 | Segment: At-Risk Customers | CRM: high | Actual churn: 1
- RFM: recency=98d, freq=12, monetary=₹6,774
- Signals: discount=0.36, complaint=0.667, engagement=0.311, sessions=9, last_visit=18d
- Last campaign: new_launch
**Recommendation:** Signal conflict — high RFM but significant complaints. Service-recovery message first (apology + account review); no promotion until satisfaction is confirmed.

---

### CUST01657 | Segment: Dormant Customers | CRM: high | Actual churn: 1
- RFM: recency=328d, freq=1, monetary=₹149
- Signals: discount=0.39, complaint=0.000, engagement=0.056, sessions=2, last_visit=60d
- Last campaign: new_launch
**Recommendation:** Mixed signals near multiple boundaries — apply action of closest segment; flag for CRM review after next interaction.

---

### CUST01606 | Segment: At-Risk Customers | CRM: high | Actual churn: 1
- RFM: recency=180d, freq=1, monetary=₹282
- Signals: discount=0.45, complaint=0.467, engagement=0.094, sessions=1, last_visit=36d
- Last campaign: none
**Recommendation:** Mixed signals near multiple boundaries — apply action of closest segment; flag for CRM review after next interaction.

---

### CUST01649 | Segment: Dormant Customers | CRM: high | Actual churn: 1
- RFM: recency=243d, freq=1, monetary=₹377
- Signals: discount=0.21, complaint=0.000, engagement=0.027, sessions=1, last_visit=56d
- Last campaign: bundle_discount
**Recommendation:** Mixed signals near multiple boundaries — apply action of closest segment; flag for CRM review after next interaction.

---

### CUST01648 | Segment: At-Risk Customers | CRM: high | Actual churn: 0
- RFM: recency=150d, freq=1, monetary=₹541
- Signals: discount=0.19, complaint=0.000, engagement=0.299, sessions=2, last_visit=23d
- Last campaign: welcome_offer
**Recommendation:** Mixed signals near multiple boundaries — apply action of closest segment; flag for CRM review after next interaction.

---

### CUST00047 | Segment: Dormant Customers | CRM: high | Actual churn: 1
- RFM: recency=204d, freq=1, monetary=₹764
- Signals: discount=0.16, complaint=0.000, engagement=0.176, sessions=2, last_visit=36d
- Last campaign: free_shipping
**Recommendation:** Mixed signals near multiple boundaries — apply action of closest segment; flag for CRM review after next interaction.

---

