# Module 03 — Pattern Builder

*Topics: SQL LAG/LEAD, Pandas transform vs apply, Distributions, Product sense GAME framework*

---

## 🔷 SQL: LAG and LEAD — Comparing Rows Across Time

`LAG(column, N)` = look N rows **back**. `LEAD(column, N)` = look N rows **forward**.

```sql
-- Month-over-month revenue growth
WITH monthly AS (
  SELECT DATE_TRUNC('month', order_date) AS month, SUM(amount) AS revenue
  FROM orders GROUP BY 1
)
SELECT month, revenue,
  LAG(revenue) OVER (ORDER BY month) AS prev_month,
  ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
    / NULLIF(LAG(revenue) OVER (ORDER BY month), 0), 2) AS growth_pct
FROM monthly;
```

**Two gotchas here:**
- `100.0` forces decimal division (integer `100` would silently round to 0)
- `NULLIF(x, 0)` returns NULL instead of dividing by zero (first month has no LAG)

**Quick quiz:** Write a query to find users whose spending THIS month is more than double their LAST month's spending.

**Answer:**
```sql
WITH monthly_spend AS (
  SELECT user_id, DATE_TRUNC('month', txn_date) AS month, SUM(amount) AS spend
  FROM transactions GROUP BY 1, 2
)
SELECT user_id, month, spend,
  LAG(spend) OVER (PARTITION BY user_id ORDER BY month) AS prev_spend
FROM monthly_spend
-- Wrap in another CTE or subquery to filter:
-- WHERE spend > 2 * prev_spend
```

---

## 🔶 Pandas: transform() vs apply() vs agg()

This is the trickiest Pandas question. The key distinction:

**agg()** → returns ONE row per group (like GROUP BY in SQL)
```python
df.groupby('dept')['salary'].agg('mean')
# dept A → 75000
# dept B → 82000
```

**transform()** → returns SAME number of rows (broadcasts group result back)
```python
df.groupby('dept')['salary'].transform('mean')
# [75000, 75000, 75000, 82000, 82000, ...]  (one per original row)
```

**apply()** → flexible but slow, can return anything

**When to use transform:** When you want a group-level stat as a new column WITHOUT losing rows.

```python
# THE classic interview pattern: employees above their department's average
df[df['salary'] > df.groupby('dept')['salary'].transform('mean')]
```

**Quick quiz:** You want to add a column showing what percentage of their department's total salary each employee represents. Which function?

**Answer:** `transform()`:
```python
df['pct_of_dept'] = df['salary'] / df.groupby('dept')['salary'].transform('sum')
```

---

## 🟢 Stats: The Key Distributions

### Normal Distribution
- Bell-shaped, symmetric, defined by mean (μ) and std dev (σ)
- **68-95-99.7 rule:** 68% within ±1σ, 95% within ±2σ, 99.7% within ±3σ
- Central Limit Theorem makes this universal — sample means are always ~normal

### Binomial Distribution
- Count of successes in n independent trials, each with probability p
- Mean = np, Variance = np(1-p)
- "Out of 100 users, how many click if click rate is 5%?" → Binomial(100, 0.05), mean = 5

### Poisson Distribution
- Count of events in a fixed interval
- Mean = λ, Variance = λ **(they're equal!)**
- "How many support calls per hour?" — if mean = 4, variance = 4 too
- Tip: if you see a count distribution where mean ≈ variance, it's likely Poisson

### Exponential Distribution
- Time BETWEEN events (complement of Poisson)
- Mean = 1/λ
- **Memoryless:** how long you've waited doesn't affect how much longer you'll wait
- "How long until the next customer arrives?"

**Quick quiz:** Average 3 emails per hour (Poisson). What's the variance? What distribution describes time between emails?

**Answer:** Variance = 3 (Poisson: mean = variance). Time between emails is Exponential with λ=3, so mean wait = 1/3 hour = 20 minutes.

---

## 🟠 Product Sense: The GAME Framework

For "How would you measure X?" questions — use GAME:

**G — Goal:** What business objective? (Don't jump to metrics — clarify first)
**A — Actions:** What user actions lead to the goal? Map the user journey.
**M — Metrics:** Define three types:
  - **Primary (North Star):** THE one metric for the goal
  - **Secondary:** Context and deeper understanding
  - **Guardrail:** Must NOT degrade (user experience, safety)
**E — Evaluate:** Tradeoffs, measurement challenges, what you'd act on.

### Practice: "How would you measure the success of Uber Eats adding a grocery delivery feature?"

**G:** Expand Uber Eats beyond restaurants to increase total orders and revenue.
**A:** User opens app → browses grocery section → adds items to cart → completes order → receives delivery → reorders.
**M:**
  - Primary: Weekly grocery orders per active user
  - Secondary: Grocery basket size, grocery → restaurant cross-usage, time to delivery
  - Guardrail: Restaurant order volume (shouldn't cannibalize), delivery quality ratings, driver earnings
**E:** If grocery orders rise but restaurant orders drop equally, we're just shifting revenue. If drivers prefer grocery runs, restaurant wait times could increase. Track whether grocery brings in NEW users or just gives existing users another option.

---

## 🔷 SQL: Conditional Aggregation (CASE WHEN)

Replace multiple queries with one:

```sql
-- Click-through rate per app
SELECT app_id,
  ROUND(100.0 *
    SUM(CASE WHEN event_type = 'click' THEN 1 ELSE 0 END) /
    NULLIF(SUM(CASE WHEN event_type = 'impression' THEN 1 ELSE 0 END), 0)
  , 2) AS ctr
FROM events
GROUP BY app_id;
```

**Also useful for pivoting:**
```sql
SELECT user_id,
  SUM(CASE WHEN platform = 'ios' THEN sessions ELSE 0 END) AS ios_sessions,
  SUM(CASE WHEN platform = 'android' THEN sessions ELSE 0 END) AS android_sessions
FROM user_activity
GROUP BY user_id;
```

---

## 🟢 Bayes' Theorem — Round 2 (Repetition)

Can you still do this without looking? Try it:

"0.5% of transactions are fraudulent. A fraud detector has 99% sensitivity and 3% false positive rate. A transaction is flagged. What's the probability it's actually fraud?"

**Work it out before reading the answer.**

**Answer:**
```
P(Fraud|Flagged) = (0.99 × 0.005) / (0.99 × 0.005 + 0.03 × 0.995)
                 = 0.00495 / (0.00495 + 0.02985)
                 = 0.00495 / 0.0348
                 ≈ 14.2%
```

Even with 99% sensitivity, most flags are false positives because fraud is rare.

---

## Module 03 Self-Test

1. What does `LAG(revenue) OVER (ORDER BY month)` return for the first row?
2. `transform()` vs `agg()` — which changes the number of rows?
3. Poisson distribution: mean = 7. What's the variance?
4. What does GAME stand for?
5. What's a guardrail metric and why does it matter?
6. Write CASE WHEN to compute a conversion rate from events with types 'view' and 'purchase'.

**Answers:**
1. NULL — there's no previous row to look back at.
2. `agg()` reduces rows (one per group). `transform()` keeps the same number of rows.
3. 7 — Poisson's mean equals its variance.
4. Goal, Actions, Metrics, Evaluate.
5. A metric that must NOT degrade while optimizing the primary metric. Catches unintended consequences (e.g., pushing engagement but increasing spam).
6. `ROUND(100.0 * SUM(CASE WHEN event_type = 'purchase' THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN event_type = 'view' THEN 1 ELSE 0 END), 0), 2) AS conversion_rate`
