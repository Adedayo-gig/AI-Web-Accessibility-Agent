from playwright.sync_api import sync_playwright


def understand_product(page):

    print("\n===== UNDERSTANDING PRODUCT =====")

    product_name = page.locator("h2").inner_text()

    price = page.locator("p").first.inner_text()

    sizes = []

    options = page.locator("#size option").all()

    for option in options:

        size = option.inner_text().strip()

        if size != "Choose size":
            sizes.append(size)

    print(f"Product: {product_name}")
    print(f"Price: {price}")
    print(f"Available sizes: {sizes}")

    return {
        "name": product_name,
        "price": price,
        "sizes": sizes
    }


with sync_playwright() as p:

    browser = p.chromium.launch(
        headless=False,
        executable_path=r"C:\Users\LENOVO\AppData\Local\Google\Chrome\Application\chrome.exe"
    )

    page = browser.new_page()

    page.goto(
        "file:///C:/Users/LENOVO/Desktop/AI-Web-agent/test_shop.html"
    )

    print("Shop opened successfully.")

    product = understand_product(page)

    print("\n===== PRODUCT INFORMATION =====")

    print(product)

    page.wait_for_timeout(3000)

    browser.close()