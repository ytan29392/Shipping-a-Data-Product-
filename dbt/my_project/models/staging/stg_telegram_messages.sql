with source as (
    select * from raw.telegram_messages
),

renamed as (
    select
        id as message_id,
        date::timestamp as message_date,
        text,
        has_media,
        sender_id,
        channel,
        image_path
    from source
)

select * from renamed