# Playwright UI + API Test Framework

![tests](https://github.com/davidkvartek/playwright-ui-testing/actions/workflows/playwright.yml/badge.svg)

UI and REST API test automation built with **Python, Playwright and pytest**, running in **GitHub Actions CI** on every push.

**At a glance:** 23 test cases (21 passing, 2 strict xfails that track known bugs) · 2 bugs reported · 7 coverage gaps found and closed by auditing my own suite.

## What's covered

| Area | Target | Tests |
|------|--------|-------|
| Login | saucedemo.com | Valid login, 6 data-driven negative cases (wrong password, locked out, required fields, unknown user), inventory page blocked without login |
| Cart | saucedemo.com | Adding products updates the cart badge |
| Checkout | saucedemo.com | Full order with exact items, item total, tax and total; each required field left blank, plus validation order |
| Known bugs | saucedemo.com | Price sort per user account, checkout last-name rule per user account |
| REST API | restful-booker | Health check, create-then-read integrity, delete with and without auth, failed login |

## Highlights
- **Page Object Model** (`pages/`): one class per page, all locators use `data-test` attributes, assertions stay in the tests
- **Data-driven negative tests** with `pytest.mark.parametrize`; adding a case is one row
- **Known defects tracked with strict xfail**, each with a written bug report, so the suite stays green without hiding the bug and fails loudly the day it is fixed
- **API layer** checks business rules below the UI, following the test pyramid
- **CI on every push:** clean checkout and fresh Chromium install; the HTML report is uploaded on every run, with screenshots and Playwright traces for any failed test

## Bugs and findings

| ID | Summary | Found by |
|----|---------|----------|
| [BUG-001](docs/BUG-001.md) | Price sort (low to high) does nothing for `problem_user` | Automated test run across user accounts |
| [BUG-002](docs/BUG-002.md) | Checkout accepts a blank last name for `error_user` | Exploratory testing, then automated |
| Finding | restful-booker answers a failed login with HTTP 200 and `{"reason": "Bad credentials"}`, not 401 | Writing the missing negative API test |
| Finding | Checkout checks only that fields are not empty; `abc` or spaces pass as a postal code | Reading how the form validates |

## How I audit this suite
A green run only proves the tests that exist pass. I review the suite against a coverage checklist (negative paths, assertion strength, required fields, test independence, locator stability, waits, CI, mutation checks, bug tracking, test pyramid) and close each gap in its own commit.

**7 gaps found and closed so far.** Full write-up with the commit for every fix: [docs/coverage-audit.md](docs/coverage-audit.md).

Examples:
- The checkout test only checked the "Thank you for your order!" screen. It now asserts the items, item total, tax and total, so a wrong product or wrong tax math fails.
- The price-sort test compared the prices to a sorted copy of themselves, which passes with missing products. It now compares against an exact list taken from the live site.
- The API login had no failure test. Writing one showed the API returns 200 on bad credentials.

## How I prove a test can fail
Every new or tightened test is broken on purpose before I trust it, by feeding the app **valid input** rather than editing the expected text. Editing the expected value only proves the comparison runs; valid input proves the test can tell good behavior from bad. Examples:
- Each blank-field checkout case is given a real value; the form moves on and the test goes red.
- The all-blank case, given a first name, goes red on "Last Name is required", which proves it checks validation order.
- A known-bug test run as `standard_user` reports XPASS(strict), which proves it detects the bug only where the bug exists.

## What I learned
- Specific assertions can still miss the point: check what the user cares about (the order), not just the last screen.
- Take expected values from the system, not from memory.
- A strict xfail accepts any failure, so run with `--runxfail` to confirm it fails for the bug's reason.
- Check behavior by hand before encoding it: saucedemo redirects after page load, which `expect(page).to_have_url` handles without a sleep.

## Run it locally
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
pytest
```
The HTML report is written to `reports/report.html`, and screenshots of failed tests go to `test-results/`. To run only the API tests: `pytest -m api`.

## Project structure
```
pages/       page objects: login, inventory, cart, checkout
tests/       UI tests, API tests, known-bug tests, shared fixtures (conftest.py)
docs/        bug reports and the coverage audit
.github/     GitHub Actions workflow
```
