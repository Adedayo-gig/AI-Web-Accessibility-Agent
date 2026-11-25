
from playwright.sync_api import sync_playwright
from pathlib import Path
from speech_output import speak

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

        speak("Form validation test started.")

        print("\nFORM VALIDATION TEST")

        fullname = input("Enter full name: ")
        email = input("Enter email address: ")
        department = input(
            "Enter department (Computer Science, Statistics, "
            "or Business Administration): "
        )

        # Enter the information
        page.locator("#fullname").fill(fullname)
        page.locator("#email").fill(email)

        if department:
            page.locator("#department").select_option(label=department)

        errors = []

        # Check required fields
        if not fullname.strip():
            errors.append("Full name is required.")

        if not email.strip():
            errors.append("Email address is required.")
        elif not page.locator("#email").evaluate(
            "(element) => element.validity.valid"
        ):
            errors.append("Please enter a valid email address.")

        if not department:
            errors.append("Please select a department.")
        elif department not in [
            "Computer Science",
            "Statistics",
            "Business Administration"
        ]:
            errors.append("The selected department is not available.")

        # Report errors
        if errors:
            print("\nAGENT: I found some problems with your form.")

            for error in errors:
                print("ERROR:", error)
                speak(error)

            speak("Please correct these errors before submitting.")
            print("The form has not been submitted.")

        else:
            speak("All form details appear valid.")

            print("\nAll form details appear valid.")

            confirmation = input(
                "Do you want to submit the form? (yes/no): "
            ).strip().lower()

            if confirmation == "yes":
                page.get_by_role(
                    "button", name="Submit Registration"
                ).click()

                result = page.locator("#result").inner_text()
                print("AGENT:", result)
                speak(result)

            else:
                print("AGENT: Submission cancelled.")
                speak("Submission cancelled. Your form was not submitted.")

        input("\nPress Enter to close the browser...")
        browser.close()


if __name__ == "__main__":
    main()
