
from flask import (
    Flask, render_template_string, request,
    jsonify, session
)
import re

app = Flask(__name__)
app.secret_key = "ai-web-agent-demo-secret-key"

# =====================================
# PRODUCT DATABASE
# =====================================

products = [
    {
        "name": "Black Running Shoe",
        "colour": "black",
        "price": 12000,
        "sizes": ["40", "41", "42", "43", "44", "45"]
    },
    {
        "name": "White Sports Shoe",
        "colour": "white",
        "price": 10000,
        "sizes": ["40", "41", "42", "43"]
    },
    {
        "name": "Black Leather Shoe",
        "colour": "black",
        "price": 20000,
        "sizes": ["42", "43", "44", "45"]
    }
]


# =====================================
# CART FUNCTIONS
# =====================================

def get_cart():
    return session.get("cart", [])


def cart_summary():

    cart = get_cart()

    if not cart:
        return "Your shopping cart is empty."

    total = 0
    answer = "Your shopping cart contains: "

    for item in cart:

        subtotal = item["price"] * item["quantity"]
        total += subtotal

        size_text = (
            f", size {item['size']}"
            if item.get("size")
            else ""
        )

        answer += (
            f"{item['name']}{size_text}, "
            f"quantity {item['quantity']}, "
            f"price {item['price']:,} naira. "
        )

    answer += f"Your total is {total:,} naira."

    return answer


def add_to_cart(product, requested_size=None):

    cart = get_cart()

    for item in cart:

        if (
            item["name"] == product["name"]
            and item.get("size") == requested_size
        ):

            item["quantity"] += 1
            session["cart"] = cart
            session.modified = True

            return (
                f"Success! Another {product['name']} "
                f"has been added to your cart. "
                f"Quantity is now {item['quantity']}."
            )

    cart.append({
        "name": product["name"],
        "price": product["price"],
        "size": requested_size,
        "quantity": 1
    })

    session["cart"] = cart
    session.modified = True

    size_text = (
        f", size {requested_size}"
        if requested_size
        else ""
    )

    return (
        f"Success! {product['name']}{size_text} "
        f"has been added to your shopping cart."
    )


def remove_from_cart(product_name):

    cart = get_cart()

    for item in cart:

        if product_name.lower() in item["name"].lower():

            cart.remove(item)
            session["cart"] = cart
            session.modified = True

            return (
                f"{item['name']} has been removed "
                f"from your cart."
            )

    return "I could not find that product in your cart."


