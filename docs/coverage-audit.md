# Coverage audit

A green run only proves the tests that exist pass; it says nothing about the tests that don't. I audit this suite against a coverage checklist (negative paths, assertion strength, required fields, test independence, locator stability, waits, CI, mutation checks, bug tracking, test pyramid) and close each gap in its own commit. This log grows as I work through it. Every new or tightened test is made to fail on purpose with valid input before it counts.

Suite size: 12 test cases before the audit (11 passing, 1 strict xfail), 23 now (21 passing, 2 strict xfails).

## Gaps found and fixed

| Gap found | Why it matters | Fix | Commit |
|-----------|----------------|-----|--------|
| API login (POST /auth) had no failure test; only correct credentials were sent and the auth response was never checked. | A login that mishandles bad credentials would go unnoticed. It does: the API returns 200, not 401, on failed authentication. | `test_auth_rejects_bad_credentials` (wrong password, empty body) plus an auth check before using the token. | 68d7e7b |
| No required-field or unknown-user login cases. | A blank field is one of the most common real user errors, and a different message for unknown users would reveal which usernames exist. | Four rows added to the negative login parametrize list. | a8e2573 |
| Nothing proved the login protects any page; the tests only checked the form. | The form could work while /inventory.html stays reachable without logging in. | `test_inventory_requires_login` asserts the redirect, error text, login button and 0 items. | 378f2e0 |
| Checkout happy path checked only the confirmation screen, not the items or totals. | A wrong product or wrong tax math would still pass. The page objects had the locators; no test used them. | Cart item and quantity, overview item, item total, tax and total asserted with exact text. | c0f3fc9 |
| Price sort checked only that prices were in order (`prices == sorted(prices)`). | Missing products or wrong prices would still pass as long as what remained was sorted. | Exact expected price list taken from the live site, plus a product count check. | c3f4d2b |
| Checkout tested only a blank postal code; blank first and last name were untested, and nothing checked which error shows when several fields are blank. | An accidental blank field is common, and a change to how the form validates would go unnoticed for two of three fields. | `test_checkout_requires_details`, parametrized over each blank field plus an all-blank case that proves validation order. | 8196620 |
| `error_user` can submit checkout with a blank last name. | Orders can be placed without a customer last name, and testing only as `standard_user` can't catch it. | Strict-xfail test plus [BUG-002](BUG-002.md). | c7a940d |

## Findings recorded without a test
- **Checkout has no format checks.** `abc` or spaces pass as a postal code. Saucedemo has no spec for postal format, so a test asserting the bad input is accepted would lock in behavior that should change.

## Lessons
- **Break tests with valid input, not a misspelled expected value.** Editing the expected text only proves the comparison runs.
- **Commit before you break.** `git restore` returns a file to its last commit, so breaking an uncommitted test can erase it.
- **An assertion can be specific and still miss the point.** Page-object locators that no test uses are a quick sign a test stops short.
- **Take expected values from the system.** Dollar amounts and price lists were read off the live site, and the green CI run confirms them.
- **A strict xfail accepts any failure.** `pytest --runxfail` shows the real failure, so a broken setup step can't pass as the bug.
- **A failed `expect` stops the test.** A break-check that fails on the first assertion proves nothing about the assertions after it.
