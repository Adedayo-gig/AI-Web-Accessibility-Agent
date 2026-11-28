
from flask import Flask, render_template_string, request, jsonify, session
import re

app = Flask(__name__)
app.secret_key = "ai-web-agent-demo-secret-key"

products = [
    {
        "name": "Black Running Shoe",
        "colour": "black",
        "price": 12000,
        "sizes": ["40", "41", "42", "43", "44", "45"],
        "description": "Comfortable black running shoe for everyday use."
    },
    {
        "name": "White Sports Shoe",
        "colour": "white",
        "price": 10000,
        "sizes": ["40", "41", "42", "43"],
        "description": "Lightweight white sports shoe."
    },
    {
        "name": "Black Leather Shoe",
        "colour": "black",
        "price": 20000,
        "sizes": ["42", "43", "44", "45"],
        "description": "Smart black leather shoe."
    }
]


def get_cart():
    return session.get("cart", [])


def cart_summary():
    cart = get_cart()

    if not cart:
        return "Your shopping cart is empty. Your total is zero naira."

    total = 0
    answer = "Your shopping cart contains: "

    for item in cart:
        subtotal = item["price"] * item["quantity"]
        total += subtotal
        size = f", size {item['size']}" if item.get("size") else ""

        answer += (
            f"{item['name']}{size}, quantity "
            f"{item['quantity']}, price {item['price']:,} naira. "
        )

    return answer + f"Your total is {total:,} naira."


def add_to_cart(product, size=None):
    if size and size not in product["sizes"]:
        return "That size is not available for this shoe."

    cart = get_cart()

    for item in cart:
        if item["name"] == product["name"] and item.get("size") == size:
            item["quantity"] += 1
            session["cart"] = cart
            session.modified = True

            return (
                f"Another {product['name']} has been added. "
                f"Quantity is now {item['quantity']}."
            )

    cart.append({
        "name": product["name"],
        "price": product["price"],
        "size": size,
        "quantity": 1
    })

    session["cart"] = cart
    session.modified = True

    size_text = f", size {size}" if size else ""

    return f"{product['name']}{size_text} has been added to your cart."


def remove_from_cart(product_name):
    cart = get_cart()

    for item in cart:
        if product_name.lower() in item["name"].lower():
            cart.remove(item)
            session["cart"] = cart
            session.modified = True

            return f"{item['name']} has been removed from your cart."

    return "I could not find that product in your cart."


