import re

import pytest
from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def test_standard_user_can_log_in(page: Page) -> None:
    LoginPage(page).open().login("standard_user", "secret_sauce")

    inventory = InventoryPage(page)
    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(inventory.title).to_have_text("Products")
    expect(inventory.items).to_have_count(6)


@pytest.mark.parametrize(
    ("user", "pwd", "expected_error"),
    [
        (
            "standard_user",
            "wrong_password",
            "Username and password do not match any user in this service",
        ),
        ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out"),
        ("", "", "Username is required"),
        ("standard_user", "", "Password is required"),
        ("", "secret_sauce", "Username is required"),
        (
            "no_such_user",
            "secret_sauce",
            "Username and password do not match any user in this service",
        ),
    ],
    ids=[
        "wrong-password",
        "locked-out",
        "empty-both",
        "empty-password",
        "empty-username",
        "unknown-user",
    ],
)
def test_invalid_login_shows_error_and_stays_on_login(
    page: Page, user: str, pwd: str, expected_error: str
) -> None:
    login_page = LoginPage(page).open()
    login_page.login(user, pwd)

    expect(login_page.error).to_contain_text(expected_error)
    expect(page).to_have_url(LoginPage.URL)