# =====================================
# REQUEST UNDERSTANDING
# =====================================

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

        question = re.sub(
            r"\b" + wrong + r"\b",
            correct,
            question
        )

    if not question:
        return "Please enter a request."

    # CLEAR CART

    if (
        "clear cart" in question
        or "empty cart" in question
        or "delete my cart" in question
    ):

        session["cart"] = []
        session.modified = True

        return "Your shopping cart has been cleared."

    # REMOVE PRODUCT

    if "remove" in question and "cart" in question:

        for product in products:

            if product["name"].lower() in question:

                return remove_from_cart(product["name"])

        return (
            "Please mention the full product name "
            "you want to remove."
        )

    # VIEW CART

    cart_words = [
        "show", "see", "view", "check",
        "display", "what", "list"
    ]

    if (
        "cart" in question
        and any(word in question.split() for word in cart_words)
    ):

        return cart_summary()

    # COUNT PRODUCTS

    if (
        "how many" in question
        or "number of products" in question
    ):

        return (
            f"There are {len(products)} "
            f"products available."
        )

    # LIST PRODUCTS

    if (
        "list all" in question
        or "show all products" in question
        or "what products" in question
    ):

        answer = "The available products are: "

        for product in products:

            answer += (
                f"{product['name']}, "
                f"priced at {product['price']:,} naira. "
            )

        return answer

    # CHEAPEST PRODUCT

    if any(word in question for word in [
        "cheapest", "lowest price", "lowest cost"
    ]):

        cheapest = min(
            products,
            key=lambda p: p["price"]
        )

        return (
            f"The cheapest product is "
            f"{cheapest['name']}, "
            f"priced at {cheapest['price']:,} naira."
        )

    # PRODUCT SEARCH

    product_keywords = [
        "shoe", "shoes", "black", "white",
        "product", "products", "sneaker",
        "sneakers", "running", "leather",
        "sports"
    ]

    if any(word in question.split() for word in product_keywords):

        matches = products.copy()

        if "running" in question:

            matches = [
                p for p in matches
                if p["name"] == "Black Running Shoe"
            ]

        elif "leather" in question:

            matches = [
                p for p in matches
                if p["name"] == "Black Leather Shoe"
            ]

        elif "sports" in question:

            matches = [
                p for p in matches
                if p["name"] == "White Sports Shoe"
            ]

        # COLOUR FILTER

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

        # SIZE FILTER

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
                p for p in matches
                if requested_size in p["sizes"]
            ]

        # PRICE FILTER

        price_match = re.search(
            r"(?:below|under|less than|up to|"
            r"not more than|max(?:imum)?(?: price)?|"
            r"of|at|for)"
            r"\s*₦?\s*([\d,]+)",
            question
        )

        if price_match:

            requested_price = int(
                price_match.group(1).replace(",", "")
            )

            if any(term in question for term in [
                "below", "under", "less than",
                "up to", "not more than",
                "maximum", "max"
            ]):

                matches = [
                    p for p in matches
                    if p["price"] <= requested_price
                ]

            else:

                matches = [
                    p for p in matches
                    if p["price"] == requested_price
                ]

        # ADD TO CART

        add_requested = (
            "add" in question and "cart" in question
        ) or "buy it" in question

        if matches:

            if add_requested:

                if len(matches) > 1:

                    names = ", ".join(
                        p["name"] for p in matches
                    )

                    return (
                        f"I found multiple matching products: "
                        f"{names}. Please specify which one "
                        "you want to add to your cart."
                    )

                return add_to_cart(
                    matches[0],
                    requested_size
                )

            answer = (
                "I found the following matching products: "
            )

            for product in matches:

                answer += (
                    f"{product['name']}, "
                    f"priced at {product['price']:,} naira. "
                )

                if requested_size:

                    answer += (
                        f"Size {requested_size} is available. "
                    )

                elif (
                    "size" in question
                    or "sizes" in question
                ):

                    answer += (
                        "Available sizes are "
                        + ", ".join(product["sizes"])
                        + ". "
                    )

            return answer

        return (
            "Sorry, I could not find a product matching "
            "your requested conditions."
        )

    return (
        "Sorry, I do not understand that request yet. "
        "You can ask about products, prices, colours, "
        "sizes or your shopping cart."
    )


# =====================================
# WEBSITE INTERFACE
# =====================================

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
content="width=device-width, initial-scale=1.0">

<title>AI Web Accessibility Agent</title>

<style>

* {
    box-sizing: border-box;
}

body {
    font-family: Arial, sans-serif;
    background: #f3f4f6;
    margin: 0;
    padding: 20px;
}

.container {
    max-width: 750px;
    margin: 30px auto;
    background: white;
    border-radius: 12px;
    padding: 25px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
}

h1 {
    text-align: center;
    color: #173b67;
}

.description {
    text-align: center;
    color: #555;
    line-height: 1.6;
}

#chat-box {
    height: 350px;
    overflow-y: auto;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    margin-top: 25px;
    background: #fafafa;
}

.message {
    padding: 12px;
    margin: 10px 0;
    border-radius: 8px;
    line-height: 1.6;
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
    gap: 10px;
    margin-top: 15px;
}

input {
    flex: 1;
    min-width: 0;
    padding: 14px;
    border: 1px solid #aaa;
    border-radius: 6px;
    font-size: 16px;
}

button {
    background: #173b67;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 12px 20px;
    cursor: pointer;
    font-size: 16px;
}