def answer_question(question):
    question = question.lower().strip()

    corrections = {
        "sheo": "shoe",
        "shoo": "shoe",
        "shose": "shoes",
        "runnig": "running",
        "runing": "running",
        "lether": "leather",
        "blak": "black",
        "wite": "white"
    }

    for wrong, correct in corrections.items():
        question = re.sub(r"\b" + wrong + r"\b", correct, question)

    if not question:
        return "Please enter a request."

    # CLEAR THE SHOPPING CART
    clear_commands = [
        "clear cart",
        "clear my cart",
        "clear the cart",
        "clear my shopping cart",
        "empty cart",
        "empty my cart",
        "empty the cart",
        "empty my shopping cart",
        "delete my cart",
        "delete the cart",
        "clear shopping cart",
        "empty shopping cart"
    ]

    if any(command in question for command in clear_commands):
        session["cart"] = []
        session.modified = True
        return "Your shopping cart has been cleared. Your total is zero naira."

    # REMOVE A PRODUCT FROM THE CART
    if "remove" in question and "cart" in question:
        for product in products:
            if product["name"].lower() in question:
                return remove_from_cart(product["name"])

        return "Please mention the full product name you want to remove."

    # DISPLAY THE SHOPPING CART
    if "cart" in question and any(
        word in question.split()
        for word in ["show", "see", "view", "check", "display", "what", "list"]
    ):
        return cart_summary()

    # COUNT PRODUCTS
    if "how many" in question or "number of products" in question:
        return f"There are {len(products)} products available."

    # LIST ALL PRODUCTS
    if any(term in question for term in [
        "list all",
        "show all products",
        "what products"
    ]):
        return "Available products: " + "; ".join(
            f"{p['name']} for {p['price']:,} naira"
            for p in products
        )

    # FIND THE CHEAPEST PRODUCT
    if any(term in question for term in [
        "cheapest",
        "lowest price",
        "lowest cost"
    ]):
        cheapest = min(products, key=lambda p: p["price"])

        return (
            f"The cheapest shoe is {cheapest['name']}, "
            f"priced at {cheapest['price']:,} naira."
        )

    # PRODUCT SEARCH
    product_keywords = [
        "shoe", "shoes", "black", "white", "product",
        "products", "sneaker", "sneakers", "running",
        "leather", "sports"
    ]

    if any(word in question.split() for word in product_keywords):
        matches = products.copy()

        if "running" in question:
            matches = [
                p for p in matches
                if "Running" in p["name"]
            ]

        elif "leather" in question:
            matches = [
                p for p in matches
                if "Leather" in p["name"]
            ]

        elif "sports" in question:
            matches = [
                p for p in matches
                if "Sports" in p["name"]
            ]

        if "black" in question.split():
            matches = [
                p for p in matches
                if p["colour"] == "black"
            ]

        elif "white" in question.split():
            matches = [
                p for p in matches
                if p["colour"] == "white"
            ]

        size_match = re.search(
            r"\bsize\s*(\d{2})\b|\b(\d{2})\s*size\b",
            question
        )

        requested_size = None

        if size_match:
            requested_size = size_match.group(1) or size_match.group(2)

            matches = [
                p for p in matches
                if requested_size in p["sizes"]
            ]

        price_match = re.search(
            r"(?:below|under|less than|up to|not more than|max(?:imum)?(?: price)?)\s*₦?\s*([\d,]+)",
            question
        )

        if price_match:
            maximum = int(
                price_match.group(1).replace(",", "")
            )

            matches = [
                p for p in matches
                if p["price"] <= maximum
            ]

        add_requested = (
            ("add" in question and "cart" in question)
            or "buy it" in question
        )

        if not matches:
            return "Sorry, I could not find a shoe matching those conditions."

        if add_requested:
            if len(matches) > 1:
                return (
                    "I found multiple matching shoes: "
                    + ", ".join(p["name"] for p in matches)
                    + ". Please specify which one you want."
                )

            return add_to_cart(matches[0], requested_size)

        answer = "I found these matching shoes: "

        for product in matches:
            answer += (
                f"{product['name']}, priced at "
                f"{product['price']:,} naira. "
            )

            if requested_size:
                answer += f"Size {requested_size} is available. "

            elif "size" in question or "sizes" in question:
                answer += (
                    "Available sizes are "
                    + ", ".join(product["sizes"])
                    + ". "
                )

        return answer

    return (
        "I can help you find shoes, check prices and sizes, "
        "and manage your shopping cart."
    )


HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AI Shoe Store and Accessibility Agent</title>

<style>
* { box-sizing: border-box; }

body {
    margin: 0;
    padding: 20px;
    font-family: Arial, sans-serif;
    background: #f3f4f6;
    color: #222;
}

.container {
    max-width: 1050px;
    margin: 20px auto;
}

header, .panel {
    background: white;
    padding: 22px;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0 3px 12px rgba(0,0,0,.07);
}

h1, h2 { color: #173b67; }

header { text-align: center; }

.description {
    color: #555;
    line-height: 1.6;
}

.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 16px;
}

.product-card {
    background: white;
    padding: 18px;
    border-radius: 10px;
    border: 1px solid #ddd;
}

.product-icon {
    font-size: 65px;
    text-align: center;
    padding: 20px;
    background: #eef2f7;
    border-radius: 8px;
}

.price {
    font-weight: bold;
    color: #173b67;
    font-size: 19px;
}

select, input {
    padding: 12px;
    border: 1px solid #aaa;
    border-radius: 6px;
    font-size: 16px;
    width: 100%;
    margin: 7px 0;
}

button {
    padding: 12px 16px;
    background: #173b67;
    color: white;
    border: 0;
    border-radius: 6px;
    cursor: pointer;
    font-size: 15px;
}

button:hover { background: #24558c; }

button:focus-visible,
input:focus-visible,
select:focus-visible {
    outline: 3px solid #f0a500;
    outline-offset: 3px;
}

button:disabled {
    opacity: .6;
    cursor: wait;
}

#chat-box {
    height: 280px;
    overflow-y: auto;
    background: #fafafa;
    border: 1px solid #ddd;
    padding: 12px;
    border-radius: 8px;
}

