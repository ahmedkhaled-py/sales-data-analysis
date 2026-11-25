# sales-data-analysis

Exploratory data analysis of retail sales with pandas and matplotlib:
monthly revenue trend, top products, and category share, saved as charts.

## Features

- Runs anywhere: generates a reproducible synthetic dataset (seeded) if no CSV is given
- `--csv` to analyze a real export with columns `date, product, category, units, unit_price`
- Prints a summary to the console (totals, best month, revenue by product)
- Saves a 3-panel chart to `output/sales_summary.png`

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
python analysis.py                       # sample data -> output/sales_summary.png
python analysis.py --csv my_sales.csv    # your own data
```

Requires Python 3.9+.
