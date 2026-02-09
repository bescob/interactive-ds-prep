# Module 08 — Imbalanced Data & Feature Engineering

*Topics: Handling imbalanced data, Feature engineering, SQL consecutive days pattern, Pandas pivot/melt, CAP theorem*

---

## 🟠 ML: Handling Imbalanced Data

If 99% of transactions are legit and 1% are fraud, a model saying "always legit" gets 99% accuracy — and catches zero fraud.

### Solutions (in priority order)

1. **Use the right metric.** Ditch accuracy. Use F1, PR-AUC, or recall.

2. **Adjust class weights.** `class_weight='balanced'` in sklearn — penalizes misclassifying the minority class more. Easy, no data modification.

3. **Adjust classification threshold.** Default is 0.5. Lower it (e.g., 0.3) to catch more positives at the cost of more false positives. Tune to business needs.

4. **SMOTE (Synthetic Minority Oversampling).** Creates synthetic minority examples by interpolating between existing ones.
   🚨 **CRITICAL: Apply ONLY to training data, NEVER to validation/test** — otherwise you get data leakage.

5. **Undersample majority class.** Simple but loses information.

**Quick quiz:** Your interviewer asks: "Why not just oversample the minority class by duplicating rows?"

**Answer:** Simple duplication doesn't add new information — the model just sees the same examples multiple times, which can lead to overfitting on those exact examples. SMOTE is better because it creates NEW synthetic points between existing minority samples, adding diversity. But even SMOTE can create unrealistic samples if the feature space is sparse.

---

## 🟠 ML: Feature Engineering

Transforming raw data into features that help the model learn. Often the highest-ROI activity in ML.

**Common techniques:**
- **Log transform:** Reduce skewness (income, prices → log(income))
- **Binning:** Age → age_group (18-25, 26-35, ...)
- **Interactions:** height × weight, price × quantity
- **Time-based:** day_of_week, is_weekend, hours_since_last_event
- **Aggregation:** customer's avg order value, total orders in last 30 days
- **One-hot encoding:** categorical → binary columns

**Feature selection interview answer:** "I'd start by removing zero-variance features, then check pairwise correlation (drop one of highly correlated pairs). Use L1 regularization or tree feature importance to rank features. Validate the selected subset with cross-validation."

---

## 🔷 SQL: The Consecutive Days Pattern (Tricky!)

"Find users who logged in 3+ consecutive days."

```sql
WITH numbered AS (
  SELECT user_id, login_date,
    login_date - INTERVAL '1 day' * ROW_NUMBER() OVER (
      PARTITION BY user_id ORDER BY login_date
    ) AS grp
  FROM (SELECT DISTINCT user_id, login_date FROM logins) t
)
SELECT user_id, COUNT(*) AS streak
FROM numbered
GROUP BY user_id, grp
HAVING COUNT(*) >= 3;
```

**Why this works:** For consecutive dates, subtracting an incrementing row number produces the SAME value (the "group anchor"). Non-consecutive dates produce different values, splitting into separate groups.

Example: dates 1,2,3,5,6 with row_numbers 1,2,3,4,5 → differences: 0,0,0,1,1 → two groups.

---

## 🔶 Pandas: Pivot Tables and Reshaping

```python
# pivot_table = aggregate + reshape (like Excel pivot)
pd.pivot_table(df,
    values='sales',
    index='region',
    columns='quarter',
    aggfunc='sum'
)

# melt = opposite of pivot (wide → long)
pd.melt(df,
    id_vars=['name'],
    value_vars=['Q1', 'Q2', 'Q3'],
    var_name='quarter',
    value_name='sales'
)
```

**When to use pivot:** When you want to see a metric across two dimensions (region × quarter).
**When to use melt:** When your columns ARE data (Q1, Q2, Q3 are values of "quarter") and you need them as rows for analysis or plotting.

---

## 🟣 Terminology: CAP Theorem and MapReduce

### CAP Theorem
A distributed system can guarantee at most 2 of 3:
- **C**onsistency — all nodes see the same data simultaneously
- **A**vailability — every request gets a response
- **P**artition tolerance — system works despite network failures

Network partitions WILL happen, so you actually choose between:
- **CP** (consistent, may reject during partitions) — banks, financial systems
- **AP** (always responds, may serve stale data) — social media, caching

### MapReduce
Processing huge datasets across many machines:
- **Map:** Apply function to each record → key-value pairs
- **Shuffle:** Group values by key
- **Reduce:** Aggregate per key

**Word count:** Map: each doc → (word, 1). Reduce: sum per word → (word, total).

**Quick quiz:** You're building a real-time fraud detector. CP or AP system? Why?

**Answer:** CP — you need consistency. A payment system can't serve stale data about account balances or fraud flags. It's better to briefly reject a transaction during a network partition than to approve a fraudulent one based on outdated info.

---

## 🟢 Repeat: P-Value Check

Without looking, answer: "Your A/B test got p = 0.08 at α = 0.05. A stakeholder asks if the feature works. What do you say?"

**Answer:** "We don't have sufficient statistical evidence at our pre-set 5% significance level to conclude the feature has an effect. This doesn't mean there's NO effect — it means our sample may not be large enough to detect it. We could run the test longer or consider if the minimum detectable effect was set appropriately."

---

## Module 08 Self-Test

1. Why is accuracy bad for imbalanced data? What metric do you use instead?
2. What is SMOTE and what's the critical rule for using it?
3. Explain the consecutive-days SQL trick in your own words.
4. When do you use pivot_table vs melt in Pandas?
5. CAP theorem: what do the three letters stand for?
6. p = 0.08 at α = 0.05. Is the null hypothesis true?

**Answers:**
1. Predicting majority class always = high accuracy, zero usefulness. Use F1, PR-AUC, or recall depending on cost of false positives vs false negatives.
2. Creates synthetic minority samples by interpolating between existing ones. ONLY apply to training data — never test/validation (data leakage).
3. Subtracting an incrementing row number from consecutive dates produces the same group value. Non-consecutive dates produce different values, creating separate groups you can count.
4. Pivot: aggregate + reshape to see a metric across two dimensions. Melt: convert column headers into row values (wide → long format).
5. Consistency, Availability, Partition tolerance.
6. No — "fail to reject H₀" ≠ "H₀ is true." It means insufficient evidence at this sample size.
