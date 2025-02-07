import json
import time
import os
import random
import requests
import shareithub
from dotenv import load_dotenv
from datetime import datetime
from shareithub import shareithub

load_dotenv()
# Token dan kunci API
discord_token = os.getenv('DISCORD_TOKEN')
google_api_key = os.getenv('GOOGLE_API_KEY')

def log_message(message):
    print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}")

def generate_message(google_api_key, use_google_ai=True):
    if use_google_ai:
        url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={google_api_key}'
        headers = {
            'Content-Type': 'application/json'
        }
        data = {
            'contents': [
                {
                    'parts': [
                        {
                            'text': "Generate a random message for a Discord chat."
                        }
                    ]
                }
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            log_message(f"Request failed: {e}")
            if response.content:
                log_message(f"Response content: {response.content.decode()}")
            return None
    else:
        try:
            with open('pesan1.txt', 'r') as file:
                lines = file.readlines()

                if lines:
                    message = lines.pop(0).strip()

                    with open('pesan1.txt', 'w') as file:
                        file.writelines(lines)
                    return {"candidates": [{"content": {"parts": [{"text": message}]}}]}
                else:
                    log_message("File pesan1.txt kosong.")
                    return None
        except FileNotFoundError:
            log_message("File pesan1.txt tidak ditemukan.")
            return None

def send_message(channel_id, message):
    headers = {
        'Authorization': f'{discord_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'content': message
    }

    try:
        response = requests.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", json=payload, headers=headers)
        response.raise_for_status()

        if response.status_code == 201:
            log_message(f"Message sent: {message}")
        else:
            log_message(f"Failed to send message: {response.status_code}")
            log_message(f"Response content: {response.content.decode()}")
    except requests.exceptions.RequestException as e:
        log_message(f"Request error: {e}")

def auto_chat(channel_id, chat_delay):
    while True:
        try:
            result = generate_message(google_api_key, use_google_ai)

            if result:
                message_text = result['candidates'][0]['content']['parts'][0]['text']
                send_message(channel_id, message_text)

            log_message(f"Waiting for {chat_delay} seconds before sending the next message...")
            time.sleep(chat_delay)
        except Exception as e:
            log_message(f"Error: {e}")
            time.sleep(chat_delay)

shareithub()

if __name__ == "__main__":
    use_google_ai = input("Ingin menggunakan Google Gemini AI? (y/n): ").lower() == 'y'
    channel_id = input("Masukkan ID channel: ")
    chat_delay = int(input("Set Delay Mengirim Pesan (dalam detik): "))

    log_message("Dimulai...")
    
    log_message("3")
    time.sleep(1)
    log_message("2")
    time.sleep(1)
    log_message("1")
    time.sleep(1)
    auto_chat(channel_id, chat_delay)
