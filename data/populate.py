import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    port=os.getenv("DB_PORT"),
)
with conn:
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO roster (name) VALUES (%s) RETURNING id",
            ("Iron Wolves",),
        )
        roster_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO characters (name, level, hp, base_hp, type, roster_id) "
            "VALUES (%s, %s, %s, %s, %s, %s) RETURNING id",
            ("Grom", 2, 30, 15, "Warrior", roster_id),
        )
        character_id = cur.fetchone()[0]