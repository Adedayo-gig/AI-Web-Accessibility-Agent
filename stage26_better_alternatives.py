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


        options = product.locator(
            ".size option"
        )

        sizes = []

        for j in range(options.count()):

            size = options.nth(j).inner_text()

            if size != "Choose size":

                sizes.append(size)


        product_list.append({

            "index": i,
            "name": name,
            "price": price,
            "sizes": sizes

        })


    return product_list


# ==========================================
# RANK ALTERNATIVES
# ==========================================

def rank_alternatives(
    products,
    requirements
):

    ranked = []

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

        reasons = []


        # ----------------------------------
        # COLOUR
        # ----------------------------------

        if requested_colour:

            if requested_colour in name:

                score += 3

                reasons.append(
                    "same colour"
                )


        # ----------------------------------
        # SIZE
        # ----------------------------------

        if requested_size:

            if requested_size in product["sizes"]:

                score += 3

                reasons.append(
                    "requested size available"
                )

            else:

                reasons.append(
                    "requested size unavailable"
                )


        # ----------------------------------
        # PRICE
        # ----------------------------------

        if max_price:

            if product["price"] <= max_price:

                score += 3

                reasons.append(
                    "within budget"
                )

            else:

                difference = (
                    product["price"]
                    - max_price
                )

                reasons.append(
                    f"₦{difference:,} above budget"
                )


        ranked.append({

            "product": product,
            "score": score,
            "reasons": reasons

        })


    # Highest score first

    ranked.sort(
        key=lambda item: item["score"],
        reverse=True
    )


    return ranked


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
    # UNDERSTAND
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
    # RANK ALTERNATIVES
    # ======================================

    ranked = rank_alternatives(
        products,
        requirements
    )


    print(
        "\nRANKED ALTERNATIVES:"
    )


    for item in ranked:

        product = item["product"]

        print(
            f"\nProduct: {product['name']}"
        )

        print(
            f"Price: ₦{product['price']:,}"
        )

        print(
            f"Sizes: {', '.join(product['sizes'])}"
        )

        print(
            f"Score: {item['score']}"
        )

        print(
            "Reasons:"
        )

        for reason in item["reasons"]:

            print(
                f"- {reason}"
            )


    page.wait_for_timeout(3000)

    browser.close()