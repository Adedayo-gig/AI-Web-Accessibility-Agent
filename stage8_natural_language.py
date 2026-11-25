from playwright.sync_api import sync_playwright


def inspect_page(page):
    elements = []

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

    return elements


def decide_action(user_request, elements):
    """
    Local rule-based decision-maker.
    This is a temporary replacement for a real AI model.
    """

    request = user_request.lower()

    # Remove common command words
    command_words = [
        "click",
        "open",
        "go to",
        "visit",
        "select",
        "the",
        "link",
        "page"
    ]

    cleaned_request = request

    for word in command_words:
        cleaned_request = cleaned_request.replace(word, " ")

    cleaned_request = cleaned_request.strip()

    # Look for a webpage element matching the request
    for element in elements:

        name = element["name"]
        name_lower = name.lower()

        if name_lower == cleaned_request:
            return {
                "action": "CLICK",
                "target": name
            }

    # Try partial matching
    for element in elements:

        name = element["name"]
        name_lower = name.lower()

        if cleaned_request in name_lower:
            return {
                "action": "CLICK",
                "target": name
            }

    return {
        "action": "NONE",
        "reason": "I could not find the requested webpage element."
    }


def execute_action(page, action):

    if action["action"] == "CLICK":

        target = action["target"]

        print(f"\nExecuting CLICK action on: {target}")

        link = page.get_by_role(
            "link",
            name=target
        ).first

        if link.count() > 0:

            link.click()

            print(
                f"Successfully clicked: {target}"
            )

        else:

            print(
                f"Could not find: {target}"
            )

    else:

        print("\nNo action executed.")


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

    # 1. PERCEIVE
    elements = inspect_page(page)

    print(
        f"\nFound {len(elements)} links."
    )

    # 2. USER REQUEST
    user_request = "Open the HTML tutorial"

    print("\nUSER REQUEST:")
    print(user_request)

    # 3. DECIDE
    decision = decide_action(
        user_request,
        elements
    )

    print("\nDECISION:")
    print(decision)

    # 4. ACT
    execute_action(
        page,
        decision
    )

    page.wait_for_timeout(3000)

    print("\nCURRENT PAGE:")
    print(page.url)

    browser.close()