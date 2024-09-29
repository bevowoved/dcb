import discord
from discord.ext import commands
import asyncio
from .utils.scheduler import Scheduler

class AutonomousBot(commands.Bot):
    def __init__(self, config, db, nlp_processor):
        intents = discord.Intents.all()
        super().__init__(command_prefix=config['prefix'], intents=intents)
        
        self.config = config
        self.db = db
        self.nlp_processor = nlp_processor
        self.scheduler = Scheduler(self)

    async def on_ready(self):
        print(f'Logged in as {self.user.name} (ID: {self.user.id})')
        await self.load_extensions()
        await self.start_background_tasks()

    async def load_extensions(self):
        for extension in ['bot.cogs.auto_responder', 'bot.cogs.task_manager']:
            await self.load_extension(extension)
            print(f'Loaded extension: {extension}')

    async def start_background_tasks(self):
        self.loop.create_task(self.scheduler.run())

    async def on_message(self, message):
        if message.author.bot:
            return

        # Process commands if message starts with prefix
        if message.content.startswith(self.command_prefix):
            await self.process_commands(message)
        else:
            # Otherwise, use NLP to understand and respond
            response = await self.nlp_processor.process_message(message.content)
            if response:
                await message.channel.send(response)

    async def on_member_join(self, member):
        welcome_message = f"Welcome to the server, {member.mention}! Feel free to ask me anything."
        default_channel = member.guild.system_channel
        if default_channel:
            await default_channel.send(welcome_message)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send("I'm not sure what you mean. Could you try rephrasing that?")
        else:
            await ctx.send(f"An error occurred: {str(error)}")
