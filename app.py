
from flask import Flask, render_template_string, request, jsonify
import re

app = Flask(__name__)

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
# PRODUCT QUESTION ANSWERING
# =====================================

def answer_question(question):

    question = question.lower().strip()

    if not question:
        return "Please enter a question."

    # Count products
    if "how many" in question or "number of products" in question:
        return f"There are {len(products)} products available."

    # List all products
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

    # Cheapest product
    if any(word in question for word in [
        "cheapest", "lowest price", "lowest cost"
    ]):

        cheapest = min(products, key=lambda p: p["price"])

        return (
            f"The cheapest product is {cheapest['name']}, "
            f"priced at {cheapest['price']:,} naira."
        )

    # Product search
    product_keywords = [
        "shoe", "shoes", "black", "white",
        "product", "products", "sneaker", "sneakers"
    ]

    if any(word in question for word in product_keywords):

        matches = products.copy()

        # Filter by colour
        if "black" in question:
            matches = [
                p for p in matches
                if p["colour"] == "black"
            ]

        elif "white" in question:
            matches = [
                p for p in matches
                if p["colour"] == "white"
            ]

        # Filter by size
        size_match = re.search(
            r"\bsize\s*(\d{2})\b|\b(\d{2})\s*size\b",
            question
        )

        requested_size = None

        if size_match:

            requested_size = (
                size_match.group(1) or size_match.group(2)
            )

            matches = [
                p for p in matches
                if requested_size in p["sizes"]
            ]

        # Filter by maximum price
        price_match = re.search(
            r"(?:below|under|less than|up to|"
            r"not more than|max(?:imum)?(?: price)?)"
            r"\s*₦?\s*([\d,]+)",
            question
        )

        if price_match:

            maximum_price = int(
                price_match.group(1).replace(",", "")
            )

            matches = [
                p for p in matches
                if p["price"] <= maximum_price
            ]

        # Return matching products
        if matches:

            answer = "I found the following matching products: "

            for product in matches:

                answer += (
                    f"{product['name']}, "
                    f"priced at {product['price']:,} naira. "
                )

                if requested_size:
                    answer += (
                        f"Size {requested_size} is available. "
                    )

                elif "size" in question or "sizes" in question:
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
        "Sorry, I do not understand that question yet. "
        "You can ask about products, prices, colours, "
        "sizes or the cheapest product."
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

    <button id="send-button" type="submit">
        Send
    </button>

</form>

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


// =====================================
// SPEECH SETTINGS
// =====================================

let speechEnabled = false;


// Turn speech on or off

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


// =====================================
// READ AGENT RESPONSES
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

    } catch (error) {

        addMessage(
            "Agent: Sorry, something went wrong. Please try again.",
            "agent"
        );

    }

    sendButton.disabled = false;

    input.focus();

});

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


# =====================================
# START APPLICATION
# =====================================

if __name__ == "__main__":

    app.run(debug=True)


