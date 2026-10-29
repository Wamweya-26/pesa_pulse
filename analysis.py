"""
Day 1 - API Data Analysis Using Python Structures
Squad Python Specialization - Data Science, AI & Analytics
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"


def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:
        # Send a request to the API and wait up to 30 seconds
        response = requests.get(url, timeout=30)

        # Raise an error if the server returns an unsuccessful status
        response.raise_for_status()

        # Convert the JSON response into Python objects
        customers = response.json()

        # Confirm that the response contains a list of records
        if not isinstance(customers, list):
            raise ValueError("The API response is not a list.")

        # Return the retrieved customer records
        return customers

    except requests.RequestException as error:
        # Handle connection errors, timeouts, and HTTP errors
        print(f"Error retrieving customers: {error}")
        return []

    except ValueError as error:
        # Handle invalid JSON or an unexpected response format
        print(f"Invalid API response: {error}")
        return []


def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a (possibly nested) record with its type, indented by depth."""
    # Go through every key and value in the current dictionary
    for key, value in record.items():
        # Print the key and the type of its value
        print(" " * indent + f"{key}: {type(value).__name__}")

        # If the value is another dictionary, explore its contents
        if isinstance(value, dict):
            explore(value, indent + 2)

        # If the value is a list, inspect dictionary items inside it
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    explore(item, indent + 2)


def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dict per customer with the attributes listed in the task."""
    extracted_customers = []

    # Process each customer individually
    for customer in customers:
        # Get nested information safely in case a field is missing
        address = customer.get("address") or {}
        geo = address.get("geo") or {}
        company = customer.get("company") or {}

        # Extract the required fields into one flat dictionary
        extracted_customer = {
            "customer_id": customer.get("id"),
            "name": customer.get("name"),
            "username": customer.get("username"),
            "email": customer.get("email"),
            "email_domain": (
                customer.get("email", "").rsplit(".", 1)[-1].lower()
                if "." in customer.get("email", "")
                else ""
                ),
            "phone": customer.get("phone"),
            "city": address.get("city"),
            "zipcode": address.get("zipcode"),
            "latitude": (
                float(geo["lat"]) if geo.get("lat") is not None else None
                ),
            "longitude": (
                float(geo["lng"]) if geo.get("lng") is not None else None
                ),
            "company": company.get("name"),
            "website": customer.get("website"),
        }

        # Add this flattened record to the output list
        extracted_customers.append(extracted_customer)

    # Return all extracted customer records
    return extracted_customers


def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    # Use a set to keep each city only once
    cities = set()

    # Visit each customer and collect their city
    for customer in customers:
        city = (customer.get("address") or {}).get("city")
        if city:
            cities.add(city)

    return cities


def city_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per city using a loop and/or a dict comprehension (no Counter, no pandas)."""
    counts = {}

    # Count each city's occurrences using a normal dictionary
    for customer in customers:
        city = (customer.get("address") or {}).get("city")
        if city:
            if city in counts:
                counts[city] += 1
            else:
                counts[city] = 1

    return counts


def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per email top-level domain (e.g. 'biz', 'tv')."""
    counts = {}

    # Extract the final part after the last dot in each email address
    for customer in customers:
        email = customer.get("email", "")
        if "@" in email and "." in email.rsplit("@", 1)[-1]:
            domain_suffix = email.rsplit(".", 1)[-1].lower()
            counts[domain_suffix] = counts.get(domain_suffix, 0) + 1

    return counts


def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    """Convert the flattened records into a pandas DataFrame."""
    # Create a table from the list of dictionaries
    return pd.DataFrame(rows)


def plot_distribution(counts: dict[str, int], path: Path) -> None:
    """Save a labelled chart of the distribution to path."""
    # Create the folder for the chart if it does not already exist
    path.parent.mkdir(parents=True, exist_ok=True)

    # The main block chooses city or email-domain counts before calling this function
    chart_counts = counts

    # Sort categories alphabetically to keep the chart easy to read
    categories = sorted(chart_counts)
    values = [chart_counts[category] for category in categories]

    # Create and label the bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(categories, values)
    plt.title("Customer Distribution")
    plt.xlabel("Category")
    plt.ylabel("Number of customers")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Save the chart image and close the figure
    plt.savefig(path, dpi=150)
    plt.close()


if __name__ == "__main__":
    # Retrieve the sample customer records from the API
    customers = get_customers()

    # Stop if the API could not return customer records
    if not customers:
        raise SystemExit("No customer records retrieved. Check your connection and try again.")

    # Explore the structure of the first record
    print("\n--- Exploring the first customer record ---")
    explore(customers[0])

    # Flatten the nested customer records
    rows = extract_attributes(customers)

    # Identify distinct cities and count customers by city
    cities = unique_cities(customers)
    city_count_results = city_counts(customers)

    # Count email suffixes using plain Python
    DOMAIN_COUNTS = email_domain_counts(customers)

    # Convert the flattened records into a pandas DataFrame
    customer_df = to_dataframe(rows)

    # Verify the city counts with pandas
    pandas_city_counts = customer_df["city"].value_counts().to_dict()
    if pandas_city_counts != city_count_results:
        print("Warning: plain Python and pandas city counts do not match.")

    # Create the output folder
    output_dir = Path("output")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Export the flattened customer data without a row index
    customer_columns = [
        "customer_id", "name", "username", "email", "email_domain",
        "phone", "city", "zipcode", "latitude", "longitude",
        "company", "website",
    ]
    customer_df[customer_columns].to_csv(
        output_dir / "customers.csv", index=False
    )

    # Sort city counts by count descending, then city name ascending
    city_count_rows = [
        {"city": city, "customer_count": count}
        for city, count in city_count_results.items()
    ]
    city_count_rows.sort(key=lambda row: (-row["customer_count"], row["city"].lower()))

    city_df = pd.DataFrame(city_count_rows, columns=["city", "customer_count"])
    city_df.to_csv(output_dir / "city_counts.csv", index=False)

    # If all cities occur once, plot email suffixes instead of a city chart
    chart_counts = (
        DOMAIN_COUNTS
        if city_count_results and all(count == 1 for count in city_count_results.values())
        else city_count_results
    )
    plot_distribution(chart_counts, output_dir / "customer_distribution.png")

    # Print the requested summary
    most_common_city = sorted(
        city_count_results.items(),
        key=lambda item: (-item[1], item[0].lower())
    )[0]

    print(f"\nCustomers retrieved : {len(customers)}")
    print(f"Unique cities       : {len(cities)}")
    print(f"Most common city    : {most_common_city[0]} ({most_common_city[1]})")
    print(f"Email domains       : {DOMAIN_COUNTS}")
    print(f"Chart saved to      : {output_dir / 'customer_distribution.png'}")
