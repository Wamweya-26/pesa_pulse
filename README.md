# Pesa Pulse — API Data Analysis

## Project Overview

Pesa Pulse is a Python project that retrieves sample user records from an API, explores nested JSON data, extracts customer attributes, analyzes city and email-domain distributions, and saves the results as CSV files and a chart.

## Objectives

- Retrieve data from an API using Python.
- Explore nested dictionaries and lists.
- Extract and flatten customer attributes.
- Identify unique cities and count customers by city.
- Count email top-level domains using plain Python.
- Use pandas to organize and verify the analysis.
- Export CSV files and create a bar chart.

## Tools and Libraries

- Python
- Requests
- Pandas
- Matplotlib
- JSON

## Project Structure

```text
day1-api-analysis/
├── analysis.py
├── output/
│   ├── customers.csv
│   ├── city_counts.csv
│   └── customer_distribution.png
├── requirements.txt
└── README.md
```

## How to Run the Analysis

1. Open the project folder in VS Code.
2. Activate the project's Python environment.
3. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Run the analysis:

   ```bash
   python analysis.py
   ```

The script retrieves the records, performs the analysis, prints a summary, and saves the output files in the `output/` folder.

## Output Files

- `customers.csv`: Flattened customer records containing the required attributes.
- `city_counts.csv`: Customer counts grouped by city and sorted by descending count.
- `customer_distribution.png`: A bar chart showing the selected distribution.

## Findings

*To be completed after running the analysis and verifying the actual results.*

## Assumptions and Limitations

- The project uses JSONPlaceholder, a sample API. Its records are not verified real Pesa Pulse customers.
- City counts are calculated using plain Python and checked against pandas results.
- Email-domain suffixes are extracted from email addresses for counting.
- If every city appears only once, email-domain distribution is used for a more informative chart.

## Conclusion

This project demonstrates API data retrieval, nested data exploration, data extraction, counting with Python data structures, pandas analysis, CSV export, and data visualization.
