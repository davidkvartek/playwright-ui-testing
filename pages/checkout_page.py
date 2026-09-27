from playwright.sync_api import Page


class CheckoutPage:
    """The three checkout steps: your information, overview, complete."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = page.locator('[data-test="title"]')
        self.cancel_button = page.locator('[data-test="cancel"]')

        # Step one: your information.
        self.first_name = page.locator('[data-test="firstName"]')
        self.last_name = page.locator('[data-test="lastName"]')
        self.postal_code = page.locator('[data-test="postalCode"]')
        self.continue_button = page.locator('[data-test="continue"]')
        # saucedemo reuses data-test="error" for login and checkout validation.
        self.error = page.locator('[data-test="error"]')

        # Step two: overview.
        self.items = page.locator('[data-test="inventory-item"]')
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.item_total = page.locator('[data-test="subtotal-label"]')
        self.tax = page.locator('[data-test="tax-label"]')
        self.total = page.locator('[data-test="total-label"]')
        self.finish_button = page.locator('[data-test="finish"]')

        # Step three: complete.
        self.complete_header = page.locator('[data-test="complete-header"]')
        self.complete_text = page.locator('[data-test="complete-text"]')
        self.back_home_button = page.locator('[data-test="back-to-products"]')

    def fill_details(
        self, first_name: str, last_name: str, postal_code: str | None = None
    ) -> None:
        """Fill the step-one form. A postal_code of None leaves the field untouched."""
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        if postal_code is not None:
            self.postal_code.fill(postal_code)

    def continue_to_overview(self) -> None:
        self.continue_button.click()

    def finish(self) -> None:
        self.finish_button.click()
