from playwright.sync_api import sync_playwright


# ==========================================
# UNDERSTAND USER CONFIRMATION
# ==========================================

def understand_confirmation(response):

    response = response.lower().strip()

    yes_responses = [
        "yes",
        "yes go ahead",
        "go ahead",
        "do it",
        "proceed",
        "confirm",
        "okay",
        "ok"
    ]

    no_responses = [
        "no",
        "cancel",
        "stop",
        "don't do it",
        "do not do it",
        "not now"
    ]

    if response in yes_responses:
        return "YES"

    elif response in no_responses:
        return "NO"

    else:
        return "UNKNOWN"


# ==========================================
# CHECK HIGH-RISK ACTION
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

    if action_type == "PLACE_ORDER":

        print("\nPLACE ORDER action requested.")

        print(
            "This action requires user confirmation."
        )

        response = input(
            "Do you want to place the order? (yes/no): "
        )

        decision = understand_confirmation(response)

        if decision == "YES":

            print(
                "\nUser confirmed the order."
            )

            print(
                "Order would now be placed."
            )

        elif decision == "NO":

            print(
                "\nUser cancelled the order."
            )

            print(
                "Order was NOT placed."
            )

        else:

            print(
                "\nI did not understand your response."
            )

            print(
                "The order was NOT placed."
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

    user_request = (
        "Place the order for the black running shoe"
    )

    print("\nUSER REQUEST:")
    print(user_request)

    # Simulated AI decision
    action = {
        "action": "PLACE_ORDER"
    }

    print("\nAI DECISION:")
    print(action)

    if requires_confirmation(action):

        print(
            "\n⚠️ CONFIRMATION REQUIRED"
        )

    execute_action(
        page,
        action
    )

    page.wait_for_timeout(3000)

    browser.close()