.message {
    padding: 11px;
    margin: 9px 0;
    border-radius: 8px;
    line-height: 1.5;
    overflow-wrap: anywhere;
}

.agent {
    background: #e5edf8;
    color: #173b67;
}

.user {
    background: #dff3e4;
    color: #174d29;
    text-align: right;
}

.input-area {
    display: flex;
    gap: 8px;
    margin-top: 12px;
}

.input-area input {
    flex: 1;
    min-width: 0;
}

#cart-display { line-height: 1.7; }

.status {
    text-align: center;
    color: #555;
}

.visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0,0,0,0);
    white-space: nowrap;
    border: 0;
}

@media(max-width: 600px) {
    body { padding: 10px; }

    .input-area {
        flex-direction: column;
    }

    .input-area button {
        width: 100%;
    }
}
</style>
</head>

<body>
<main class="container">

<header>
    <h1>AI Shoe Store</h1>
    <p class="description">
        Browse shoes, choose your size and add products to your cart.
        You can also use the AI Web Accessibility Agent below.
    </p>
</header>

<section class="panel">
    <h2>Shop Shoes</h2>

    <div class="product-grid">
    {% for product in products %}
        <article class="product-card">
            <div class="product-icon" aria-hidden="true">👟</div>

            <h3>{{ product.name }}</h3>
            <p>{{ product.description }}</p>

            <p class="price">
                ₦{{ "{:,}".format(product.price) }}
            </p>

            <label for="size-{{ loop.index }}">
                Choose shoe size
            </label>

            <select id="size-{{ loop.index }}" class="size-choice">
                {% for size in product.sizes %}
                <option value="{{ size }}">Size {{ size }}</option>
                {% endfor %}
            </select>

            <button type="button"
                onclick="addProduct('{{ product.name }}', 'size-{{ loop.index }}')">
                Add to Cart
            </button>
        </article>
    {% endfor %}
    </div>
</section>

<section class="panel" aria-live="polite">
    <h2>My Shopping Cart</h2>

    <p id="cart-display">Loading cart...</p>

    <button type="button" id="refresh-cart">
        Refresh Cart
    </button>
</section>

<section class="panel">
    <h2>AI Web Accessibility Agent</h2>

    <p class="description">
        Ask the agent to find shoes, check prices, select sizes
        or manage your shopping cart.
    </p>

    <div id="chat-box"
         role="log"
         aria-label="Conversation"
         aria-live="polite"
         aria-relevant="additions">

        <div class="message agent">
            Agent: Hello! Welcome to the AI Shoe Store. How can I help you?
        </div>
    </div>

    <form id="chat-form" class="input-area">

        <label for="user-input" class="visually-hidden">
            Enter your request
        </label>

        <input id="user-input"
            type="text"
            placeholder="Example: Find a black shoe size 45 below 15000"
            autocomplete="off"
            required>

        <button type="button"
            id="mic-button"
            aria-label="Start voice input"
            aria-pressed="false">
            🎤 Speak
        </button>

        <button id="send-button" type="submit">
            Send
        </button>
    </form>

    <p id="speech-status" class="status" aria-live="polite">
        Speech is currently off.
    </p>

    <div style="text-align:center">
        <button type="button"
            id="speech-toggle"
            aria-pressed="false">
            Turn speech on
        </button>
    </div>
</section>

</main>

<script>
const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const sendButton = document.getElementById("send-button");
const micButton = document.getElementById("mic-button");
const speechToggle = document.getElementById("speech-toggle");
const speechStatus = document.getElementById("speech-status");
const cartDisplay = document.getElementById("cart-display");

let speechEnabled = false;
let recognition = null;
let isListening = false;


function speakText(message) {
    if (!speechEnabled || !("speechSynthesis" in window)) return;

    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(message);
    speech.lang = "en-NG";
    speech.rate = 0.9;

    window.speechSynthesis.speak(speech);
}


speechToggle.addEventListener("click", function() {
    speechEnabled = !speechEnabled;

    speechToggle.textContent = speechEnabled
        ? "Turn speech off"
        : "Turn speech on";

    speechToggle.setAttribute(
        "aria-pressed",
        String(speechEnabled)
    );

    if (speechEnabled) {
        speechStatus.textContent = "Speech is on.";
        speakText("Speech is now enabled.");
    } else {
        window.speechSynthesis.cancel();
        speechStatus.textContent = "Speech is currently off.";
    }
});


