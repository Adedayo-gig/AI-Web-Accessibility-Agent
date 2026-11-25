from playwright.sync_api import sync_playwright
import re


# ==========================================
# READ PRODUCT
# ==========================================

def understand_product(page):

    product_name = page.locator("h2").inner_text()

    price_text = page.locator("p").first.inner_text()

    # Extract the number from the price
    price_match = re.search(
        r"[\d,]+",
        price_text
    )

    price = int(
        price_match.group().replace(",", "")
    )

    sizes = []

    options = page.locator("#size option").all()

    for option in options:

        size = option.inner_text().strip()

        if size != "Choose size":

            sizes.append(size)

    return {
        "name": product_name,
        "price": price,
        "sizes": sizes
    }


# ==========================================
# UNDERSTAND USER REQUEST
# ==========================================

def understand_request(user_request):

    request = user_request.lower()

    print("\n===== UNDERSTANDING REQUEST =====")


    # Find requested size

    size_match = re.search(
        r"size\s*(40|41|42|43|44|45)",
        request
    )

    requested_size = None

    if size_match:

        requested_size = size_match.group(1)

        print(
            f"Requested size: {requested_size}"
        )


    # Find maximum price

    price_match = re.search(
        r"(?:below|under|less than)\s*[₦n]?\s*([\d,]+)",
        request
    )

    max_price = None

    if price_match:

        max_price = int(
            price_match.group(1).replace(",", "")
        )

        print(
            f"Maximum price: ₦{max_price:,}"
        )


    # Product name

    product_requested = (
        "black running shoe"
        if "black running shoe" in request
        else None
    )


    if product_requested:

        print(
            f"Requested product: {product_requested}"
        )


    # Add to cart

    add_to_cart = (
        "add" in request
        and "cart" in request
    )


    if add_to_cart:

        print("Action requested: Add to cart")


    return {
        "product": product_requested,
        "size": requested_size,
        "max_price": max_price,
        "add_to_cart": add_to_cart
    }


# ==========================================
# MATCH REQUIREMENTS
# ==========================================

def match_requirements(
    request,
    product
):

    print("\n===== MATCHING REQUIREMENTS =====")


    # Product check

    if request["product"]:

        if request["product"].lower() in product["name"].lower():

            print("Product match: YES")

        else:

            print("Product match: NO")

            return False


    # Price check

    if request["max_price"]:

        if product["price"] < request["max_price"]:

            print(
                f"Price check: YES (₦{product['price']:,})"
            )

        else:

            print(
                f"Price check: NO (₦{product['price']:,})"
            )

            return False


    # Size check

    if request["size"]:

        if request["size"] in product["sizes"]:

            print(
                f"Size {request['size']}: AVAILABLE"
            )

        else:

            print(
                f"Size {request['size']}: NOT AVAILABLE"
            )

            return False


    print("\nAll requirements matched successfully.")

    return True


# ==========================================
# EXECUTE ACTION
# ==========================================

def execute_actions(page, request):

    # Select size

    if request["size"]:

        print("\nExecuting SELECT...")

        page.locator(
            "#size"
        ).select_option(
            label=request["size"]
        )

        print(
            f"Selected size {request['size']}."
        )


    # Add to cart

    if request["add_to_cart"]:

        print("\nExecuting CLICK...")

        page.locator(
            "#add-to-cart"
        ).click()

        print(
            "Add to Cart button clicked."
        )


# ==========================================
# VERIFY
# ==========================================

def verify_cart(page):

    print("\n===== VERIFYING CART =====")

    status = page.locator(
        "#cart-status"
    ).inner_text()

    print("Cart status:")

    print(status)

    if "added to cart" in status.lower():

        print(
            "VERIFICATION: Product added successfully."
        )

        return True

    else:

        print(
            "VERIFICATION: Product was not added."
        )

        return False


# ==========================================
# MAIN PROGRAM
# ==========================================

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        executable_path=r"C:\Users\LENOVO\AppData\Local\Google\Chrome\Application\chrome.exe"
    )

    page = browser.new_page()


    # OPEN SHOP

    page.goto(
        "file:///C:/Users/LENOVO/Desktop/AI-Web-agent/test_shop.html"
    )

    print("Shop opened successfully.")


    # USER REQUEST

    user_request = (
        "I want the black running shoe, "
        "size 44, below ₦15,000. "
        "Add it to my cart."
    )


    print("\nUSER REQUEST:")

    print(user_request)


    # READ PRODUCT

    product = understand_product(page)


    print("\n===== PRODUCT INFORMATION =====")

    print(product)


    # UNDERSTAND REQUEST

    request = understand_request(
        user_request
    )


    # MATCH REQUIREMENTS

    matched = match_requirements(
        request,
        product
    )


    # ONLY ACT IF EVERYTHING MATCHES

    if matched:

        print(
            "\nRequirements satisfied."
        )

        execute_actions(
            page,
            request
        )

        verify_cart(page)

    else:

        print(
            "\nRequirements NOT satisfied."
        )

        print(
            "Agent will NOT add the product to the cart."
        )


    page.wait_for_timeout(3000)

    browser.close()