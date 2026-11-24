from datetime import date

import pytest

from app.loaders import load_product_records


def _active_ids(as_of: date) -> set[str]:
    return {d.metadata["product_id"] for d in load_product_records(as_of=as_of)}


@pytest.mark.parametrize(
    "as_of, should_be_active",
    [
        (date(2026, 5, 31), False),   # day before it starts
        (date(2026, 6, 1), True),     # first valid day
        (date(2026, 9, 30), True),    # last valid day
        (date(2026, 10, 1), False),   # day after it ends
    ],
)
def test_sav_easy_01_effective_dates(as_of, should_be_active):
    assert ("SAV-EASY-01" in _active_ids(as_of)) is should_be_active


def test_sav_easy_01_rate_is_served_while_valid():
    docs = load_product_records(as_of=date(2026, 8, 1))
    text = next(d.page_content for d in docs if d.metadata["product_id"] == "SAV-EASY-01")
    assert "2.85%" in text