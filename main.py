from src import bot
from src.model import *
from src.network import http
import asyncio
import marshmallow_dataclass
from marshmallow_dataclass import dataclass

import pdb


def onDispatch(data):
    e = data.get('e')
    d = data.get('d')
    if e == 'USER_TYPING':
        typingschema = marshmallow_dataclass.class_schema(Typing)
        typing: Typing = typingschema().load(d)
        print(typing)
        return
    if e == 'USER_PRESENCE_UPDATE':
        presenceschema = marshmallow_dataclass.class_schema(Presence)
        p: Presence = presenceschema().load(d)
        print(p)
    if e == 'MESSAGE_CREATE':
        print(d)


if __name__ == "__main__":
    bot_app = bot.Bot()
    http = http.HTTPClient()


    async def main():
        bot_app.on(bot.OpCodeEvent.DISPATCH, onDispatch)
        await bot_app.startWithPassword('KZHIWEI#7479', 'A66871068a')

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
