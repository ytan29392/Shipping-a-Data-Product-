with source as (
    select distinct message_date from {{ ref('stg_telegram_messages') }}
)

select
    message_date::date as date,
    extract(dow from message_date) as day_of_week,
    extract(week from message_date) as week_number,
    extract(month from message_date) as month,
    extract(year from message_date) as year
from source
