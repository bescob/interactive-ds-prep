# Module 13 — Chicago Company Prep & Mixed Review

*Topics: Chicago interview patterns, PCA, SQL HAVING vs WHERE, Python `if __name__`, Behavioral collaboration story*

---

## 🏙️ Chicago Interview Differences

Chicago DS interviews are NOT FAANG interviews. Key differences:

**17% more modeling questions** — they want to know you understand the algorithms, not just call `.fit()`.

**Domain knowledge matters.** Discover wants credit risk intuition. AbbVie wants clinical trial awareness. McDonald's wants supply chain thinking. United wants demand forecasting context.

**Take-home assignments are standard.** United gives 48hrs (intentionally open-ended). Grubhub gives 72hrs. Allstate has a transportation company case study.

**STAR behavioral is used rigidly.** Allstate starts with 10 automated behavioral questions recorded by phone. AbbVie and Caterpillar use strict STAR rubrics.

**Communication > algorithmic puzzles.** Explaining technical work to non-technical stakeholders is tested explicitly.

### Company Quick-Hits

| Company | Key Focus | Watch Out |
|---|---|---|
| Discover | SQL (Snowflake), credit risk, statistics | Learn QUALIFY clause |
| Allstate | ML math (imbalanced data, CV, logistic internals) | Automated phone behavioral first |
| United | Strategic thinking over technical depth | Very slow process (3+ months) |
| McDonald's | SQL + Python + cultural fit | 5-6 rounds, ~2 months |
| AbbVie | Logistic regression + clinical trial context | Must explain analytics to pharma stakeholders |
| CME Group | Financial derivatives domain knowledge | Brain teasers common |
| Morningstar | NLP, transformers, AI | Extremely slow (7+ months reported) |

**Your edge:** SWE background at Meta + D.Eng is rare in the Chicago market. Most candidates come from analytics or academia. Lean into your ability to build end-to-end systems.

---

## 🟠 ML: PCA in Simple Terms

**What it does:** Finds new axes (principal components) that capture the most variance. The first component captures the most, the second captures the most remaining variance perpendicular to the first, and so on.

**Keep only the top k components** → reduce dimensions while retaining most information.

**It's a rotation + projection, not feature selection.** Each component is a LINEAR COMBINATION of original features, not a single feature.

**When to use:** High-dimensional data where features are correlated (100 survey questions → 5 underlying factors). Also for visualization (reduce to 2D/3D).

**Quick quiz:** You have 200 features. After PCA, the first 15 components explain 95% of variance. What do you do?

**Answer:** Keep 15 components, drop the rest. You've reduced from 200 to 15 dimensions while retaining 95% of the information. The remaining 185 components mostly capture noise.

---

## 🔷 SQL: WHERE vs HAVING — Once and For All

**WHERE** filters **individual rows** BEFORE grouping.
**HAVING** filters **groups** AFTER aggregation.

```sql
-- WHERE: filter rows before grouping
SELECT department, AVG(salary) AS avg_salary
FROM employees
WHERE hire_date > '2020-01-01'     -- Only recent hires (row-level)
GROUP BY department
HAVING AVG(salary) > 80000;        -- Only departments with high avg (group-level)
```

**The rule:** If it involves an aggregate function (COUNT, SUM, AVG, MAX, MIN), it goes in HAVING. If it filters individual column values, it goes in WHERE.

**Quick quiz:** "Find departments with more than 10 employees who earn over $50K."

```sql
SELECT department, COUNT(*) AS high_earners
FROM employees
WHERE salary > 50000           -- Row filter: only high earners
GROUP BY department
HAVING COUNT(*) > 10;          -- Group filter: departments with 10+ of them
```

Both WHERE and HAVING in the same query — WHERE narrows the rows first, HAVING filters the groups after.

---

## 🔶 Python: `if __name__ == '__main__'`

```python
if __name__ == '__main__':
    main()
```

**What it does:** Checks if the file is being run directly (not imported).

- Run `python script.py` → `__name__` is `'__main__'` → code inside executes
- Another file does `import script` → `__name__` is `'script'` → code inside is SKIPPED

**Why it exists:** So you can write a module that's both importable (other files use its functions) AND runnable as a standalone script.

---

## 🟠 Behavioral: The "Cross-Functional Collaboration" Story

Chicago companies emphasize this heavily — they want proof you can work with non-DS teams.

**Template:**
- **S:** "I worked with [engineering/product/business team] on [project]."
- **T:** "My role was to [provide the data/analytical perspective]."
- **A:** "I [specific collaboration: translated requirements, built shared dashboards, presented findings in accessible terms, iterated based on their feedback]."
- **R:** "[Outcome] — and the process established a [repeatable workflow/better relationship]."

**The key phrase interviewers want to hear:** "I translated the technical findings into business terms" or "I met with stakeholders to understand their actual decision, then shaped the analysis around that."

---

## 🟢 Repeat: A/B Test Design

Without looking, list the 7 steps of designing an A/B test:

**Try it, then check.**

**Answer:**
1. Define hypothesis
2. Pick metrics (primary, secondary, guardrail)
3. Calculate sample size (n ≈ 16σ²/δ²)
4. Set duration (≥2 weeks)
5. Randomize by user (hash user ID)
6. Analyze at predetermined end date (no peeking)
7. Check statistical AND practical significance

---

## 🟠 Repeat: Bias-Variance Diagnostic

| You see... | It's... | You do... |
|---|---|---|
| Both train and test error high | High bias (underfitting) | More complex model, add features |
| Low train, high test error | High variance (overfitting) | More data, regularize, simplify |
| Both low and close | Just right | Ship it |

---

## Module 13 Self-Test

1. Name 2 ways Chicago DS interviews differ from FAANG.
2. What is PCA? Is it feature selection?
3. WHERE vs HAVING: which filters groups after aggregation?
4. What does `if __name__ == '__main__'` do?
5. Recite the A/B test design steps from memory.
6. Your SWE background — how is this an advantage for Chicago DS roles?

**Answers:**
1. More modeling questions (less LeetCode), domain knowledge heavily weighted, take-home assignments standard, rigid STAR behavioral.
2. PCA finds new axes (principal components) that capture maximum variance, then keeps the top k. It's NOT feature selection — each component is a linear combination of ALL original features.
3. HAVING — WHERE filters individual rows before grouping.
4. Checks if the script is run directly (executes the code) vs imported as a module (skips the code).
5. (1) Hypothesis (2) Metrics (primary/secondary/guardrail) (3) Sample size (4) Duration ≥2 weeks (5) Randomize by user (6) Analyze at end date — no peeking (7) Statistical + practical significance.
6. Most Chicago DS candidates come from analytics/academia. Your ability to build end-to-end systems (pipelines, deployment, production code) is rare and highly valued. Lean into this in every behavioral.
