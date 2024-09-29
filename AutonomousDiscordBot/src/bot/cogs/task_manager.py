from discord.ext import commands
import asyncio

class TaskManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def schedule(self, ctx, time: str, *, task: str):
        try:
            scheduled_time = await self.bot.scheduler.parse_time(time)
            await self.bot.scheduler.add_task(ctx.author.id, ctx.channel.id, task, scheduled_time)
            await ctx.send(f"Task scheduled for {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
        except ValueError as e:
            await ctx.send(str(e))

    @commands.command()
    async def tasks(self, ctx):
        user_tasks = await self.bot.scheduler.get_tasks(ctx.author.id)
        if user_tasks:
            task_list = "\n".join([f"{task['time'].strftime('%Y-%m-%d %H:%M:%S')}: {task['task']}" for task in user_tasks])
            await ctx.send(f"Your scheduled tasks:\n{task_list}")
        else:
            await ctx.send("You have no scheduled tasks.")

async def setup(bot):
    await bot.add_cog(TaskManager(bot))
