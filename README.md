# 🏨 Booking Review Analyzer

This project scrapes hotel reviews from [Booking.com](https://www.booking.com), summarizes them using OpenAI's API, and provides actionable business insights — all via a user-friendly interactive CLI.

---

## 🚀 Features

- ✅ Interactive command-line interface (CLI) using `menu.py`
- ✅ Scrape hotel reviews from Booking.com with Selenium
- ✅ Analyze and summarize reviews using OpenAI's GPT models
- ✅ Choose between `gpt-4o-mini` and `gpt-4.1-nano`
- ✅ Adjust review limit (1–999) and store persistent settings in `settings.json`
- ✅ Works via virtual environment with one-click `start.bat` setup (Windows)

---

## 📦 Installation & First Run

### 🖥 Option 1: One-click (Windows only)

```bash
start.bat
```

This will:
- Create a virtual environment
- Install all required dependencies
- Launch the CLI menu

---

### 💻 Option 2: Manual setup

```bash
python -m venv venv
venv\Scripts\activate            # On Windows
# OR
source venv/bin/activate         # On macOS/Linux

pip install -r requirements.txt
python menu.py
```

---

## 🔧 CLI Usage Overview

After running `menu.py`, choose an option:

```
1. Scrape reviews
2. Analyze reviews
3. Scrape AND analyze
4. Options
5. Exit
```

---

### ⚙️ Options Menu

- Set max number of reviews to scrape
- Select OpenAI model to use
- Enter your OpenAI API key (required for analysis)

Settings are saved to `settings.json` and automatically used on next run.

---

## 📁 File Structure

| File | Description |
|------|-------------|
| `menu.py` | CLI menu launcher |
| `booking_scraper.py` | Scrapes hotel reviews from Booking.com |
| `analyze_reviews.py` | Sends reviews to OpenAI for summarization |
| `settings.json` | Stores OpenAI key, model, and review limits |
| `requirements.txt` | Python dependencies |
| `start.bat` | Windows batch script to set up & run |
| `.gitignore` | Prevents tracking sensitive or generated files |

---

## 🔐 API Key Usage

- Your OpenAI key is stored locally in `settings.json` (automatically ignored by Git)
- The script prioritizes the environment variable `OPENAI_API_KEY`, if set

---

## 🧪 Example (Manual Execution)

```bash
# Scrape 30 reviews (visible browser)
python booking_scraper.py --url "<booking_hotel_url>" --max 30 --output booking_reviews.json --debug

# Analyze and summarize them
python analyze_reviews.py --input booking_reviews.json --limit 30 --output analysis.txt
```

---

## 🔗 URL Requirements

> **Important:** The scraper will only work if the Booking.com hotel URL points directly to the **Guest Reviews tab** — otherwise, reviews won't load.

✅ **The most reliable way to get the correct URL:**

1. Go to the hotel's page on [Booking.com](https://www.booking.com)
2. Click the **"Guest Reviews"** tab
3. Copy the full URL from your browser's address bar

Example:
```text
https://www.booking.com/hotel/gr/super-nice-hotel.en-gb.html?aid=1234567&label=abc123#tab-reviews
```

❌ **Avoid links that don’t include `#tab-reviews`, like:**
```text
https://www.booking.com/hotel/gr/super-nice-hotel.en-gb.html
```

## 🛡 .gitignore

The following are excluded from version control:
```
__pycache__/
*.pyc
settings.json
.env
analysis.txt
booking_reviews.json
```

---

## 📌 Requirements

- Python 3.9+
- Google Chrome installed (for Selenium)
- A valid OpenAI API key

---

## 🧠 Powered by

- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Selenium](https://www.selenium.dev/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [webdriver-manager](https://pypi.org/project/webdriver-manager/)

---

## 🛠 Future Ideas

- Add sentiment graphs
- Export results to PDF or Markdown
- Auto-detect hotel name & location
- Add GUI version
- Add separate files for different hotels
- Fix scraper ability to click on the reviews tab by itself.

---

## 👤 Author

Made with ❤️ by [@Langerais](https://github.com/Langerais)
