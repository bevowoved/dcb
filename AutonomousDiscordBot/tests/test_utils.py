import pytest
from src.bot.utils.nlp_processor import NLPProcessor
from src.bot.utils.scheduler import Scheduler
from unittest.mock import MagicMock

@pytest.fixture
def nlp_processor():
    return NLPProcessor()

@pytest.mark.asyncio
async def test_process_message(nlp_processor):
    assert await nlp_processor.process_message("Hello there!") == "Hello! How can I assist you today?"
    assert await nlp_processor.process_message("How are you doing?") == "I'm functioning well, thank you! How can I help you?"
    assert await nlp_processor.process_message("Goodbye!") == "Goodbye! Feel free to ask if you need anything else."
    assert await nlp_processor.process_message("This is a test.") is None

@pytest.fixture
def scheduler():
    bot = MagicMock()
    return Scheduler(bot)

@pytest.mark.asyncio
async def test_parse_time(scheduler):
    from datetime import datetime, timedelta
    now = datetime.now()
    
    result = await scheduler.parse_time("in 5 minutes")
    assert now + timedelta(minutes=4) < result < now + timedelta(minutes=6)
    
    with pytest.raises(ValueError):
        await scheduler.parse_time("invalid time string")

# Add more tests as needed
