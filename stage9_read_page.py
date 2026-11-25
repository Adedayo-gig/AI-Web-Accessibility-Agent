from playwright.sync_api import sync_playwright


def read_page(page):
    print("\n===== PAGE CONTENT =====")

    # Page title
    print("\nPAGE TITLE:")
    print(page.title())

    # Headings
    print("\nHEADINGS:")

    headings = page.get_by_role("heading").all()

    for heading in headings[:10]:
        try:
            text = heading.inner_text().strip()

            if text:
                print(f"- {text}")

        except Exception:
            pass

    # Links
    print("\nLINKS:")

    links = page.get_by_role("link").all()

    for link in links[:15]:
        try:
            text = link.inner_text().strip()

            if text:
                print(f"- {text}")

        except Exception:
            pass

    # Buttons
    print("\nBUTTONS:")

    buttons = page.get_by_role("button").all()

    for button in buttons[:10]:
        try:
            text = button.inner_text().strip()

            if text:
                print(f"- {text}")

        except Exception:
            pass

    # Main page text
    print("\nMAIN PAGE TEXT:")

    body_text = page.locator("body").inner_text()

    print(body_text[:3000])


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        executable_path=r"C:\Users\LENOVO\AppData\Local\Google\Chrome\Application\chrome.exe"
    )

    page = browser.new_page()

    page.goto(
    "https://example.com",
    wait_until="domcontentloaded",
    timeout=60000
)

    print("Website opened successfully.")

    # Read the webpage
    read_page(page)

    page.wait_for_timeout(3000)

    browser.close()