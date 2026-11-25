from playwright.sync_api import sync_playwright


# ==========================================
# CHECK WHETHER ACTION NEEDS CONFIRMATION
# ==========================================

def requires_confirmation(action):

    high_risk_actions = [
        "CHECKOUT",
        "PLACE_ORDER",
        "PAYMENT"
    ]

    return action["action"] in high_risk_actions


# ==========================================
# EXECUTE ACTION
# ==========================================

def execute_action(page, action):

    action_type = action["action"]


    # SAFE ACTION

    if action_type == "SELECT":

        value = action["value"]

        print("\nExecuting SELECT...")

        page.locator(
            action["target"]
        ).select_option(
            label=value
        )

        print(
            f"Selected size {value}."
        )


    elif action_type == "CLICK":

        print("\nExecuting CLICK...")

        page.locator(
            action["target"]
        ).click()

        print("Button clicked.")


    # HIGH-RISK ACTION

    elif action_type == "PLACE_ORDER":

        print(
            "\nPLACE ORDER action requested."
        )

        print(
            "This action requires user confirmation."
        )

        confirmation = input(
            "Do you want to place the order? (yes/no): "
        )


        if confirmation.lower() == "yes":

            print(
                "User confirmed the order."
            )

            print(
                "Order would now be placed."
            )

        else:

            print(
                "User did not confirm."
            )

            print(
                "Order cancelled."
            )


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
        "file:///C:/Users/LENOVO/Desktop/AI-Web-agent/test_shop.html"
    )


    print(
        "Shop opened successfully."
    )


    # USER REQUEST

    user_request = (
        "Place the order for the black running shoe"
    )


    print("\nUSER REQUEST:")

    print(user_request)


    # AI DECISION
    # Simulated for now

    action = {

        "action": "PLACE_ORDER"

    }


    print("\nAI DECISION:")

    print(action)


    # CHECK SAFETY

    if requires_confirmation(action):

        print(
            "\n⚠️ CONFIRMATION REQUIRED"
        )

        print(
            "The requested action can have consequences."
        )


    # EXECUTE

    execute_action(
        page,
        action
    )


    page.wait_for_timeout(3000)


    browser.close()