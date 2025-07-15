from .database import get_db_connection

def get_top_products(limit: int = 10):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT text, COUNT(*) as count
        FROM marts.fct_messages
        WHERE text IS NOT NULL
        GROUP BY text
        ORDER BY count DESC
        LIMIT %s;
    """, (limit,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return [{"text": r[0], "count": r[1]} for r in results]

def get_channel_activity(channel_name: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT d.day_of_week, COUNT(*) as post_count
        FROM marts.fct_messages m
        JOIN marts.dim_channels c ON m.channel_id = c.channel_id
        JOIN marts.dim_dates d ON m.message_date::date = d.date
        WHERE c.channel_name = %s
        GROUP BY d.day_of_week
        ORDER BY d.day_of_week;
    """, (channel_name,))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return [{"day": r[0], "post_count": r[1]} for r in results]

def search_messages(keyword: str):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT message_id, message_date, text, has_media, channel_id, image_path
        FROM marts.fct_messages
        WHERE text ILIKE %s;
    """, (f"%{keyword}%",))
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
