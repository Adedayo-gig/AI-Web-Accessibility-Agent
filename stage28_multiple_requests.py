
import re
from playwright.sync_api import sync_playwright
from speech_output import speak


def understand_request(request):
    request = request.lower()

    requirements = {
        "colour": None,
        "size": None,
        "max_price": None,
        "add_to_cart": False
    }

    if "black" in request:
        requirements["colour"] = "black"
    elif "white" in request:
        requirements["colour"] = "white"

    size_match = re.search(
        r"size\s*(\d+)",
        request
    )

    if size_match:
        requirements["size"] = size_match.group(1)

    price_match = re.search(
        r"(?:below|under|less than)\s*₦?\s*(\d+(?:,\d{3})*|\d+)\s*(thousand|k)?",
        request
    )

    if price_match:
        amount = int(price_match.group(1).replace(",", ""))

        if price_match.group(2) in ("thousand", "k"):
            amount *= 1000

        requirements["max_price"] = amount

    if any(phrase in request for phrase in [
        "add to cart",
        "in my cart",
        "put it in my cart"
    ]):
        requirements["add_to_cart"] = True

    return requirements


def main():
    request = input("What would you like me to do? ")

    requirements = understand_request(request)

    print("\nUNDERSTOOD:")
    print(requirements)

    speak("I have understood your request.")

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
            executable_path=(
                r"C:\Users\LENOVO\AppData\Local\Google\Chrome"
                r"\Application\chrome.exe"
            )
        )

        page = browser.new_page()

        page.goto(
            "file:///" +
            r"C:\Users\LENOVO\Desktop\AI-Web-agent\test_multiple_products.html"
        )

        products = page.locator(".product")
        matching_product = None

        for index in range(products.count()):
            product = products.nth(index)

            name = product.locator("h2").inner_text()
            price_text = product.locator(".price").inner_text()
            price_match = re.search(r"[\d,]+", price_text)

            if not price_match:
                continue

            price = int(price_match.group().replace(",", ""))
            product_text = product.inner_text().lower()

            if requirements["colour"]:
                if requirements["colour"] not in product_text:
                    continue

            if requirements["max_price"] is not None:
                if price >= requirements["max_price"]:
                    continue

            size_options = product.locator("select option").all_text_contents()
            available_sizes = [
                re.search(r"\d+", option).group()
                for option in size_options
                if re.search(r"\d+", option)
            ]

            if requirements["size"]:
                if requirements["size"] not in available_sizes:
                    continue

            matching_product = {
                "index": index,
                "name": name,
                "price": price,
                "sizes": available_sizes
            }
            break

        if matching_product is None:
            message = "Sorry, I could not find a matching product."
            print("\n" + message)
            speak(message)

        else:
            print("\nMATCHING PRODUCT:")
            print(matching_product)

            product_element = products.nth(
                matching_product["index"]
            )

            if requirements["size"]:
                product_element.locator("select").select_option(
                    requirements["size"]
                )

                message = (
                    f"Size {requirements['size']} selected."
                )
                print(message)
                speak(message)

            if requirements["add_to_cart"]:
                product_element.locator(".add-cart").click()

                print("Add to Cart clicked.")

                cart_status = page.locator(
                    "#cart-status"
                ).inner_text()

                print("\nVERIFICATION:")
                print(cart_status)

                speak(cart_status)

        input("\nPress Enter to close the browser...")
        page.close()
        browser.close()


if __name__ == "__main__":
    main()
