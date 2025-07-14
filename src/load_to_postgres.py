import os
import json
import psycopg2
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

# Load env variables
load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("POSTGRES_PORT", 5432)

def load_json_to_postgres(folder_path):
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    files = Path(folder_path).glob("*.json")
    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            messages = json.load(f)
            for msg in messages:
                cur.execute("""
                    INSERT INTO raw.telegram_messages (id, date, text, has_media, sender_id, channel, image_path)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """, (
                    msg.get("id"),
                    msg.get("date"),
                    msg.get("text"),
                    msg.get("has_media"),
                    msg.get("sender_id"),
                    msg.get("channel"),
                    msg.get("image_path")
                ))

    conn.commit()
    cur.close()
    conn.close()