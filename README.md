# Mamaearth Returns & Growth Intelligence Pipeline

**Capstone Project — Data Analytics with AI & GenAI**
**Program:** E&ICT Academy, IIT Roorkee
**Author:** Amarjit Kahlon

An end-to-end data analytics project that integrates SQL, Python, data visualization, and Generative AI to analyze product returns, customer behavior, payment methods, and revenue trends.

All figures documented in this README are intended to be reproduced by running the three layers against the committed seed data.

---

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

---

## Project Overview

The Mamaearth Returns & Growth Intelligence Pipeline is designed to transform raw retail transaction data into actionable business insights.

The project combines three analytical layers:

1. **SQL Layer:** Loads relational data into SQLite and generates business reports using the raw order records.
2. **Python Layer:** Cleans and validates the data, performs exploratory data analysis (EDA), calculates return rates, analyzes customer segments, and generates visualizations.
3. **GenAI Layer:** Converts verified analytical findings into a structured Situation–Complication–Resolution (SCR) business narrative using Gemini or an offline template.

The three layers share a consistent data workflow. The narrative generator reads the findings produced by the Python analysis rather than independently calculating or inventing business figures.

## Key Objectives

* Analyze revenue and order-level performance.
* Identify duplicate records and missing values.
* Standardize payment-method categories.
* Investigate product returns across payment methods.
* Identify customer segments associated with higher return rates.
* Analyze monthly revenue trends and outlier effects.
* Generate visual reports for business decision-making.
* Use Generative AI to summarize verified findings.
* Validate narrative figures against the computed analytical results.

---

## 1. SQL Layer — Schema, Seed Data and Reports

### Purpose

The SQL layer establishes the relational database, loads the seed data, and produces business reports using SQLite.

### Prerequisites

* SQLite 3
* Terminal or command prompt

### Step 1: Create the database

Run the following command from the repository root:

```bash
sqlite3 mamaearth.db < sql/schema.sql
```

### Step 2: Load the seed data

```bash
sqlite3 mamaearth.db < sql/seed_data.sql
```

### Step 3: Verify record counts

Run the following commands to validate the database:

```bash
sqlite3 mamaearth.db "SELECT COUNT(*) FROM customers;"
sqlite3 mamaearth.db "SELECT COUNT(*) FROM products;"
sqlite3 mamaearth.db "SELECT COUNT(*) FROM orders;"
```

Expected record counts:

| Table     | Expected Records |
| --------- | ---------------: |
| Customers |               45 |
| Products  |               16 |
| Orders    |              180 |

### Step 4: Execute SQL reports

```bash
sqlite3 mamaearth.db < sql/reports.sql
```

The reports file contains the Task 3 SQL queries (a–i), covering the relational analysis specified for the project.

### Data Import Note

If CSV files are imported using SQLite's `.import` command instead of `seed_data.sql`, empty strings in the following fields should be converted to `NULL` where applicable:

```sql
UPDATE orders
SET discount_pct = NULL
WHERE discount_pct = '';

UPDATE orders
SET rating = NULL
WHERE rating = '';
```

**SQL Layer Output:** A populated SQLite database and query results for the raw transaction data.

---

## 2. Python Analysis Layer — Data Cleaning, EDA and Visualization

### Purpose

The Python layer reads the committed CSV files, cleans the data, performs exploratory analysis, calculates business metrics, and generates the findings consumed by the GenAI layer.

### Prerequisites

* Python 3
* pandas
* matplotlib

### Step 1: Install dependencies

```bash
pip install pandas matplotlib
```

### Step 2: Run data cleaning and exploratory analysis

```bash
python analysis/clean_and_eda.py
```

The script performs the data preparation and analytical tasks defined in the project, including:

* Inspecting dataset dimensions and data quality.
* Standardizing payment-method casing.
* Identifying and removing duplicate records according to the implemented rules.
* Handling missing values and imputing ratings where required.
* Calculating cleaned revenue and reconciling it against raw revenue.
* Identifying outliers using the Interquartile Range (IQR) method.
* Calculating return rates by payment method.
* Segmenting customers and identifying higher-risk groups.
* Examining correlations between relevant numerical variables.
* Calculating monthly revenue series.
* Generating the machine-readable findings file.

