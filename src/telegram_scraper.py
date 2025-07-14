import os
import json
from pathlib import Path
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv

# Load credentials
load_dotenv()
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")

def scrape_telegram_channels(channels: list, limit=100):
    """
    Scrapes text and image messages from public Telegram channels.

    Args:
        channels (list): List of Telegram channel URLs.
        limit (int): Max number of messages to retrieve per channel.

    Returns:
        dict: Dictionary of results with channel name as key.
    """
    TODAY = datetime.now().strftime("%Y-%m-%d")
    raw_data_dir = Path(f"data/raw/telegram_messages/{TODAY}")
    image_dir = Path(f"data/raw/images/{TODAY}")
    raw_data_dir.mkdir(parents=True, exist_ok=True)
    image_dir.mkdir(parents=True, exist_ok=True)

    all_channel_data = {}

    with TelegramClient("anon", API_ID, API_HASH) as client:
        for url in channels:
            try:
                entity = client.get_entity(url)
                messages = []

                for message in client.iter_messages(entity, limit=limit):
                    msg = {
                        "id": message.id,
                        "date": str(message.date),
                        "text": message.text,
                        "has_media": bool(message.media),
                        "sender_id": getattr(message.sender_id, 'user_id', None),
                        "channel": entity.title
                    }

                    # Save image if available
                    if isinstance(message.media, MessageMediaPhoto):
                        image_path = image_dir / f"{entity.title}_{message.id}.jpg"
                        client.download_media(message.media, file=image_path)
                        msg["image_path"] = str(image_path)

                    messages.append(msg)

                # Save to JSON
                json_path = raw_data_dir / f"{entity.title}.json"
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(messages, f, ensure_ascii=False, indent=2)

                all_channel_data[entity.title] = messages

            except Exception as e:
                print(f"Error scraping {url}: {e}")

    return all_channel_data