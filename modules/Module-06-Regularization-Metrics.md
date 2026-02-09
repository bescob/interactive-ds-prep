# Module 06 — Regularization & Metrics

*Topics: L1/L2 regularization, Classification metrics, A/B testing basics, Python generators, SQL duplicates*

---

## 🟠 ML: L1 (Lasso) vs L2 (Ridge) Regularization

Regularization adds a penalty to the loss function to discourage overly complex models.

**L1 (Lasso):** Penalty = λ × Σ|βᵢ|
- Drives coefficients to **exactly zero** → built-in feature selection
- Produces sparse models (few features left)
- Use when many features are irrelevant

**L2 (Ridge):** Penalty = λ × Σβᵢ²
- Shrinks coefficients toward zero but **never exactly zero**
- Keeps all features with smaller weights
- Use when features are correlated (distributes weight among them)

**Elastic Net** = α×L1 + (1-α)×L2. Best of both worlds.

### 🚨 THE TRAP QUESTION

**"Are L1/L2 applicable to Random Forest?"**

**Answer: No.** L1/L2 regularize model *coefficients.* Trees have no coefficients — they split on features. Trees regularize via: max_depth, min_samples_leaf, min_samples_split, n_estimators, learning rate (boosting).

**Quick quiz:** You have 500 features but suspect only ~20 matter. L1 or L2?

**Answer:** L1 (Lasso) — it will zero out the ~480 irrelevant features, effectively doing feature selection.

---

## 🟠 ML: Classification Metrics — When to Use What

**Confusion matrix:**

|  | Predicted + | Predicted - |
|---|---|---|
| Actually + | TP | FN |
| Actually - | FP | TN |

**Precision** = TP/(TP+FP) — "Of everything I flagged, how many were correct?"
→ Use when **false positives are costly** (spam filter — don't block real emails)

**Recall** = TP/(TP+FN) — "Of everything actually positive, how many did I catch?"
→ Use when **false negatives are costly** (cancer screening — don't miss cancer)

**F1** = 2 × (P×R)/(P+R) — harmonic mean, balances both.

**Accuracy** = (TP+TN)/Total — **NEVER use for imbalanced data** (predicting majority class always = high accuracy but useless)

**ROC-AUC:** Good for comparing models. Can be misleadingly optimistic on imbalanced data.
**PR-AUC:** Better than ROC-AUC for imbalanced data — focuses on the positive class.

**Quick quiz:** You're building a fraud detection system. What metric do you prioritize and why?

**Answer:** Recall — missing fraud (false negative) is far more costly than investigating a legitimate transaction (false positive). You'd also track precision to ensure you're not overwhelming the fraud team with false alerts.

---

## 🟢 Stats: A/B Testing Design Checklist

1. **Define hypothesis:** "Changing X will increase metric Y"
2. **Pick metrics:** Primary, secondary, guardrail
3. **Calculate sample size:** n ≈ 16σ²/δ² (α=0.05, power=0.80, δ = min detectable effect)
4. **Set duration:** Minimum 2 weeks (capture weekly patterns)
5. **Randomize:** By user (not session) — hash user ID for consistency
6. **Analyze at predetermined end date** — don't peek
7. **Check statistical AND practical significance**

**Quick quiz:** Why randomize by user ID, not by session?

**Answer:** A user might have multiple sessions. If they see version A in one session and B in another, you're contaminating the experiment. Hashing user ID ensures they always see the same version.

---

## 🔶 Python: Generators

A generator yields values one at a time instead of storing everything in memory.

```python
# List = all in memory at once
squares = [x**2 for x in range(10_000_000)]  # ~80MB

# Generator = computes one at a time
squares = (x**2 for x in range(10_000_000))  # ~120 bytes
```

**Custom generator with yield:**
```python
def read_large_file(path):
    with open(path) as f:
        for line in f:
            yield line.strip()  # One line at a time

for line in read_large_file('huge.csv'):
    process(line)  # Never loads entire file
```

**Quick quiz:** What's the difference between `[x for x in range(n)]` and `(x for x in range(n))`?

**Answer:** Square brackets = list comprehension (stores all values, O(n) memory). Parentheses = generator expression (yields one at a time, O(1) memory).

---

## 🔷 SQL: Duplicate Detection and the NULL Trap

**Finding duplicates:**
```sql
SELECT email, COUNT(*) AS cnt
FROM users
GROUP BY email
HAVING COUNT(*) > 1;
```

**The NULL comparison trap:**
- `NULL = NULL` → returns NULL (not TRUE!)
- `NULL != 5` → returns NULL (not TRUE!)
- Always use `IS NULL` or `IS NOT NULL`
- `COUNT(column)` ignores NULLs, `COUNT(*)` counts all rows
- `AVG(column)` ignores NULLs (divides by non-NULL count)

**Quick quiz:** Table has 100 rows. Column `bonus` has 20 NULLs. What does `AVG(bonus)` divide by?

**Answer:** 80 — it ignores the 20 NULL rows. This can be surprising if you expect it to treat NULLs as 0. If you want NULLs as 0: `AVG(COALESCE(bonus, 0))`.

---

## Module 06 Self-Test

1. L1 vs L2: which one can zero out coefficients?
2. Can you apply L1/L2 to a Random Forest? Why or why not?
3. Precision vs recall: which do you prioritize for a cancer screening model?
4. Why is accuracy misleading for imbalanced data?
5. In an A/B test, why not check results every day?
6. `NULL = NULL` returns what?
7. What's a generator and when would you use one?

**Answers:**
1. L1 (Lasso) — its absolute value penalty can drive coefficients to exactly zero.
2. No — L1/L2 regularize coefficients. Trees have no coefficients. Trees use max_depth, min_samples_leaf, etc.
3. Recall — missing cancer (false negative) is far worse than a false alarm (false positive).
4. A model predicting only the majority class gets high accuracy while catching zero minority cases. 99% accuracy on 99/1 split = useless.
5. Peeking inflates false positive rates — a test designed for α=0.05 can have 20-30% actual error rates with repeated peeking. Pre-commit to end date or use sequential methods.
6. NULL (not TRUE). Use `IS NULL` for NULL comparison.
7. A function/expression that yields values lazily one at a time. Use for large datasets that don't fit in memory.
