# ds-interview-prep

Interactive study tool for data science interview prep. 14 modules covering SQL, Python, stats, ML, product sense, and behavioral.

## quick start

```bash
git clone https://github.com/bescob/interactive-ds-prep.git
cd interactive-ds-prep
pip install -r requirements.txt
python scripts/ingest_all.py
python run.py
```

Open `http://localhost:5050` and start studying.

## what's in it

- **Quiz mode** — randomized questions with self-grading, HTMX-driven so no page reloads
- **Flashcards** — flip cards with keyboard nav (space to flip, arrows to navigate)
- **Spaced repetition** — tracks your grades and resurfaces questions on a schedule (1d/3d/7d/14d/30d)
- **Progress tracking** — per-module completion bars, streak counter, review queue
- **STAR timer** — 2-minute countdown ring for behavioral answers so you practice staying concise
- **Code editor** — syntax-highlighted textarea for SQL/Python with tab handling and auto-indent
- **Admin panel** — add/edit/delete questions, import new markdown content with auto-parsing

## modules

01. Warm-up (SQL basics, Python data structures, probability rules, STAR)
02. First Contact (window functions, Pandas groupby/merge, Bayes, OLAP vs OLTP)
03. Pattern Builder (LAG/LEAD, transform vs apply, distributions, GAME framework)
04. Stats Core (hypothesis testing, p-values, power, confidence intervals)
05. Algorithm Arena (bias-variance, RF vs XGBoost, rolling averages, probability puzzles)
06. Regularization & Metrics (L1/L2, precision/recall, ROC/AUC, confusion matrix)
07. A/B Testing Deep Dive (peeking, multiple testing, novelty effect, Simpson's paradox)
08. Imbalanced Data & Feature Engineering (SMOTE, encoding, binning, target leakage)
09. Cross-Validation & Product Metrics (k-fold, GAME framework, metric decomposition)
10. CLT & Confidence Intervals (sampling distributions, margin of error, advanced SQL)
11. Estimation & Deep Learning (Fermi estimation, neural net basics, backprop intuition)
12. Terminology Blitz (NLP, time series, MLOps, UNION, advanced product sense)
13. Chicago Company Prep (Discover, Allstate, United, McDonald's, AbbVie interview patterns)
14. Final Boss Review (31 mixed questions across all topics, timed rounds)

## add your own content

Go to `/admin/ingest` in the browser. Paste markdown and it auto-parses into sections and questions. Headers become categories, quiz/answer pairs get extracted into the right question types. You can also manually add individual questions at `/admin/questions`.

## stack

Flask, HTMX, highlight.js. Progress stored as JSON on disk. No database, no npm, no build step.

## deploy

Standard Flask app. For studying with friends just run it locally. If you want it hosted, works on fly.io, Railway, Render, or any platform that runs Python.

---

[bescob.ar](https://bescob.ar)