button:hover {
    background: #24558c;
}

button:focus-visible,
input:focus-visible {
    outline: 3px solid #f0a500;
    outline-offset: 3px;
}

button:disabled {
    opacity: 0.6;
    cursor: wait;
}

.speech-area {
    text-align: center;
    margin-top: 15px;
}

.cart-area {
    margin-top: 20px;
    padding: 15px;
    background: #f3f6fa;
    border-radius: 8px;
}

.cart-area h2 {
    color: #173b67;
    font-size: 19px;
}

.cart-area p {
    line-height: 1.5;
}

.status {
    text-align: center;
    color: #555;
    font-size: 14px;
    margin-top: 10px;
}

.visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}

@media (max-width: 500px) {

    .input-area {
        flex-direction: column;
    }

    .input-area button {
        width: 100%;
    }

    .container {
        padding: 18px;
        margin: 10px auto;
    }
}

</style>

</head>

<body>

<main class="container">

<h1>AI Web Accessibility Agent</h1>

<p class="description">
Welcome! I am your web accessibility assistant.
Ask me questions about products on the test shop.
</p>

<section
    id="chat-box"
    role="log"
    aria-label="Conversation"
    aria-live="polite"
    aria-relevant="additions">

    <div class="message agent">
        Agent: Hello! How can I help you today?
    </div>

</section>

<form id="chat-form" class="input-area">

    <label for="user-input" class="visually-hidden">
        Enter your request
    </label>

    <input
        type="text"
        id="user-input"
        placeholder="Ask about products, prices or sizes..."
        autocomplete="off"
        required
    >

    <button
        type="button"
        id="mic-button"
        aria-label="Start voice input"
        aria-pressed="false">
        🎤 Speak
    </button>

    <button id="send-button" type="submit">
        Send
    </button>

</form>

<div class="cart-area" aria-live="polite">

    <h2>Shopping Cart</h2>

    <p id="cart-display">
        Your shopping cart is empty.
    </p>

    <button type="button" id="refresh-cart">
        Refresh Cart
    </button>

</div>

<div class="speech-area">

    <button
        type="button"
        id="speech-toggle"
        aria-pressed="false">
        Turn speech on
    </button>

</div>

<p id="speech-status" class="status" aria-live="polite">
    Speech is currently off.
</p>

</main>


<script>

// =====================================
// GET WEBSITE ELEMENTS
// =====================================

const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const sendButton = document.getElementById("send-button");
const speechToggle = document.getElementById("speech-toggle");
const speechStatus = document.getElementById("speech-status");
const cartDisplay = document.getElementById("cart-display");
const refreshCartButton = document.getElementById("refresh-cart");
const micButton = document.getElementById("mic-button");

let speechEnabled = false;


// =====================================
// TEXT TO SPEECH SETTINGS
// =====================================

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

        speechStatus.textContent =
            "Speech is currently off.";

    }

});


// =====================================
// TEXT TO SPEECH
// =====================================

function speakText(message) {

    if (!speechEnabled) {
        return;
    }

    if (!("speechSynthesis" in window)) {

        speechStatus.textContent =
            "Speech is not supported by this browser.";

        return;
    }

    window.speechSynthesis.cancel();

    const speech = new SpeechSynthesisUtterance(message);

    speech.lang = "en-NG";
    speech.rate = 0.9;
    speech.pitch = 1;

    speech.onend = function() {
        speechStatus.textContent = "Speech finished.";
    };

    speech.onerror = function() {
        speechStatus.textContent = "Speech could not be played.";
    };

    window.speechSynthesis.speak(speech);

}


// =====================================
// SPEECH TO TEXT
// =====================================

// Check browser support

const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

let recognition = null;
let isListening = false;

