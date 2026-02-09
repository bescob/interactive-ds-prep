# Module 11 — Estimation & Deep Learning Basics

*Topics: Fermi estimation, DL basics (when asked), Pandas memory optimization, Coupon collector, Star schema*

---

## 🟠 Product Sense: Fermi Estimation

These test structured thinking, not exact numbers.

### The framework
1. **Clarify scope:** Define what you're estimating
2. **Break into components:** Multiplication chain of estimable pieces
3. **Estimate each component:** Round numbers are fine
4. **Sanity check:** Does the result feel reasonable?

### Worked example: "How many Uber rides happen in Chicago per day?"

**Approach 1 (demand-side):**
- Chicago metro: ~9.5M people
- Maybe 10% use ride-sharing monthly: 950K
- Average ride-share user: ~4 rides/month ÷ 30 days ≈ 0.13/day
- 950K × 0.13 ≈ **~125K rides/day**

**Approach 2 (supply-side):**
- Estimate ~30K active drivers in Chicago
- Each driver does ~8-10 rides per shift
- Maybe 60% are active on a given day: 18K
- 18K × 9 ≈ **~160K rides/day**

Two approaches giving roughly similar answers → confidence we're in the right ballpark.

**Practice these on your own:**
- How many text messages are sent in the US per day?
- How much revenue does a single Starbucks generate per year?
- How many data scientists are there in Chicago?

---

## 🟣 Terminology: Deep Learning (When They Ask)

### Neural Networks
Layers of connected nodes. Data flows through layers; weights are adjusted via backpropagation to minimize loss. "Deep" = many layers.

### CNN (Convolutional Neural Networks)
For spatial data (images). Learnable filters slide across input detecting patterns: edges → textures → objects. Parameter sharing makes them efficient.

### RNN / LSTM
For sequential data. RNNs maintain hidden state but suffer from vanishing gradients (forget long sequences). LSTMs add gating to selectively remember/forget.

### Transformers
Process entire sequences in parallel via self-attention (each element attends to all others). Much faster than RNNs. Foundation of BERT, GPT.

### The key interview answer

**"When do you use deep learning vs gradient boosting?"**

For **tabular data** (most DS work): gradient-boosted trees almost always win. Faster to train, more interpretable, needs less data.

For **unstructured data** (images, text, audio): deep learning wins. Feature engineering is impractical — let the network learn features.

---

## 🔶 Pandas: Memory Optimization

```python
# Check current memory
df.info(memory_usage='deep')

# 1. Categorical columns (low cardinality strings → massive savings)
df['status'] = df['status'].astype('category')  # 'active','inactive' repeated 1M times

# 2. Downcast numerics
df['age'] = pd.to_numeric(df['age'], downcast='integer')  # int64 → int8 if values fit

# 3. Float64 → Float32 (halves memory)
float_cols = df.select_dtypes(include=['float64']).columns
df[float_cols] = df[float_cols].astype('float32')

# 4. Load only needed columns
df = pd.read_csv('big.csv', usecols=['col1', 'col2', 'col3'])
```

**Quick quiz:** A column has 2 million rows but only 5 unique string values. How do you reduce its memory?

**Answer:** `df['col'] = df['col'].astype('category')` — stores 5 unique values + integer codes instead of 2M full strings. Can reduce memory 95%+.

---

## 🟢 Stats: Coupon Collector Problem (Meta Favorite)

"Expected rolls to see all 6 sides of a fair die?"

When you've seen k sides, P(new side) = (6-k)/6. Expected rolls for that stage = 6/(6-k).

```
E = 6/6 + 6/5 + 6/4 + 6/3 + 6/2 + 6/1
  = 1 + 1.2 + 1.5 + 2 + 3 + 6
  = 14.7 rolls
```

**Generalized:** For n types: E = n × (1 + 1/2 + 1/3 + ... + 1/n) = n × Hₙ (harmonic number)

---

## 🟣 Terminology: Star Schema

A data warehouse design pattern:
- Central **fact table** = events/transactions (order_id, customer_id, product_id, date_id, amount)
- Surrounding **dimension tables** = descriptive context (customers, products, dates, stores)

**Why it works for analytics:** Queries join the fact table to whichever dimensions they need. Simple, predictable, fast.

```
          [dim_customer]
               |
[dim_date] — [fact_sales] — [dim_product]
               |
          [dim_store]
```

---

## 🟢 Repeat: Bayes' Theorem — Final Boss

Do this one cold. No formula lookup.

"A factory has two machines. Machine A produces 60% of items and has a 2% defect rate. Machine B produces 40% and has a 5% defect rate. A randomly chosen item is defective. What's the probability it came from Machine A?"

**Work it out, then check.**

**Answer:**
```
P(A|Defective) = P(Def|A) × P(A) / [P(Def|A) × P(A) + P(Def|B) × P(B)]
               = (0.02 × 0.60) / (0.02 × 0.60 + 0.05 × 0.40)
               = 0.012 / (0.012 + 0.020)
               = 0.012 / 0.032
               = 0.375 → 37.5%
```

Even though Machine A makes more items, its lower defect rate means a defective item is more likely from Machine B (62.5%).

---

## Module 11 Self-Test

1. Walk through a Fermi estimate for "How many pizza deliveries happen in Chicago per day?"
2. Tabular data: deep learning or gradient boosting? Why?
3. How does converting a string column to category type save memory?
4. Expected rolls to see all 6 die faces?
5. What's a star schema? Name the two types of tables.
6. Bayes — a defective item from a two-machine factory. Can you set up the formula without looking?

**Answers:**
1. ~2.8M population in city proper. Maybe 20% order pizza weekly = 560K orders/week ÷ 7 = ~80K/day. Of those, maybe 60% delivery = ~48K. Sanity check: there are ~2,000 pizza places × ~25 deliveries/day ≈ 50K. ✓
2. Gradient boosting — faster, more interpretable, needs less data, usually outperforms DL on tabular data.
3. Stores unique values once + integer codes per row, instead of full string per row. For 2M rows with 5 unique values, goes from storing 2M strings to 5 strings + 2M tiny integers.
4. 14.7 rolls. E = 6(1 + 1/2 + 1/3 + 1/4 + 1/5 + 1/6).
5. Central fact table (transactions/events) surrounded by dimension tables (who, what, where, when). Optimized for analytical queries with simple, predictable joins.
6. P(A|Def) = P(Def|A)×P(A) / [P(Def|A)×P(A) + P(Def|B)×P(B)]
