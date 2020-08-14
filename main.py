from src import bot
from src.network import http
import asyncio
import pdb

if __name__ == "__main__":
    bot = bot.Bot()
    http = http.HTTPClient()


    async def main():
        result = await bot.startWithPassword('xiao#8050', 'Troph2019$')
        await asyncio.sleep(20)

        ## ------- Test Case -----------##

        # send message
        # await http.send_message(token = bot.token(), channel_id = "151217779805831168", content = "my testing")
        # send a file
        # await http.send_files(token = bot.token(), channel_id = "151217779805831168", content = "my 1 file", files = ['./example.jpg','./example2.jpg'])
        # edit message
        # await http.edit_message(token = bot.token(), channel_id = "158904117601988608", message_id = '159417868029779968', content = "change message testing")
        # get channels
        # channels = await http.get_guild_channels(token = bot.token(), guild_id = "124456710235492352")
        # print(channels)


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print("finish")
