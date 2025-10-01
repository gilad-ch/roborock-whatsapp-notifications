import requests
from dotenv import load_dotenv
import os

load_dotenv()
base_url = os.getenv("WHAH_BASE_URL")
session_name = (
    os.getenv("WHAH_SESSION_NAME") if os.getenv("WHAH_SESSION_NAME") else "default"
)

if not (base_url or session_name):
    raise ValueError("WHAH_BASE_URL or WHAH_SESSION_NAME is not set")


class WhahApi:
    @staticmethod
    def send_message(message: str, number: int):
        chat_id = f"{number}@c.us"
        url = f"{base_url}/api/sendText"
        payload = {
            "chatId": chat_id,
            "reply_to": None,
            "text": message,
            "linkPreview": True,
            "session": session_name,
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error sending message: {e}")
            raise e

    @staticmethod
    def send_group_message(message: str, group_id: str):
        chat_id = f"{group_id}@g.us"
        url = f"{base_url}/api/sendText"
        payload = {
            "chatId": chat_id,
            "reply_to": None,
            "text": message,
            "linkPreview": True,
            "session": session_name,
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error sending message: {e}")
            raise e
