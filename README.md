# E-Commerce Customer Cohort, Retention and Profitability Analysis

[![Reproducibility check](https://github.com/Haven-Pham/ecommerce-cohort-retention-analysis/actions/workflows/ci.yml/badge.svg)](https://github.com/Haven-Pham/ecommerce-cohort-retention-analysis/actions/workflows/ci.yml)
![Python 3.12](https://img.shields.io/badge/python-3.12-3776AB)
![License: MIT](https://img.shields.io/badge/license-MIT-lightgrey)

## Overview

This project analyses four years of order data (2020–2023) from an e-commerce retailer of beauty and home products to
assess whether its sales growth is supported by customer retention and whether that growth is profitable. The dataset is
synthetic and educational, and covers 51,290 order lines from 17,415 customers.

**Summary of results.** Sales increased by 24% in 2023 while profit declined by 12%, as the profit margin fell from 18.0%
to 12.8% across all product categories. Repeat customers represent 31% of the customer base but generate 56% of profit,
and the median interval before a second purchase is 364 days. Order lines discounted by more than 20% produced a
cumulative loss of $288.6K.

![Annual sales, profit and margin](reports/figures/01_yearly_sales_profit_margin.png)

## Business Questions

1. What share of new customers make a repeat purchase, and how long does it take?
2. Does retention differ across acquisition cohorts and customer segments?
3. How much of total profit depends on repeat customers?
4. Which customer groups and pricing practices drive or reduce profitability?

## Methodology

- **Data validation:** checks for duplicate keys, missing values and orders without a matching customer record.
- **Cohort construction:** each customer is assigned to the month and quarter of their first purchase; multiple lines
  of the same order count as one purchase event.
- **Retention measurement:** monthly and quarterly retention matrices, plus a size-weighted retention curve so that
  small cohorts do not distort the average.
- **Customer value:** profit comparison of one-time and repeat customers and the distribution of time to second purchase.
- **Profitability analysis:** margin by year, product category, discount band, customer segment and income bracket,
  including a diagnosis of the 2023 margin decline.

## Key Findings

### 2023 Margin Decline

- Sales grew from $1.77M to $2.19M (+24%) while profit fell from $319K to $280K (−12%); the margin declined from 18.0%
  to 12.8%. At 2023 volume, the difference represents approximately $115K of profit.
- The decline is not explained by discounting: the margin on undiscounted lines also fell (33.4% to 28.1%) and the
  discount mix was unchanged.
- It is not explained by product mix either: every category lost 4–8 percentage points of margin, while category
  shares of sales changed by less than one point. The evidence points to a company-wide change in unit cost or pricing.

![Margin decline diagnosis](reports/figures/01b_margin_drop_diagnosis.png)

### Customer Retention

- Between 1.6% and 2.4% of a cohort makes a purchase in any given later month; on a quarterly basis the range is
  2.7% to 8.9%.
- Retention does not follow a gradual decay pattern. Most customers do not return, and those who do return at long and
  irregular intervals.

![Monthly retention, 2022 cohorts](reports/figures/03_monthly_retention_heatmap_2022.png)

### Value of Repeat Customers

- Customers with two or more orders (31% of the base) generate 56% of profit, averaging $110.6 per customer compared
  with $38.8 for one-time buyers.
- The median time to a second purchase is 364 days, and 14.5% of repeat customers return within 90 days, which is
  consistent with an annual or replenishment-driven purchase cycle.

![Repeat customer value](reports/figures/05_repeat_customer_value.png)

### Discount Profitability

- Undiscounted lines earn a 31.7% margin and lines discounted by 1–20% earn 15.0%.
- Lines discounted by 21–40% and by more than 40% (22% of all lines) operate at margins of −8.1% and −27.0%
  respectively, with a combined loss of $288.6K.

![Profit by discount band](reports/figures/08_discount_profit_leakage.png)

### Segments and Income

- Corporate customers account for 30% of customers, 59% of sales and 57% of profit. Retention is similar across the
  Consumer, Corporate and Self-Employed segments.
- Customer income is not a meaningful differentiator: each income bracket's share of profit is in line with its share
  of customers, and profit per customer ranges only from $54 to $62.

## Recommendations

| Priority | Recommendation | Owner | Estimated impact |
|---|---|---|---|
| 1 | Investigate the 2023 margin decline using cost and list-price data before setting 2024 targets | Finance, Procurement | Up to ~$115K per year |
| 2 | Introduce a 20% discount ceiling, with approval and margin review for exceptions | Commercial | Up to ~$72K per year |
| 3 | Launch a second-purchase programme timed at months 10–12, with an A/B-tested reminder at 60–90 days | CRM, Marketing | ~$43K for a 5% increase in repeat conversion |
| 4 | Establish account management for Corporate customers (reorder cadence, volume pricing in place of deep discounts) | Sales | Protects 57% of profit |
| 5 | Replace income-based targeting with RFM and discount-sensitivity segmentation | Marketing Analytics | Improved targeting at no additional cost |

## Deliverables

| File | Description |
|---|---|
| [`notebooks/cohort_retention_profitability.ipynb`](notebooks/cohort_retention_profitability.ipynb) | Complete analysis with outputs |
| [`reports/Cohort_Retention_Executive_Deck.pdf`](reports/Cohort_Retention_Executive_Deck.pdf) | Eight-slide executive presentation (PowerPoint version included) |
| [`reports/Cohort_Retention_Profitability_Report.xlsx`](reports/Cohort_Retention_Profitability_Report.xlsx) | KPIs, retention matrices, segment and discount tables |
| [`reports/figures/`](reports/figures), [`reports/tables/`](reports/tables) | Charts (PNG) and result tables (CSV) |

## Repository Structure

```text
ecommerce-cohort-retention-analysis/
├── data/
│   ├── raw/                 EcomSales.csv, Customer.csv, Product.csv
│   └── README.md            data dictionary
├── notebooks/               analysis notebook
├── src/cohort_analysis/     data loading, cohort, profitability and plotting modules
├── scripts/                 notebook runner and report builder
├── reports/                 figures, tables, Excel report, presentation
├── tests/                   unit tests
├── .github/workflows/       continuous integration
└── requirements.txt
```

## Reproducing the Analysis

```bash
pip install -r requirements.txt
pytest -q                          # run unit tests
python scripts/run_notebook.py     # execute the notebook and refresh figures and tables
python scripts/build_report.py     # rebuild the Excel report and presentation
```

The workflow in `.github/workflows/ci.yml` runs the same steps on every push.

## Data

The data are synthetic and created for educational use; they do not describe a real company or real customers. The
published customer table is limited to customer ID and annual income. Field definitions are documented in
[`data/README.md`](data/README.md).

## Limitations

- Because the data are synthetic, the findings illustrate the method rather than describe a real business.
- The dataset contains no cost or list-price fields, so the specific cause of the 2023 margin decline cannot be
  confirmed.
- Retention is measured by purchases only, and recent cohorts have shorter observation periods.
- Impact estimates are indicative sizing, not causal effects; recommendations 2 and 3 should be validated through
  controlled tests.

## Author

Pham Hong Hieu (Haven) · [Portfolio](https://haven-portfolio02.vercel.app) · [LinkedIn](https://www.linkedin.com/in/havenpham) · [GitHub](https://github.com/Haven-Pham)