The script prints intermediate results so that the calculations can be inspected and checked against the project requirements.

### Step 3: Generate visualizations

```bash
python analysis/visualize.py
```

The script generates the required charts in the `visualizations/` directory.

### Required Visualizations

**1. Return Rate by Payment Method**

File: `visualizations/return_rate_by_payment.png`

This chart compares return rates across payment methods and helps identify differences in return behavior.

**2. Monthly Revenue Trend**

File: `visualizations/monthly_revenue_trend.png`

This chart presents monthly revenue trends and supports the analysis of seasonal patterns and outlier effects.

### Step 4: Verify the findings file

After running the Python analysis, inspect:

```text
narrator/findings.json
```

This file contains the analytical findings generated by the Python script. It acts as the handoff between the analysis layer and the narrative generation layer.

**Python Layer Output:** Cleaned analytical results, printed validation metrics, two visualization files, and `narrator/findings.json`.

---

## 3. GenAI Layer — Business Narrative Generation

### Purpose

The GenAI layer converts the verified analytical findings into a business-oriented narrative using the Situation–Complication–Resolution (SCR) framework.

The generator consumes `narrator/findings.json`, which is produced by the Python analysis layer.

### Option A: Offline Execution

The offline mode uses a deterministic narrative template and does not require an API key.

Run:

```bash
python narrator/generate_narrative.py
```

This mode is useful for reproducible testing and environments without internet access or API credentials.

### Option B: Online Execution with Gemini

Install the optional dependency:

```bash
pip install google-genai
```

Obtain an API key from Google AI Studio and configure the environment variable.

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

The implementation also supports `GOOGLE_API_KEY` when configured as specified in the code.

When the online configuration is available, the generator attempts to produce a structured narrative using Gemini. If the API call fails, the implementation is designed to fall back to the offline narrative path.

### Generated Output

The narrative generator writes its result to:

```text
narrator/sample_output.txt
```

The output includes the generated business narrative and the results of the Task 5 numeric accuracy checks, according to the implementation.

The saved sample output is intended to provide a reproducible artifact for project review without requiring the reviewer to make a live API call.

**GenAI Layer Output:** A structured business narrative, a saved sample output, and numeric accuracy validation results.

---

## How the Three Layers Connect

The project follows this end-to-end workflow:

```text
Committed CSV Files
        |
        +-----------------------------+
        |                             |
        v                             v
    SQL Layer                    Python Layer
        |                             |
        v                             v
 Raw Relational Reports       Cleaning and EDA
        |                             |
        v                             v
 Raw Revenue Metrics          Cleaned Metrics
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
                              SCR Narrative
                                      |
                                      v
                              sample_output.txt
                                      |
                                      v
                         Numeric Accuracy Checks
```

### Data Consistency

* The SQL layer analyzes the raw relational data.
* The Python layer independently processes the committed CSV files.
* The findings file is generated programmatically rather than manually populated.
* The narrative generator uses the generated findings instead of independently inventing analytical figures.
* The saved sample and accuracy checks support reproducibility and verification.

The raw and cleaned revenue totals are expected to differ because the Python pipeline applies its documented cleaning and duplicate-handling rules.

---

## Key Verified Figures

The following figures are the project's documented target results and should be verified by executing the relevant scripts against the committed data.

| Metric                                 | Expected Value |
| -------------------------------------- | -------------: |
| Raw total revenue — Part 1             |     ₹99,860.20 |
| Cleaned total revenue — Part 2         |     ₹97,358.30 |
| Revenue reconciliation difference      |      ₹2,501.90 |
| COD return rate                        |          44.4% |
| CARD return rate                       |          14.7% |
| UPI return rate                        |          18.9% |
| Highest-risk customer segment          |   COD + Tier-2 |
| COD + Tier-2 return rate               |          54.5% |
| Peak month after outlier correction    |          March |
| March revenue after outlier correction |     ₹20,318.90 |

