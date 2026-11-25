from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        executable_path=r"C:\Users\LENOVO\AppData\Local\Google\Chrome\Application\chrome.exe"
    )

    page = browser.new_page()

    page.goto("https://example.com")

    print("Page title:", page.title())
    print("Page text:")
    print(page.locator("body").inner_text())

    browser.close()