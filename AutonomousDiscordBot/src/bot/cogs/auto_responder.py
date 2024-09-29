from discord.ext import commands

class AutoResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        # Auto-respond to certain patterns or keywords
        response = await self.bot.nlp_processor.auto_respond(message.content)
        if response:
            await message.channel.send(response)

async def setup(bot):
    await bot.add_cog(AutoResponder(bot))
