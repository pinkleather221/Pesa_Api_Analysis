# Pesa Pulse — Customer API Analysis

This project retrieves synthetic customer records from the public JSONPlaceholder API, explores their nested JSON structure, summarizes customers by city and email top-level domain (TLD), validates the summaries with pandas, and exports CSV files and charts.

## Project structure

```text
Pesa_Api_Analysis/
├── analysis.py
├── pyproject.toml
├── requirements.txt
├── uv.lock
├── src/
│   └── pesa_api_analysis/
│       └── __init__.py
└── output/
    ├── customers.csv
    ├── city_counts.csv
    ├── customer_distribution.png
    └── email_tld_distribution.png
```

## Setup

The project requires Python 3.14 or newer. Install dependencies with either `uv` or `pip`:

```bash
uv sync
```

Or:

```bash
python -m pip install -r requirements.txt
```

## Run

Run the analysis from the project root so generated files are written to `output/`:

```bash
uv run python analysis.py
```

Or, after installing dependencies:

```bash
python analysis.py
```

The script fetches the data, prints a nested-structure walkthrough and findings, checks the hand-written counts against pandas, then recreates both CSVs and PNG charts. If the API request fails or returns no records, it reports the issue and exits without attempting analysis.

## Task walkthrough

1. **Retrieve data:** `get_customers()` requests the JSONPlaceholder users endpoint with a 10-second timeout and reports request exceptions.
2. **Explore nested data:** `explore()` recursively walks dictionaries and lists, printing each field's type and nesting level.
3. **Extract attributes:** `extract_attributes()` flattens each record into a row. It converts latitude and longitude to floating-point numbers and stores the email's TLD in `email_domain`.
4. **Summarize:** `unique_cities()` uses a set comprehension. `city_counts()` counts customers per city, while `email_domain_counts()` counts TLDs using a dictionary.
5. **Validate:** pandas `value_counts()` and `groupby()` results are compared with the pure-Python counts using printed checks and assertions.
6. **Export and chart:** the script writes the customer and city summaries to CSV and generates horizontal bar charts for city and TLD counts.

## Data structure deep dive

The API returns one dictionary per customer. Fields used by this project include top-level `id`, `name`, `username`, `email`, `phone`, and `website`, as well as nested fields:

| Output attribute | Source path | Transformation |
|---|---|---|
| `customer_id` | `id` | Renamed for clarity |
| `city` | `address.city` | None |
| `zipcode` | `address.zipcode` | None |
| `latitude` | `address.geo.lat` | Converted to `float` |
| `longitude` | `address.geo.lng` | Converted to `float` |
| `company` | `company.name` | None |
| `email_domain` | `email` | Final portion after `.` (for example, `biz` in `name@example.biz`), lower-cased |

These nested paths demonstrate how a flat row can be built from values several levels down in a JSON object.

## Key findings

For the 10 records returned by JSONPlaceholder:

- There are 10 distinct cities, so each city has one customer.
- The email TLD counts are `biz` (3), `ca` (1), `info` (1), `io` (1), `me` (1), `net` (1), `org` (1), and `tv` (1).
- The city chart makes the lack of city-level variation easy to see. The email TLD chart is more informative for comparing categories in this sample because its counts are not all tied.

The API supplies synthetic example data; these results should not be treated as representative customer or market statistics. Running the script refreshes the findings and output files from the current API response.

## Output files

- `output/customers.csv` — one flattened row per customer, including `customer_id` and `email_domain`.
- `output/city_counts.csv` — city totals in descending count order, with ties alphabetized; the count column is `customer_count`.
- `output/customer_distribution.png` — customer counts by city.
- `output/email_tld_distribution.png` — customer counts by email TLD.

## Dependencies

The runtime dependencies are listed in both [`pyproject.toml`](./pyproject.toml) and [`requirements.txt`](./requirements.txt): `requests` for the HTTP request, `pandas` for tabular validation and CSV export, and `matplotlib` for charts.
