from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        executable_path=r"C:\Users\LENOVO\AppData\Local\Google\Chrome\Application\chrome.exe"
    )

    page = browser.new_page()

    # Open a safe test website
    page.goto("https://www.w3schools.com/html/html_forms.asp")

    print("Page opened successfully.")

    # Find the first text input
    textbox = page.locator("input[type='text']").first

    # Type into the textbox
    textbox.fill("Black shoe")

    print("Text entered successfully.")

    # Find the submit button
    button = page.locator("input[type='submit']").first

    # Click the button
    button.click()

    print("Button clicked successfully.")

    # Give the page a moment to update
    page.wait_for_timeout(2000)

    print("\nPage title:")
    print(page.title())

    browser.close()