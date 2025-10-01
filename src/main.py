import asyncio
import logging
from datetime import datetime
from utils.whahApi import WhahApi
from utils.roborockApi import RoborockApi
from notifications_config import (
    NOTIFICATION_NUMBERS,
    NO_NOTIFY_HOURS,
    PULL_COOLDOWN,
    NOTIFICATION_COOLDOWN,
    STATUS_MESSAGES,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def seconds_until_morning():
    now = datetime.now()
    morning = now.replace(hour=NO_NOTIFY_HOURS[1], minute=0, second=0, microsecond=0)
    if now.hour < NO_NOTIFY_HOURS[1]:
        return (morning - now).total_seconds()
    elif now.hour >= NO_NOTIFY_HOURS[0] and now.hour < NO_NOTIFY_HOURS[1]:
        return (morning - now).total_seconds()
    return 0


async def main():
    logging.info("Starting Roborock monitor...")
    async with RoborockApi() as roborock_api:
        while True:
            logging.debug("Fetching Roborock status...")
            status = await roborock_api.get_status()
            logging.debug(f"Status received: {status}")

            sent_notification = False

            for key, message_template in STATUS_MESSAGES.items():
                if status.get(key):
                    now = datetime.now()
                    if NO_NOTIFY_HOURS[0] <= now.hour < NO_NOTIFY_HOURS[1]:
                        wait_seconds = seconds_until_morning()
                        logging.info(
                            f"It's between {NO_NOTIFY_HOURS[0]} and {NO_NOTIFY_HOURS[1]}. Waiting {wait_seconds} seconds until morning..."
                        )
                        await asyncio.sleep(wait_seconds)

                    for name, number in NOTIFICATION_NUMBERS.items():
                        message = message_template.format(name=name)
                        WhahApi.send_message(message, number)
                        logging.info(f"Sent '{key}' notification to {name} ({number})")

                    sent_notification = True
                    break

            if sent_notification:
                logging.debug(
                    f"Sleeping for {NOTIFICATION_COOLDOWN} seconds (notification cooldown)."
                )
                await asyncio.sleep(NOTIFICATION_COOLDOWN)
            else:
                logging.debug(
                    f"No issues detected. Sleeping for {PULL_COOLDOWN} seconds."
                )
                await asyncio.sleep(PULL_COOLDOWN)


if __name__ == "__main__":
    asyncio.run(main())
