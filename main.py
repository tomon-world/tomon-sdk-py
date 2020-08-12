from src import bot
import asyncio

if __name__ == "__main__":
    bot = bot.Bot()

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(
        bot.startWithPassword('xiao#8050', 'Troph2019$'))
    
    #print("-------result------"
