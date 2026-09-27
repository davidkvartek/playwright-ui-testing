from playwright.sync_api import expect

from pages.inventory_page import InventoryPage


def test_adding_two_products_updates_cart_badge(logged_in: InventoryPage) -> None:
    expect(logged_in.add_to_cart_button("sauce-labs-backpack")).to_be_visible()
    expect(logged_in.cart_badge).not_to_be_visible()

    logged_in.add_to_cart("sauce-labs-backpack")
    logged_in.add_to_cart("sauce-labs-bike-light")

    expect(logged_in.cart_badge).to_have_text("2")
