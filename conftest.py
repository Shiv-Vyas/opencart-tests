import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

@pytest.fixture
def driver():
    driver = webdriver.Remote(
        command_executor="http://localhost:4444/wd/hub",
        desired_capabilities=DesiredCapabilities.CHROME
    )
    yield driver
    driver.quit()