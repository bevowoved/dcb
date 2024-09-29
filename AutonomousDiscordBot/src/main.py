import asyncio
from bot.bot import AutonomousBot
from bot.utils.database import Database
from bot.utils.nlp_processor import NLPProcessor
import yaml

async def main():
    with open('config/config.yaml', 'r') as config_file:
        config = yaml.safe_load(config_file)

    db = Database(config['database_url'])
    nlp_processor = NLPProcessor()
    
    bot = AutonomousBot(config, db, nlp_processor)
    
    try:
        await bot.start(config['discord_token'])
    except KeyboardInterrupt:
        await bot.close()
    finally:
        await db.close()

if __name__ == "__main__":
    asyncio.run(main())
