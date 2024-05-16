import webbrowser
import ctypes
import time
import sys

# Hiding console window
SW_HIDE = 0
GetConsoleWindow = ctypes.windll.kernel32.GetConsoleWindow
ShowWindow = ctypes.windll.user32.ShowWindow
ShowWindow(GetConsoleWindow(), SW_HIDE)

# Open link
url = "https://github.com/TheDoctor200/Base64Tools/releases/latest"
webbrowser.open(url)

# Wait for 3 seconds
time.sleep(3)

# Close script
sys.exit()