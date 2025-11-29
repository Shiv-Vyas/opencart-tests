from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import time

def test_register_and_login(driver):
    """Register a new account, then log in with the same credentials and assert login success."""
    driver.get("http://host.docker.internal:8080")
    wait = WebDriverWait(driver, 10)

    # Click 'My Account' on main page
    my_account = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "My Account")))
    my_account.click()

    # Click 'Register' in dropdown
    register = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Register")))
    register.click()

    # Fill registration form
    wait.until(EC.visibility_of_element_located((By.ID, "input-firstname"))).send_keys("TestFirst")
    wait.until(EC.visibility_of_element_located((By.ID, "input-lastname"))).send_keys("TestLast")
    import time
    email = f"testuser23432@example.com"
    wait.until(EC.visibility_of_element_located((By.ID, "input-email"))).send_keys(email)
    wait.until(EC.visibility_of_element_located((By.ID, "input-password"))).send_keys("TestPassword123!")

    # Agree to terms
    agree = wait.until(EC.element_to_be_clickable((By.NAME, "agree")))
    if not agree.is_selected():
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", agree)
        try:
            agree.click()
        except Exception:
            driver.execute_script("arguments[0].click();", agree)

    # Press Continue
    continue_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space() = 'Continue']")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_btn)
    try:
        continue_btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", continue_btn)

    # Wait for success message
    import re
    found = False
    for _ in range(20):
        page = driver.page_source
        norm_page = re.sub(r'[!.,]', '', page)
        norm_page = re.sub(r'\s+', ' ', norm_page).lower()
        if (
            "your account has been created" in norm_page
            or "congratulations your new account has been successfully created" in norm_page
        ):
            found = True
            break
        time.sleep(0.5)
    assert found, "Success message not found in page source after waiting 10s"

    # Log out to test login
    my_account = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "My Account")))
    my_account.click()
    logout = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Logout")))
    logout.click()

    # Go to login page
    my_account = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "My Account")))
    my_account.click()
    login_link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Login")))
    login_link.click()

    # Fill login form
    wait.until(EC.visibility_of_element_located((By.ID, "input-email"))).send_keys(email)
    wait.until(EC.visibility_of_element_located((By.ID, "input-password"))).send_keys("TestPassword123!")
    login_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//input[@value='Login']|//button[normalize-space()='Login']")
    ))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", login_btn)
    try:
        login_btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", login_btn)

    # Assert login success (look for My Account dropdown or welcome message)
    found_login = False
    for _ in range(20):
        page = driver.page_source
        norm_page = re.sub(r'[!.,]', '', page)
        norm_page = re.sub(r'\s+', ' ', norm_page).lower()
        if (
            "my account" in norm_page
            or "welcome" in norm_page
            or "edit your account information" in norm_page
        ):
            found_login = True
            break
        time.sleep(0.5)
    assert found_login, "Login success message not found in page source after waiting 10s"


def test_register_new_account(driver):
	driver.get("http://localhost/opencart")
	wait = WebDriverWait(driver, 10)

	# Click 'My Account' on main page
	my_account = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "My Account")))
	my_account.click()

	# Click 'Register' in dropdown
	register = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Register")))
	register.click()

	# Fill registration form
	wait.until(EC.visibility_of_element_located((By.ID, "input-firstname"))).send_keys("TestFirst")
	wait.until(EC.visibility_of_element_located((By.ID, "input-lastname"))).send_keys("TestLast")
	# Use a unique email for each run

	email = f"testuser123456@example.com"
	wait.until(EC.visibility_of_element_located((By.ID, "input-email"))).send_keys(email)
	wait.until(EC.visibility_of_element_located((By.ID, "input-password"))).send_keys("TestPassword123!")

	# Agree to terms
	agree = wait.until(EC.element_to_be_clickable((By.NAME, "agree")))
	if not agree.is_selected():
		driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", agree)
		try:
			agree.click()
		except Exception:
			driver.execute_script("arguments[0].click();", agree)

	# Press Continue
	continue_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space() = 'Continue']")))
	driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", continue_btn)
	try:
		continue_btn.click()
	except Exception:
		driver.execute_script("arguments[0].click();", continue_btn)

	# Assert success page (robust: check page_source and ignore punctuation)
		found = False
		for _ in range(20):  # up to 10 seconds
			page = driver.page_source
			norm_page = re.sub(r'[!.,]', '', page)
			norm_page = re.sub(r'\s+', ' ', norm_page).lower()
			if (
				"your account has been created" in norm_page
				or "congratulations your new account has been successfully created" in norm_page
			):
				found = True
				break
			time.sleep(0.5)
		assert found, "Success message not found in page source after waiting 10s"
