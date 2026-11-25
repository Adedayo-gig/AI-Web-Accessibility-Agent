from playwright.sync_api import sync_playwright


def inspect_page(page):
    print("\n===== PAGE INFORMATION =====")

    print("\nPAGE TITLE:")
    print(page.title())

    print("\nHEADINGS:")
    for heading in page.get_by_role("heading").all():
        text = heading.inner_text().strip()

        if text:
            print(f"- {text}")

    print("\nTEXTBOXES:")
    for textbox in page.get_by_role("textbox").all():
        try:
            name = textbox.get_attribute("aria-label")
            placeholder = textbox.get_attribute("placeholder")

            print(f"- aria-label: {name}")
            print(f"  placeholder: {placeholder}")

        except Exception:
            print("- Textbox found")

    print("\nBUTTONS:")
    for button in page.get_by_role("button").all():
        try:
            print(f"- {button.inner_text().strip()}")
        except Exception:
            print("- Button found")

    print("\nLINKS:")
    for link in page.get_by_role("link").all()[:10]:
        try:
            print(f"- {link.inner_text().strip()}")
        except Exception:
            print("- Link found")


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

    inspect_page(page)

    page.wait_for_timeout(3000)

    browser.close()