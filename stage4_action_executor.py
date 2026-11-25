from playwright.sync_api import sync_playwright


def execute_action(page, action):
    action_type = action["action"]
    target = action.get("target")
    value = action.get("value")

    if action_type == "TYPE":
        textbox = page.locator(target).first
        textbox.fill(value)
        print(f"Typed '{value}' successfully.")

    elif action_type == "CLICK":
        button = page.locator(target).first
        button.click()
        print("Clicked successfully.")

    else:
        print(f"Unknown action: {action_type}")


with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        executable_path=r"C:\Users\LENOVO\AppData\Local\Google\Chrome\Application\chrome.exe"
    )

    page = browser.new_page()

    # Open test website
    page.goto("https://www.w3schools.com/html/html_forms.asp")

    print("Page opened successfully.")

    # This represents what an AI model could produce later
    actions = [
        {
            "action": "TYPE",
            "target": "input[type='text']",
            "value": "Black shoe"
        },
        {
            "action": "CLICK",
            "target": "input[type='submit']"
        }
    ]

    # Execute each action
    for action in actions:
        print("\nExecuting action:")
        print(action)

        execute_action(page, action)

    page.wait_for_timeout(2000)

    print("\nPage title:")
    print(page.title())

    browser.close()