These figures are expected results, not a substitute for running the project. Their correctness depends on the committed CSV files, the implemented cleaning rules, the SQL queries, and the analytical scripts.

---

## Installation and Execution — Quick Start

Follow these steps from the repository root.

### 1. Install Python dependencies

```bash
pip install pandas matplotlib
```

For the optional online Gemini integration:

```bash
pip install google-genai
```

### 2. Initialize the SQLite database

```bash
sqlite3 mamaearth.db < sql/schema.sql
sqlite3 mamaearth.db < sql/seed_data.sql
```

### 3. Run SQL reports

```bash
sqlite3 mamaearth.db < sql/reports.sql
```

### 4. Run Python analysis

```bash
python analysis/clean_and_eda.py
```

### 5. Generate visualizations

```bash
python analysis/visualize.py
```

### 6. Generate the business narrative

```bash
python narrator/generate_narrative.py
```

### 7. Review the generated artifacts

Verify the following files:

* `narrator/findings.json`
* `narrator/sample_output.txt`
* `visualizations/return_rate_by_payment.png`
* `visualizations/monthly_revenue_trend.png`

For a complete project review, compare the printed analytical results, SQL report outputs, generated findings, and narrative accuracy checks.

---

## Business Value

This project demonstrates how data analytics can support retail decision-making by:

* Measuring revenue before and after data cleaning.
* Highlighting payment methods associated with different return rates.
* Identifying customer segments that may require additional investigation.
* Monitoring monthly revenue performance.
* Making analytical results easier to understand through charts.
* Converting numerical findings into a concise business narrative.
* Improving reproducibility through automated validation and saved outputs.

The findings can help stakeholders identify areas for further investigation into return patterns, customer experience, payment behavior, and revenue performance.

---

## Technologies Used

| Technology       | Purpose                                     |
| ---------------- | ------------------------------------------- |
| SQLite           | Relational database and SQL reporting       |
| Python           | Analysis pipeline and automation            |
| Pandas           | Data cleaning and exploratory data analysis |
| Matplotlib       | Data visualization                          |
| Google GenAI SDK | Optional AI-generated narrative             |
| JSON             | Structured transfer of analytical findings  |
| Git and GitHub   | Version control and project sharing         |

---

## Project Deliverables

The repository is intended to contain the following deliverables:

1. SQL schema and seed scripts.
2. SQL business reports.
3. Customer, product, and order CSV datasets.
4. Python data-cleaning and exploratory-analysis script.
5. Python visualization script.
6. Return-rate visualization.
7. Monthly revenue trend visualization.
8. Machine-generated findings JSON.
9. GenAI narrative-generation script.
10. Saved narrative output with numeric accuracy checks.
11. README documentation with setup and execution instructions.

---

## Troubleshooting

### SQLite command not found

Install SQLite 3 and ensure the `sqlite3` executable is available in your system's PATH.

### Python dependency errors

Install the required packages:

```bash
pip install pandas matplotlib
```

### Gemini API errors

Confirm that the API key is valid and configured in the current terminal session. The offline mode can be used without an API key.

### Missing output files

Run the scripts in the documented order and verify that the required input CSV files exist in the `data/` directory.

### Unexpected numerical results

Check that the committed CSV files are unchanged, the SQL database has been initialized correctly, and the analysis scripts have completed successfully. Compare intermediate results before investigating downstream differences.

---

## Author Declaration

This project is presented as an end-to-end capstone pipeline combining SQL-based relational analysis, Python data cleaning and exploratory analysis, visualization, and Generative AI narrative generation with an offline fallback.

**Author:** Amarjit Kahlon
**Program:** Data Analytics with AI & GenAI
**Institution:** E&ICT Academy, IIT Roorkee

---

*To reproduce the reported results, execute the SQL, Python, and narrative-generation scripts against the committed project data and verify the generated outputs.*
