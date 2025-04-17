import tkinter as tk
from tkinter import messagebox
import json
import subprocess
import os
import sys

SETTINGS_FILE = "settings.json"


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {"openai_key": "", "model": "gpt-4o-mini", "max_reviews": 30, "extra_prompt": ""}
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def run_command(args, env=None):
    subprocess.run(args, env=env)


def scrape():
    url = url_entry.get().strip()
    if not url:
        messagebox.showwarning("Missing URL", "Please enter a Booking.com URL.")
        return
    save_settings(current_settings())
    run_command([sys.executable, "booking_scraper.py", "--url", url, "--max", str(max_reviews.get()), "--output",
                 "booking_reviews.json"])


def analyze():
    settings = current_settings()
    env = os.environ.copy()
    env["OPENAI_API_KEY"] = settings["openai_key"]
    env["MODEL"] = settings["model"]
    run_command([sys.executable, "analyze_reviews.py", "--input", "booking_reviews.json", "--limit",
                 str(settings["max_reviews"]), "--output", "analysis.txt"], env=env)


def scrape_and_analyze():
    scrape()
    analyze()


def current_settings():
    return {
        "openai_key": api_key_var.get(),
        "model": model_var.get(),
        "max_reviews": max_reviews.get(),
        "extra_prompt": extra_prompt.get("1.0", tk.END).strip()
    }


# GUI
root = tk.Tk()
root.title("Booking Review Assistant")

settings = load_settings()

tk.Label(root, text="Booking.com Hotel URL:").pack()
url_entry = tk.Entry(root, width=80)
url_entry.pack()

tk.Button(root, text="Scrape Reviews", command=scrape).pack(pady=2)
tk.Button(root, text="Analyze Reviews", command=analyze).pack(pady=2)
tk.Button(root, text="Scrape and Analyze", command=scrape_and_analyze).pack(pady=2)

tk.Label(root, text="OpenAI API Key:").pack()
api_key_var = tk.StringVar(value=settings["openai_key"])
tk.Entry(root, textvariable=api_key_var, show="*").pack()

tk.Label(root, text="Model:").pack()
model_var = tk.StringVar(value=settings["model"])
tk.OptionMenu(root, model_var, "gpt-4o-mini", "gpt-4.1-nano").pack()

tk.Label(root, text="Max Reviews:").pack()
max_reviews = tk.IntVar(value=settings["max_reviews"])
tk.Entry(root, textvariable=max_reviews).pack()

tk.Label(root, text="Extra Prompt Instructions:").pack()
extra_prompt = tk.Text(root, height=5, width=60)
extra_prompt.insert(tk.END, settings.get("extra_prompt", ""))
extra_prompt.pack()

tk.Button(root, text="Save Settings", command=lambda: save_settings(current_settings())).pack(pady=10)

root.mainloop()
