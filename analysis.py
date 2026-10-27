"""
Day 1 - API Data Analysis Using Python Structures
Squad Python Specialization - Data Science, AI & Analytics
"""
import json
from pathlib import Path

import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"


def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:
        response = requests.get(url,timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.request.exceptions.RequestException as error:
        print(f"Error fetching customers: {error}")
        return []

customers = get_customers()
print(customers)


def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a (possibly nested) record with its type, indented by depth."""
    pad = "     " * indent
    if isinstance(record, dict):
        for key, value in record.items():
            print(f"{pad}{key}:{type(value).__name__}") #class <str>
            explore(value, indent + 1)
    elif isinstance(record, list):
        for i, item in enumerate(record):
            if isinstance(item, (dict, list)):
                print(f"{pad}{i}:{type(item).__name__}")
                explore(item, indent + 1)

if customers:
    explore(customers[0])

def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dict per customer with the attributes listed in the task."""
    rows = [
        # creating an empty list , inisde it will have many dictionaries, each dictinary has individual attributes from the jason file(a nested dictinary)
    ]
    # customers is the whole jason file with (eg 500 customers), c stands for one out of the 500 customers.
    for c in customers:
        rows.append({
            'id': c['id'],
            'name': c['name'],
            "username": c["username"],
            "email": c["email"],
            "email_domain": c["email"].split("@")[-1].lower(),
            "phone": c["phone"],
            "city": c["address"]["city"],
            "zipcode": c["address"]["zipcode"],
            "latitude": float(c["address"]["geo"]["lat"]),
            "longitude": float(c["address"]["geo"]["lng"]),
            "company": c["company"]["name"],
            "website": c["website"],
        })
    return rows


result_x = extract_attributes(customers)
print(result_x)


# def unique_cities(customers: list[dict]) -> set[str]:
#     """Return the set of distinct cities."""
#     raise NotImplementedError


# def city_counts(customers: list[dict]) -> dict[str, int]:
#     """Count customers per city using a loop and/or a dict comprehension (no Counter, no pandas)."""
#     raise NotImplementedError


# def email_domain_counts(customers: list[dict]) -> dict[str, int]:
#     """Count customers per email top-level domain (e.g. 'biz', 'tv')."""
#     raise NotImplementedError


# def to_dataframe(rows: list[dict]) -> pd.DataFrame:
#     raise NotImplementedError


# def plot_distribution(counts: dict[str, int], path: Path) -> None:
#     """Save a labelled chart of the distribution to path."""
#     raise NotImplementedError


# if __name__ == "__main__":
#     # TODO: run each step and print a short findings summary
#     pass
