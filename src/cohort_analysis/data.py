"""Loading and validating the raw tables."""

from pathlib import Path

import pandas as pd

SALES_COLUMNS = [
    "RowID", "OrderID", "OrderDate", "CustomerID", "Segment", "RegionCode",
    "ProductCode", "Quantity", "Sales", "Discount", "Profit",
]
CUSTOMER_COLUMNS = ["CustomerID", "AnnualIncome"]


def load_sales(data_dir: Path) -> pd.DataFrame:
    """Order lines. OrderDate is stored as M/D/YYYY text in the source file."""
    sales = pd.read_csv(Path(data_dir) / "EcomSales.csv")
    missing = set(SALES_COLUMNS) - set(sales.columns)
    if missing:
        raise ValueError(f"EcomSales.csv is missing columns: {sorted(missing)}")
    sales["OrderDate"] = pd.to_datetime(sales["OrderDate"], format="%m/%d/%Y")
    return sales


def load_customers(data_dir: Path) -> pd.DataFrame:
    """Customer attributes used by the analysis (ID and annual income only)."""
    customers = pd.read_csv(Path(data_dir) / "Customer.csv", usecols=CUSTOMER_COLUMNS)
    return customers


def load_products(data_dir: Path) -> pd.DataFrame:
    """Product catalogue (one row per ProductCode)."""
    return pd.read_csv(Path(data_dir) / "Product.csv").drop_duplicates("ProductCode")


def validate(sales: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    """Return a one-row-per-check table; raise if a blocking check fails."""
    checks = [
        ("Order lines", len(sales), True),
        ("Customers", customers["CustomerID"].nunique(), True),
        ("Duplicate RowID", int(sales["RowID"].duplicated().sum()), sales["RowID"].is_unique),
        ("Duplicate CustomerID in Customer", int(customers["CustomerID"].duplicated().sum()), customers["CustomerID"].is_unique),
        ("Missing values in sales", int(sales.isna().sum().sum()), not sales.isna().any().any()),
        ("Sales customers without a profile", len(set(sales["CustomerID"]) - set(customers["CustomerID"])),
         set(sales["CustomerID"]) <= set(customers["CustomerID"])),
        ("Customers with more than one segment", int((sales.groupby("CustomerID")["Segment"].nunique() > 1).sum()),
         True),
        ("Order lines with negative profit", int((sales["Profit"] < 0).sum()), True),
    ]
    report = pd.DataFrame(checks, columns=["check", "value", "passed"])
    blocking = report.loc[report["check"].isin(
        ["Duplicate RowID", "Duplicate CustomerID in Customer", "Missing values in sales", "Sales customers without a profile"])]
    if not blocking["passed"].all():
        raise ValueError(f"Data validation failed:\n{blocking[~blocking['passed']]}")
    return report
