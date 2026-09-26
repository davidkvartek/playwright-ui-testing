from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com/"


def test_adding_two_products_updates_cart_badge(page: Page) -> None:
    page.goto(BASE_URL)

    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()

    badge = page.locator('[data-test="shopping-cart-badge"]')
    expect(page.locator('[data-test="add-to-cart-sauce-labs-backpack"]')).to_be_visible()
    expect(badge).not_to_be_visible()

    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    page.locator('[data-test="add-to-cart-sauce-labs-bike-light"]').click()

    expect(badge).to_have_text("2")
