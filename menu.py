import sys
import os
import json
import subprocess

SETTINGS_FILE = "settings.json"


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        default = {
            "openai_key": "",
            "model": "gpt-4o-mini",
            "max_reviews": 30,
            "extra_prompt": ""
        }
        save_settings(default)
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=2)


def set_options(settings):
    while True:
        print("\n--- Options Menu ---")
        print(f"1. Set number of reviews to scrape (current: {settings['max_reviews']})")
        print(f"2. Select AI model (current: {settings['model']})")
        print(f"3. Set OpenAI API Key ({'set' if settings['openai_key'] else 'not set'})")
        print(f"4. Set extra prompt instructions ({'set' if settings.get('extra_prompt') else 'not set'})")
        print("5. Back to main menu")

        opt = input("Choose option: ").strip()

        if opt == "1":
            val = input("Enter number of reviews to scrape (1-999): ").strip()
            if val.isdigit() and 1 <= int(val) <= 999:
                settings["max_reviews"] = int(val)
                print(f"[\u2713] Max reviews set to {val}")
            else:
                print("[!] Invalid number.")
        elif opt == "2":
            print("Choose model:")
            print("1. gpt-4o-mini")
            print("2. gpt-4.1-nano")
            m = input("Select: ").strip()
            if m == "1":
                settings["model"] = "gpt-4o-mini"
            elif m == "2":
                settings["model"] = "gpt-4.1-nano"
            else:
                print("[!] Invalid choice.")
        elif opt == "3":
            key = input("Enter your OpenAI API key: ").strip()
            if key:
                settings["openai_key"] = key
                print("[\u2713] API key saved.")
            else:
                print("[!] Invalid key.")
        elif opt == "4":
            extra = input("Enter any extra instructions you'd like to include in the prompt (leave blank to clear): ")
            settings["extra_prompt"] = extra.strip()
            print("[\u2713] Extra instructions updated.")
        elif opt == "5":
            break
        else:
            print("[!] Invalid option.")

        save_settings(settings)


def clamp(val, min_val=1, max_val=999):
    return max(min_val, min(val, max_val))


def scrape_reviews(settings):
    url = input("Paste Booking.com hotel URL: ").strip()
    output = "booking_reviews.json"
    max_reviews = clamp(settings["max_reviews"])
    cmd = [
        sys.executable, "booking_scraper.py",
        "--url", url,
        "--max", str(max_reviews),
        "--output", output
    ]
    subprocess.run(cmd)


def analyze_reviews(settings):
    input_file = "booking_reviews.json"
    output_file = "analysis.txt"

    env = os.environ.copy()
    env["OPENAI_API_KEY"] = settings["openai_key"]
    env["MODEL"] = settings["model"]

    cmd = [
        sys.executable, "analyze_reviews.py",
        "--input", input_file,
        "--limit", str(settings["max_reviews"]),
        "--output", output_file
    ]
    subprocess.run(cmd, env=env)


def scrape_and_analyze(settings):
    scrape_reviews(settings)
    analyze_reviews(settings)


def main_menu():
    settings = load_settings()

    while True:
        print("\n=== Booking Review Assistant ===")
        print("1. Scrape reviews")
        print("2. Analyze reviews")
        print("3. Scrape AND analyze")
        print("4. Options")
        print("5. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            scrape_reviews(settings)
        elif choice == "2":
            analyze_reviews(settings)
        elif choice == "3":
            scrape_and_analyze(settings)
        elif choice == "4":
            set_options(settings)
        elif choice == "5":
            break
        else:
            print("[!] Invalid selection")


if __name__ == "__main__":
    main_menu()
