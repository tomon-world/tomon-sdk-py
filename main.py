import asyncio
import nest_asyncio
from tomon_sdk import bot

nest_asyncio.apply()
bot_app = None

loop = asyncio.get_event_loop()


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
    bot_app.on(bot.OpCodeEvent.DISPATCH, on_dispatch)
    bot_app.start_with_password("name#0000", "password")
