import webbrowser
import ctypes
import time
import requests
import json
import sys
import os

# Constants
GITHUB_API_URL = "https://api.github.com/repos/TheDoctor200/Base64Tools/releases/latest"
RELEASE_PAGE_URL = "https://github.com/TheDoctor200/Base64Tools/releases/latest"
CURRENT_VERSION_FILE = "version.txt"  # Path to your app version file

# Hiding console window
SW_HIDE = 0
GetConsoleWindow = ctypes.windll.kernel32.GetConsoleWindow
ShowWindow = ctypes.windll.user32.ShowWindow
ShowWindow(GetConsoleWindow(), SW_HIDE)

# Utility to display message boxes
def show_message_box(title, message):
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x40 | 0x1)  # 0x40 = INFO_ICON, 0x1 = OK_BUTTON

# Function to get current version from the local version file
def get_current_version():
    try:
        if os.path.exists(CURRENT_VERSION_FILE):
            with open(CURRENT_VERSION_FILE, 'r') as version_file:
                return version_file.read().strip()
        else:
            return None  # No version file found
    except Exception as e:
        print(f"Error reading current version: {e}")
        return None

# Function to check for the latest version on GitHub
def get_latest_version():
    try:
        response = requests.get(GITHUB_API_URL, timeout=5)
        if response.status_code == 200:
            release_info = json.loads(response.text)
            return release_info["tag_name"]
        else:
            print(f"Failed to get latest version, status code: {response.status_code}")
            return None
    except requests.ConnectionError:
        print("Failed to connect to GitHub API")
        return None

# Function to check if update is needed
def check_for_updates():
    current_version = get_current_version()
    latest_version = get_latest_version()

    if current_version and latest_version:
        if current_version != latest_version:
            return True, latest_version
        else:
            return False, None
    else:
        return None, None

# Main update function
def main():
    # Checking for updates
    update_needed, latest_version = check_for_updates()

    if update_needed:
        # Notify the user that an update is available
        show_message_box(
            "Update Available",
            f"A new version {latest_version} is available. You are currently using an older version."
        )

        # Open the browser to the latest release page
        webbrowser.open(RELEASE_PAGE_URL)

        # Wait for 2 seconds before exiting
        time.sleep(2)
    elif update_needed is False:
        # Notify user that the app is up to date
        show_message_box(
            "No Updates Available",
            "You are already using the latest version of the app."
        )
    else:
        # If there was an issue checking for updates
        show_message_box(
            "Update Check Failed",
            "Unable to check for updates at this time. Please try again later."
        )

    # Close script
    sys.exit()

if __name__ == "__main__":
    main()
