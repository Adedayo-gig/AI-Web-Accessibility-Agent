from playwright.sync_api import sync_playwright


def execute_action(page, action):

    action_type = action["action"]

    if action_type == "SELECT":

        target = action["target"]
        value = action["value"]

        print("\nExecuting SELECT action...")
        print(f"Selecting: {value}")

        dropdown = page.locator(target).first

        dropdown.select_option(label=value)

        print("Option selected successfully.")

        # VERIFY
        selected_value = dropdown.locator("option:checked").inner_text()

        if selected_value == value:
            print("VERIFICATION: SELECT action successful.")
            return True
        else:
            print("VERIFICATION: SELECT action failed.")
            return False

    else:

        print("\nUnknown action:", action_type)

        return False


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        executable_path=r"C:\Users\LENOVO\AppData\Local\Google\Chrome\Application\chrome.exe"
    )

    page = browser.new_page()

    page.goto(
    "file:///C:/Users/LENOVO/Desktop/AI-Web-agent/test_dropdown.html"
    )
    print("Website opened successfully.")


    # USER REQUEST

    user_request = "Select the option United Kingdom"

    print("\nUSER REQUEST:")
    print(user_request)


    # AI DECISION
    # Simulated for now

    action = {
        "action": "SELECT",
        "target": "#country",
        "value": "United Kingdom"
    }


    print("\nAI DECISION:")
    print(action)


    # EXECUTE + VERIFY

    success = execute_action(
        page,
        action
    )


    print("\nFINAL RESULT:")

    if success:
        print("Action completed and verified successfully.")
    else:
        print("Action failed verification.")


    page.wait_for_timeout(3000)

    browser.close()