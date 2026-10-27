"""Unit tests on a tiny hand-checkable dataset."""
import sys
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from cohort_analysis import (  # noqa: E402
    add_cohort_columns,
    cohort_counts,
    discount_profitability,
    pooled_retention,
    purchase_events,
    repeat_purchase_summary,
    retention_matrix,
    time_to_second_purchase,
    validate,
)


@pytest.fixture
def sales():
    rows = [
        # RowID, OrderID, OrderDate, CustomerID, Segment, Sales, Discount, Profit
        (1, "O1", "2022-01-05", "A", "Consumer", 100, 0.0, 30),
        (2, "O1", "2022-01-05", "A", "Consumer", 50, 0.0, 10),   # same order, same day
        (3, "O2", "2022-02-10", "A", "Consumer", 80, 0.1, 12),   # A returns in month 1
        (4, "O3", "2022-01-20", "B", "Corporate", 200, 0.5, -60),
        (5, "O4", "2022-02-01", "C", "Consumer", 60, 0.0, 18),
        (6, "O5", "2022-05-01", "C", "Consumer", 40, 0.3, -4),   # C returns in month 3
    ]
    frame = pd.DataFrame(rows, columns=["RowID", "OrderID", "OrderDate", "CustomerID", "Segment", "Sales", "Discount", "Profit"])
    frame["OrderDate"] = pd.to_datetime(frame["OrderDate"])
    frame["RegionCode"], frame["ProductCode"], frame["Quantity"] = "R1", "P1", 1
    return frame


@pytest.fixture
def customers():
    return pd.DataFrame({"CustomerID": ["A", "B", "C"], "AnnualIncome": [40_000, 90_000, 60_000]})


def test_purchase_events_collapse_lines_of_one_order(sales):
    assert len(purchase_events(sales)) == 5


def test_monthly_cohorts_and_retention(sales):
    counts = cohort_counts(add_cohort_columns(purchase_events(sales), "M"))
    jan, feb = pd.Period("2022-01", "M"), pd.Period("2022-02", "M")
    assert counts.loc[jan, 0] == 2 and counts.loc[feb, 0] == 1
    retention = retention_matrix(counts)
    assert retention.loc[jan, 1] == pytest.approx(0.5)
    assert retention.loc[feb, 3] == pytest.approx(1.0)


def test_pooled_retention_weights_by_cohort_size(sales):
    curve = pooled_retention(cohort_counts(add_cohort_columns(purchase_events(sales), "M")))
    assert curve[0] == pytest.approx(1.0)
    assert curve[1] == pytest.approx(1 / 3)  # 1 active out of 3 customers in cohorts observed at month 1


def test_repeat_summary_and_gap(sales):
    summary = repeat_purchase_summary(sales)
    assert summary.loc["Repeat (2+ orders)", "customers"] == 2
    assert summary["profit_share"].sum() == pytest.approx(1.0)
    gaps = time_to_second_purchase(purchase_events(sales))
    assert sorted(gaps.tolist()) == [36, 89]


def test_discount_bands_split_profit(sales):
    bands = discount_profitability(sales)
    assert bands["order_lines"].sum() == len(sales)
    assert bands.loc[">40%", "profit"] == -60


def test_validate_rejects_orphan_customers(sales, customers):
    validate(sales, customers)
    with pytest.raises(ValueError):
        validate(sales, customers[customers["CustomerID"] != "C"])
