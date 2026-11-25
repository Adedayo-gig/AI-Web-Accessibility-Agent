
import re
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

        # Collect product information
        products = page.locator(".product")
        product_data = []

        for i in range(products.count()):

            product = products.nth(i)

            name = product.locator("h2").inner_text()
            price_text = product.locator(".price").inner_text()

            price = int(
                "".join(filter(str.isdigit, price_text))
            )

            sizes = product.locator(
                "select option"
            ).all_inner_texts()

            sizes = [
                size.strip()
                for size in sizes
                if size.strip()
                and "choose" not in size.lower()
            ]

            product_data.append({
                "name": name,
                "price": price,
                "sizes": sizes
            })

        print("\nAI WEB ACCESSIBILITY AGENT")
        print("INTERACTIVE WEBPAGE QUESTION AND ANSWER")

        welcome = (
            "Welcome. You can ask me questions about "
            "the products on this webpage."
        )

        print("AGENT:", welcome)
        speak(welcome)

        print("\nExamples of questions:")
        print("- How many products are available?")
        print("- What is the cheapest shoe?")
        print("- Show me black shoes.")
        print("- What sizes are available for white shoes?")
        print("- Find a black shoe size 45 below 15000.")
        print("- List all products.")
        print("\nType exit to stop.\n")

        while True:

            question = input("Your question: ").strip().lower()

            if question == "exit":

                answer = (
                    "Goodbye. Thank you for using "
                    "the accessibility agent."
                )

                print("AGENT:", answer)
                speak(answer)
                break

            answer = ""

            # Count products
            if (
                "how many" in question
                or "number of products" in question
            ):

                answer = (
                    f"There are {len(product_data)} "
                    "products on this webpage."
                )

            # List all products
            elif (
                "list all" in question
                or "show all products" in question
                or "what products" in question
            ):

                answer = "The products available are: "

                answer += ". ".join(
                    f"{item['name']}, "
                    f"priced at {item['price']:,} naira"
                    for item in product_data
                )

            # Find cheapest product
            elif any(word in question for word in [
                "cheapest",
                "lowest price",
                "lowest cost"
            ]):

                cheapest = min(
                    product_data,
                    key=lambda item: item["price"]
                )

                answer = (
                    f"The cheapest product is "
                    f"{cheapest['name']}, "
                    f"priced at {cheapest['price']:,} naira."
                )

            # Product search
            elif any(word in question for word in [
                "shoe", "shoes", "footwear",
                "sneaker", "sneakers",
                "black", "white"
            ]):

                matches = product_data.copy()

                # Identify colour
                colour = None

                if "black" in question:
                    colour = "black"

                elif "white" in question:
                    colour = "white"

                if colour:

                    matches = [
                        item for item in matches
                        if colour in item["name"].lower()
                    ]

                # Identify requested size
                size_match = re.search(
                    r"\bsize\s*(\d{2})\b|\b(\d{2})\s*size\b",
                    question
                )

                requested_size = None

                if size_match:

                    requested_size = (
                        size_match.group(1)
                        or size_match.group(2)
                    )

                    matches = [
                        item for item in matches
                        if requested_size in item["sizes"]
                    ]

                # Identify maximum price
                price_match = re.search(
                    r"(?:below|under|less than|up to|"
                    r"not more than|max(?:imum)?(?: price)?)"
                    r"\s*₦?\s*([\d,]+)",
                    question
                )

                maximum_price = None

                if price_match:

                    maximum_price = int(
                        price_match.group(1).replace(",", "")
                    )

                    matches = [
                        item for item in matches
                        if item["price"] <= maximum_price
                    ]

                # Prepare answer
                if matches:

                    answer = "I found the following matching products: "

                    for item in matches:

                        answer += (
                            f"{item['name']}, "
                            f"priced at {item['price']:,} naira. "
                        )

                        if requested_size:

                            answer += (
                                f"Size {requested_size} "
                                f"is available. "
                            )

                        elif (
                            "size" in question
                            or "sizes" in question
                        ):

                            answer += (
                                "Available sizes are "
                                + ", ".join(item["sizes"])
                                + ". "
                            )

                else:

                    answer = (
                        "Sorry, I could not find a product "
                        "matching all your requested conditions."
                    )

            else:

                answer = (
                    "Sorry, I do not understand that question yet. "
                    "You can ask about products, prices, colours, "
                    "sizes or the cheapest product."
                )

            # Display and speak the answer
            print("\nAGENT:", answer)
            speak(answer)

        browser.close()


if __name__ == "__main__":
    main()




