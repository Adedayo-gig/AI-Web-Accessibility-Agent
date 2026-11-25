
from playwright.sync_api import sync_playwright
from speech_output import speak


def main():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            executable_path=r"C:\Users\LENOVO\AppData\Local\Google\Chrome\Application\chrome.exe"
        )

        page = browser.new_page()

        page.goto(
            "file:///C:/Users/LENOVO/Desktop/AI-Web-agent/test_multiple_products.html"
        )

        page.wait_for_load_state("domcontentloaded")

        print("\nAI WEB ACCESSIBILITY AGENT")
        print("WEBPAGE ACCESSIBILITY REPORT")

        # Read webpage title
        title = page.title()

        print("\nWEBPAGE TITLE")
        print(title)

        # Identify headings
        headings = page.locator("h1, h2, h3").all_inner_texts()

        print("\nWEBPAGE HEADINGS")

        for heading in headings:
            print("-", heading)

        # Identify links
        links = page.locator("a")

        print("\nWEBPAGE LINKS")

        if links.count() > 0:

            for i in range(links.count()):

                link_text = links.nth(i).inner_text().strip()

                if link_text:
                    print("-", link_text)

        else:
            print("No links found.")

        # Identify buttons
        buttons = page.locator("button")

        print("\nWEBPAGE BUTTONS")

        if buttons.count() > 0:

            for i in range(buttons.count()):

                button_text = buttons.nth(i).inner_text().strip()

                print("-", button_text)

        else:
            print("No buttons found.")

        # Identify form fields
        fields = page.locator("input, select, textarea")

        print("\nFORM FIELDS")

        if fields.count() > 0:

            for i in range(fields.count()):

                field = fields.nth(i)

                field_type = field.get_attribute("type") or field.evaluate(
                    "(element) => element.tagName.toLowerCase()"
                )

                field_name = field.get_attribute("aria-label")

                if not field_name:

                    field_id = field.get_attribute("id")

                    if field_id:

                        label = page.locator(
                            f'label[for="{field_id}"]'
                        )

                        if label.count() > 0:
                            field_name = label.first.inner_text().strip()

                if not field_name:
                    field_name = "Unnamed field"

                print(f"- {field_name} ({field_type})")

        else:
            print("No form fields found.")

        # Read product information
        products = page.locator(".product")

        product_count = products.count()

        print(f"\nI found {product_count} products on this webpage.")

        descriptions = []

        for i in range(product_count):

            product = products.nth(i)

            name = product.locator("h2").inner_text()

            price = product.locator(".price").inner_text()

            size_options = product.locator(
                "select option"
            ).all_inner_texts()

            sizes = [
                size.strip()
                for size in size_options
                if size.strip() and "choose" not in size.lower()
            ]

            button = product.locator("button").inner_text()

            description = (
                f"Product: {name}. "
                f"Price: {price}. "
                f"Available sizes: {', '.join(sizes)}. "
                f"Action: {button}."
            )

            descriptions.append(description)

            print(description)

        # Prepare spoken accessibility report
        report = (
            f"The webpage title is {title}. "
            f"There are {len(headings)} headings. "
            f"There are {links.count()} links. "
            f"There are {buttons.count()} buttons. "
            f"There are {fields.count()} form fields. "
            + " ".join(descriptions)
        )

        print("\nAGENT: Reading the webpage accessibility report.")

        speak(report)

        input("\nPress Enter to close the browser...")

        browser.close()


if __name__ == "__main__":
    main()
