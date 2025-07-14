select
    stg.message_id,
    stg.message_date,
    stg.text,
    stg.has_media,
    stg.image_path,
    dim_channels.channel_id,
    dim_dates.date
from {{ ref('stg_telegram_messages') }} stg
left join {{ ref('dim_channels') }} dim_channels
    on stg.channel = dim_channels.channel_name
left join {{ ref('dim_dates') }} dim_dates
    on stg.message_date::date = dim_dates.date

