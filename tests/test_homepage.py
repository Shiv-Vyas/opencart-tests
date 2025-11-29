def test_homepage_loads(driver):
    driver.get("http://localhost/opencart")
    assert "Your Store" in driver.title