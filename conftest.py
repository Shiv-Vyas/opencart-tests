import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")        # Run headless
    options.add_argument("--no-sandbox")      # Required in many CI environments
    options.add_argument("--disable-dev-shm-usage")  # Avoids /dev/shm issues in CI

    # Create the Chrome WebDriver
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    yield driver  # Provide the fixture value to the test

    # Quit after the test completes
    driver.quit()