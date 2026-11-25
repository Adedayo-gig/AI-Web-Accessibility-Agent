from playwright.sync_api import sync_playwright
import re


# ==========================================
# OBSERVE
# ==========================================

def observe_page(page):

    print("\n===== OBSERVING PAGE =====")

    elements = []

    # Find dropdowns
    for dropdown in page.locator("select").all():

        try:

            element_id = dropdown.get_attribute("id")

            if element_id:

                elements.append({
                    "type": "SELECT",
                    "target": f"#{element_id}"
                })

        except Exception:
            pass


    # Find buttons
    for button in page.get_by_role("button").all():

        try:

            name = button.inner_text().strip()

            element_id = button.get_attribute("id")

            if name:

                elements.append({
                    "type": "BUTTON",
                    "name": name,
                    "target": f"#{element_id}"
                })

        except Exception:
            pass


    print("Elements found:")

    for element in elements:

        print("-", element)


    return elements


# ==========================================
# UNDERSTAND USER REQUEST
# ==========================================

def understand_request(user_request):

    request = user_request.lower()

    print("\n===== UNDERSTANDING REQUEST =====")


    # Find a size number

    size_match = re.search(
        r"size\s*(40|41|42|43|44|45)",
        request
    )


    size = None

    if size_match:

        size = size_match.group(1)

        print(f"Detected size: {size}")

    else:

        print("No size detected.")


    # Check whether user wants to add to cart

    add_to_cart = (
        "add" in request
        and "cart" in request
    )


    if add_to_cart:

        print("Detected: Add to cart")

    else:

        print("Add to cart not requested.")


    return {
        "size": size,
        "add_to_cart": add_to_cart
    }


# ==========================================
# DECIDE
# ==========================================

def decide_actions(request_data, elements):

    print("\n===== DECIDING ACTIONS =====")

    actions = []


    if request_data["size"]:

        actions.append({
            "action": "SELECT",
            "target": "#size",
            "value": request_data["size"]
        })


    if request_data["add_to_cart"]:

        actions.append({
            "action": "CLICK",
            "target": "#add-to-cart"
        })


    return actions


# ==========================================
# ACT
# ==========================================

def execute_action(page, action):

    if action["action"] == "SELECT":

        value = action["value"]

        print("\nExecuting SELECT...")

        page.locator(
            action["target"]
        ).select_option(
            label=value
        )

        print(f"Selected size {value}.")


    elif action["action"] == "CLICK":

        print("\nExecuting CLICK...")

        page.locator(
            action["target"]
        ).click()

        print("Button clicked.")


# ==========================================
# VERIFY
# ==========================================

def verify_action(page, action):

    if action["action"] == "SELECT":

        expected = action["value"]

        selected = page.locator(
            action["target"]
        ).locator(
            "option:checked"
        ).inner_text()


        if selected == expected:

            print(
                "VERIFICATION: Size selection successful."
            )

            return True


        print(
            "VERIFICATION: Size selection failed."
        )

        return False


    elif action["action"] == "CLICK":

        cart_status = page.locator(
            "#cart-status"
        ).inner_text()


        if "added to cart" in cart_status.lower():

            print(
                "VERIFICATION: Product added to cart."
            )

            return True


        print(
            "VERIFICATION: Add to cart failed."
        )

        return False


# ==========================================
# MAIN AGENT
# ==========================================

with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        executable_path=r"C:\Users\LENOVO\AppData\Local\Google\Chrome\Application\chrome.exe"
    )

    page = browser.new_page()


    # OPEN LOCAL SHOP

    page.goto(
        "file:///C:/Users/LENOVO/Desktop/AI-Web-agent/test_shop.html"
    )

    print("Website opened successfully.")


    # USER REQUEST

    user_request = (
        "Please choose size 44 and add it to my cart"
    )


    print("\nUSER REQUEST:")

    print(user_request)


    # OBSERVE

    elements = observe_page(page)


    # UNDERSTAND

    request_data = understand_request(
        user_request
    )


    # DECIDE

    actions = decide_actions(
        request_data,
        elements
    )


    print("\nAI DECIDED ACTIONS:")

    for action in actions:

        print(action)


    # ACT + VERIFY

    for action in actions:

        execute_action(
            page,
            action
        )


        success = verify_action(
            page,
            action
        )


        if not success:

            print(
                "\nAgent stopped because verification failed."
            )

            break


    # FINAL RESULT

    print("\n===== FINAL RESULT =====")

    print(
        page.locator("#cart-status").inner_text()
    )


    page.wait_for_timeout(3000)

    browser.close()