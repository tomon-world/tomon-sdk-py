import asyncio
import marshmallow_dataclass
from marshmallow_dataclass import dataclass
import nest_asyncio
from tomon_sdk import bot

nest_asyncio.apply()
bot_app = None


def on_dispatch(data):
    loop.run_until_complete(speak(data))


async def speak(data):
    e = data.get('e')
    d = data.get('d')
    if e == 'MESSAGE_CREATE':
        if d.get('author').get('id') != bot_app.id:
            if d.get('content') == '/ping':
                channel_id = d.get('channel_id')
                payload = {}
                payload['content'] = 'pong'
                await bot_app.api().route('/channels/{}/messages'.format(channel_id)).post(data=payload)


if __name__ == "__main__":
    bot_app = bot.Bot()


    async def main():
        bot_app.on(bot.OpCodeEvent.DISPATCH, on_dispatch)
        # await bot_app.start('your.bot.token')
        await bot_app.start_with_password('name#xxxx', 'password')


    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    print("finish")
