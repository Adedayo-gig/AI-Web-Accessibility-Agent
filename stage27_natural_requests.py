import re
from playwright.sync_api import sync_playwright


HTML_FILE = "file:///C:/Users/LENOVO/Desktop/AI-Web-agent/test_multiple_products.html"


def understand_request(request):
    request_lower = request.lower()

    # -----------------------------
    # Find colour
    # -----------------------------
    colour = None

    for c in ["black", "white", "red", "blue"]:
        if c in request_lower:
            colour = c
            break

    # -----------------------------
    # Find size
    # -----------------------------
    size = None

    size_match = re.search(r"\bsize\s*(\d+)", request_lower)

    if size_match:
        size = size_match.group(1)
    else:
        size_match = re.search(r"\bin\s*size\s*(\d+)", request_lower)

        if size_match:
            size = size_match.group(1)

    # -----------------------------
    # Find budget
    # -----------------------------
    max_price = None

    price_match = re.search(
        r"(?:around|under|below|less than|max(?:imum)?|up to)?\s*[₦]?\s*([\d,]+)\s*(?:k)?",
        request_lower
    )

    if price_match:
        number = price_match.group(1).replace(",", "")

        max_price = int(number)

        # Convert 15k → 15,000
        if "k" in request_lower[price_match.start():price_match.end()]:
            max_price *= 1000

    # -----------------------------
    # Check cart request
    # -----------------------------
    add_to_cart = (
        "cart" in request_lower
        and (
            "add" in request_lower
            or "put" in request_lower
            or "place" in request_lower
        )
    )

    return {
        "colour": colour,
        "size": size,
        "max_price": max_price,
        "add_to_cart": add_to_cart
    }


def inspect_products(page):
    products = []

    product_elements = page.locator(".product")

    for i in range(product_elements.count()):
        product = product_elements.nth(i)

        name = product.locator("h2").inner_text()
        price_text = product.locator("p").inner_text()

        price_match = re.search(r"[\d,]+", price_text)

        price = int(price_match.group().replace(",", ""))

        sizes = product.locator("option").all_inner_texts()

        sizes = [
            size.strip()
            for size in sizes
            if size.strip() and size.strip() != "Choose size"
        ]

        products.append({
            "index": i,
            "name": name,
            "price": price,
            "sizes": sizes
        })

    return products


def find_matching_product(products, requirements):

    for product in products:

        colour_match = (
            requirements["colour"] is None
            or requirements["colour"] in product["name"].lower()
        )

        size_match = (
            requirements["size"] is None
            or requirements["size"] in product["sizes"]
        )

        price_match = (
            requirements["max_price"] is None
            or product["price"] <= requirements["max_price"]
        )

        if colour_match and size_match and price_match:
            return product

    return None


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        executable_path=r"C:\Users\LENOVO\AppData\Local\Google\Chrome\Application\chrome.exe"
    )

    page = browser.new_page()

    page.goto(HTML_FILE)

    # Natural language request
    user_request = (
        "Can you find me a black shoe around 15k "
        "in size 45 and put it in the cart?"
    )

    print("\n===== USER REQUEST =====")
    print(user_request)

    # Understand request
    requirements = understand_request(user_request)

    print("\n===== UNDERSTOOD REQUIREMENTS =====")
    print(requirements)

    # Inspect products
    products = inspect_products(page)

    print("\n===== PRODUCTS FOUND =====")

    for product in products:
        print(product)

    # Find matching product
    matching_product = find_matching_product(
        products,
        requirements
    )

    if matching_product is None:

        print("\nNO MATCHING PRODUCT FOUND.")

    else:

        print("\n===== MATCHING PRODUCT =====")
        print(matching_product)

        # Select requested size
        if requirements["size"]:

            product_element = page.locator(".product").nth(
                matching_product["index"]
            )

            product_element.locator(".size").select_option(
                requirements["size"]
            )

            print(
                f"\nSize {requirements['size']} selected successfully."
            )

        # Add to cart
        if requirements["add_to_cart"]:

            product_element = page.locator(".product").nth(
                matching_product["index"]
            )

            product_element.locator(".add-cart").click()

            print("\nAdd to Cart clicked.")

            # Verify
            cart_status = page.locator("#cart-status").inner_text()

            print("\n===== CART VERIFICATION =====")
            print(cart_status)

    input("\nPress Enter to close the browser...")

    browser.close()