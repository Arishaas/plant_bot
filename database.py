import aiosqlite
from datetime import date
from plants_data import plants_data

DB = "plants.db"


async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS plants (
            name TEXT PRIMARY KEY,
            category TEXT,
            water_days INTEGER,
            feed_days INTEGER,
            transplant_days INTEGER
        )
        """)

        await db.execute("""
                CREATE TABLE IF NOT EXISTS user_plants (
                    user_id INTEGER,
                    plant_name TEXT,
                    last_water TEXT,
                    last_feed TEXT,
                    last_trans TEXT,
                    notes TEXT,
                    PRIMARY KEY (user_id, plant_name)
                )
                """)

        for p in plants_data:
            try:
                await db.execute(
                    "INSERT INTO plants (name, category, water_days, feed_days, transplant_days) VALUES (?, ?, ?, ?, ?)",
                    (p["name"].lower(), p["category"], p["water"], p["feed"], p["trans"])
                )
            except:
                pass

        await db.commit()


async def add_user_plant(user_id: int, plant_name: str):
    today = date.today().isoformat()
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            """INSERT OR REPLACE INTO user_plants (
            user_id, plant_name, last_water, last_feed, last_trans, notes
            )
            VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, plant_name, today, today, today, "")
        )
        await db.commit()


async def get_user_plants(user_id: int):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute(
            "SELECT plant_name, last_water, last_feed, last_trans, notes FROM user_plants WHERE user_id = ?",
            (user_id,)
        )
        return await cur.fetchall()


async def get_user_plant(user_id: int, plant_name: str):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute(
            "SELECT plant_name, last_water, last_feed, last_trans, notes FROM user_plants WHERE  user_id = ? and "
            "plant_name = ?",
            (user_id, plant_name)
        )
        return await cur.fetchone()


async def update_user_date(user_id: int, plant_name: str, field: str, date_iso: str):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            f"UPDATE user_plants SET {field} = ? WHERE user_id = ? AND plant_name = ?",
            (date_iso, user_id, plant_name)
        )
        await db.commit()


async def update_notes(user_id: int, plant_name: str, notes: str):
    async with aiosqlite.connect(DB) as db:
        await db.execute(
            "UPDATE user_plants SET notes WHERE user_id = ? AND plant_name = ?",
            (notes, user_id, plant_name)
        )
        await db.commit()


async def get_plant_default(name: str):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute(
            "SELECT water_days, feed_days, trans_days FROM plants WHERE name = ?",
            (name,)
        )
        return cur.fetchone()