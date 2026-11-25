
import re
from pathlib import Path
from playwright.sync_api import sync_playwright
from speech_output import speak


def understand_request(request):
    """Extract product details from different ways of speaking."""

    request = request.lower()

    # Identify colour
    colour = None

    if re.search(r"\bblack\b", request):
        colour = "black"
    elif re.search(r"\bwhite\b", request):
        colour = "white"

    # Identify size: size 45, size: 45, or 45 size
    size_match = re.search(
        r"\b(?:size\s*[:#-]?\s*(\d{2})|(\d{2})\s*size)\b",
        request
    )

    requested_size = None

    if size_match:
        requested_size = size_match.group(1) or size_match.group(2)

    # Identify maximum price
    price_match = re.search(
        r"(?:below|under|less than|up to|not more than|"
        r"maximum(?: price)?(?: of)?|max(?:imum)?(?: price)?(?: of)?|"
        r"within)\s*₦?\s*([\d,]+)",
        request
    )

    maximum_price = None

    if price_match:
        maximum_price = int(
            price_match.group(1).replace(",", "")
        )

    # Identify product type
    product_type = None

    if re.search(
        r"\b(shoe|shoes|footwear|sneaker|sneakers|trainer|trainers)\b",
        request
    ):
        product_type = "shoe"

    return colour, requested_size, maximum_price, product_type


def main():
    project_folder = Path(__file__).parent
    shop_url = (project_folder / "test_multiple_products.html").as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            executable_path=r"C:\Users\LENOVO\AppData\Local\Google\Chrome\Application\chrome.exe"
        )

        page = browser.new_page()
        page.goto(shop_url)
        page.wait_for_load_state("domcontentloaded")

        print("AI WEB ACCESSIBILITY AGENT - PRODUCT ACTION")
        speak("Welcome. I can help you find a product and add it to your cart.")

        request = input(
            "\nWhat product would you like me to find? "
        ).strip().lower()

        if request == "exit":
            browser.close()
            return

        # Understand the user's request
        colour, requested_size, maximum_price, product_type = (
            understand_request(request)
        )

        print("\nUNDERSTANDING YOUR REQUEST")
        print("Colour:", colour if colour else "Any colour")
        print("Size:", requested_size if requested_size else "Not specified")
        print(
            "Maximum price:",
            f"{maximum_price:,} naira" if maximum_price else "Not specified"
        )
        print("Product:", product_type if product_type else "Not specified")

        # Read products from webpage
        products = page.locator(".product")
        matches = []

        for i in range(products.count()):
            product = products.nth(i)

            name = product.locator("h2").inner_text()
            price_text = product.locator(".price").inner_text()

            price = int(
                "".join(filter(str.isdigit, price_text))
            )

            sizes = product.locator(".size option").evaluate_all(
                "(options) => options.map(option => option.value).filter(value => value)"
            )

            if colour and colour not in name.lower():
                continue

            if product_type and product_type != "shoe":
                continue

            if maximum_price is not None and price > maximum_price:
                continue

            if requested_size and requested_size not in sizes:
                continue

            matches.append({
                "index": i,
                "name": name,
                "price": price,
                "sizes": sizes
            })

        if not matches:
            print("\nAGENT: Sorry, I could not find a matching product.")
            speak("Sorry, I could not find a matching product.")
            browser.close()
            return

        # Handle multiple matching products
        if len(matches) > 1:
            print("\nI found multiple matching products:")

            for number, item in enumerate(matches, start=1):
                print(
                    f"{number}. {item['name']} - "
                    f"{item['price']:,} naira"
                )

            selection = input(
                "\nEnter the product number you want: "
            ).strip()

            if not selection.isdigit() or not (
                1 <= int(selection) <= len(matches)
            ):
                print("Invalid product selection.")
                browser.close()
                return

            selected = matches[int(selection) - 1]

        else:
            selected = matches[0]

        # Ask for size if not specified
        if not requested_size:
            print("Available sizes:", ", ".join(selected["sizes"]))

            requested_size = input(
                "Which size would you like? "
            ).strip()

        if requested_size not in selected["sizes"]:
            print("Sorry, that size is not available.")
            speak("Sorry, that size is not available.")
            browser.close()
            return

        # Display selected product
        print("\nPRODUCT FOUND")
        print("Product:", selected["name"])
        print("Price:", f"{selected['price']:,} naira")
        print("Size:", requested_size)

        speak(
            f"I found {selected['name']} "
            f"for {selected['price']:,} naira, "
            f"size {requested_size}."
        )

        # Ask for confirmation
        confirmation = input(
            "\nDo you want me to add this product to your cart? (yes/no): "
        ).strip().lower()

        if confirmation in ["yes", "y"]:
            product = products.nth(selected["index"])

            product.locator(".size").select_option(
                value=requested_size
            )

            product.locator(".add-cart").click()

            result = page.locator("#cart-status").inner_text()

            print("\nAGENT:", result)
            speak(result)

        else:
            print("AGENT: Product was not added to your cart.")
            speak("Product was not added to your cart.")

        input("\nPress Enter to close the browser...")
        browser.close()


if __name__ == "__main__":
    main()

