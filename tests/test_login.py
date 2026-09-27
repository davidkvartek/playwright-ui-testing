import re

from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def test_standard_user_can_log_in(page: Page) -> None:
    LoginPage(page).open().login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(inventory.title).to_have_text("Products")
    expect(inventory.items).to_have_count(6)


def test_wrong_password_shows_error_and_stays_on_login(page: Page) -> None:
    login_page = LoginPage(page).open()
    login_page.login("standard_user", "wrong_password")

    expect(login_page.error).to_contain_text(
        "Username and password do not match any user in this service"
    )
    expect(page).to_have_url(LoginPage.URL)


def test_locked_out_user_sees_locked_out_error(page: Page) -> None:
    login_page = LoginPage(page).open()
    login_page.login("locked_out_user", "secret_sauce")

    expect(login_page.error).to_contain_text("Sorry, this user has been locked out")
