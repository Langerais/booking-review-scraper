# booking_scraper.py

import argparse
import json
import time
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def init_driver(debug=False):
    options = Options()
    if not debug:
        options.add_argument("--headless=new")
    options.add_argument("--disable-notifications")
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


def click_see_all_reviews(driver):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='#tab-reviews']"))
        ).click()
        time.sleep(2)
    except Exception as e:
        print(f"[!] Couldn't click review tab: {e}")


def parse_reviews_from_soup(soup):
    reviews = []
    review_cards = soup.select('div[data-testid="review-card"]')

    for card in review_cards:
        try:
            reviewer = card.select_one('div[data-testid="review-avatar"] + div .a3332d346a')
            country_img = card.select_one('div[data-testid="review-avatar"] + div img')
            country = country_img["alt"] if country_img else None

            score = card.select_one('[data-testid="review-score"] .ac4a7896c7')
            date = card.select_one('[data-testid="review-date"]')
            title = card.select_one('[data-testid="review-title"]')
            positive_text = card.select_one('[data-testid="review-positive-text"] .a53cbfa6de')
            negative_text = card.select_one('[data-testid="review-negative-text"] .a53cbfa6de')

            reviews.append({
                "name": reviewer.get_text(strip=True) if reviewer else None,
                "country": country,
                "review_date": date.get_text(strip=True).replace("Reviewed: ", "") if date else None,
                "score": score.get_text(strip=True).replace("Scored ", "") if score else None,
                "title": title.get_text(strip=True) if title else None,
                "positive": positive_text.get_text(strip=True) if positive_text else None,
                "negative": negative_text.get_text(strip=True) if negative_text else None,
                "scraped_at": datetime.now().isoformat()
            })
        except Exception as e:
            print(f"[!] Error parsing one review: {e}")
            continue

    return reviews


def scroll_and_load_reviews(driver, max_reviews):
    collected_reviews = []
    seen = set()
    page = 1

    while len(collected_reviews) < max_reviews:
        print(f"[*] Scraping page {page}...")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        new_reviews = parse_reviews_from_soup(soup)

        initial_count = len(collected_reviews)
        for r in new_reviews:
            r_id = hash(json.dumps(r, sort_keys=True))
            if r_id not in seen:
                collected_reviews.append(r)
                seen.add(r_id)
            if len(collected_reviews) >= max_reviews:
                break

        if len(collected_reviews) == initial_count:
            print("[!] No new reviews found. Stopping.")
            break

        # Try clicking "Next page"
        try:
            next_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Next page"]'))
            )
            if "disabled" in next_btn.get_attribute("class"):
                print("[*] Reached last page.")
                break
            next_btn.click()
            page += 1
            time.sleep(3)
        except Exception:
            print("[!] Couldn't click 'Next page'. Ending scroll.")
            break

    return collected_reviews


def scrape_booking_reviews(url, max_reviews, output_file, debug=False):
    driver = init_driver(debug)
    try:
        driver.get(url)
        time.sleep(3)
        click_see_all_reviews(driver)
        reviews = scroll_and_load_reviews(driver, max_reviews)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(reviews, f, indent=2, ensure_ascii=False)

        print(f"[✓] Saved {len(reviews)} reviews to {output_file}")

    finally:
        driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Booking.com hotel reviews")
    parser.add_argument("--url", required=True, help="Booking.com hotel URL")
    parser.add_argument("--max", type=int, default=50, help="Maximum number of reviews to scrape")
    parser.add_argument("--output", type=str, default="booking_reviews.json", help="Output JSON file")
    parser.add_argument("--debug", action="store_true", help="Run with visible browser")

    args = parser.parse_args()
    scrape_booking_reviews(args.url, args.max, args.output, debug=args.debug)
