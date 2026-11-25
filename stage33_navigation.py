
from playwright.sync_api import sync_playwright
from speech_output import speak
from pathlib import Path

def main():
    project_folder = Path(__file__).parent
    home_page = (project_folder / "home.html").as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            executable_path=r"C:\Users\LENOVO\AppData\Local\Google\Chrome\Application\chrome.exe"
        )

        page = browser.new_page()
        page.goto(home_page)

        print("AI WEB ACCESSIBILITY NAVIGATION AGENT")
        speak("Welcome. You are on the home page.")

        while True:
            command = input(
                "\nWhat would you like me to do? "
            ).strip().lower()

            if command in ["exit", "quit", "stop"]:
                speak("Navigation session ended. Goodbye.")
                break

            elif "about" in command:
                page.get_by_role("link", name="About Page").click()
                speak("You are now on the About page.")

            elif "contact" in command:
                page.get_by_role("link", name="Contact Page").click()
                speak("You are now on the Contact page.")

            elif "home" in command:
                page.get_by_role("link", name="Home Page").click()
                speak("You are now on the Home page.")

            elif "back" in command:
                page.go_back()
                speak("You have returned to the previous page.")

            elif "title" in command:
                title = page.title()
                speak(f"The current page title is {title}.")

            elif "read page" in command:
                heading = page.locator("h1").first.inner_text()
                content = page.locator("body").inner_text()
                speak(f"{heading}. {content}")

            else:
                speak(
                    "Sorry, I did not understand. "
                    "Try saying open about, open contact, "
                    "go home, go back, or read page."
                )

        browser.close()


if __name__ == "__main__":
    main()
