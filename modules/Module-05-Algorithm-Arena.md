# Module 05 — Algorithm Arena

*Topics: Bias-variance tradeoff, Random Forest vs XGBoost, SQL rolling averages, Probability puzzles*

---

## 🟠 ML: The Bias-Variance Tradeoff

**Total Error = Bias² + Variance + Irreducible Error**

**Bias** = systematic error from oversimplified model. "A straight line trying to fit a curve."
**Variance** = sensitivity to training data. "The model memorized the noise."

| Symptom | Diagnosis | Fix |
|---|---|---|
| Both train AND test error high | High bias (underfitting) | More complex model, add features, less regularization |
| Low train error, HIGH test error | High variance (overfitting) | More data, regularization, simpler model, dropout |

**Quick quiz:** Your model gets 95% train accuracy and 72% test accuracy. What's the problem and what do you try first?

**Answer:** Overfitting (high variance) — 23% gap between train and test. Try: more training data, add regularization (L1/L2), reduce model complexity, or use dropout if neural net.

---

## 🟠 ML: Random Forest vs Gradient Boosting

| Aspect | Random Forest | Gradient Boosting (XGBoost) |
|---|---|---|
| How trees are built | Independently, in parallel | Sequentially, each corrects errors |
| Individual trees | Deep (strong learners) | Shallow (weak learners, 3-6 levels) |
| Primary effect | Reduces variance | Reduces bias |
| Overfitting risk | Lower | Higher |
| Tuning difficulty | Easy (good defaults) | Hard (learning rate, depth, subsample) |
| When to use | Quick baseline, noisy data, limited tuning time | Max accuracy, clean data, time to tune |

**Interview question:** "When would you pick Random Forest over XGBoost?"

**Answer:** "When I have limited tuning time, noisy data, or need a reliable baseline fast. RF is harder to screw up — works well with defaults. XGBoost can outperform with careful tuning but can also overfit badly with wrong hyperparameters."

---

## 🔷 SQL: Rolling Averages

```sql
-- 7-day rolling average of daily revenue
SELECT date, revenue,
  AVG(revenue) OVER (
    ORDER BY date
    ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
  ) AS rolling_7d_avg
FROM daily_revenue;
```

**Key detail:** 6 PRECEDING + CURRENT ROW = 7 rows total. A common mistake is writing `7 PRECEDING` which gives 8 rows.

**Running total (cumulative sum):**
```sql
SUM(amount) OVER (ORDER BY date ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)
```

---

## 🟢 Stats: Classic Probability Puzzles

### Monty Hall
You pick Door 1 (1/3 chance of winning). Host opens Door 3 (goat). Should you switch to Door 2?

**Always switch. Switching = 2/3. Staying = 1/3.**

Your initial 1/3 didn't change. The other two doors had 2/3 combined. Host revealed one was wrong, so the remaining door inherits the full 2/3.

### Birthday Problem
How many people for >50% chance of a shared birthday? **23.**

Compute complement: P(no match) = (364/365)(363/365)...(343/365). At n=23, P(no match) < 0.5.

### Expected value of a die roll
E = 1(1/6) + 2(1/6) + 3(1/6) + 4(1/6) + 5(1/6) + 6(1/6) = **3.5**

"Would you pay $4 to play a game where you win whatever you roll in dollars?" **No** — expected payout is $3.50, you'd lose $0.50 on average.

---

## 🟠 Behavioral: The "Data-Driven Decision" Story

This is the #1 most-asked behavioral question. Have your STAR ready:

**Template (adapt to your experience):**
- **S:** "On the [X] team, stakeholders wanted to [do something based on intuition]."
- **T:** "I needed to validate/challenge this assumption with data."
- **A:** "I pulled data from [source], ran [analysis], and found [counterintuitive insight]. I presented this to [stakeholders] using [visualization/simple framing]."
- **R:** "This changed the decision to [better outcome], resulting in [quantified impact]."

**Practice saying your version out loud right now. Time yourself — aim for under 2 minutes.**

---

## Module 05 Self-Test

1. Your model has high BOTH train and test error. Diagnosis and fix?
2. RF reduces ___. XGBoost reduces ___.
3. Write a 3-day rolling average window clause.
4. Why should you switch in Monty Hall?
5. Expected value of rolling a fair die?
6. How many people for >50% shared birthday probability?

**Answers:**
1. Underfitting (high bias). Fix: more complex model, add features, reduce regularization.
2. RF reduces variance. XGBoost reduces bias.
3. `AVG(x) OVER (ORDER BY date ROWS BETWEEN 2 PRECEDING AND CURRENT ROW)`
4. Initial pick = 1/3. The remaining door inherits the full 2/3 after the host reveals a goat.
5. 3.5
6. 23 people.
