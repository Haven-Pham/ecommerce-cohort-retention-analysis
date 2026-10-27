"""Profitability views: by year, segment, income bracket and discount band."""

import pandas as pd

INCOME_BINS = [0, 50_000, 80_000, 110_000, float("inf")]
INCOME_LABELS = ["<$50k", "$50k–80k", "$80k–110k", ">$110k"]
DISCOUNT_BINS = [-0.001, 0.0, 0.20, 0.40, 1.0]
DISCOUNT_LABELS = ["No discount", "1–20%", "21–40%", ">40%"]


def _add_margin(frame: pd.DataFrame) -> pd.DataFrame:
    frame["margin"] = frame["profit"] / frame["sales"]
    return frame


def yearly_kpis(sales: pd.DataFrame) -> pd.DataFrame:
    first_year = sales.groupby("CustomerID")["OrderDate"].min().dt.year
    kpis = sales.groupby(sales["OrderDate"].dt.year).agg(
        sales=("Sales", "sum"), profit=("Profit", "sum"),
        orders=("OrderID", "nunique"), customers=("CustomerID", "nunique"),
        avg_discount=("Discount", "mean"))
    kpis.index.name = "year"
    kpis["new_customers"] = first_year.value_counts().sort_index()
    kpis["aov"] = kpis["sales"] / kpis["orders"]
    kpis["deep_discount_share"] = sales.assign(deep=sales["Discount"] > 0.20).groupby(
        sales["OrderDate"].dt.year)["deep"].mean()
    return _add_margin(kpis)


def margin_by_year(sales: pd.DataFrame, column: str) -> pd.DataFrame:
    """Profit margin with years as rows and the levels of `column` as columns."""
    grouped = sales.groupby([sales["OrderDate"].dt.year.rename("year"), column], observed=False).agg(
        sales=("Sales", "sum"), profit=("Profit", "sum"))
    return (grouped["profit"] / grouped["sales"]).unstack(column)


def segment_summary(sales: pd.DataFrame) -> pd.DataFrame:
    orders = sales.groupby(["Segment", "CustomerID"])["OrderID"].nunique()
    summary = sales.groupby("Segment").agg(
        customers=("CustomerID", "nunique"), sales=("Sales", "sum"), profit=("Profit", "sum"))
    summary["repeat_rate"] = orders.groupby("Segment").apply(lambda n: (n >= 2).mean())
    summary["sales_share"] = summary["sales"] / summary["sales"].sum()
    summary["profit_share"] = summary["profit"] / summary["profit"].sum()
    return _add_margin(summary)


def income_profitability(sales: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    brackets = customers.assign(
        income_bracket=pd.cut(customers["AnnualIncome"], bins=INCOME_BINS, labels=INCOME_LABELS))
    merged = sales.merge(brackets[["CustomerID", "income_bracket"]], on="CustomerID", how="inner")
    summary = merged.groupby("income_bracket", observed=False).agg(
        customers=("CustomerID", "nunique"), sales=("Sales", "sum"), profit=("Profit", "sum"))
    summary["profit_per_customer"] = summary["profit"] / summary["customers"]
    summary["customer_share"] = summary["customers"] / summary["customers"].sum()
    summary["profit_share"] = summary["profit"] / summary["profit"].sum()
    return _add_margin(summary)


def discount_profitability(sales: pd.DataFrame) -> pd.DataFrame:
    banded = sales.assign(discount_band=pd.cut(sales["Discount"], bins=DISCOUNT_BINS, labels=DISCOUNT_LABELS))
    summary = banded.groupby("discount_band", observed=False).agg(
        order_lines=("RowID", "size"), sales=("Sales", "sum"), profit=("Profit", "sum"),
        loss_making_lines=("Profit", lambda p: int((p < 0).sum())))
    summary["line_share"] = summary["order_lines"] / summary["order_lines"].sum()
    return _add_margin(summary)
