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
        r"size\s*(40|41|42|43|44|45|46)",
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

        name = product.locator(
            "h2"
        ).inner_text()

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
# FIND EXACT MATCH
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
# FIND ALTERNATIVES
# ==========================================

def find_alternatives(
    products,
    requirements
):

    alternatives = []

    requested_colour = requirements.get(
        "colour"
    )

    requested_size = requirements.get(
        "size"
    )

    max_price = requirements.get(
        "max_price"
    )


    for product in products:

        name = product["name"].lower()

        score = 0


        # Same colour

        if requested_colour:

            if requested_colour in name:

                score += 2


        # Requested size available

        if requested_size:

            if requested_size in product["sizes"]:

                score += 2


        # Price within requested limit

        if max_price:

            if product["price"] <= max_price:

                score += 2


        if score > 0:

            alternatives.append(
                (score, product)
            )


    # Highest score first

    alternatives.sort(
        key=lambda item: item[0],
        reverse=True
    )


    return [
        product
        for score, product in alternatives
    ]


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


    print(
        "Shop opened successfully."
    )


    # ======================================
    # USER REQUEST
    # ======================================

    user_request = (
        "Find a black shoe, size 46, below ₦10,000"
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

    products = inspect_products(
        page
    )


    print("\nPRODUCTS FOUND:")

    for product in products:

        print(product)


    # ======================================
    # FIND EXACT MATCH
    # ======================================

    matching_product = find_matching_product(
        products,
        requirements
    )


    # ======================================
    # RESULT
    # ======================================

    if matching_product:

        print(
            "\nEXACT MATCH FOUND:"
        )

        print(
            matching_product
        )


    else:

        print(
            "\nNO EXACT MATCH FOUND."
        )


        # ==================================
        # FIND ALTERNATIVES
        # ==================================

        alternatives = find_alternatives(
            products,
            requirements
        )


        if alternatives:

            print(
                "\nPOSSIBLE ALTERNATIVES:"
            )


            for product in alternatives:

                print(
                    f"- {product['name']} | "
                    f"₦{product['price']:,} | "
                    f"Sizes: "
                    f"{', '.join(product['sizes'])}"
                )


        else:

            print(
                "\nNo suitable alternatives found."
            )


    page.wait_for_timeout(3000)

    browser.close()