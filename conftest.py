import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless=new")

    driver = webdriver.Remote(
        command_executor="http://selenium:4444/wd/hub",
        options=options
    )

    yield driver
    driver.quit()