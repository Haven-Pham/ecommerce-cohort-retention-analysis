"""Reusable building blocks for customer cohort, retention and profitability analysis."""

from .data import load_customers, load_products, load_sales, validate
from .cohort import (
    add_cohort_columns,
    cohort_counts,
    pooled_retention,
    purchase_events,
    repeat_purchase_summary,
    retention_matrix,
    time_to_second_purchase,
)
from .profitability import (
    DISCOUNT_BINS,
    DISCOUNT_LABELS,
    discount_profitability,
    income_profitability,
    margin_by_year,
    segment_summary,
    yearly_kpis,
)

__all__ = [
    "load_customers",
    "load_products",
    "load_sales",
    "validate",
    "purchase_events",
    "add_cohort_columns",
    "cohort_counts",
    "pooled_retention",
    "retention_matrix",
    "repeat_purchase_summary",
    "time_to_second_purchase",
    "yearly_kpis",
    "margin_by_year",
    "segment_summary",
    "income_profitability",
    "discount_profitability",
    "DISCOUNT_BINS",
    "DISCOUNT_LABELS",
]
