select
    det.id as detection_id,
    det.message_id,
    msg.channel_id,
    det.detected_object_class,
    det.confidence_score,
    det.detected_at
from {{ ref('stg_image_detections') }} det
left join {{ ref('fct_messages') }} msg
  on det.message_id = msg.message_id
