import re

import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

# Captured 2026-10-06 by logging in as standard_user and reading
# InventoryPage.price_values() with no sort applied, which returned
# [29.99, 9.99, 15.99, 49.99, 7.99, 15.99]. This is that list sorted ascending.
EXPECTED_LOHI_PRICES = [7.99, 9.99, 15.99, 15.99, 29.99, 49.99]


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

    assert len(prices) == len(EXPECTED_LOHI_PRICES), (
        f"Expected {len(EXPECTED_LOHI_PRICES)} products, found {len(prices)}: {prices}"
    )
    assert prices == EXPECTED_LOHI_PRICES, (
        f"Prices not in expected low-to-high order: {prices}"
    )


@pytest.mark.ui
@pytest.mark.xfail(reason="BUG-002: checkout accepts a blank last name for error_user", strict=True)
def test_checkout_requires_last_name_for_error_user(page):
    LoginPage(page).open().login("error_user", "secret_sauce")

    inventory = InventoryPage(page)
    inventory.add_to_cart("sauce-labs-backpack")
    inventory.cart_link.click()

    cart = CartPage(page)
    expect(cart.item_names).to_have_text(["Sauce Labs Backpack"])
    cart.checkout()

    checkout = CheckoutPage(page)
    checkout.fill_details("David", "", "34994")
    checkout.continue_to_overview()

    expect(checkout.error).to_contain_text("Error: Last Name is required")
    expect(page).to_have_url(re.compile(r"/checkout-step-one\.html$"))
