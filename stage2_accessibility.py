from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,
        executable_path=r"C:\Users\LENOVO\AppData\Local\Google\Chrome\Application\chrome.exe"
    )

    page = browser.new_page()

    page.goto("https://www.w3.org/WAI/ARIA/apg/patterns/")

    print("\nPAGE TITLE:")
    print(page.title())

    print("\nHEADINGS:")
    for heading in page.get_by_role("heading").all():
        print("-", heading.inner_text())

    print("\nLINKS:")
    for link in page.get_by_role("link").all()[:10]:
        print("-", link.inner_text())

    browser.close()