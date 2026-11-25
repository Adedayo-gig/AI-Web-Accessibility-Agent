from playwright.sync_api import sync_playwright
import re


# ==========================================
# UNDERSTAND USER REQUEST
# ==========================================

def understand_request(request):

    request = request.lower()

    requirements = {}

    if "black" in request:
        requirements["colour"] = "black"

    elif "white" in request:
        requirements["colour"] = "white"


    size_match = re.search(
        r"size\s*(40|41|42|43|44|45)",
        request
    )

    if size_match:
        requirements["size"] = size_match.group(1)


    price_match = re.search(
        r"(?:below|under|less than)\s*[₦n]?\s*([\d,]+)",
        request
    )

    if price_match:

        price = price_match.group(1)

        price = price.replace(",", "")

        requirements["max_price"] = int(price)


    return requirements


# ==========================================
# INSPECT PRODUCTS
# ==========================================

def inspect_products(page):

    products = page.locator(".product")

    product_list = []

    for i in range(products.count()):

        product = products.nth(i)

        name = product.locator("h2").inner_text()

        price_text = product.locator(
            ".price"
        ).inner_text()

        price = re.sub(
            r"[^\d]",
            "",
            price_text
        )

        price = int(price)

        sizes = product.locator(
            ".size option"
        )

        available_sizes = []

        for j in range(sizes.count()):

            size = sizes.nth(j).inner_text()

            if size != "Choose size":

                available_sizes.append(size)


        product_list.append({

            "index": i,
            "name": name,
            "price": price,
            "sizes": available_sizes

        })


    return product_list


# ==========================================
# FIND MATCHING PRODUCT
# ==========================================

def find_matching_product(
    products,
    requirements
):

    for product in products:

        name = product["name"].lower()


        if "colour" in requirements:

            if requirements["colour"] not in name:

                continue


        if "max_price" in requirements:

            if product["price"] > requirements["max_price"]:

                continue


        if "size" in requirements:

            if requirements["size"] not in product["sizes"]:

                continue


        return product


    return None


# ==========================================
# MAIN PROGRAM
# ==========================================

with sync_playwright() as p:

    browser = p.chromium.launch(

        headless=False,

        executable_path=r"C:\Users\LENOVO\AppData\Local\Google\Chrome\Application\chrome.exe"

    )

    page = browser.new_page()

    page.goto(
        "file:///C:/Users/LENOVO/Desktop/AI-Web-agent/test_multiple_products.html"
    )


    print("Shop opened successfully.")


    # ======================================
    # USER REQUEST
    # ======================================

    user_request = (
        "Find a black shoe, size 45, below ₦15,000 "
        "and add it to my cart"
    )


    print("\nUSER REQUEST:")

    print(user_request)


    # ======================================
    # UNDERSTAND REQUEST
    # ======================================

    requirements = understand_request(
        user_request
    )


    print("\nREQUIREMENTS:")

    print(requirements)


    # ======================================
    # INSPECT
    # ======================================

    products = inspect_products(page)


    print("\nPRODUCTS FOUND:")

    for product in products:

        print(product)


    # ======================================
    # MATCH
    # ======================================

    matching_product = find_matching_product(
        products,
        requirements
    )


    print("\nMATCHING PRODUCT:")

    print(matching_product)


    # ======================================
    # TAKE ACTION
    # ======================================

    if matching_product:

        index = matching_product["index"]

        size = requirements["size"]


        product = page.locator(
            ".product"
        ).nth(index)


        print(
            "\nMatching product found."
        )


        # SELECT SIZE

        print(
            "Selecting size:",
            size
        )


        product.locator(
            ".size"
        ).select_option(
            label=size
        )


        print(
            "Size selected successfully."
        )


        # CLICK ADD TO CART

        print(
            "\nClicking Add to Cart..."
        )


        product.locator(
            ".add-cart"
        ).click()


        print(
            "Add to Cart clicked."
        )


        # ==================================
        # VERIFY
        # ==================================

        print(
            "\nVERIFYING CART..."
        )


        cart_status = page.locator(
            "#cart-status"
        ).inner_text()


        print(
            "Cart status:"
        )

        print(
            cart_status
        )


        expected = (
            matching_product["name"]
            + ", Size "
            + size
            + " added to cart."
        )


        if cart_status == expected:

            print(
                "\nVERIFICATION: "
                "Product added successfully."
            )

        else:

            print(
                "\nVERIFICATION FAILED."
            )


    else:

        print(
            "\nNo matching product found."
        )


    page.wait_for_timeout(3000)

    browser.close()