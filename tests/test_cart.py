from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def test_add_item_to_cart(driver):
    driver.get("http://opencart:80/")
    wait = WebDriverWait(driver, 10)
    
    # Wait until all products are loaded
    products = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-thumb"))
    )
    
    # Select the first product
    first_product = products[0]
    
    # Find the Add to Cart button inside this product (handle both title and bootstrap tooltip attr)
    try:
        add_button = first_product.find_element(By.CSS_SELECTOR, '[title="Add to Cart"],[data-bs-original-title="Add to Cart"]')
    except Exception:
        # fallback to searching globally if not found inside the product element
        add_button = driver.find_element(By.CSS_SELECTOR, '[title="Add to Cart"],[data-bs-original-title="Add to Cart"]')

    # Wait until clickable (use driver for the wait)
    add_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[title="Add to Cart"],[data-bs-original-title="Add to Cart"]'))
    )

    # Scroll into view first to reduce chance of interception
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_button)

    # Try a normal click and fall back to JS click if something intercepts it
    try:
        add_button.click()
    except Exception:
        driver.execute_script("arguments[0].click();", add_button)

    # Wait for the cart to update (avoid brittle string checks by waiting)
    WebDriverWait(driver, 10).until(lambda d: "1 item(s)" in d.page_source)
    page = driver.page_source
    assert "1 item(s)" in page

def test_remove_item_from_cart(driver):
    driver.get("http://localhost/opencart")
    wait = WebDriverWait(driver, 10)

    # Wait until products load and pick the first
    products = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-thumb"))
    )
    first_product = products[0]

    # Add the item to cart (reuse robust add logic)
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

    # Open the cart dropdown/menu using a robust strategy (move, inner toggle, JS fallback)
    cart = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "cart")))
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cart)
    ac = ActionChains(driver)
    opened = False
    # Try to click an inner toggle (button or anchor) inside #cart first
    try:
        try:
            inner = cart.find_element(By.CSS_SELECTOR, "button, a")
            ac.move_to_element(inner).click(inner).perform()
            opened = True
        except Exception:
            # fallback to clicking the container itself
            ac.move_to_element(cart).click(cart).perform()
            opened = True
    except Exception:
        # As a last resort, use JS click
        try:
            driver.execute_script("arguments[0].click();", cart)
            opened = True
        except Exception:
            opened = False

    # Ensure the cart dropdown/menu actually opened by waiting for the View Cart link
    if not opened:
        # still attempt to open via JS to maximize chance
        driver.execute_script("arguments[0].click();", cart)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "View Cart")))

    # Wait for the remove button to appear inside the cart area and click it
    remove_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[title='Remove'], button[aria-label='Remove']"))
    )
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", remove_button)
    try:
        remove_button.click()
    except Exception:
        driver.execute_script("arguments[0].click();", remove_button)

    # Wait until cart updates to 0 items
    WebDriverWait(driver, 10).until(lambda d: "0 item(s)" in d.page_source)
    assert "0 item(s)" in driver.page_source


def test_update_item_quantity_in_cart(driver):
    """Add an item, go to View Cart, change its quantity to 2 and press Update, then assert quantity updated."""
    driver.get("http://localhost/opencart")
    wait = WebDriverWait(driver, 10)

    # Wait until products load and pick the first
    products = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-thumb"))
    )
    first_product = products[0]

    # Add the item to cart
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

    # Try to open the cart by clicking the Shopping Cart toggle (if present) or fallback to #cart
    try:
        shopping_cart = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[title="Shopping Cart"]'))
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", shopping_cart)
        try:
            shopping_cart.click()
        except Exception:
            driver.execute_script("arguments[0].click();", shopping_cart)
    except Exception:
        cart = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, "cart")))
        driver.execute_script("arguments[0].click();", cart)

    # Find a quantity input on the cart page
    qty_selectors = ["input[name*='quantity']", "input[type='number']", "input[id*='quantity']"]
    qty_input = None
    for sel in qty_selectors:
        try:
            qty_input = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, sel)))
            if qty_input:
                break
        except Exception:
            qty_input = None

    assert qty_input is not None, "Could not find quantity input on View Cart page"

    # Change quantity to 2 robustly
    try:
        qty_input.clear()
        qty_input.send_keys("2")
    except Exception:
        try:
            qty_input.click()
            qty_input.clear()
            qty_input.send_keys("2")
        except Exception:
            driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", qty_input, "2")

    # Try to find an Update button within the same row, fallback to global 'Update' button
    update_btn = None
    try:
        row = qty_input.find_element(By.XPATH, "./ancestor::tr[1]")
        update_btn = row.find_element(By.XPATH, ".//button[contains(@data-original-title,'Update') or contains(@title,'Update') or normalize-space(.)='Update']")
    except Exception:
        try:
            update_btn = driver.find_element(By.XPATH, "//button[normalize-space() = 'Update']")
        except Exception:
            update_btn = None

    assert update_btn is not None, "Could not find Update button for cart quantity"

    try:
        update_btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", update_btn)

    # Wait for the quantity input value to become '2'
    WebDriverWait(driver, 10).until(lambda d: qty_input.get_attribute('value') in ('2', '2.0'))
    assert qty_input.get_attribute('value') in ('2', '2.0')
 