if (SpeechRecognition) {

    recognition = new SpeechRecognition();

    recognition.lang = "en-NG";

    recognition.continuous = false;

    recognition.interimResults = false;

    recognition.maxAlternatives = 1;

    recognition.onstart = function() {

        isListening = true;

        micButton.textContent = "Listening...";

        micButton.setAttribute(
            "aria-pressed",
            "true"
        );

        speechStatus.textContent =
            "Listening. Please speak your request.";

    };


    recognition.onresult = function(event) {

        const spokenText =
            event.results[0][0].transcript;

        input.value = spokenText;

        speechStatus.textContent =
            "Speech recognised: " + spokenText;

        input.focus();

    };


    recognition.onerror = function(event) {

        let message = "Voice recognition failed.";

        if (event.error === "not-allowed") {

            message =
                "Microphone permission was denied. Please allow microphone access.";

        } else if (event.error === "no-speech") {

            message =
                "No speech was detected. Please try again.";

        } else if (event.error === "network") {

            message =
                "Network error. Check your internet connection and try again.";

        } else if (event.error === "audio-capture") {

            message =
                "No working microphone was detected.";

        } else if (event.error === "service-not-allowed") {

            message =
                "The browser speech recognition service is unavailable.";

        }

        speechStatus.textContent = message;

    };


    recognition.onend = function() {

        isListening = false;

        micButton.textContent = "🎤 Speak";

        micButton.setAttribute(
            "aria-pressed",
            "false"
        );

    };

} else {

    micButton.disabled = true;

    micButton.textContent =
        "Voice input unavailable";

    speechStatus.textContent =
        "Your browser does not support speech recognition. Try Google Chrome.";

}


// =====================================
// MICROPHONE BUTTON
// =====================================

micButton.addEventListener("click", function() {

    if (!recognition) {

        speechStatus.textContent =
            "Speech recognition is not supported.";

        return;

    }

    if (isListening) {

        recognition.stop();

        return;

    }

    try {

        recognition.start();

    } catch (error) {

        speechStatus.textContent =
            "Unable to start the microphone. Please try again.";

    }

});


// =====================================
// DISPLAY CHAT MESSAGES
// =====================================

function addMessage(message, sender) {

    const element = document.createElement("div");

    element.className = "message " + sender;

    element.textContent = message;

    chatBox.appendChild(element);

    chatBox.scrollTop = chatBox.scrollHeight;

}


// =====================================
// REFRESH CART DISPLAY
// =====================================

async function refreshCart() {

    try {

        const response = await fetch("/cart");

        const data = await response.json();

        cartDisplay.textContent = data.summary;

    } catch (error) {

        cartDisplay.textContent =
            "Unable to load your cart.";

    }

}

refreshCartButton.addEventListener(
    "click",
    refreshCart
);


// =====================================
// SEND MESSAGE TO PYTHON
// =====================================

form.addEventListener("submit", async function(event) {

    event.preventDefault();

    const message = input.value.trim();

    if (!message) {
        return;
    }

    addMessage("You: " + message, "user");

    input.value = "";

    sendButton.disabled = true;

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        if (!response.ok) {

            throw new Error(
                data.error || "Request failed."
            );

        }

        addMessage(
            "Agent: " + data.answer,
            "agent"
        );

        speakText(data.answer);

        await refreshCart();

    } catch (error) {

        addMessage(
            "Agent: Sorry, something went wrong. Please try again.",
            "agent"
        );

    }

    sendButton.disabled = false;

    input.focus();

});


// =====================================
// LOAD CART WHEN WEBSITE OPENS
// =====================================

refreshCart();

</script>

</body>
</html>
"""


# =====================================
# FLASK ROUTES
# =====================================

@app.route("/")
def home():

    return render_template_string(HTML_PAGE)


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    question = data.get("message", "")

    if not isinstance(question, str):

        return jsonify({
            "error": "Invalid message."
        }), 400

    answer = answer_question(question)

    return jsonify({
        "answer": answer
    })


@app.route("/cart", methods=["GET"])
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


# =====================================
# START APPLICATION
# =====================================

if __name__ == "__main__":

    app.run(debug=True)
