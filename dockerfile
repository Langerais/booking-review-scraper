FROM python:3.11-slim

# Install Chromium and dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    curl \
    unzip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install ChromeDriver that matches Chromium 135.0.7049.84
RUN mkdir -p /opt/chrome && \
    curl -Lo /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/135.0.7049.84/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip -d /opt/chrome && \
    mv /opt/chrome/chromedriver-linux64/chromedriver /usr/bin/chromedriver && \
    chmod +x /usr/bin/chromedriver && \
    rm -rf /tmp/chromedriver.zip /opt/chrome/chromedriver-linux64

# Setup environment for Selenium
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# App setup
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Start CLI app
CMD ["python", "menu.py"]
