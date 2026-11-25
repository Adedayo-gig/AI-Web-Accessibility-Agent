from playwright.sync_api import sync_playwright


def inspect_page(page):
    elements = []

    # Find links
    for link in page.get_by_role("link").all():
        try:
            name = link.inner_text().strip()

            if name:
                elements.append({
                    "type": "LINK",
                    "name": name
                })
        except Exception:
            pass

    # Find buttons
    for button in page.get_by_role("button").all():
        try:
            name = button.inner_text().strip()

            if name:
                elements.append({
                    "type": "BUTTON",
                    "name": name
                })
        except Exception:
            pass

    return elements


def decide_action(user_request, elements):
    """
    Simulated AI decision-maker.
    Later, this will be replaced by a real AI model.
    """

    request = user_request.lower()

    for element in elements:
        name = element["name"]

        if name.lower() in request:
            return {
                "action": "CLICK",
                "target": name
            }

    return {
        "action": "NONE",
        "reason": "No matching webpage element found."
    }


def execute_action(page, action):
    """
    Executes the action selected by the decision-maker.
    """

    if action["action"] == "CLICK":

        target = action["target"]

        print(f"\nExecuting CLICK action on: {target}")

        link = page.get_by_role("link", name=target).first

        if link.count() > 0:
            link.click()
            print(f"Successfully clicked: {target}")
        else:
            print(f"Could not find link: {target}")

    else:
        print("\nNo action was executed.")


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

    # STEP 1: Perceive the webpage
    elements = inspect_page(page)

    print(f"\nFound {len(elements)} webpage elements.")

    # STEP 2: Receive user request
    user_request = "Click HTML"

    print("\nUSER REQUEST:")
    print(user_request)

    # STEP 3: Decide what action to take
    decision = decide_action(user_request, elements)

    print("\nAI DECISION:")
    print(decision)

    # STEP 4: Execute the decision
    execute_action(page, decision)

    # Give the browser time to show the result
    page.wait_for_timeout(3000)

    print("\nCurrent page:")
    print(page.url)

    browser.close()