import asyncio
from datetime import datetime, timedelta
import parsedatetime

class Scheduler:
    def __init__(self, bot):
        self.bot = bot
        self.tasks = []
        self.cal = parsedatetime.Calendar()

    async def add_task(self, user_id, channel_id, task, time):
        self.tasks.append({
            'user_id': user_id,
            'channel_id': channel_id,
            'task': task,
            'time': time
        })
        await self.bot.db.execute(
            "INSERT INTO tasks (user_id, channel_id, task, time) VALUES (?, ?, ?, ?)",
            (user_id, channel_id, task, time.isoformat())
        )

    async def get_tasks(self, user_id):
        rows = await self.bot.db.fetch(
            "SELECT task, time FROM tasks WHERE user_id = ? ORDER BY time",
            (user_id,)
        )
        return [{'task': row[0], 'time': datetime.fromisoformat(row[1])} for row in rows]

    async def remove_task(self, task_id):
        await self.bot.db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))

    async def run(self):
        while True:
            now = datetime.now()
            to_remove = []
            for task in self.tasks:
                if task['time'] <= now:
                    channel = self.bot.get_channel(task['channel_id'])
                    if channel:
                        await channel.send(f"<@{task['user_id']}> Task reminder: {task['task']}")
                    to_remove.append(task)
            
            for task in to_remove:
                self.tasks.remove(task)
                await self.remove_task(task['id'])
            
            await asyncio.sleep(60)  # Check every minute

    async def parse_time(self, time_str):
        time_struct, parse_status = self.cal.parse(time_str)
        if parse_status == 0:
            raise ValueError("Could not parse the time string. Please use a format like '5 minutes' or 'tomorrow at 3pm'.")
        return datetime(*time_struct[:6])
