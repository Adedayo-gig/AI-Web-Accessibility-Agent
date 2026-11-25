from playwright.sync_api import sync_playwright


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
# DECIDE
# ==========================================

def decide_actions(user_request, elements):

    print("\n===== DECIDING ACTIONS =====")

    request = user_request.lower()

    actions = []


    # Understand size request

    if "size 45" in request:

        actions.append({
            "action": "SELECT",
            "target": "#size",
            "value": "45"
        })


    # Understand add-to-cart request

    if "add" in request and "cart" in request:

        actions.append({
            "action": "CLICK",
            "target": "#add-to-cart"
        })


    return actions


# ==========================================
# ACT
# ==========================================

def execute_action(page, action):

    action_type = action["action"]


    if action_type == "SELECT":

        target = action["target"]

        value = action["value"]

        print("\nExecuting SELECT...")

        dropdown = page.locator(target)

        dropdown.select_option(label=value)

        print(f"Selected size {value}.")


    elif action_type == "CLICK":

        target = action["target"]

        print("\nExecuting CLICK...")

        button = page.locator(target)

        button.click()

        print("Button clicked.")


# ==========================================
# VERIFY
# ==========================================

def verify_action(page, action):

    action_type = action["action"]


    if action_type == "SELECT":

        target = action["target"]

        expected = action["value"]

        dropdown = page.locator(target)

        selected = dropdown.locator(
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


    elif action_type == "CLICK":

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


    # OPEN WEBSITE

    page.goto(
        "file:///C:/Users/LENOVO/Desktop/AI-Web-agent/test_shop.html"
    )


    print("Website opened successfully.")


    # USER REQUEST

    user_request = (
        "Select size 45 and add the product to the cart"
    )


    print("\nUSER REQUEST:")

    print(user_request)


    # ==========================================
    # AGENT LOOP
    # ==========================================

    print("\n===== AGENT STARTED =====")


    # OBSERVE

    elements = observe_page(page)


    # DECIDE

    actions = decide_actions(
        user_request,
        elements
    )


    print("\nActions decided:")

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