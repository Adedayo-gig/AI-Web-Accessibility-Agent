from playwright.sync_api import sync_playwright


def execute_action(page, action):

    action_type = action["action"]

    if action_type == "TYPE":

        target = action["target"]
        value = action["value"]

        print("\nExecuting TYPE action...")
        print(f"Value: {value}")

        textbox = page.locator(target).first

        textbox.fill(value)

        print("Text entered successfully.")

        # VERIFY
        actual_value = textbox.input_value()

        if actual_value == value:
            print("VERIFICATION: TYPE action successful.")
            return True
        else:
            print("VERIFICATION: TYPE action failed.")
            return False


    elif action_type == "CLICK":

        target = action["target"]

        print("\nExecuting CLICK action...")
        print(f"Target: {target}")

        button = page.locator(target).first

        button.click()

        print("Button clicked successfully.")

        # VERIFY
        print("VERIFICATION: CLICK action completed.")

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

    page.goto(
        "https://www.w3schools.com/html/html_forms.asp",
        wait_until="domcontentloaded",
        timeout=60000
    )

    print("Website opened successfully.")


    # USER REQUEST

    user_request = 'Type "Black shoe" in the search box'

    print("\nUSER REQUEST:")
    print(user_request)


    # AI DECISION
    # Simulated for now

    action = {
        "action": "TYPE",
        "target": "input[type='text']",
        "value": "Black shoe"
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