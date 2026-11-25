from playwright.sync_api import sync_playwright


def inspect_page(page):
    elements = []

    # Get links
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

    # Get buttons
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
    Later, an actual AI model will perform this job.
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

    # Perceive the webpage
    elements = inspect_page(page)

    print("\nWEBPAGE ELEMENTS:")

    for element in elements:
        print(f"- {element['type']}: {element['name']}")

    # Simulated user request
    user_request = "Click HTML"

    print("\nUSER REQUEST:")
    print(user_request)

    # AI decision
    decision = decide_action(user_request, elements)

    print("\nAI DECISION:")
    print(decision)

    browser.close()