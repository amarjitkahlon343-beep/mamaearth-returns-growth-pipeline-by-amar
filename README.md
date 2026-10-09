# Mamaearth Returns & Growth Intelligence Pipeline

**Capstone Project — Data Analytics with AI & GenAI**
**Program:** E&ICT Academy, IIT Roorkee
**Author:** Amarjit Kahlon

An end-to-end data analytics project integrating SQL, Python, data visualization, and Generative AI to analyze retail revenue, product returns, customer behavior, and business growth opportunities.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [Project Objectives](#project-objectives)
4. [SQL Layer](#1-sql-layer)
5. [Python Analysis Layer](#2-python-analysis-layer)
6. [GenAI Narrative Layer](#3-genai-narrative-layer)
7. [How the Three Layers Connect](#how-the-three-layers-connect)
8. [Key Verified Figures](#key-verified-figures)
9. [Installation and Execution](#installation-and-execution)
10. [Business Value](#business-value)
11. [Technologies Used](#technologies-used)
12. [Project Deliverables](#project-deliverables)
13. [Troubleshooting](#troubleshooting)
14. [Author Declaration](#author-declaration)

---

## Project Overview

The Mamaearth Returns & Growth Intelligence Pipeline is an end-to-end analytics project designed to transform raw retail transaction data into actionable business insights.

The project integrates three layers:

* **SQL:** Relational database management and business reporting.
* **Python:** Data cleaning, exploratory data analysis (EDA), statistical analysis, and visualization.
* **Generative AI:** Business narrative generation using verified analytical findings.

The pipeline aims to make analytical results reproducible by generating findings programmatically and using them as input for the narrative generation stage.

## Repository Structure

```text
mamaearth-returns-growth-pipeline-by-amar/
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
```

## Project Objectives

* Analyze raw and cleaned revenue.
* Identify and handle duplicate records.
* Standardize payment-method categories.
* Investigate return rates across payment methods.
* Analyze customer segments and return behavior.
* Examine monthly revenue trends and outliers.
* Generate visualizations to communicate findings.
* Produce an SCR (Situation–Complication–Resolution) narrative.
* Validate narrative figures against computed results.

---

## 1. SQL Layer

The SQL layer loads the seed data into SQLite and generates relational reports from the raw transaction records.

### Prerequisites

* SQLite 3
* Terminal or command prompt

### Create the database

```bash
sqlite3 mamaearth.db < sql/schema.sql
```

### Load seed data

```bash
sqlite3 mamaearth.db < sql/seed_data.sql
```

### Verify record counts

```bash
sqlite3 mamaearth.db "SELECT COUNT(*) FROM customers;"
sqlite3 mamaearth.db "SELECT COUNT(*) FROM products;"
sqlite3 mamaearth.db "SELECT COUNT(*) FROM orders;"
```

Expected counts:

| Table     | Expected Records |
| --------- | ---------------: |
| Customers |               45 |
| Products  |               16 |
| Orders    |              180 |

### Execute reports

```bash
sqlite3 mamaearth.db < sql/reports.sql
```

The reports file contains the project's Task 3 SQL queries (a–i).

If CSV import produces empty strings in numeric fields, normalize them where appropriate:

```sql
UPDATE orders
SET discount_pct = NULL
WHERE discount_pct = '';

UPDATE orders
SET rating = NULL
WHERE rating = '';
```

**Output:** SQLite database and SQL report results.

---

## 2. Python Analysis Layer

The Python layer independently reads the CSV datasets, cleans the data, performs EDA, and generates the findings used by the narrative generator.

### Install dependencies

```bash
pip install pandas matplotlib
```

### Run data cleaning and analysis

```bash
python analysis/clean_and_eda.py
```

The script is designed to report intermediate analytical results, including:

* Dataset shapes and payment-method counts.
* Duplicate order IDs and duplicate handling.
* Rating imputation.
* Cleaned revenue and reconciliation.
* IQR bounds and outlier analysis.
* Return rates by payment method.
* Customer segmentation.
* Correlation analysis.
* Monthly revenue trends.

### Generate visualizations

```bash
python analysis/visualize.py
```

Expected output files:

* `visualizations/return_rate_by_payment.png`
* `visualizations/monthly_revenue_trend.png`

### Findings file

The analysis script generates:

```text
narrator/findings.json
```

This file serves as the structured data source for the GenAI layer.

**Output:** Cleaned analytical results, visualizations, and `findings.json`.

---

## 3. GenAI Narrative Layer

The GenAI layer transforms the verified findings into a business narrative using the Situation–Complication–Resolution (SCR) framework.

### Offline execution

The offline template does not require an API key:

```bash
python narrator/generate_narrative.py
```

### Online execution with Gemini

Install the optional dependency:

```bash
pip install google-genai
```

Set your Gemini API key.

**Windows PowerShell:**

```powershell
$env:GEMINI_API_KEY="your-api-key-here"
python narrator/generate_narrative.py
```

**Windows Command Prompt:**

```cmd
set GEMINI_API_KEY=your-api-key-here
python narrator/generate_narrative.py
```

**Linux or macOS:**

```bash
export GEMINI_API_KEY="your-api-key-here"
python narrator/generate_narrative.py
```

The implementation supports online narrative generation and is designed to fall back to the offline template if the API call fails.

### Generated output

The script writes its narrative to:

```text
narrator/sample_output.txt
```

The saved output is intended to include numeric accuracy checks for the required figures.

**Output:** SCR business narrative and saved validation results.

---

## How the Three Layers Connect

```text
CSV Seed Data
     |
     +--------------------------+
     |                          |
     v                          v
  SQL Layer                Python Layer
     |                          |
     v                          v
Raw SQL Reports          Data Cleaning and EDA
                                |
                                v
                         Cleaned Metrics
                                |
                                v
                          Visualizations
                                |
                                v
                         findings.json
                                |
                                v
                           GenAI Layer
                                |
                                v
                        SCR Business Narrative
                                |
                                v
                        sample_output.txt
                                |
                                v
                      Numeric Accuracy Checks
```

The SQL layer analyzes the raw relational data, while the Python layer applies the project's data-cleaning rules. The narrative generator consumes the generated findings instead of independently calculating business metrics.

---

## Key Verified Figures

The following are the expected figures documented for the project. Run the pipeline to verify them against the committed datasets.

| Metric                                 | Expected Value |
| -------------------------------------- | -------------: |
| Raw total revenue                      |     ₹99,860.20 |
| Cleaned total revenue                  |     ₹97,358.30 |
| Revenue reconciliation difference      |      ₹2,501.90 |
| COD return rate                        |          44.4% |
| CARD return rate                       |          14.7% |
| UPI return rate                        |          18.9% |
| Highest-risk segment                   |   COD + Tier-2 |
| COD + Tier-2 return rate               |          54.5% |
| Peak month after outlier correction    |          March |
| March revenue after outlier correction |     ₹20,318.90 |

These are expected results supplied in the project specification. Their accuracy depends on the committed data and the actual implementation of the SQL and Python scripts.

---

## Installation and Execution

Run the following commands from the repository root.

### Step 1: Install Python dependencies

```bash
pip install pandas matplotlib
```

For online Gemini integration:

```bash
pip install google-genai
```

### Step 2: Initialize SQLite

```bash
sqlite3 mamaearth.db < sql/schema.sql
sqlite3 mamaearth.db < sql/seed_data.sql
```

### Step 3: Run SQL reports

```bash
sqlite3 mamaearth.db < sql/reports.sql
```

### Step 4: Run Python analysis

```bash
python analysis/clean_and_eda.py
```

### Step 5: Generate charts

```bash
python analysis/visualize.py
```

### Step 6: Generate the narrative

```bash
python narrator/generate_narrative.py
```

### Step 7: Check generated files

Verify that these files exist and contain the expected results:

* `narrator/findings.json`
* `narrator/sample_output.txt`
* `visualizations/return_rate_by_payment.png`
* `visualizations/monthly_revenue_trend.png`

---

## Business Value

The pipeline supports data-driven decision-making by helping stakeholders:

* Compare raw and cleaned revenue.
* Investigate return behavior by payment method.
* Identify customer segments with higher observed return rates.
* Analyze monthly revenue patterns.
* Review potential outlier effects.
* Communicate analytical findings through visualizations.
* Convert computed results into a structured business narrative.

These findings can guide further investigation into customer experience, payment behavior, return prevention, and revenue performance.

## Technologies Used

| Technology       | Purpose                               |
| ---------------- | ------------------------------------- |
| SQLite           | Relational database and SQL reporting |
| Python           | Analysis and automation               |
| Pandas           | Data cleaning and EDA                 |
| Matplotlib       | Data visualization                    |
| Google GenAI SDK | Optional narrative generation         |
| JSON             | Structured analytical findings        |
| Git and GitHub   | Version control and project hosting   |

## Project Deliverables

1. SQL schema and seed-data scripts.
2. SQL business reports.
3. Customer, product, and order CSV files.
4. Python cleaning and EDA script.
5. Python visualization script.
6. Return-rate visualization.
7. Monthly revenue visualization.
8. Generated findings JSON.
9. GenAI narrative-generation script.
10. Saved narrative with numeric accuracy checks.
11. README documentation.

## Troubleshooting

### SQLite is not recognized

Install SQLite 3 and ensure its executable is available in your system PATH.

### Python dependency errors

Run:

```bash
pip install pandas matplotlib
```

### Gemini API errors

Verify the API key and its environment variable. Alternatively, run the offline narrative generator.

### Output files are missing

Run the scripts in the documented order and check that all three CSV files exist in `data/`.

### Numerical results do not match

Check the source CSVs, duplicate-handling rules, missing-value treatment, revenue calculations, and outlier adjustments. Compare intermediate results before investigating downstream differences.

---

## Author Declaration

This project presents an end-to-end capstone pipeline integrating SQL relational analysis, Python-based data cleaning and exploratory analysis, visualization, and Generative AI narrative generation with an offline fallback.

**Author:** Amarjit Kahlon
**Program:** Data Analytics with AI & GenAI
**Institution:** E&ICT Academy, IIT Roorkee

---

*Reproducibility requires executing the project scripts against the committed data and validating their generated outputs.*
