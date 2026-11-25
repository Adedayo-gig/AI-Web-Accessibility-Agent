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

    # Find headings
    for heading in page.get_by_role("heading").all():
        try:
            name = heading.inner_text().strip()

            if name:
                elements.append({
                    "type": "HEADING",
                    "name": name
                })

        except Exception:
            pass

    return elements


def decide_action(user_request, elements):
    """
    Local decision-maker.
    """

    request = user_request.lower().strip()

    # Understand requests to read the page
    if (
        "read this page" in request
        or "read the page" in request
        or "what is on this page" in request
        or "describe this page" in request
    ):
        return {
            "action": "READ_PAGE"
        }

    # Understand simple click requests
    command_words = [
        "click",
        "open",
        "go to",
        "visit",
        "the",
        "link",
        "page"
    ]

    cleaned_request = request

    for word in command_words:
        cleaned_request = cleaned_request.replace(word, " ")

    cleaned_request = cleaned_request.strip()

    for element in elements:

        name = element["name"]

        if name.lower() == cleaned_request:
            return {
                "action": "CLICK",
                "target": name
            }

    for element in elements:

        name = element["name"]

        if cleaned_request in name.lower():
            return {
                "action": "CLICK",
                "target": name
            }

    return {
        "action": "NONE",
        "reason": "No matching action found."
    }


def execute_action(page, action):

    # READ PAGE
    if action["action"] == "READ_PAGE":

        print("\n===== READING PAGE =====")

        print("\nPAGE TITLE:")
        print(page.title())

        print("\nPAGE CONTENT:")

        text = page.locator("body").inner_text()

        print(text[:3000])

    # CLICK
    elif action["action"] == "CLICK":

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

    # Use the reliable test website
    page.goto(
        "https://example.com",
        wait_until="domcontentloaded",
        timeout=60000
    )

    print("Website opened successfully.")

    # PERCEIVE
    elements = inspect_page(page)

    print(
        f"\nFound {len(elements)} webpage elements."
    )

    # USER REQUEST
    user_request = "Read this page"

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

    browser.close()