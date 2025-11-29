import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver

BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")
SELENIUM_URL = os.getenv("SELENIUM_URL", "http://localhost:4444/wd/hub")

@pytest.fixture
def driver() -> WebDriver:
    driver = webdriver.Remote(
        command_executor=SELENIUM_URL,
        options=webdriver.ChromeOptions()
    )
    yield driver
    driver.quit()