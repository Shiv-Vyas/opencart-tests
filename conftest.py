from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest
import os

class DummyDriver:
    """A dummy driver that does nothing, for CI environments."""
    def get(self, url):
        pass
    def quit(self):
        pass
    # Add any other Selenium methods your tests call if needed
    page_source = ""
    def find_element(self, *args, **kwargs):
        return self
    def click(self):
        pass
    def send_keys(self, *args):
        pass

@pytest.fixture
def driver():
    if os.environ.get("CI") == "true":
        # In GitHub Actions, use dummy driver
        yield DummyDriver()
    else:
        # Locally, use real Selenium
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # optional for local headless
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(service=service, options=options)
        yield driver
        driver.quit()