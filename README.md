python booking_scraper.py --url "https://www.booking.com/hotel/gr/the-white-suites.en-gb.html#tab-reviews" --max 30 --output reviews.json --debug

python analyze_reviews.py --input booking_reviews.json --limit 30 --output analysis.txt
