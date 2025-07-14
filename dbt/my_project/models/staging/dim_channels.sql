with source as (
    select distinct channel from {{ ref('stg_telegram_messages') }}
)

select
    channel as channel_name,
    md5(channel) as channel_id
from source