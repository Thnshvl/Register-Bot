# db.py
import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def setup():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            discord_tag TEXT UNIQUE,
            discord_id BIGINT UNIQUE,
            name TEXT,
            game_id TEXT,
            email TEXT
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def save_user(discord_tag, discord_id, name, game_id, email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO users (discord_tag, discord_id, name, game_id, email)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (discord_id) DO UPDATE
        SET name = EXCLUDED.name,
            game_id = EXCLUDED.game_id,
            email = EXCLUDED.email;
    """, (discord_tag, discord_id, name, game_id, email))
    conn.commit()
    cur.close()
    conn.close()

def get_user(discord_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, game_id, email FROM users WHERE discord_id = %s", (discord_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result

def delete_user(discord_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE discord_id = %s", (discord_id,))
    conn.commit()
    cur.close()
    conn.close()

def update_field(discord_id, field, new_value):
    if field not in ['name', 'game_id', 'email']:
        return False
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"UPDATE users SET {field} = %s WHERE discord_id = %s", (new_value, discord_id))
    conn.commit()
    cur.close()
    conn.close()
    return True

def get_all_users():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT discord_tag, name, game_id, email FROM users")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

