from dagster import op, job
from scripts.telegram_scraper import scrape_telegram_channels
from scripts.load_to_postgres import load_json_to_postgres
from scripts.yolo_detection import detect_objects_in_images
import datetime

CHANNELS = [
    "https://t.me/lobelia4cosmetics",
    "https://t.me/tikvahpharma"
]

@op
def scrape_data():
    scrape_telegram_channels(CHANNELS, limit=50)

@op
def load_data():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    folder = f"data/raw/telegram_messages/{today}"
    load_json_to_postgres(folder)

@op
def run_dbt():
    import subprocess
    subprocess.run(["dbt", "run"], cwd="dbt/my_project")

@op
def detect_images():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    folder = f"data/raw/images/{today}"
    detect_objects_in_images(folder, today)

@job
def telegram_pipeline():
    detect_images(run_dbt(load_data(scrape_data())))
