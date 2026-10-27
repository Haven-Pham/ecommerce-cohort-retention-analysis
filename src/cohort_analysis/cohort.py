"""Cohort construction and retention metrics.

A customer's cohort is the period of their first purchase. Retention at index k
is the share of the cohort that purchased again exactly k periods later.
"""

import pandas as pd


def purchase_events(sales: pd.DataFrame) -> pd.DataFrame:
    """One row per customer per order date (several lines of one order count once)."""
    return sales[["CustomerID", "OrderDate"]].drop_duplicates().reset_index(drop=True)


def add_cohort_columns(events: pd.DataFrame, freq: str = "M") -> pd.DataFrame:
    """Add cohort period, activity period and the cohort index for monthly ("M") or quarterly ("Q") cohorts."""
    out = events.copy()
    first = out.groupby("CustomerID")["OrderDate"].transform("min")
    out["cohort"] = first.dt.to_period(freq)
    out["period"] = out["OrderDate"].dt.to_period(freq)
    out["cohort_index"] = (out["period"] - out["cohort"]).apply(lambda offset: offset.n)
    return out


def cohort_counts(events: pd.DataFrame) -> pd.DataFrame:
    """Active customers per cohort (rows) and cohort index (columns)."""
    return events.pivot_table(index="cohort", columns="cohort_index", values="CustomerID", aggfunc="nunique")


def retention_matrix(counts: pd.DataFrame) -> pd.DataFrame:
    """Divide every column by the cohort size (index 0)."""
    return counts.divide(counts[0], axis=0)


def pooled_retention(counts: pd.DataFrame) -> pd.Series:
    """Size-weighted retention curve: active customers at index k divided by the size of all
    cohorts old enough to be observed at k (avoids small cohorts dominating a simple mean).

    An empty cell can mean "no customer returned" or "not observable yet"; observability is
    decided from the last period present in the data, so true zeros stay in the denominator."""
    filled = counts.stack()
    last_period = max(cohort + k for cohort, k in filled.index)
    sizes = counts[0]
    curve = {}
    for k in counts.columns:
        observable = [cohort for cohort in counts.index if cohort + k <= last_period]
        curve[k] = counts.loc[observable, k].fillna(0).sum() / sizes.loc[observable].sum()
    return pd.Series(curve, name="retention")


def repeat_purchase_summary(sales: pd.DataFrame) -> pd.DataFrame:
    """Compare one-time and repeat customers on count, sales and profit."""
    per_customer = sales.groupby("CustomerID").agg(
        orders=("OrderID", "nunique"), sales=("Sales", "sum"), profit=("Profit", "sum"))
    per_customer["type"] = per_customer["orders"].map(lambda n: "Repeat (2+ orders)" if n >= 2 else "One-time")
    summary = per_customer.groupby("type").agg(
        customers=("orders", "size"), sales=("sales", "sum"), profit=("profit", "sum"),
        avg_profit_per_customer=("profit", "mean"))
    summary["customer_share"] = summary["customers"] / summary["customers"].sum()
    summary["profit_share"] = summary["profit"] / summary["profit"].sum()
    return summary


def time_to_second_purchase(events: pd.DataFrame) -> pd.Series:
    """Days between each repeat customer's first and second purchase date."""
    ordered = events.sort_values(["CustomerID", "OrderDate"])
    ordered = ordered.assign(rank=ordered.groupby("CustomerID").cumcount())
    first = ordered[ordered["rank"] == 0].set_index("CustomerID")["OrderDate"]
    second = ordered[ordered["rank"] == 1].set_index("CustomerID")["OrderDate"]
    return (second - first.reindex(second.index)).dt.days.rename("days_to_second_purchase")
