import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


@pytest.mark.ui
@pytest.mark.parametrize(
    "user",
    [
        "standard_user",
        pytest.param(
            "problem_user",
            marks=pytest.mark.xfail(reason="BUG-001: price sort broken for problem_user", strict=True),
        ),
    ],
)
def test_price_sort_for_each_user(page, user):
    login = LoginPage(page)
    login.open()
    login.login(user, "secret_sauce")

    inventory = InventoryPage(page)
    inventory.sort_by("lohi")
    prices = inventory.price_values()

    assert prices == sorted(prices), f"Prices not sorted: {prices}"