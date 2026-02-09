# Module 09 — Cross-Validation & Product Metrics

*Topics: Cross-validation, Decision trees, Product metric design, Python decorators, SQL date manipulation*

---

## 🟠 ML: Cross-Validation

A single train/test split is noisy — results depend on WHICH data ended up where. Cross-validation averages over multiple splits.

**K-fold CV:** Split into k parts. Train on k-1, validate on 1. Repeat k times. Average the k scores. Typical k = 5 or 10.

**Stratified k-fold:** Each fold has the same class distribution as the full dataset. **Critical for imbalanced data.**

### When NOT to use standard k-fold

**Time series:** Random splitting uses future data to predict the past. Use **walk-forward validation:** train on months 1-6, test on 7; train on 1-7, test on 8; etc.

**Grouped data:** Multiple measurements per patient → all measurements from one patient must stay in the same fold. Use `GroupKFold`.

**Quick quiz:** You're predicting daily stock prices. Can you use standard 5-fold CV?

**Answer:** No — time series data has temporal dependencies. Random folds would leak future information into training. Use walk-forward or time-series split.

---

## 🟠 ML: Decision Trees — The Intuitive Model

**What they do:** Repeatedly split data on feature thresholds that best separate the target. Like playing 20 questions.

**How splits are chosen:**
- Classification: minimize **Gini impurity** = 1 - Σ(pᵢ²) where pᵢ = class proportion. Gini=0 → pure, Gini=0.5 → maximum impurity (binary).
- Regression: minimize variance/MSE in each resulting group.

**Pros:** Interpretable, handles nonlinear relationships, no scaling needed, handles mixed types.
**Cons:** Overfits easily, unstable (small data change → different tree), biased toward features with more levels.

This is WHY Random Forest and boosting exist — they address the instability and overfitting of single trees.

**Quick quiz:** Your decision tree has 100% training accuracy. Good or bad?

**Answer:** Bad — almost certainly overfitting. An unconstrained tree can memorize every training example by creating a leaf for each one. Regularize with max_depth, min_samples_leaf.

---

## 🟠 Product Sense: Metric Design

### North Star metrics (memorize a few)

| Company | North Star |
|---|---|
| Facebook | Daily active users |
| Airbnb | Nights booked |
| Spotify | Time spent listening |
| Slack | Messages sent per user per day |
| Uber | Rides completed |

### The counter-metric test

For ANY proposed metric, ask: "What happens if someone games this?"
- "Clicks" → people click but immediately bounce (meaningless)
- "Time spent" → people are frustrated and can't find what they need
- "Messages sent" → spam bots inflate numbers

This is why you need **guardrail metrics** — they catch when a win on one dimension creates a loss elsewhere.

### Vanity vs actionable metrics

**Vanity:** total registered users, total page views, total downloads. Only go up. Tell you nothing about health.

**Actionable:** DAU/MAU ratio (stickiness), retention rate (d1/d7/d30), revenue per user, conversion rate.

**Quick quiz:** "Total app downloads reached 50 million!" Is this a good success metric?

**Answer:** No — it's a vanity metric. It only goes up and says nothing about engagement. Many downloaded apps are never opened. Better: DAU, d7 retention, or MAU with an engagement threshold.

---

## 🔶 Python: Decorators

A decorator wraps a function to add behavior without modifying it.

```python
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} took {time.time()-start:.2f}s")
        return result
    return wrapper

@timer  # Same as: process_data = timer(process_data)
def process_data(df):
    return df.groupby('category').sum()
```

**What `@timer` actually does:** Replaces `process_data` with `wrapper`, which calls the original function but adds timing around it.

**Common decorators you've seen:**
- `@staticmethod`, `@classmethod` — modify method behavior
- `@property` — make a method accessible like an attribute
- `@functools.lru_cache` — memoize function results

---

## 🔷 SQL: Date Manipulation Cheat Sheet

```sql
DATE_TRUNC('month', date)         -- 2024-03-15 → 2024-03-01
EXTRACT(MONTH FROM date)          -- 2024-03-15 → 3
EXTRACT(DOW FROM date)            -- 0=Sunday, 6=Saturday (PostgreSQL)
date + INTERVAL '1 day'           -- Add time
DATEDIFF('day', start, end)       -- Days between (Snowflake/Redshift)
AGE(end_date, start_date)         -- PostgreSQL interval
DATE_PART('year', date)           -- Extract year as number
```

**Quick quiz:** Write a query to get the first day of each user's signup month.

**Answer:** `SELECT user_id, DATE_TRUNC('month', signup_date) AS signup_month FROM users`

---

## 🟢 Repeat: Classification Metrics (Can You Still Explain?)

Fill in the blanks without looking:

1. Precision = TP / (TP + ___)
2. Recall = TP / (TP + ___)
3. Use precision when ___ are costly.
4. Use recall when ___ are costly.
5. For imbalanced data, use ___ instead of ROC-AUC.

**Answers:**
1. FP
2. FN
3. False positives (flagging innocent things)
4. False negatives (missing real positives)
5. PR-AUC (Precision-Recall AUC)

---

## Module 09 Self-Test

1. Why can't you use standard k-fold CV on time series data?
2. What is Gini impurity? What value means maximum impurity for binary classification?
3. Name 3 North Star metrics for 3 different companies.
4. What does a Python decorator actually do mechanically?
5. `DATE_TRUNC('month', '2024-07-18')` returns what?
6. Your decision tree has 100% train accuracy and 60% test accuracy. Diagnose.

**Answers:**
1. Random splits leak future data into training, violating temporal order. Use walk-forward/time-series split.
2. Gini = 1 - Σ(pᵢ²). For binary: max impurity = 0.5 (50/50 class split).
3. Facebook: DAU. Airbnb: nights booked. Spotify: time listening. Slack: messages/user/day. Uber: rides completed.
4. It replaces the original function with a wrapper function that calls the original but adds behavior (logging, timing, caching, etc.).
5. 2024-07-01 (first day of the month).
6. Overfitting — 40% gap between train and test. Regularize: increase min_samples_leaf, decrease max_depth, or switch to Random Forest/boosting.
