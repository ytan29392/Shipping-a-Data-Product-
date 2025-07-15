from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Message(BaseModel):
    message_id: int
    message_date: datetime
    text: Optional[str]
    has_media: bool
    channel_id: str
    image_path: Optional[str]

class ChannelActivity(BaseModel):
    channel_id: str
    day: str
    post_count: int

class DetectedObject(BaseModel):
    message_id: int
    detected_object_class: str
    confidence_score: float
