def test_homepage_loads(driver):
    driver.get("http://host.docker.internal:8080")
    assert "Your Store" in driver.title