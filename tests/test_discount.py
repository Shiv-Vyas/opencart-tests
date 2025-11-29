def test_apply_invalid_discount_code(driver):
	"""Add a product, go to View Cart, apply an invalid coupon code, and assert error message."""
	driver.get("http://opencart:80/")
	wait = WebDriverWait(driver, 10)

	# Wait until products are loaded and pick the first product
	products = wait.until(
		EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-thumb"))
	)
	first_product = products[0]

	# Find the Add to Cart button (handle different attributes)
	try:
		add_button = first_product.find_element(By.CSS_SELECTOR, '[title="Add to Cart"],[data-bs-original-title="Add to Cart"]')
	except Exception:
		add_button = driver.find_element(By.CSS_SELECTOR, '[title="Add to Cart"],[data-bs-original-title="Add to Cart"]')

	add_button = WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable((By.CSS_SELECTOR, '[title="Add to Cart"],[data-bs-original-title="Add to Cart"]'))
	)
	driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_button)
	try:
		add_button.click()
	except Exception:
		driver.execute_script("arguments[0].click();", add_button)

	# Wait for cart to show 1 item
	WebDriverWait(driver, 10).until(lambda d: "1 item(s)" in d.page_source)

	# Open the cart dropdown/menu by clicking the element titled 'Shopping Cart'
	shopping_cart = WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable((By.CSS_SELECTOR, '[title="Shopping Cart"]'))
	)
	driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", shopping_cart)
	try:
		shopping_cart.click()
	except Exception:
		driver.execute_script("arguments[0].click();", shopping_cart)

	# Open the coupon accordion, enter invalid coupon into #input-coupon, and apply
	coupon_toggle = WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-bs-target="#collapse-coupon"]'))
	)
	driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", coupon_toggle)
	try:
		coupon_toggle.click()
	except Exception:
		driver.execute_script("arguments[0].click();", coupon_toggle)

	# Wait for the coupon input inside the expanded accordion (visible & enabled)
	coupon_input = WebDriverWait(driver, 10).until(
		EC.visibility_of_element_located((By.ID, "input-coupon"))
	)
	# Robustly set the coupon value: try clear/send_keys, fallback to click then send_keys, final fallback to JS set
	try:
		coupon_input.clear()
		coupon_input.send_keys("INVALIDCODE")
	except Exception:
		try:
			coupon_input.click()
			coupon_input.clear()
			coupon_input.send_keys("INVALIDCODE")
		except Exception:
			driver.execute_script(
				"arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));",
				coupon_input,
				"INVALIDCODE",
			)

	# Click the button with visible text 'Apply Coupon'
	apply_btn = WebDriverWait(driver, 10).until(
		EC.element_to_be_clickable((By.XPATH, "//button[normalize-space() = 'Apply Coupon']"))
	)
	try:
		apply_btn.click()
	except Exception:
		driver.execute_script("arguments[0].click();", apply_btn)

	# Wait for success message
	WebDriverWait(driver, 10).until(lambda d: "Warning: Coupon is either invalid, expired or reached its usage limit!" in d.page_source)
	assert "Warning: Coupon is either invalid, expired or reached its usage limit!" in driver.page_source
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
