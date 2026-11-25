from playwright.sync_api import sync_playwright


def inspect_page(page):
    elements = []

    # Find textboxes
    for textbox in page.get_by_role("textbox").all():
        try:
            name = textbox.get_attribute("name")
            placeholder = textbox.get_attribute("placeholder")
            aria_label = textbox.get_attribute("aria-label")

            elements.append({
                "type": "TEXTBOX",
                "name": name,
                "placeholder": placeholder,
                "aria_label": aria_label
            })

        except Exception:
            pass

    return elements


def decide_action(user_request, elements):
    """
    Local decision-maker for TYPE actions.
    """

    request = user_request.lower()

    # Example:
    # "Type black shoe in the search box"

    if "type" in request or "enter" in request:

        value = ""

        # Extract the text between quotation marks if present
        if '"' in user_request:

            parts = user_request.split('"')

            if len(parts) >= 3:
                value = parts[1]

        # If quotation marks were not used,
        # use a simple test value.
        if not value:
            value = "Black shoe"

        return {
            "action": "TYPE",
            "target": "input[type='text']",
            "value": value
        }

    return {
        "action": "NONE",
        "reason": "No matching action found."
    }


def execute_action(page, action):

    if action["action"] == "TYPE":

        target = action["target"]
        value = action["value"]

        print(
            f"\nExecuting TYPE action..."
        )

        print(
            f"Value: {value}"
        )

        textbox = page.locator(target).first

        textbox.fill(value)

        print(
            "Text entered successfully."
        )

    else:

        print("\nNo action executed.")


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        executable_path=r"C:\Users\LENOVO\AppData\Local\Google\Chrome\Application\chrome.exe"
    )

    page = browser.new_page()

    # Safe test page
    page.goto(
        "https://www.w3schools.com/html/html_forms.asp",
        wait_until="domcontentloaded",
        timeout=60000
    )

    print("Website opened successfully.")

    # PERCEIVE
    elements = inspect_page(page)

    print(
        f"\nFound {len(elements)} textboxes."
    )

    # USER REQUEST
    user_request = 'Type "Black shoe" in the search box'

    print("\nUSER REQUEST:")
    print(user_request)

    # DECIDE
    decision = decide_action(
        user_request,
        elements
    )

    print("\nAI DECISION:")
    print(decision)

    # ACT
    execute_action(
        page,
        decision
    )

    page.wait_for_timeout(3000)

    browser.close