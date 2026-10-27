# Pesa Pulse — Customer API Analysis

> **Context:** Pesa Pulse, a Nairobi-based fintech start-up, receives a customer directory from a new partner via a REST API. This project pulls that data, explores its nested structure, extracts the attributes that matter, counts and maps the customer distribution, and produces publication-ready CSV exports and charts for the marketing team.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Learning Objectives](#learning-objectives)
3. [Project Structure](#project-structure)
4. [Setup & Installation](#setup--installation)
5. [How to Run](#how-to-run)
6. [Task Walkthrough](#task-walkthrough)
   - [Task 1 – Retrieve Customer Data with Requests](#task-1--retrieve-customer-data-with-requests)
   - [Task 2 – Explore Nested Dictionaries and Lists](#task-2--explore-nested-dictionaries-and-lists)
   - [Task 3 – Extract Customer Attributes](#task-3--extract-customer-attributes)
   - [Task 4 – Find Unique Cities with Sets](#task-4--find-unique-cities-with-sets)
   - [Task 5 – Count Customers by City and Email Domain](#task-5--count-customers-by-city-and-email-domain)
   - [Task 6 – Convert Data into a DataFrame](#task-6--convert-data-into-a-dataframe)
   - [Task 7 – Export Results to CSV](#task-7--export-results-to-csv)
   - [Task 8 – Visualise the Customer Distribution](#task-8--visualise-the-customer-distribution)
7. [Data Structure Deep Dive](#data-structure-deep-dive)
8. [Key Findings](#key-findings)
9. [Output Files](#output-files)
10. [Dependencies](#dependencies)

---

## Project Overview

- Calling a live REST API
- Navigating deeply nested JSON
- Aggregating data with pure Python structures (sets, dicts, comprehensions)
- Cross-validating results with pandas
- Exporting clean CSVs and generating charts for non-technical stakeholders

The data source is the public mock API at **[`https://jsonplaceholder.typicode.com/users`](https://jsonplaceholder.typicode.com/users)**, which returns 10 synthetic customer records in JSON format.

---

## Learning Objectives

| # | Skill |
|---|-------|
| 1 | Retrieve JSON from an API with `requests` and handle failures gracefully |
| 2 | Navigate nested dictionaries and lists confidently |
| 3 | Use sets to find unique values and dictionaries to count them |
| 4 | Write dict comprehensions for aggregation without pandas |
| 5 | Move cleaned data into pandas, export it, and visualise a distribution |

---

## Project Structure

```
Pesa_Api_Analysis/
│
├── analysis.py              # Main implementation — all 8 tasks
├── starter.py               # Original scaffold with stub functions
├── analysis.ipynb           # Jupyter notebook version
│
├── output/
│   ├── customers.csv            # One row per customer (12 columns)
│   ├── city_counts.csv          # City name + customer count, sorted desc
│   ├── customer_distribution.png  # Bar chart: customers per city
│   └── email_tld_distribution.png # Bar chart: customers per email domain
│
├── pyproject.toml           # Project metadata and dependencies (uv)
├── uv.lock                  # Locked dependency tree
├── .python-version          # Python version pin
└── README.md                # This file
```

---

## Setup & Installation

This project uses **[uv](https://docs.astral.sh/uv/)** as its package manager (configured in `pyproject.toml`).

### Prerequisites

- Python >= 3.14
- `uv` installed ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))

### Steps

```bash
# 1. Clone or navigate to the project directory
cd Pesa_Api_Analysis

# 2. Create a virtual environment and install all dependencies
uv sync

# 3. (Optional) Install dependencies manually with pip
pip install requests pandas matplotlib
```

### Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `requests` | >= 2.34.2 | HTTP API calls |
| `pandas` | >= 3.1.0 | DataFrame creation, CSV export |
| `matplotlib` | >= 3.11.2 | Chart generation |

---

## How to Run

```bash
# Run the full analysis pipeline
python analysis.py

# Or run via uv
uv run python analysis.py
```

The script will:
1. Fetch customer data from the API
2. Print the nested structure explorer output
3. Print unique cities, city counts, and email domain counts
4. Confirm pandas counts match hand-written counts
5. Write CSV files and PNG charts to the `output/` folder

---

