from playwright.sync_api import sync_playwright


def execute_action(page, action):

    action_type = action["action"]

    if action_type == "TYPE":

        target = action["target"]
        value = action["value"]

        print(f"\nExecuting TYPE action...")
        print(f"Value: {value}")

        textbox = page.locator(target).first

        textbox.fill(value)

        print("Text entered successfully.")


    elif action_type == "CLICK":

        target = action["target"]

        print("\nExecuting CLICK action...")
        print(f"Target: {target}")

        button = page.locator(target).first

        button.click()

        print("Button clicked successfully.")


    elif action_type == "READ_PAGE":

        print("\n===== READING PAGE =====")

        print("\nPAGE TITLE:")
        print(page.title())

        print("\nPAGE CONTENT:")

        text = page.locator("body").inner_text()

        print(text[:3000])


    else:

        print("\nUnknown action:", action_type)


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

    user_request = "Type Black shoe and then click the submit button"

    print("\nUSER REQUEST:")
    print(user_request)


    # AI DECISION
    # For now, we are simulating the AI's decision.

    actions = [

        {
            "action": "TYPE",
            "target": "input[type='text']",
            "value": "Black shoe"
        },

        {
            "action": "CLICK",
            "target": "input[type='submit']"
        },

        {
            "action": "READ_PAGE"
        }

    ]


    print("\nAI DECIDED ACTIONS:")

    for action in actions:

        print(action)


    # EXECUTE ACTIONS

    for action in actions:

        execute_action(
            page,
            action
        )


    page.wait_for_timeout(3000)

    print("\nFINAL PAGE URL:")
    print(page.url)


    browser.close()