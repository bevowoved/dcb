import pytest
from src.bot.bot import AutonomousBot
from unittest.mock import MagicMock

@pytest.fixture
def bot():
    config = {
        'prefix': '!',
        'discord_token': 'test_token',
        'database_url': ':memory:'
    }
    db = MagicMock()
    nlp_processor = MagicMock()
    return AutonomousBot(config, db, nlp_processor)

@pytest.mark.asyncio
async def test_on_ready(bot):
    bot.load_extensions = MagicMock()
    bot.start_background_tasks = MagicMock()
    await bot.on_ready()
    bot.load_extensions.assert_called_once()
    bot.start_background_tasks.assert_called_once()

@pytest.mark.asyncio
async def test_on_message(bot):
    message = MagicMock()
    message.author.bot = False
    message.content = "Hello, bot!"
    
    bot.nlp_processor.process_message = MagicMock(return_value="Hello, human!")
    
    await bot.on_message(message)
    
    bot.nlp_processor.process_message.assert_called_once_with("Hello, bot!")
    message.channel.send.assert_called_once_with("Hello, human!")

# Add more tests as needed
