import aiosqlite
import disnake


class DataBase:
    def __init__(self):
        self.name = 'dbs/payment.db'
        self.color = 0x2B2D31

    async def create_table(self):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = '''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                name TEXT,
                money INTEGER,
                sub INTEGER,
                sub_time INTEGER
            );
            CREATE TABLE IF NOT EXISTS transfers (
                user_id INTEGER,
                label TEXT,
                amount INTEGER
            );
            '''
            await cursor.executescript(query)
            await db.commit()

    async def add_user(self, user: disnake.Member):
        async with aiosqlite.connect(self.name) as db:
            if not await self.get_user(user):
                cursor = await db.cursor()
                query = 'INSERT INTO users (user_id, money) VALUES (?, ?)'
                await cursor.execute(query, (user.id, 0))
                await db.commit()

    async def get_user(self, user: disnake.Member):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'SELECT * FROM users WHERE user_id = ?'
            await cursor.execute(query, (user.id,))
            return await cursor.fetchone()

    async def get_labels(self, label: str):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'SELECT * FROM transfers WHERE label = ?'
            await cursor.execute(query, (label,))
            return await cursor.fetchone()

    async def add_transfer(self, user: disnake.Member, label: str, amount: int):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'INSERT INTO transfers (user_id, label, amount) VALUES (?, ?, ?)'
            await cursor.execute(query, (user.id, label, amount))
            await db.commit()

    async def get_transfers(self):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'SELECT * FROM transfers'
            await cursor.execute(query)
            return await cursor.fetchall()

    async def add_money(self, user_id: int, amount: int):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'UPDATE users SET money = money + ? WHERE user_id = ?'
            await cursor.execute(query, (amount, user_id))
            await db.commit()

    async def rm_transfer(self, label: str):
        async with aiosqlite.connect(self.name) as db:
            cursor = await db.cursor()
            query = 'DELETE FROM transfers WHERE label = ?'
            await cursor.execute(query, (label,))
            await db.commit()