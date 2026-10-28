"""
Day 1 - API Data Analysis Using Python Structures
Squad Python Specialization - Data Science, AI & Analytics
"""

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"


def get_customers(url: str = API_URL) -> list[dict[str, Any]]:
    """Fetch customer records and report request failures clearly."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        print(f"Error fetching customers: {error}")
        return []


def explore(record: Any, indent: int = 0) -> None:
    """Print every key in a nested record with its type and depth."""
    pad = "     " * indent
    if isinstance(record, dict):
        for key, value in record.items():
            print(f"{pad}{key}: {type(value).__name__}")
            explore(value, indent + 1)
    elif isinstance(record, list):
        for index, item in enumerate(record):
            if isinstance(item, (dict, list)):
                print(f"{pad}{index}: {type(item).__name__}")
                explore(item, indent + 1)


def email_tld(email: str) -> str:
    """Return the lower-case top-level domain from an email address."""
    return email.rsplit("@", 1)[-1].rsplit(".", 1)[-1].lower()


def extract_attributes(customers: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Flatten the customer records into the attributes used by the analysis."""
    rows = []
    for customer in customers:
        rows.append(
            {
                "customer_id": customer["id"],
                "name": customer["name"],
                "username": customer["username"],
                "email": customer["email"],
                "email_domain": email_tld(customer["email"]),
                "phone": customer["phone"],
                "city": customer["address"]["city"],
                "zipcode": customer["address"]["zipcode"],
                "latitude": float(customer["address"]["geo"]["lat"]),
                "longitude": float(customer["address"]["geo"]["lng"]),
                "company": customer["company"]["name"],
                "website": customer["website"],
            }
        )
    return rows


def unique_cities(customers: list[dict[str, Any]]) -> set[str]:
    """Return the set of distinct cities."""
    return {customer["address"]["city"] for customer in customers}


def city_counts(customers: list[dict[str, Any]]) -> dict[str, int]:
    """Count customers per city using a dictionary."""
    counts: dict[str, int] = {}
    for customer in customers:
        city = customer["address"]["city"]
        counts[city] = counts.get(city, 0) + 1
    return counts


def email_domain_counts(customers: list[dict[str, Any]]) -> dict[str, int]:
    """Count customers by email top-level domain."""
    domains = [email_tld(customer["email"]) for customer in customers]
    counts = {domain: 0 for domain in set(domains)}
    for domain in domains:
        counts[domain] += 1
    return counts


def print_sorted(counts: dict[str, int], title: str) -> None:
    """Print counts from most to least common, with alphabetical tie-breaking."""
    print(title)
    for name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        print(f"  {name}: {count}")


def to_dataframe(rows: list[dict[str, Any]]) -> pd.DataFrame:
    """Convert flattened customer records to a pandas DataFrame."""
    return pd.DataFrame(rows)


def plot_distribution(
    counts: dict[str, int],
    path: Path,
    title: str,
    xlabel: str = "Customers",
) -> None:
    """Save a horizontal bar chart of counts, most common first."""
    items = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    labels = [name for name, _ in items]
    values = [count for _, count in items]

    fig, ax = plt.subplots(figsize=(8, max(3, 0.4 * len(labels))))
    ax.barh(labels, values, color="steelblue")
    ax.invert_yaxis()
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    if values:
        ax.set_xticks(range(0, max(values) + 1))
        for index, value in enumerate(values):
            ax.text(value + 0.05, index, str(value), va="center")

    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)


def main() -> None:
    """Fetch, analyze, export, and chart customer data."""
    customers = get_customers()
    if not customers:
        print("No customer records were returned; analysis was not run.")
        return

    print("Nested structure of the first customer:")
    explore(customers[0])

    rows = extract_attributes(customers)
    cities = unique_cities(customers)
    hand_cities = city_counts(customers)
    hand_domains = email_domain_counts(customers)

    print(f"\nUnique cities: {len(cities)}")
    print(f"Customer records: {len(customers)}")
    print(f"Unique city count equals customer count: {len(cities) == len(customers)}")
    print_sorted(hand_cities, "\nCustomers by city:")
    print_sorted(hand_domains, "\nCustomers by email TLD:")

    df = to_dataframe(rows)
    pd.set_option("display.max_columns", None)
    print(f"\nDataFrame shape: {df.shape}")
    print("DataFrame dtypes:")
    print(df.dtypes)

    pd_cities = df["city"].value_counts().to_dict()
    pd_domains = df["email_domain"].value_counts().to_dict()
    groupby_cities = df.groupby("city").size().to_dict()

    print("\nPandas validation:")
    print(f"City counts match value_counts: {hand_cities == pd_cities}")
    print(f"City counts match groupby: {hand_cities == groupby_cities}")
    print(f"Email TLD counts match value_counts: {hand_domains == pd_domains}")

    assert hand_cities == pd_cities == groupby_cities
    assert hand_domains == pd_domains

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    df.to_csv(output_dir / "customers.csv", index=False)
    city_df = (
        df.groupby("city")
        .size()
        .reset_index(name="customer_count")
        .sort_values(["customer_count", "city"], ascending=[False, True])
    )
    city_df.to_csv(output_dir / "city_counts.csv", index=False)
    print(
        f"\nWrote {len(df)} customer rows and {len(city_df)} city rows "
        f"to {output_dir}."
    )

    plot_distribution(
        hand_cities,
        output_dir / "customer_distribution.png",
        title="Customers by city",
    )
    plot_distribution(
        hand_domains,
        output_dir / "email_tld_distribution.png",
        title="Customers by email TLD",
    )

    print("\nFindings:")
    print(f"- {len(customers)} customer records span {len(cities)} unique cities.")
    print(f"- The email TLDs represented are: {', '.join(sorted(hand_domains))}.")
    print("- The city chart shows geographic counts; the TLD chart shows email-domain mix.")
    print("  The TLD chart is more informative for this sample because city counts are tied.")


if __name__ == "__main__":
    main()