const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;


if (SpeechRecognition) {

    recognition = new SpeechRecognition();

    recognition.lang = "en-NG";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = function() {
        isListening = true;
        micButton.textContent = "Listening...";

        micButton.setAttribute("aria-pressed", "true");

        speechStatus.textContent = "Listening. Please speak.";
    };

    recognition.onresult = function(event) {
        input.value = event.results[0][0].transcript;

        speechStatus.textContent =
            "Speech recognised: " + input.value;

        input.focus();
    };

    recognition.onerror = function(event) {

        const messages = {
            "not-allowed": "Please allow microphone access.",
            "no-speech": "No speech was detected. Try again.",
            "network": "Speech recognition network error.",
            "audio-capture": "No working microphone was detected."
        };

        speechStatus.textContent =
            messages[event.error] || "Voice recognition failed.";
    };

    recognition.onend = function() {
        isListening = false;

        micButton.textContent = "🎤 Speak";

        micButton.setAttribute("aria-pressed", "false");
    };

    micButton.addEventListener("click", function() {

        if (isListening) {
            recognition.stop();
        } else {
            try {
                recognition.start();
            } catch (error) {
                speechStatus.textContent =
                    "Unable to start microphone. Try again.";
            }
        }
    });

} else {

    micButton.disabled = true;
    micButton.textContent = "Voice input unavailable";

    speechStatus.textContent =
        "Use a browser that supports speech recognition, such as Chrome.";
}


function addMessage(message, sender) {

    const element = document.createElement("div");

    element.className = "message " + sender;
    element.textContent = message;

    chatBox.appendChild(element);
    chatBox.scrollTop = chatBox.scrollHeight;
}


async function refreshCart() {

    try {

        const response = await fetch("/cart");
        const data = await response.json();

        cartDisplay.textContent = data.summary;

    } catch (error) {

        cartDisplay.textContent = "Unable to load your cart.";
    }
}


async function addProduct(productName, sizeElementId) {

    const size = document.getElementById(sizeElementId).value;

    try {

        const response = await fetch("/add-to-cart", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                name: productName,
                size: size
            })
        });

        const data = await response.json();

        addMessage("Agent: " + data.answer, "agent");

        speakText(data.answer);

        await refreshCart();

    } catch (error) {

        addMessage(
            "Agent: Unable to add this shoe to the cart.",
            "agent"
        );
    }
}


document.getElementById("refresh-cart")
    .addEventListener("click", refreshCart);


form.addEventListener("submit", async function(event) {

    event.preventDefault();

    const message = input.value.trim();

    if (!message) return;

    addMessage("You: " + message, "user");

    input.value = "";

    sendButton.disabled = true;

    try {

        const response = await fetch("/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error("Request failed");
        }

        addMessage("Agent: " + data.answer, "agent");

        speakText(data.answer);

        await refreshCart();

    } catch (error) {

        addMessage(
            "Agent: Something went wrong. Please try again.",
            "agent"
        );
    }

    sendButton.disabled = false;
    input.focus();
});


refreshCart();
</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML_PAGE, products=products)


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}
    question = data.get("message", "")

    if not isinstance(question, str):
        return jsonify({"error": "Invalid message."}), 400

    return jsonify({
        "answer": answer_question(question)
    })


@app.route("/cart")
def view_cart():

    cart = get_cart()

    total = sum(
        item["price"] * item["quantity"]
        for item in cart
    )

    return jsonify({
        "cart": cart,
        "total": total,
        "summary": cart_summary()
    })


@app.route("/add-to-cart", methods=["POST"])
def add_product_route():

    data = request.get_json(silent=True) or {}

    name = data.get("name")
    size = data.get("size")

    product = next(
        (p for p in products if p["name"] == name),
        None
    )

    if not product:
        return jsonify({
            "answer": "Product not found."
        }), 404

    if not isinstance(size, str) or size not in product["sizes"]:
        return jsonify({
            "answer": "Please select an available shoe size."
        }), 400

    return jsonify({
        "answer": add_to_cart(product, size)
    })


if __name__ == "__main__":
    app.run(debug=True)
