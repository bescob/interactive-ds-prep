# Module 02 — First Contact

*Topics: SQL window functions, Pandas groupby/merge, Bayes' theorem, OLAP vs OLTP*

---

## 🔷 SQL: Window Functions — The #1 Interview Topic

Window functions compute a value for each row using OTHER rows, **without collapsing the table** like GROUP BY. Think "add a column that knows about its neighbors."

**Syntax:** `FUNCTION() OVER (PARTITION BY ... ORDER BY ...)`
- PARTITION BY = restart calculation per group (like GROUP BY but keeps all rows)
- ORDER BY = what order the window sees rows in

### The three ranking functions

Given sales values: 100, 100, 90, 80:

| Function | Output | How it handles ties |
|---|---|---|
| `ROW_NUMBER()` | 1, 2, 3, 4 | Always unique, ties get arbitrary order |
| `RANK()` | 1, 1, 3, 4 | Same rank for ties, **skips** next |
| `DENSE_RANK()` | 1, 1, 2, 3 | Same rank for ties, **no skip** |

**When to use which:**
- `ROW_NUMBER()` — need exactly N rows per group
- `RANK()` — ties share rank, gaps okay (sports standings)
- `DENSE_RANK()` — ties share rank, no gaps ("second highest salary")

**Quick quiz:** You need the second-highest salary per department. Which ranking function and why?

**Answer:** `DENSE_RANK()`. If two people tie for #1, RANK would make the next person #3 (skipping #2). DENSE_RANK gives the next person #2, which is what "second highest" means.

---

## 🔶 Pandas: GroupBy and Merge

### merge() — SQL-style joins in Pandas

```python
# Inner join on a column
pd.merge(df1, df2, on='customer_id', how='inner')

# Left join with different column names
pd.merge(df1, df2, left_on='id', right_on='cust_id', how='left')

# Debug joins with indicator
pd.merge(df1, df2, on='id', how='left', indicator=True)
# Adds _merge column: 'left_only', 'right_only', 'both'
```

### groupby() basics

```python
# Single aggregation
df.groupby('department')['salary'].mean()

# Multiple aggregations
df.groupby('department').agg(
    avg_salary=('salary', 'mean'),
    headcount=('employee_id', 'count'),
    max_salary=('salary', 'max')
)
```

**Quick quiz:** You want to find customers in df1 that do NOT exist in df2. How?

**Answer:**
```python
merged = pd.merge(df1, df2, on='customer_id', how='left', indicator=True)
only_in_df1 = merged[merged['_merge'] == 'left_only']
```

---

## 🟢 Stats: Bayes' Theorem — The Most Asked Probability Topic

Bayes lets you **flip a conditional probability.** You know P(B|A), you want P(A|B).

```
P(A|B) = P(B|A) × P(A) / [P(B|A) × P(A) + P(B|¬A) × P(¬A)]
```

### The classic interview question

"1 in 1,000 people have a disease. A test is 98% sensitive (true positive rate) with a 1% false positive rate. Someone tests positive — probability they're actually sick?"

**Step by step:**
- P(Disease) = 0.001
- P(Positive | Disease) = 0.98
- P(Positive | No Disease) = 0.01

```
P(Disease | Positive) = (0.98 × 0.001) / (0.98 × 0.001 + 0.01 × 0.999)
                      = 0.00098 / (0.00098 + 0.00999)
                      = 0.00098 / 0.01097
                      ≈ 0.089 → about 8.9%
```

**Why so low?** The disease is so rare that even a 1% false positive rate applied to 999 healthy people (~10 false positives) swamps the ~1 true positive. This is called **base rate neglect** — most people guess 98% because they ignore how rare the disease is.

**The follow-up:** "How would you make this test useful?"
→ Re-test positives with a more specific second test, or only test high-risk populations where the base rate is higher.

---

## 🟣 Terminology: OLAP vs OLTP

**OLTP (Online Transaction Processing)**
- Optimized for fast individual transactions: INSERT, UPDATE, DELETE one row
- Row-based storage
- Used by applications (checkout page, banking transfer)
- Think: "cash register"

**OLAP (Online Analytical Processing)**
- Optimized for complex queries: aggregate millions of rows, GROUP BY, JOINs
- Columnar storage (reads only needed columns → faster for analytics)
- Used by analysts, dashboards, BI tools
- Think: "business intelligence"

**Quick quiz:** Your e-commerce app writes 10,000 orders per minute. Your analytics team runs daily reports aggregating all orders. Same database?

**Answer:** No — use OLTP for the app (fast writes) and replicate to an OLAP warehouse for analytics (fast reads/aggregations). Running heavy analytical queries on the production OLTP database would slow down the app.

---

## 🔷 SQL: The CTE Pattern (and why you need it)

A CTE (Common Table Expression) is a named temporary result you define with `WITH`. You NEED CTEs because you **cannot filter window functions in WHERE.**

```sql
-- "Top 2 products by spending per category"
WITH ranked AS (
  SELECT category, product, SUM(spend) AS total_spend,
    RANK() OVER (PARTITION BY category ORDER BY SUM(spend) DESC) AS ranking
  FROM product_spend
  GROUP BY category, product
)
SELECT category, product, total_spend
FROM ranked
WHERE ranking <= 2;
```

**Why the CTE is mandatory:** Window functions compute during SELECT. WHERE runs before SELECT. So you can't write `WHERE RANK() OVER (...) <= 2`. The CTE computes the rank first, then the outer query filters on it.

---

## Module 02 Self-Test

1. What's the difference between RANK() and DENSE_RANK() for values [50, 50, 40]?
2. In Pandas, what does `indicator=True` add to a merge?
3. Work through Bayes: disease rate 1/500, test sensitivity 95%, false positive rate 2%. Someone tests positive — what's the probability they're sick? (Do the math.)
4. OLTP vs OLAP — which uses columnar storage and why?
5. Why can't you filter a window function directly in WHERE?

**Answers:**
1. RANK: 1, 1, 3 (skips 2). DENSE_RANK: 1, 1, 2 (no skip).
2. A `_merge` column with values 'left_only', 'right_only', or 'both' — shows which rows matched.
3. P = (0.95 × 0.002) / (0.95 × 0.002 + 0.02 × 0.998) = 0.0019 / (0.0019 + 0.01996) = 0.0019 / 0.02186 ≈ **8.7%**
4. OLAP uses columnar storage because analytical queries typically read few columns across many rows — columnar means you only load the columns you need.
5. WHERE executes before SELECT, and window functions are computed during SELECT. Need a CTE/subquery to filter.
