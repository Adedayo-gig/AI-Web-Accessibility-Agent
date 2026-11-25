from playwright.sync_api import sync_playwright


def execute_action(page, action):

    action_type = action["action"]

    # SELECT
    if action_type == "SELECT":

        target = action["target"]
        value = action["value"]

        print("\nExecuting SELECT action...")
        print(f"Selecting size: {value}")

        dropdown = page.locator(target).first

        dropdown.select_option(label=value)

        print("Size selected successfully.")

        # VERIFY
        selected_value = dropdown.locator(
            "option:checked"
        ).inner_text()

        if selected_value == value:
            print("VERIFICATION: SELECT action successful.")
            return True

        else:
            print("VERIFICATION: SELECT action failed.")
            return False


    # CLICK
    elif action_type == "CLICK":

        target = action["target"]

        print("\nExecuting CLICK action...")
        print(f"Target: {target}")

        button = page.locator(target).first

        button.click()

        print("Add to Cart button clicked.")

        return True


    else:

        print("\nUnknown action:", action_type)

        return False


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

    print("Shop opened successfully.")


    # USER REQUEST

    user_request = "Select size 45 and add the product to the cart"

    print("\nUSER REQUEST:")
    print(user_request)


    # AI DECISION
    # Simulated for now

    actions = [

        {
            "action": "SELECT",
            "target": "#size",
            "value": "45"
        },

        {
            "action": "CLICK",
            "target": "#add-to-cart"
        }

    ]


    print("\nAI DECIDED ACTIONS:")

    for action in actions:
        print(action)


    # EXECUTE ACTIONS

    for action in actions:

        success = execute_action(
            page,
            action
        )

        if not success:

            print("\nACTION FAILED.")

            break


    # VERIFY CART

    print("\nVERIFYING CART...")

    cart_status = page.locator(
        "#cart-status"
    ).inner_text()

    print("Cart status:")
    print(cart_status)


    page.wait_for_timeout(3000)

    browser.close()