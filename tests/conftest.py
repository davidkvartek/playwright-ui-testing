import pytest
from playwright.sync_api import Page

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.fixture
def logged_in(page: Page) -> InventoryPage:
    """Log in as the standard user and hand back the inventory page."""
    LoginPage(page).open().login("standard_user", "secret_sauce")
    return InventoryPage(page)
