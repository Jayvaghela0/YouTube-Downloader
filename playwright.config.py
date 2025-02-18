import os
from playwright.sync_api import sync_playwright

# Set the cache directory for Playwright
os.environ['PLAYWRIGHT_BROWSERS_PATH'] = '0'  # Current working directory mein browsers install karein

# Install browsers
with sync_playwright() as p:
    p.chromium.download()
    p.firefox.download()
    p.webkit.download()
