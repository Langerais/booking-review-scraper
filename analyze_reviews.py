import argparse
import json
import openai
import os

SETTINGS_FILE = "settings.json"

def load_extra_prompt():
    if not os.path.exists(SETTINGS_FILE):
        return ""
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
        return settings.get("extra_prompt", "")


openai.api_key = os.getenv("OPENAI_API_KEY")
EXTRA_PROMPT = load_extra_prompt()

# Optional override from settings if present
if not openai.api_key:
    with open("settings.json", "r") as f:
        openai.api_key = json.load(f).get("openai_key")


def load_reviews(json_file, limit=50):
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data[:limit]


def prepare_prompt(reviews):
    texts = []
    for r in reviews:
        pos = f"Positive: {r['positive']}" if r.get("positive") else ""
        neg = f"Negative: {r['negative']}" if r.get("negative") else ""
        full = f"{pos}\n{neg}".strip()
        if full:
            texts.append(full)
    combined = "\n\n".join(texts)
    prompt = (
        "You are an expert in customer experience analysis.\n"
        "Given the following customer reviews from a hotel on Booking.com, analyze and summarize them.\n"
        "Please return:\n"
        "- A summary of customer sentiment\n"
        "- The most common pros\n"
        "- The most common cons\n"
        "- Actionable suggestions the business can take to improve based on the feedback.\n"
    )
    if EXTRA_PROMPT:
        prompt += f"\n\nAdditional user request:\n{EXTRA_PROMPT.strip()}\n"
    else:
        print("No Extra prompt!")
    prompt += f"\n\nReviews:\n{combined}"
    print(EXTRA_PROMPT)
    return prompt


def analyze_reviews(reviews):
    if not reviews:
        print("[!] No reviews to analyze. Skipping OpenAI request.")
        return "No reviews available for analysis."

    prompt = prepare_prompt(reviews)

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You summarize and analyze hotel reviews."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1000
    )

    return response.choices[0].message["content"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze hotel reviews using OpenAI")
    parser.add_argument("--input", type=str, required=True, help="Path to JSON reviews file")
    parser.add_argument("--limit", type=int, default=50, help="Max number of reviews to use")
    parser.add_argument("--output", type=str, help="Output file to save analysis")

    args = parser.parse_args()
    reviews = load_reviews(args.input, args.limit)
    result = analyze_reviews(reviews)

    print("\n=== Analysis Result ===\n")
    print(result)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"\n[\u2713] Saved analysis to {args.output}")
