# Module 14 — Final Boss Review

*All topics mixed. This is your last-pass review. Every question here is something that has actually appeared in DS interviews. Try answering each before reading the answer.*

---

## Round 1: Speed Definitions (30 seconds each)

**1. What does ETL stand for?**
Extract, Transform, Load.

**2. OLAP vs OLTP in one sentence each?**
OLTP: fast individual transactions (app backend). OLAP: complex analytical queries across millions of rows (BI/dashboards).

**3. What is the CAP theorem?**
Distributed systems can guarantee at most 2 of 3: Consistency, Availability, Partition tolerance. Since partitions happen, you choose CP or AP.

**4. Batch vs streaming?**
Batch: process data on a schedule (reports, ETL). Streaming: process in real-time as it arrives (fraud, live dashboards).

**5. What is a feature store?**
Centralized system for storing/serving ML features, ensuring consistency between training and production.

---

## Round 2: SQL (Write the Query)

**6.** Top 3 highest-spending customers. Just write it.

```sql
SELECT customer_id, SUM(amount) AS total_spend
FROM orders
GROUP BY customer_id
ORDER BY total_spend DESC
LIMIT 3;
```

**7.** Second highest salary per department.

```sql
WITH ranked AS (
  SELECT department, employee, salary,
    DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC) AS rnk
  FROM employees
)
SELECT * FROM ranked WHERE rnk = 2;
```

**8.** Month-over-month growth rate.

```sql
WITH monthly AS (
  SELECT DATE_TRUNC('month', order_date) AS month, SUM(revenue) AS rev
  FROM orders GROUP BY 1
)
SELECT month, rev,
  ROUND(100.0 * (rev - LAG(rev) OVER (ORDER BY month))
    / NULLIF(LAG(rev) OVER (ORDER BY month), 0), 2) AS growth_pct
FROM monthly;
```

**9.** Users who exist in signups but never made a purchase.

```sql
SELECT s.user_id
FROM signups s
LEFT JOIN purchases p ON s.user_id = p.user_id
WHERE p.user_id IS NULL;
```

**10.** Click-through rate: clicks / impressions per campaign.

```sql
SELECT campaign_id,
  ROUND(100.0 *
    SUM(CASE WHEN event = 'click' THEN 1 ELSE 0 END) /
    NULLIF(SUM(CASE WHEN event = 'impression' THEN 1 ELSE 0 END), 0)
  , 2) AS ctr
FROM events GROUP BY campaign_id;
```

---

## Round 3: Stats & Probability (Explain It)

**11. State Bayes' theorem and work through: 1% disease rate, 95% sensitivity, 3% false positive. Person tests positive.**

P(D|+) = (0.95 × 0.01) / (0.95 × 0.01 + 0.03 × 0.99) = 0.0095 / (0.0095 + 0.0297) = 0.0095 / 0.0392 ≈ **24.2%**

**12. What does p = 0.04 mean?**
If H₀ were true (no effect), there's only a 4% chance of observing data this extreme. At α=0.05, we reject H₀.

**13. Type I vs Type II?**
Type I (α) = false positive, crying wolf. Type II (β) = false negative, missing the wolf. Power = 1-β ≥ 0.80.

**14. Why always switch in Monty Hall?**
Initial pick = 1/3. Other two doors = 2/3. Host reveals one is wrong, remaining door gets the full 2/3. Switching = 2/3 win rate.

**15. 95% confidence interval: what does it ACTUALLY mean?**
If you repeated the experiment 100 times, ~95 of the intervals would contain the true value. NOT "95% probability the true value is in this specific interval."

---

## Round 4: ML (Explain the Tradeoff)

**16. Bias-variance: your model has 97% train accuracy, 68% test accuracy.**
Overfitting (high variance). Big gap. Fix: more data, regularize, simplify, dropout.

**17. L1 vs L2: 300 features, you think ~20 matter.**
L1 (Lasso) — drives irrelevant features to exactly zero. Built-in feature selection.

