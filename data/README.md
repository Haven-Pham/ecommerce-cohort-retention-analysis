# Data

Synthetic educational dataset for a global e-commerce retailer (beauty and home products), January 2020 to December 2023.
It does not describe a real company, and no real customer data are included.

| File | Rows | Grain | Used for |
|---|---:|---|---|
| `raw/EcomSales.csv` | 51,290 | one order line | cohorts, retention, profitability |
| `raw/Customer.csv` | 17,415 | one customer | income brackets |
| `raw/Product.csv` | 28,356 | one product | category margin diagnosis |

## Data dictionary

**EcomSales.csv**

| Column | Type | Description |
|---|---|---|
| `RowID` | int | Unique order-line ID |
| `OrderID` | text | Order ID (an order can have several lines) |
| `OrderDate` | date (M/D/YYYY) | Order date |
| `CustomerID` | text | Customer key |
| `Segment` | text | Consumer, Corporate or Self-Employed (one per customer) |
| `RegionCode` | text | Region key |
| `ProductCode` | text | Product key |
| `Quantity` | int | Units |
| `Sales` | int | Line revenue (USD) |
| `Discount` | float | Discount rate, 0–0.85 |
| `Profit` | float | Line profit (USD); negative for loss-making lines |

**Customer.csv**: `CustomerID`, `AnnualIncome` (USD).

**Product.csv**: `ProductCode`, `Product`, `Category`, `Subcategory`.

## Data minimisation

The original customer table also contains names, e-mail addresses, birth dates and other demographics. They are not
needed for this analysis, so the published copy keeps only `CustomerID` and `AnnualIncome`.
