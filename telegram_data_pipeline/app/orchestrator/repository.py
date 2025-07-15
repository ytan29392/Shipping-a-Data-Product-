from dagster import repository
from orchestrator.pipeline import telegram_pipeline

@repository
def telegram_repo():
    return [telegram_pipeline]
