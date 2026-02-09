# Module 07 — A/B Testing Deep Dive

*Topics: A/B testing pitfalls, Root cause analysis, Logistic regression, Python missing data, Behavioral "failure" story*

---

## 🟢 Stats: A/B Testing Pitfalls (Interviewers Love These)

### Peeking — The #1 Pitfall
Checking results daily and stopping when you see significance. A test designed for α=0.05 can have **20-30% actual false positive rates** with repeated peeking.

**Fix:** Pre-commit to a sample size and duration. Or use sequential testing methods (e.g., always-valid p-values).

### Multiple Testing
Testing 20 metrics at α=0.05? Expect 1 false positive by pure chance.

**Fix:** Bonferroni correction (use α/k for k tests), or designate ONE primary metric beforehand.

### Novelty Effect
Users engage more with something just because it's new, not because it's better.

**Fix:** Run long enough for novelty to wear off (typically 2-4 weeks).

### Simpson's Paradox
Aggregate results can show the OPPOSITE of segment-level results.

**Example:** Treatment looks worse overall, but better in EVERY demographic — because the treatment group had proportionally more users from a harder-to-convert segment.

**Fix:** Always check segment-level results.

### Network Effects
On social platforms, treated and control users interact, contaminating results.

**Fix:** Cluster randomization (by geography, social graph, or time).

**Quick quiz:** You run an A/B test for 3 days, see p=0.02, and your PM wants to ship immediately. What do you say?

**Answer:** "We should wait. Three days isn't enough to capture weekly patterns (weekday vs weekend behavior differs). Also, early significance with a small sample is unreliable — the effect size estimate is noisy and may shrink. Let's run to our pre-committed duration."

---

## 🟢 Stats: CUPED (Advanced — 2024-25 Interview Trend)

**What it is:** Controlled-experiment Using Pre-Existing Data. Reduces variance by adjusting for pre-experiment behavior.

**The intuition:** If a user was already high-spending BEFORE the experiment, their high spending DURING the experiment isn't due to the treatment. CUPED subtracts this pre-experiment baseline, reducing noise and letting you detect smaller effects with the same sample size.

**Where it's used:** Meta, Netflix, Microsoft, Uber — almost every major tech company.

**Why interviewers ask:** It shows you understand that A/B testing isn't just "compare two means." It's about reducing variance to make better decisions faster.

---

## 🟠 Product Sense: Root Cause Analysis

When an interviewer says "Metric X dropped Y%," use this structure:

1. **Clarify:** What exactly is the metric? How is it calculated? What timeframe?
2. **Decompose:** Revenue = Users × Conversion × AOV. Which piece dropped?
3. **Internal first:** Recent deployments? Bugs? Logging changes? A/B tests?
4. **External:** Seasonality? Competitor actions? Market events?
5. **Segment:** All users or specific group? All platforms? All regions?
6. **Classify and recommend:** Name the likely cause, suggest next steps.

**Practice:** "DAU dropped 8% this week." Walk through the framework in your head before reading.

**Example answer:** "First, is this vs last week or vs same week last year? Is it all platforms? I'd decompose into new user signups vs returning user logins. Check: any recent app updates or outages? Any logging changes that might be measurement artifacts? External: is there a holiday, competitor launch, or app store ranking change? I'd segment by platform (iOS/Android), geography, and acquisition channel to isolate where the drop is concentrated."

---

## 🟠 ML: Logistic Regression — Classification, Not Regression

**How it works:** Takes linear combination z = β₀ + β₁x₁ + ... and passes it through the **sigmoid function:**

```
P(Y=1) = 1 / (1 + e^(-z))
```

Sigmoid squashes any real number to (0, 1) → interpreted as probability.

**Interpreting coefficients:** A one-unit increase in xᵢ multiplies the **odds** by e^βᵢ. If β = 0.7, odds multiply by e^0.7 ≈ 2.01 → odds roughly double.

**Q: "Why not use linear regression for classification?"**
A: Linear regression can predict values outside [0,1], which don't work as probabilities. It also minimizes squared error, which isn't the right objective for classification. Logistic regression constrains output to [0,1] and uses log loss (binary cross-entropy).

---

## 🔶 Python: Handling Missing Data

```python
# Detect
df.isnull().sum()                     # NaN count per column
df.isnull().mean()                    # Fraction missing per column

# Remove
df.dropna()                           # Drop ANY row with NaN
df.dropna(subset=['critical_col'])    # Only if specific column is NaN

# Fill
df['col'].fillna(0)                   # Constant
df['col'].fillna(df['col'].mean())    # Column mean
df['col'].fillna(method='ffill')      # Forward fill (last known value)
```

**Interview question:** "When would you drop NaN vs fill it?"

**Answer:** Drop when: missingness is random AND few rows affected (<5%). Fill when: data is valuable, missingness has a pattern (time series → ffill), or the column is critical. NEVER blindly fill with mean — check if the missingness is informative (e.g., income=NaN might mean "refused to answer," which IS information).

---

## 🟠 Behavioral: The "Failure" Story

Every company asks this. The secret: **they're testing self-awareness, not perfection.**

**Template:**
- **S/T:** "I was tasked with [X] under [constraints]."
- **A:** "I chose [approach] because [reasoning]. It didn't work because [specific issue — own it]."
- **A (continued):** "I then pivoted to [better approach]."
- **R:** "The outcome was [result]. The lesson I took away was [specific takeaway I still apply today]."

**Rules:**
- Take ownership — never blame the data, the team, or the timeline
- Show learning, not just failure
- Pick something real but not catastrophic
- End on what you do differently NOW because of it

**Practice saying yours out loud. Time it — under 2 minutes.**

---

## 🟢 Repeat: Bias-Variance (Can You Still Explain It?)

Without looking at Module 05, answer:

1. What are the two components of reducible error?
2. Which one means "too simple"?
3. Which one means "memorized noise"?
4. Your model: 98% train accuracy, 65% test accuracy. What's wrong?

**Answers:**
1. Bias and variance.
2. High bias = too simple (underfitting).
3. High variance = memorized noise (overfitting).
4. Overfitting — massive gap between train and test. Regularize, get more data, or simplify model.

---

## Module 07 Self-Test

1. Name 3 A/B testing pitfalls and the fix for each.
2. What is CUPED and why does it help?
3. "DAU dropped 10%." What's your first question?
4. What does the sigmoid function do in logistic regression?
5. When should you drop NaN vs fill it?
6. Tell your "failure" STAR story in under 2 minutes. (Actually do this out loud.)

**Answers:**
1. Peeking (pre-commit to end date), multiple testing (Bonferroni correction or single primary metric), novelty effect (run longer). Also: Simpson's paradox (check segments), network effects (cluster randomization).
2. Reduces variance by adjusting for pre-experiment behavior, letting you detect smaller effects with the same sample size.
3. "Is this compared to last week or same week last year? Is it all platforms/regions, or concentrated somewhere?" — clarify before decomposing.
4. Squashes any real number to (0,1), making the output interpretable as a probability.
5. Drop if random + few rows. Fill if data is valuable, but check whether missingness itself is informative.
6. (Self-grade: Did you use "I"? Quantify? Show learning? Under 2 min?)
