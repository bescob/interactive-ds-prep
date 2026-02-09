# Module 01 — Warm Up

*Topics: SQL basics, Python basics, Probability rules, Key terminology*

---

## 🔷 SQL: How Queries Actually Execute

You write `SELECT ... FROM ... WHERE ...` but SQL runs them in a totally different order:

```
FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT
```

**Why this matters:** You can't reference a column alias from SELECT in your WHERE clause — WHERE runs first. You can't filter a window function in WHERE — it's computed during SELECT. This execution order explains 90% of "why doesn't this query work?" moments.

**Quick quiz — no peeking:**
What happens if you write `WHERE total_sales > 100` and `total_sales` is an alias from `SELECT SUM(sales) AS total_sales`?

**Answer:** It fails. WHERE runs before SELECT, so the alias doesn't exist yet. Use HAVING instead (runs after GROUP BY/aggregation).

---

## 🔶 Python: The Core Data Structures

**List** `[1, 2, 3]` — ordered, mutable, allows duplicates.
**Tuple** `(1, 2, 3)` — ordered, **immutable**, allows duplicates. Faster than lists, usable as dict keys.
**Set** `{1, 2, 3}` — unordered, mutable, **no duplicates**. Membership check is O(1) vs O(n) for lists.
**Dict** `{'key': 'val'}` — key-value pairs, ordered (Python 3.7+), O(1) lookup.

**The interview trick:** "Remove duplicates from a list while preserving order?"
```python
list(dict.fromkeys(my_list))  # Dict preserves insertion order, rejects dup keys
```

**Quick quiz:** Which data structure would you use if you need to check whether an item exists in a collection of 10 million elements, and why?

**Answer:** A `set`. Lookup is O(1) via hashing, vs O(n) for a list scanning every element.

---

## 🟢 Stats: The Three Probability Rules

Everything in probability comes from three rules:

**Addition (OR):** P(A or B) = P(A) + P(B) - P(A and B)
If mutually exclusive: P(A or B) = P(A) + P(B)

**Multiplication (AND):** P(A and B) = P(A) × P(B|A)
If independent: P(A and B) = P(A) × P(B)

**Complement (NOT):** P(not A) = 1 - P(A)
Useful trick: "probability of at least one" = 1 - P(none)

**Quick quiz:** You roll two dice. What's P(at least one 6)?

**Answer:** 1 - P(no sixes) = 1 - (5/6 × 5/6) = 1 - 25/36 = **11/36 ≈ 0.306**

---

## 🟣 Terminology: ETL and Data Storage

**ETL** = Extract, Transform, Load. The pipeline for moving data into an analytics system.
- Extract: pull raw data from databases, APIs, logs
- Transform: clean, validate, restructure, aggregate
- Load: write into the target (warehouse)

Modern twist: **ELT** — load raw first, transform inside the warehouse. Cheaper storage makes this viable.

**Data Warehouse** = structured, processed data, optimized for analytical queries (Snowflake, BigQuery, Redshift). Think "organized library."

**Data Lake** = raw data in ANY format at any scale (S3, Azure Data Lake). Think "dump everything, organize later." Risk: becomes a "data swamp" without governance.

**Quick quiz:** Your company stores raw JSON logs from 50 different services. Where does this go — warehouse or lake?

**Answer:** Data lake — it's raw, mixed-format data. After ETL/ELT processing, the cleaned structured version goes into the warehouse for analysis.

---

## 🔷 SQL: JOINs Refresher

**INNER JOIN** — only matching rows from both tables survive.
**LEFT JOIN** — ALL left table rows survive. Non-matching right columns become NULL.
**FULL OUTER JOIN** — all rows from both sides. NULLs fill gaps.
**CROSS JOIN** — every row × every row (cartesian product). Usually accidental.

**The anti-join pattern** (find things with NO match):
```sql
SELECT c.customer_id
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
WHERE o.order_id IS NULL;  -- Customers who never ordered
```

**Quick quiz:** You INNER JOIN a table of 100 customers with a table of 80 orders. Can you get more than 100 rows?

**Answer:** Yes! If a customer has multiple orders, they appear once per order. INNER JOIN produces one row per match, not per left-side row.

---

## 🟢 Stats: What's a Conditional Probability?

P(A|B) means "probability of A, given B already happened."

P(A|B) = P(A and B) / P(B)

**Example:** Deck of cards. P(King | Face card)?
- P(King AND Face card) = 4/52 (all Kings are face cards)
- P(Face card) = 12/52
- P(King | Face card) = (4/52) / (12/52) = 4/12 = **1/3**

This concept is the building block for Bayes' theorem, which we'll hit in Module 02.

---

## 🟠 Behavioral: The STAR Framework

Every behavioral answer uses this structure:

| Part | Time | What to do |
|---|---|---|
| **S**ituation | 20% (~30s) | Set the scene briefly |
| **T**ask | 10% (~15s) | YOUR specific responsibility |
| **A**ction | 60% (~90s) | What YOU did (say "I" not "we") |
| **R**esult | 10% (~15s) | Quantified outcome |

**Homework:** Think of ONE specific project where you used data to influence a decision. Write down the S, T, A, R in 2-3 sentences each. You'll need this story in multiple interviews.

---

## Module 01 Self-Test (cover answers, try first)

1. What's the SQL execution order?
2. Why is set lookup O(1) but list lookup O(n)?
3. P(A or B) when A and B are NOT mutually exclusive?
4. What does ETL stand for?
5. How do you find customers with no orders using SQL?
6. What does STAR stand for?

**Answers:**
1. FROM → JOIN → WHERE → GROUP BY → HAVING → SELECT → DISTINCT → ORDER BY → LIMIT
2. Sets use hash tables (compute hash, jump to bucket). Lists scan every element sequentially.
3. P(A) + P(B) - P(A and B) — subtract the overlap to avoid double-counting.
4. Extract, Transform, Load.
5. LEFT JOIN customers to orders, then WHERE orders.id IS NULL.
6. Situation, Task, Action, Result.