**18. RF vs XGBoost: you have noisy data and 1 hour before deadline.**
Random Forest — good defaults, resistant to noise, hard to screw up. XGBoost needs tuning.

**19. You built a fraud model with 99.5% accuracy. Your manager is impressed. Should you be?**
No — if fraud is 0.5% of transactions, predicting "not fraud" always = 99.5% accuracy. Check precision, recall, F1, PR-AUC.

**20. Can you apply L1/L2 to Random Forest?**
No. L1/L2 regularize coefficients. Trees have none. Trees regularize via max_depth, min_samples_leaf, etc.

---

## Round 5: Python/Pandas (What's Wrong?)

**21. What's wrong with:** `df[df['x'] > 5]['y'] = 10`
Chained indexing — may modify a copy. Fix: `df.loc[df['x'] > 5, 'y'] = 10`

**22. You need each employee's department average as a new column.** `agg()`, `transform()`, or `apply()`?
`transform()` — keeps the same number of rows.

**23. `df.loc[0:3]` returns how many rows?**
4 rows (labels 0, 1, 2, 3 — loc is inclusive on both ends).

**24. Why is NumPy faster than Python lists?**
Contiguous memory (cache-friendly), homogeneous types (no per-element type checking), vectorized C operations (no Python loop overhead). 10-100x faster.

**25. List vs generator for 10M items?**
Generator — O(1) memory (yields one at a time) vs O(n) memory for list (stores all at once).

---

## Round 6: Product Sense (Structure Your Answer)

**26. "How would you measure success of a search feature?" Use GAME.**
- G: Reduce time to find what users want, increase actions from search
- A: Type query → see results → click result → complete action
- M: Primary — search-to-action conversion. Secondary — zero-result rate, avg result position clicked. Guardrail — page load time, user satisfaction
- E: High clicks but low conversions = results look relevant but aren't. Track post-click behavior.

**27. "Revenue dropped 15% this quarter." First 3 things you do.**
(1) Clarify: vs last quarter or YoY? All segments? (2) Decompose: Revenue = Users × Conversion × AOV — which dropped? (3) Check internal (deployments, bugs, logging changes) before external (seasonality, competitors).

**28. Estimate: How many data scientists work in Chicago?**
~5,000 companies with 500+ employees in Chicago. Maybe 30% have DS teams averaging ~5 DS each. 1,500 × 5 = ~7,500. Plus smaller companies and consultancies → maybe ~10-12K. (Rough but defensible.)

---

## Round 7: Behavioral (Say These Out Loud)

**29. "Tell me about a time you used data to influence a decision."** (2 min)
*Use your prepared STAR story. Time yourself.*

**30. "Describe a failed project."** (2 min)
*Own it. Show learning. End on what you do differently now.*

**31. "How do you explain a model to a non-technical stakeholder?"** (1 min)
*Focus on: no jargon, use visualization/analogy, tie to business outcome.*

---

## The Final Checklist

Before your interview, can you:

- [ ] Write a top-N-per-group query with a window function and CTE?
- [ ] Calculate Bayes' theorem for a new scenario from scratch?
- [ ] Explain what a p-value IS and IS NOT?
- [ ] Name 3 A/B testing pitfalls and fixes?
- [ ] Explain bias-variance tradeoff with a diagnosis for each scenario?
- [ ] Say when to use L1 vs L2 and explain why L1 does feature selection?
- [ ] Use the GAME framework for a product metrics question?
- [ ] Walk through root cause analysis for a dropped metric?
- [ ] Tell 3 STAR stories (data decision, failure, collaboration) under 2 min each?
- [ ] Define: ETL, data warehouse vs lake, OLAP vs OLTP, CAP theorem?
- [ ] Explain why accuracy is bad for imbalanced data and what to use instead?
- [ ] Write `transform()` vs `agg()` use cases without mixing them up?

If you can check all of those, you're ready. Go get it. 🔪
