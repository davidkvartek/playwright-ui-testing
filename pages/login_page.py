from playwright.sync_api import Page


class LoginPage:
    """The saucedemo sign-in form."""

    URL = "https://www.saucedemo.com/"

    def __init__(self, page: Page) -> None:
        self.page = page
        self.username = page.locator('[data-test="username"]')
        self.password = page.locator('[data-test="password"]')
        self.login_button = page.locator('[data-test="login-button"]')
        self.error = page.locator('[data-test="error"]')

    def open(self) -> "LoginPage":
        self.page.goto(self.URL)
        return self

    def login(self, user: str, pwd: str) -> None:
        self.username.fill(user)
        self.password.fill(pwd)
        self.login_button.click()
