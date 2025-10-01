# Roborock WhatsApp Notifications

This script monitors the status of a **Roborock robotic cleaner** and sends notifications via **WAHA API** to WhatsApp recipients when issues are detected.  
It supports configurable recipients, notification cooldowns, and quiet hours.

---

## Installation

1. **Setup WAHA**  
   Start a WAHA instance with an active WhatsApp session:  
   [Quick Start Guide](https://waha.devlike.pro/docs/overview/quick-start/)

2. **Environment variables**  
   Create a `.env` file with the required values (see `.env.example` for reference).

3. **Configuration**  
   Adjust `notifications_config.py` to set:
   - Phone numbers and names  
   - Notification timing (cooldown, quiet hours)  

4. **Install dependencies**  
   Using [uv](https://github.com/astral-sh/uv):  
   ```bash
   uv sync
````

5. **Run the script**

   ```bash
   uv run main.py
   ```

   Or via Docker using the provided `docker-compose.yml` and `Dockerfile`.

---

## Supported Devices

[python-roborock supported devices](https://python-roborock.readthedocs.io/en/latest/supported_devices.html)

