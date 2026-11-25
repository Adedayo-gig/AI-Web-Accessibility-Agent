
from playwright.sync_api import sync_playwright
from speech_output import speak
from pathlib import Path


def main():
    project_folder = Path(__file__).parent
    form_url = (project_folder / "test_accessible_form.html").as_uri()

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            executable_path=r"C:\Users\LENOVO\AppData\Local\Google\Chrome\Application\chrome.exe"
        )

        page = browser.new_page()
        page.goto(form_url)

        speak("I have opened the student registration form.")

        print("\nFORM INFORMATION")
        print("Page title:", page.title())

        fields = page.locator("input")
        print("Number of text fields:", fields.count())

        for i in range(fields.count()):
            field = fields.nth(i)
            print(
                "Field:", field.get_attribute("name"),
                "Type:", field.get_attribute("type")
            )

        print("Dropdown menus:", page.locator("select").count())

        speak(
            "The form requires your full name, email address, "
            "and department."
        )

        fullname = input("\nEnter your full name: ").strip()
        email = input("Enter your email address: ").strip()
        department_choice = input(
            "Enter department (Computer Science, Statistics, "
            "or Business Administration): "
        ).strip().title()

        page.locator("#fullname").fill(fullname)
        page.locator("#email").fill(email)
        page.locator("#department").select_option(
            label=department_choice
        )

        print("\nFORM DETAILS")
        print("Name:", fullname)
        print("Email:", email)
        print("Department:", department_choice)

        speak("Your registration details have been entered.")

        confirmation = input(
            "\nDo you want to submit this registration? (yes/no): "
        ).strip().lower()

        if confirmation == "yes":
            page.get_by_role(
                "button", name="Submit Registration"
            ).click()

            is_valid = page.locator(
                "#registration-form"
            ).evaluate("(form) => form.checkValidity()")

            if is_valid:
                result = page.locator("#result").inner_text()
                print("\nAGENT:", result)
                speak(result)
            else:
                result = (
                    "Invalid form details. Please check your "
                    "name, email address, and department."
                )
                print("\nAGENT:", result)
                speak(result)

        else:
            print("AGENT: Registration was not submitted.")
            speak("Registration was not submitted.")

        input("\nPress Enter to close the browser...")
        browser.close()


if __name__ == "__main__":
    main()
