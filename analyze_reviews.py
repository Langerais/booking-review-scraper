# analyze_reviews.py

import argparse
import json

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Optional override from settings if present
if not client.api_key:
    with open("settings.json", "r") as f:
        client.api_key = json.load(f).get("openai_key")


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
        "- Actionable suggestions the business can take to improve based on the feedback.\n\n"
        f"Reviews:\n{combined}"
    )
    return prompt


def analyze_reviews(reviews):
    if not reviews:
        print("[!] No reviews to analyze. Skipping OpenAI request.")
        return "No reviews available for analysis."

    prompt = prepare_prompt(reviews)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You summarize and analyze hotel reviews."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.5,
        max_tokens=1000
    )

    return response.choices[0].message.content



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
        print(f"\n[✓] Saved analysis to {args.output}")
