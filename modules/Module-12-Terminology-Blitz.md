# Module 12 — Terminology Blitz & Advanced Product Sense

*Topics: NLP basics, Time series concepts, Advanced product questions, MLOps terminology, SQL UNION*

---

## 🟣 Terminology: NLP Basics

**Tokenization:** Splitting text into units. "I love cats" → ["I", "love", "cats"]. Modern models use subword tokenization (handles unknown words).

**TF-IDF:** Term Frequency × Inverse Document Frequency. Words frequent in one document but rare everywhere get high scores. Common words ("the", "is") get low scores. Simple but surprisingly effective baseline.

**Word Embeddings (Word2Vec, GloVe):** Map words to dense vectors. Similar words are close together. Famous: "king" - "man" + "woman" ≈ "queen".

**Transformers/BERT:** Contextual embeddings — same word gets DIFFERENT vectors depending on context. "bank" in "river bank" ≠ "bank" in "bank account." Foundation of modern NLP.

**Quick quiz:** What's the key advantage of BERT over Word2Vec?

**Answer:** BERT produces contextual embeddings — the same word gets different representations depending on surrounding words. Word2Vec gives each word a single fixed vector regardless of context.

---

## 🟣 Terminology: Time Series Concepts

**Stationarity:** Statistical properties (mean, variance) don't change over time. Most models require this. Test: ADF (Augmented Dickey-Fuller). Fix: differencing.

**Seasonality:** Regular periodic patterns (daily, weekly, yearly).

**Trend:** Long-term directional movement (up, down, flat).

**Autocorrelation:** Correlation of a series with lagged versions of itself. High at lag 7? Weekly pattern.

**ARIMA:** AutoRegressive (past values predict future) + Integrated (differencing) + Moving Average (past errors predict future). Parameters: (p, d, q) = AR order, differencing order, MA order.

**Quick quiz:** A time series of daily ice cream sales has an upward slope and spikes every summer. Name the two components.

**Answer:** Trend (upward slope) and seasonality (annual summer spikes).

---

## 🟣 Terminology: MLOps & Production ML

**Feature Store:** Centralized system for storing/serving ML features. Ensures consistency between training and serving.

**Training-Serving Skew:** When features are computed differently in training (batch) vs production (real-time). Causes silent performance degradation. Feature stores fix this.

**Model Drift:** Performance degrades over time because real-world distributions change. Two types:
- **Data drift:** Input distribution changes (user demographics shift)
- **Concept drift:** Relationship between inputs and outputs changes (what "spam" looks like evolves)

Solution: Monitor predictions, set alerts, retrain periodically.

---

## 🟠 Product Sense: Advanced Questions

### "DAU dropped 5% but revenue is up 3%. What's happening?"

"Fewer users are spending more each. Possible explanations:
- Churned users were low-value (free tier, light users) — not necessarily bad
- A price increase drove away price-sensitive users — check sustainability
- A new premium feature engages power users but alienates casual ones
- Seasonal user mix shift (holiday shoppers spend more per visit)

I'd segment by user cohort and revenue tier to understand which users left and which are spending more."

### "Notifications increased DAU by 8% but also increased uninstalls by 3%. Ship it?"

"Depends on the math. Questions I'd ask:
- What's the LTV of retained users vs lost users?
- Is the DAU gain a novelty effect that will fade?
- Are uninstallers low-value users who weren't going to monetize?
- Run test longer — if the DAU gain fades but uninstalls persist, net is negative.
- Can we tune notification frequency to keep most of the DAU gain with fewer uninstalls?"

---

## 🔷 SQL: UNION vs UNION ALL

**UNION** — combines results and **removes duplicates** (slower — must sort/compare).
**UNION ALL** — combines results and **keeps everything** including duplicates (faster).

**Rule:** Use UNION ALL unless you specifically need deduplication. It's significantly faster.

```sql
-- Combine two event sources
SELECT user_id, event_time, 'web' AS source FROM web_events
UNION ALL
SELECT user_id, event_time, 'mobile' AS source FROM mobile_events;
```

**Quick quiz:** When would you actually need UNION (not UNION ALL)?

**Answer:** When the two tables might have overlapping rows and you want each unique row exactly once. Example: combining a "customers who bought" list with a "customers who browsed" list, and you want a unique list of all customers who did either.

---

## 🟢 Repeat: Standard Error and Sample Size

Answer without looking:

1. SE formula?
2. You want to halve your confidence interval width. How much more data?
3. What does CLT guarantee about sample means?

**Answers:**
1. SE = σ / √n
2. 4× the data. Width ∝ 1/√n, so halving requires √n to double, meaning n quadruples.
3. They approach a normal distribution regardless of the underlying data distribution, with mean = population mean and SD = σ/√n.

---

## 🟠 Repeat: L1 vs L2 Speed Round

1. Which drives coefficients to exactly zero?
2. Which is better when features are correlated?
3. Can you apply either to XGBoost?
4. You suspect 90% of your 200 features are noise. Which one?

**Answers:**
1. L1 (Lasso)
2. L2 (Ridge) — distributes weight among correlated features
3. No — they regularize coefficients, trees don't have coefficients
4. L1 — it will zero out the ~180 irrelevant features

---

## Module 12 Self-Test

1. BERT vs Word2Vec — key difference in one sentence?
2. What is stationarity and how do you test for it?
3. What is model drift? Name the two types.
4. "DAU down, revenue up" — give 2 possible explanations.
5. UNION vs UNION ALL — which is faster and why?
6. SE = σ/√n. If n goes from 100 to 400, what happens to SE?

**Answers:**
1. BERT gives contextual embeddings (same word → different vector based on context); Word2Vec gives one fixed vector per word.
2. Statistical properties don't change over time. Test with ADF (Augmented Dickey-Fuller). Fix with differencing.
3. Model performance degrades as real-world data changes. Data drift (input distribution changes) and concept drift (input-output relationship changes).
4. (a) Churned users were low-value, remaining users spend more. (b) Price increase drove away price-sensitive users.
5. UNION ALL — no deduplication step needed, no sorting/comparing.
6. Halves. SE = σ/√400 = σ/20 vs σ/√100 = σ/10. √n doubled, so SE halved.
