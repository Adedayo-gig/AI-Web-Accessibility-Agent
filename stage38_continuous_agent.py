

from speech_output import speak


def main():
    print("================================")
    print(" AI WEB ACCESSIBILITY AGENT")
    print("================================")

    print("Welcome! I am your AI Web Accessibility Agent.")
    speak("Welcome! I am your AI Web Accessibility Agent.")

    while True:
        print("\nWhat would you like me to do?")
        print("1. Read a webpage")
        print("2. Navigate between pages")
        print("3. Answer questions about a webpage")
        print("4. Fill a form")
        print("5. Find a product and add it to cart")
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            print("Opening webpage reading feature...")
            import stage30_understand_page
            stage30_understand_page.main()

        elif choice == "2":
            print("Opening page navigation feature...")
            import stage33_navigation
            stage33_navigation.main()

        elif choice == "3":
            print("Opening webpage question-answering feature...")
            import stage32_answer_questions
            stage32_answer_questions.main()

        elif choice == "4":
            print("Opening form filling feature...")
            import stage34_form_interaction
            stage34_form_interaction.main()

        elif choice == "5":
            print("Opening product action feature...")
            import stage44_product_action
            stage44_product_action.main()

        elif choice == "6":
            print("Thank you for using the AI Web Accessibility Agent.")
            speak("Thank you for using the AI Web Accessibility Agent.")
            break

        else:
            print("Invalid choice. Please select a number from 1 to 6.")


if __name__ == "__main__":
    main()
