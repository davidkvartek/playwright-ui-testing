import re

from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage


def test_checkout_completes_for_single_product(logged_in: InventoryPage) -> None:
    page = logged_in.page

    logged_in.add_to_cart("sauce-labs-backpack")
    logged_in.cart_link.click()
    CartPage(page).checkout()

    checkout = CheckoutPage(page)
    checkout.fill_details("David", "Tester", "34994")
    checkout.continue_to_overview()
    checkout.finish()

    expect(checkout.complete_header).to_have_text("Thank you for your order!")
    expect(page).to_have_url(re.compile(r"/checkout-complete\.html$"))


def test_checkout_requires_postal_code(logged_in: InventoryPage) -> None:
    page = logged_in.page

    logged_in.add_to_cart("sauce-labs-backpack")
    logged_in.cart_link.click()
    CartPage(page).checkout()

    checkout = CheckoutPage(page)
    checkout.fill_details("David", "Tester")
    checkout.continue_to_overview()

    expect(checkout.error).to_contain_text("Error: Postal Code is required")
    expect(page).to_have_url(re.compile(r"/checkout-step-one\.html$"))
