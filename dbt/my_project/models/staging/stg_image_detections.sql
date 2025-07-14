select
    id,
    message_id,
    detected_object_class,
    confidence_score,
    detected_at
from raw.image_detections
