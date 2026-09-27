from playwright.sync_api import Locator, Page


class InventoryPage:
    """The product listing shown after a successful login."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = page.locator('[data-test="title"]')
        self.items = page.locator('[data-test="inventory-item"]')
        self.item_names = page.locator('[data-test="inventory-item-name"]')
        self.prices = page.locator('[data-test="inventory-item-price"]')
        self.cart_badge = page.locator('[data-test="shopping-cart-badge"]')
        self.cart_link = page.locator('[data-test="shopping-cart-link"]')
        self.sort_menu = page.locator('[data-test="product-sort-container"]')

    def add_to_cart_button(self, product_slug: str) -> Locator:
        return self.page.locator(f'[data-test="add-to-cart-{product_slug}"]')

    def add_to_cart(self, product_slug: str) -> None:
        self.add_to_cart_button(product_slug).click()

    def sort_by(self, option_value: str) -> None:
        """Sort the listing. Valid values: az, za, lohi, hilo."""
        self.sort_menu.select_option(option_value)

    def price_values(self) -> list[float]:
        """Prices in listed order, as floats. "$29.99" -> 29.99"""
        # all_inner_texts() reads immediately instead of auto-waiting, so wait
        # for the listing to render first or a freshly loaded page returns [].
        self.prices.first.wait_for()
        return [float(text.lstrip("$")) for text in self.prices.all_inner_texts()]
