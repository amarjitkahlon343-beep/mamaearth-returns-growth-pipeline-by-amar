# Mamaearth Returns & Growth Intelligence Pipeline

**Capstone Project** — Data Analytics with AI & GenAI  
**Program:** E&ICT Academy, IIT Roorkee  
**Author:** Amarjit Kahlon

One public GitHub repository. Every number in this brief is produced by running the three layers below against the committed seed data.

---

## Repository Structure
/
├── README.md
├── sql/
│   ├── schema.sql
│   ├── seed_data.sql
│   └── reports.sql
├── data/
│   ├── customers.csv
│   ├── products.csv
│   └── orders.csv
├── analysis/
│   ├── clean_and_eda.py
│   └── visualize.py
├── visualizations/
│   ├── return_rate_by_payment.png
│   └── monthly_revenue_trend.png
└── narrator/
├── findings.json
├── generate_narrative.py
└── sample_output.txt
text---

## How the Three Layers Connect

1. **SQL Layer** loads the same CSVs into SQLite and answers relational questions on the *raw* 180 rows (gross revenue ₹99,860.20).
2. **Python Layer** re-reads the same CSVs, cleans them (payment casing, 5 duplicates, imputations, IQR flags), and writes verified numbers to `narrator/findings.json` (cleaned revenue ₹97,358.30).
3. **GenAI Layer** reads *only* `findings.json` and produces an SCR narrative (online Gemini or offline template). No layer invents a number the previous layer did not compute.

---

## 1. SQL Layer — Schema, Seed & Reports

Requires SQLite 3 (or any engine that accepts the syntax in `schema.sql`).

```bash
# Create empty DB and apply schema
sqlite3 mamaearth.db < sql/schema.sql

# Load seed data (45 customers, 16 products, 180 orders)
sqlite3 mamaearth.db < sql/seed_data.sql

# Sanity counts
sqlite3 mamaearth.db "SELECT COUNT(*) FROM customers;"   # → 45
sqlite3 mamaearth.db "SELECT COUNT(*) FROM products;"    # → 16
sqlite3 mamaearth.db "SELECT COUNT(*) FROM orders;"      # → 180

# Run all Task 3 reports (a–i)
# Expected outputs are documented as comments above each query
sqlite3 mamaearth.db < sql/reports.sql
If you use .import instead of seed_data.sql, run this cleanup after import:
SQLUPDATE orders SET discount_pct = NULL WHERE discount_pct = '';
UPDATE orders SET rating = NULL WHERE rating = '';

2. Python Analysis Layer — Cleaning, EDA, Charts & findings.json
Bashpip install pandas matplotlib

# Tasks 1–10 of Part 2 + writes narrator/findings.json
python analysis/clean_and_eda.py

# Task 11 — regenerates the two required PNGs
python analysis/visualize.py
clean_and_eda.py prints every intermediate acceptance value (shape, payment counts, dropped order_ids, median rating, cleaned total, reconciliation paragraph, IQR bounds, return rates, segmentation, correlations, and both monthly series).
findings.json is written programmatically by the script — never hand-typed — so it cannot drift from the Part 2 numbers.

3. GenAI Narrative Layer — Online or Offline
Bash# Offline path (no API key required) — deterministic SCR template
python narrator/generate_narrative.py

# Online path — free Gemini key from Google AI Studio
export GEMINI_API_KEY="your-free-key-here"
python narrator/generate_narrative.py

With GEMINI_API_KEY (or GOOGLE_API_KEY) set: Calls google-genai with temperature=0.0, explicit max_output_tokens, and timeout ≥ 10 seconds. Returns a structured {status, narrative, tokens} dictionary. On any failure it automatically falls back to the offline path.
With no key: Runs the offline function only.

Both paths write narrator/sample_output.txt and run the Task 5 numeric accuracy checker (pass/fail line for each required figure). The grader verifies the saved sample, not a live API call.
Optional dependency for the online path only:
Bashpip install google-genai

Key Verified Figures

































FigureValueRaw total revenue (Part 1)99,860.20Cleaned total revenue (Part 2)97,358.30Duplicate reconciliation delta2,501.90COD / CARD / UPI return rates44.4% / 14.7% / 18.9%Highest-risk segmentCOD + Tier-2 at 54.5%True peak month (outlier-corrected)March 20,318.90
A reader who has never seen this repository can reproduce every number above by following this README from top to bottom.

Author Declaration
This complete end-to-end pipeline (SQL relational layer, Pandas cleaning & EDA, visualizations, and GenAI narrative with offline fallback) was independently designed, implemented, tested and documented by Amarjit Kahlon as the Capstone Project for the program Data Analytics with AI & GenAI – E&ICT Academy, IIT Roorkee.
All logic, numbers and outputs were generated and verified by the author against the provided seed data.
