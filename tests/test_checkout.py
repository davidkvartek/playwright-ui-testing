import re

from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com/"


def test_checkout_completes_for_single_product(page: Page) -> None:
    page.goto(BASE_URL)

    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()

    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    page.locator('[data-test="shopping-cart-link"]').click()
    page.locator('[data-test="checkout"]').click()

    page.locator('[data-test="firstName"]').fill("David")
    page.locator('[data-test="lastName"]').fill("Tester")
    page.locator('[data-test="postalCode"]').fill("34994")
    page.locator('[data-test="continue"]').click()

    page.locator('[data-test="finish"]').click()

    expect(page.locator('[data-test="complete-header"]')).to_have_text(
        "Thank you for your order!"
    )
    expect(page).to_have_url(re.compile(r"/checkout-complete\.html$"))


def test_checkout_requires_postal_code(page: Page) -> None:
    page.goto(BASE_URL)

    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()

    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    page.locator('[data-test="shopping-cart-link"]').click()
    page.locator('[data-test="checkout"]').click()

    page.locator('[data-test="firstName"]').fill("David")
    page.locator('[data-test="lastName"]').fill("Tester")
    page.locator('[data-test="continue"]').click()

    expect(page.locator('[data-test="error"]')).to_contain_text(
        "Error: Postal Code is required"
    )
    expect(page).to_have_url(re.compile(r"/checkout-step-one\.html$"))
