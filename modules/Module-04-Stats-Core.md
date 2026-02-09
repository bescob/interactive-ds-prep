# Module 04 — The Stats Core

*Topics: Hypothesis testing, P-values, Type I/II errors, SQL self-joins, Python loc vs iloc*

---

## 🟢 Stats: Hypothesis Testing Step-by-Step

1. **State hypotheses:** H₀ (null — no effect) vs H₁ (alternative — there IS an effect)
2. **Choose significance level:** α = 0.05 (accept 5% false positive risk)
3. **Collect data and compute test statistic**
4. **Find p-value**
5. **Decision:** p < α → reject H₀. p ≥ α → fail to reject H₀.

### P-Value — The Most Misunderstood Concept

**What it IS:** The probability of seeing data this extreme or more extreme, **assuming H₀ is true.**

**What it is NOT:**
- ❌ NOT the probability that H₀ is true
- ❌ NOT the probability your result is due to chance
- ❌ NOT the probability of making an error

**Example:** P-value = 0.03 means: "If there were truly no effect, there's only a 3% chance we'd see results this extreme." Since 0.03 < 0.05, we reject H₀.

**P-value = 0.06:** We fail to reject H₀ at α = 0.05. But this does NOT mean "no effect." It means insufficient evidence. Say "we don't have sufficient evidence to conclude there's an effect" — never say "the null is true."

**Quick quiz:** An interviewer asks: "Your A/B test got p = 0.04. What does that mean?" Answer in one clear sentence.

**Answer:** "If the new feature truly had no effect on the metric, there's only a 4% probability we'd observe a difference this large or larger in our experiment — so we reject the null hypothesis at the 5% significance level."

---

## 🟢 Stats: Type I and Type II Errors

|  | H₀ True (no effect) | H₀ False (real effect) |
|---|---|---|
| Reject H₀ | **Type I (α)** — false positive, "crying wolf" | ✅ Correct! (Power = 1-β) |
| Fail to reject H₀ | ✅ Correct! | **Type II (β)** — false negative, "missing the wolf" |

**Power = 1 - β** = probability of detecting a real effect when it exists. Benchmark: ≥ 0.80.

**What increases power?** Larger sample size, larger effect size, higher α, lower variance.

**The √n relationship:** Doubling your sample size does NOT double precision. It multiplies precision by √2 ≈ 1.41. To halve your confidence interval, you need 4× the sample.

**Quick quiz:** Your boss says "we can only detect a 5% lift — the actual lift is probably 2%. What do we need?"

**Answer:** More sample size. Power depends on effect size — a smaller expected effect needs a much larger sample to detect. You'd recalculate n using the power formula with the smaller minimum detectable effect.

---

## 🔷 SQL: Self-Joins

A self-join joins a table to itself. You need this when a row references another row in the SAME table.

```sql
-- Employees earning more than their manager
SELECT e.name AS employee, e.salary AS emp_salary,
       m.name AS manager, m.salary AS mgr_salary
FROM employees e
JOIN employees m ON e.manager_id = m.employee_id
WHERE e.salary > m.salary;
```

**The trick:** You alias the same table twice (e and m) and treat them as two separate tables. The JOIN condition links the employee's manager_id to the manager's employee_id.

**Another self-join pattern — consecutive events:**
```sql
-- Users who made purchases on consecutive days
SELECT DISTINCT a.user_id
FROM purchases a
JOIN purchases b ON a.user_id = b.user_id
  AND b.purchase_date = a.purchase_date + INTERVAL '1 day';
```

**Quick quiz:** Table `flights` has columns: flight_id, origin, destination, departure_time. Write a query to find all pairs of flights where you can connect (flight 1's destination = flight 2's origin, and flight 2 departs after flight 1 arrives).

**Answer:**
```sql
SELECT f1.flight_id AS first_flight, f2.flight_id AS connecting_flight
FROM flights f1
JOIN flights f2 ON f1.destination = f2.origin
  AND f2.departure_time > f1.arrival_time;
```

---

## 🔶 Pandas: loc vs iloc — THE Most Asked Question

```python
# loc = Label-based (uses index/column NAMES)
# iloc = Integer position-based (uses 0-indexed positions)

df.loc[0:5]     # Rows with LABELS 0 through 5 → INCLUSIVE (6 rows)
df.iloc[0:5]    # Rows at POSITIONS 0 through 4 → EXCLUSIVE (5 rows)
```

**The key gotcha:** `loc` includes BOTH endpoints. `iloc` excludes the end (like normal Python slicing).

**Most common real-world usage:**
```python
# Boolean filtering + column selection (this is what you'll actually write)
df.loc[df['age'] > 30, 'name']            # Label-based filter + column
df.loc[df['salary'] > 100000, ['name', 'dept']]  # Multiple columns
```

**The SettingWithCopyWarning (bonus — it's related):**
```python
# WRONG — may modify a copy, not the original
df[df['category'] == 'A']['price'] = 10

# RIGHT — use loc for assignment
df.loc[df['category'] == 'A', 'price'] = 10
```

---

## 🟣 Terminology: Normalization vs Denormalization

**Normalization** = split data into related tables to reduce redundancy.
- Example: instead of storing customer_name in every order row, store customer_id and look up the name in a separate customers table.
- Good for: OLTP/write-heavy systems (update customer name in one place)
- Downside: queries need many JOINs

**Denormalization** = intentionally add redundancy by pre-joining tables.
- Example: store customer_name directly in the orders table
- Good for: OLAP/analytics (fewer JOINs = faster reads)
- Downside: update customer name → must update it everywhere

**Quick quiz:** You're designing a data warehouse for analytics. Normalized or denormalized? Why?

**Answer:** Denormalized (or a star schema). Analytics queries aggregate across many dimensions — pre-joining reduces the need for expensive runtime JOINs. Read performance matters more than write efficiency in a warehouse.

---

## 🟢 Stats Repeat: Bayes' Theorem (Third Time)

Without looking at the formula, try this one:

"2% of emails are spam. Your filter catches 97% of spam but also flags 5% of legitimate emails. An email is flagged. Probability it's actually spam?"

**Work it out, then check.**

**Answer:**
```
P(Spam|Flagged) = (0.97 × 0.02) / (0.97 × 0.02 + 0.05 × 0.98)
                = 0.0194 / (0.0194 + 0.049)
                = 0.0194 / 0.0684
                ≈ 28.4%
```

Higher than the disease examples because the base rate (2%) is much higher than 0.1%.

---

## Module 04 Self-Test

1. State what a p-value means in one sentence.
2. Type I vs Type II — which is the false positive?
3. Write a self-join to find employees who report to the same manager.
4. `df.loc[0:3]` vs `df.iloc[0:3]` — how many rows each?
5. What's the SettingWithCopyWarning and how do you fix it?
6. Normalized vs denormalized database — which for analytics and why?

**Answers:**
1. The probability of observing data as extreme or more extreme than what was observed, assuming the null hypothesis is true.
2. Type I is the false positive (rejecting H₀ when it's true — "crying wolf").
3. `SELECT a.name, b.name FROM employees a JOIN employees b ON a.manager_id = b.manager_id AND a.employee_id < b.employee_id` (the < avoids duplicates and self-pairs)
4. `loc[0:3]` = 4 rows (labels 0,1,2,3 — inclusive). `iloc[0:3]` = 3 rows (positions 0,1,2 — exclusive end).
5. Chained indexing (`df[...][...] = val`) may modify a copy. Fix: use `df.loc[condition, column] = val`.
6. Denormalized — fewer JOINs means faster analytical queries. Read performance > write efficiency for analytics.
