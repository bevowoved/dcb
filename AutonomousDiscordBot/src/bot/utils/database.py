import aiosqlite

class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    async def execute(self, query, params=()):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(query, params)
            await db.commit()

    async def fetch(self, query, params=()):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(query, params) as cursor:
                return await cursor.fetchall()

    async def fetch_one(self, query, params=()):
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute(query, params) as cursor:
                return await cursor.fetchone()

    async def close(self):
        # No need to close anything as we're using context managers
        pass

    async def init_db(self):
        queries = [
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                channel_id INTEGER NOT NULL,
                task TEXT NOT NULL,
                time TIMESTAMP NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS learned_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                trigger TEXT NOT NULL,
                response TEXT NOT NULL
            )
            """
        ]
        for query in queries:
            await self.execute(query)
