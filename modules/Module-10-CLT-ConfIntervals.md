# Module 10 — CLT, Confidence Intervals, Advanced SQL

*Topics: CLT, Confidence intervals, SQL anti-join + EXISTS, Gradient descent, Batch vs streaming*

---

## 🟢 Stats: Central Limit Theorem — The Foundation of Everything

**What it says:** Take many random samples of size n from ANY distribution. The distribution of sample means will be approximately normal, with:
- Mean = population mean
- Standard deviation = σ/√n (called **standard error**)

**Why it matters:** This is why normal distribution-based tests (z-test, t-test, confidence intervals) work even when the underlying data isn't normal. As long as n ≥ ~30, CLT kicks in.

**The √n factor:** Larger samples → smaller standard error → narrower CI → more precise. But it's √n, not n. **Quadrupling sample size only halves uncertainty.**

**Quick quiz:** You sample 100 customer wait times. Mean = 5 min, SD = 3 min. What's the standard error of the mean?

**Answer:** SE = σ/√n = 3/√100 = 3/10 = **0.3 minutes.** Even though individual wait times vary widely (SD=3), the mean of 100 observations is estimated with much more precision.

---

## 🟢 Stats: Confidence Intervals — What They Really Mean

```
CI = x̄ ± z × (σ/√n)
```

z-values: 90% → 1.645, **95% → 1.96**, 99% → 2.576

**What 95% CI means:** "If we repeated this experiment 100 times, about 95 of the resulting intervals would contain the true population parameter."

**What it does NOT mean:** "There's a 95% probability the true value is in this interval." The true value is fixed — it either is or isn't. The confidence is about the *procedure.*

**For proportions:** CI = p̂ ± z × √[p̂(1-p̂)/n]

**Quick quiz:** Sample mean = 50, SD = 12, n = 36. What's the 95% CI?

**Answer:** SE = 12/√36 = 2. CI = 50 ± 1.96 × 2 = 50 ± 3.92 = **(46.08, 53.92)**

---

## 🔷 SQL: Anti-Join Patterns and EXISTS

### Method 1: LEFT JOIN + IS NULL
```sql
SELECT p.page_id
FROM pages p
LEFT JOIN page_likes pl ON p.page_id = pl.page_id
WHERE pl.page_id IS NULL;
```

### Method 2: NOT EXISTS (often faster)
```sql
SELECT page_id FROM pages p
WHERE NOT EXISTS (
  SELECT 1 FROM page_likes pl WHERE pl.page_id = p.page_id
);
```

### EXISTS vs IN

**EXISTS** — checks if any row exists, stops at first match. Efficient for correlated subqueries.
**IN** — checks against a list. Simpler for small static lists.

**Rule of thumb:** EXISTS for large tables with correlated subqueries. IN for small, static value lists.

### Correlated subquery (know this term)
A subquery that references the outer query, so it re-executes per row:
```sql
-- Employees earning above their department average
SELECT name, salary, department
FROM employees e
WHERE salary > (
  SELECT AVG(salary) FROM employees WHERE department = e.department
);
```

---

## 🟠 ML: Gradient Descent

**What it is:** An optimization algorithm that iteratively adjusts parameters to minimize the loss function.

**Intuition:** You're on a hilly landscape in fog. You can only feel the slope beneath your feet. You take a step downhill. Repeat until you reach the bottom.

**Learning rate:**
- Too high → overshoot the minimum, bounce around, diverge
- Too low → converge very slowly, might get stuck in local minimum
- Just right → smooth convergence

**Variants:**
- **Batch:** Use ALL data per step — stable but slow
- **Stochastic (SGD):** Use ONE random sample — fast but noisy
- **Mini-batch:** Use a subset (e.g., 32-256 samples) — best of both worlds, standard in practice

**Quick quiz:** "What IS a loss function?" (Explain simply.)

**Answer:** A measure of how wrong the model's predictions are. Lower = better. MSE for regression (average squared error), log loss for classification (penalizes confident wrong predictions heavily). Gradient descent minimizes this function.

---

## 🟣 Terminology: Batch vs Streaming Processing

**Batch:** Process accumulated data at scheduled intervals.
- When: reports, model training, ETL jobs
- Tools: Spark, Hadoop, Airflow
- Latency: minutes to hours

**Streaming:** Process data in real-time as it arrives.
- When: fraud detection, live dashboards, recommendation updates
- Tools: Kafka, Flink, Spark Streaming
- Latency: milliseconds to seconds

**Quick quiz:** You're building a dashboard that shows the CEO daily revenue summaries. Batch or streaming?

**Answer:** Batch — daily summaries don't need real-time processing. Run a daily ETL job overnight. Reserve streaming for things that need sub-second response (fraud detection, live pricing).

---

## 🟢 Repeat: Window Functions Speed Round

Without looking, write the window clause for:

1. Rank employees by salary within each department (no gaps for ties)
2. Get the previous month's revenue
3. Running total of sales ordered by date

**Answers:**
1. `DENSE_RANK() OVER (PARTITION BY department ORDER BY salary DESC)`
2. `LAG(revenue) OVER (ORDER BY month)`
3. `SUM(sales) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`

---

## Module 10 Self-Test

1. State the CLT in one sentence.
2. Sample mean = 100, SD = 20, n = 64. What's the 95% CI?
3. What does a 95% confidence interval ACTUALLY mean?
4. EXISTS vs IN — when do you use each?
5. What is a correlated subquery?
6. Learning rate too high → what happens? Too low?
7. Batch vs streaming — which for a real-time fraud alert system?

**Answers:**
1. Regardless of the underlying distribution, sample means approach a normal distribution as sample size increases, with mean = population mean and SD = σ/√n.
2. SE = 20/√64 = 2.5. CI = 100 ± 1.96 × 2.5 = 100 ± 4.9 = **(95.1, 104.9)**
3. If you repeated the experiment 100 times, ~95 of the resulting intervals would contain the true value. NOT "95% probability the true value is in this interval."
4. EXISTS for large tables/correlated subqueries (stops at first match). IN for small static value lists.
5. A subquery that references the outer query, re-executing for each outer row.
6. Too high → overshoots, oscillates, may diverge. Too low → very slow convergence.
7. Streaming — fraud detection needs millisecond response times.
