from fastapi import FastAPI, Query
from app.models import Message, ChannelActivity
from app import crud

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Telegram Analytics API is running"}

@app.get("/api/reports/top-products")
def top_products(limit: int = Query(10)):
    return crud.get_top_products(limit)

@app.get("/api/channels/{channel_name}/activity", response_model=list[ChannelActivity])
def channel_activity(channel_name: str):
    return crud.get_channel_activity(channel_name)

@app.get("/api/search/messages", response_model=list[Message])
def search_messages(query: str = Query(...)):
    results = crud.search_messages(query)
    return [Message(
        message_id=r[0],
        message_date=r[1],
        text=r[2],
        has_media=r[3],
        channel_id=r[4],
        image_path=r[5]
    ) for r in results]
