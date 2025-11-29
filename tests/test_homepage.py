from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def test_homepage_loads(driver):
    driver.get("https://demo.opencart.com/")
    # Wait for the site to finish any interim page (e.g. Cloudflare) and load the actual store
    try:
        WebDriverWait(driver, 30).until(EC.title_contains("Your Store"))
    except TimeoutException:
        # Capture some diagnostics to help debugging
        title = driver.title
        page_snippet = driver.page_source[:200]
        raise AssertionError(
            f"Homepage did not load in time. Current title: {title!r}. Page start: {page_snippet!r}"
        )