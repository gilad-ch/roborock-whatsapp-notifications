import logging
import time
from pyrate_limiter import wraps
import requests
from dotenv import load_dotenv
import os

load_dotenv()
logger = logging.getLogger(__name__)

base_url = os.getenv("WHAH_BASE_URL")
session_name = (
    os.getenv("WHAH_SESSION_NAME") if os.getenv("WHAH_SESSION_NAME") else "default"
)

if not (base_url or session_name):
    raise ValueError("WHAH_BASE_URL or WHAH_SESSION_NAME is not set")


def ensure_session(func):
    """Decorator to make sure WAHA session is running before the function call."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        WhahApi._start_session()
        return func(*args, **kwargs)

    return wrapper


class WhahApi:
    @staticmethod
    def _start_session():
        session_info_url = f"{base_url}/api/sessions/{session_name}"
        try:
            response = requests.get(session_info_url)
            if response.json().get("status") != "WORKING":
                logger.info("WHAHA Session stopped, starting WAHA session...")
                start_url = f"{base_url}/api/sessions/{session_name}/start"
                response = requests.post(start_url)
                time.sleep(20)
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Error starting session: {e}")
            raise e

    @staticmethod
    @ensure_session
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
            logger.error(f"Error sending message: {e}")
            raise e

    @staticmethod
    @ensure_session
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
            logger.error(f"Error sending message: {e}")
            raise e
