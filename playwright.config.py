import os
import subprocess

# Set the cache directory for Playwright
os.environ['PLAYWRIGHT_BROWSERS_PATH'] = '0'  # Current working directory mein browsers install karein

# Install browsers using playwright install command
subprocess.run(["playwright", "install"])
