import re

from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com/"


def test_standard_user_can_log_in(page: Page) -> None:
    page.goto(BASE_URL)

    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(page.locator(".title")).to_have_text("Products")
    expect(page.locator(".inventory_item")).to_have_count(6)


def test_wrong_password_shows_error_and_stays_on_login(page: Page) -> None:
    page.goto(BASE_URL)

    page.locator('[data-test="username"]').fill("standard_user")
    page.locator('[data-test="password"]').fill("wrong_password")
    page.locator('[data-test="login-button"]').click()

    expect(page.locator('[data-test="error"]')).to_contain_text(
        "Username and password do not match any user in this service"
    )
    expect(page).to_have_url(BASE_URL)


def test_locked_out_user_sees_locked_out_error(page: Page) -> None:
    page.goto(BASE_URL)

    page.locator('[data-test="username"]').fill("locked_out_user")
    page.locator('[data-test="password"]').fill("secret_sauce")
    page.locator('[data-test="login-button"]').click()

    expect(page.locator('[data-test="error"]')).to_contain_text(
        "Sorry, this user has been locked out"
    )
