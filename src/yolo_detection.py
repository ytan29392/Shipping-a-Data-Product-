import os
import cv2
import psycopg2
from ultralytics import YOLO
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Load .env
load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("POSTGRES_PORT", 5432)

# Initialize YOLOv8 (you can use yolov8s.pt or yolov8n.pt too)
model = YOLO("yolov8n.pt")

def detect_objects_in_images(image_folder: str, date_folder: str):
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

    folder = Path(image_folder)
    for image_path in folder.glob("*.jpg"):
        results = model(str(image_path))
        boxes = results[0].boxes

        for box in boxes:
            cls = int(box.cls[0].item())
            conf = float(box.conf[0].item())
            class_name = model.names[cls]

            # Try to extract message_id from filename
            try:
                base = image_path.stem  # e.g. "Lobelia Cosmetics_1234"
                message_id = int(base.split("_")[-1])
            except:
                message_id = None

            # Insert detection
            cur.execute("""
                INSERT INTO raw.image_detections (message_id, detected_object_class, confidence_score, detected_at)
                VALUES (%s, %s, %s, %s)
            """, (message_id, class_name, conf, datetime.now()))

    conn.commit()
    cur.close()
    conn.close()
