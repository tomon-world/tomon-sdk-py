import asyncio
import marshmallow_dataclass
from marshmallow_dataclass import dataclass
import nest_asyncio
from tomon_sdk import bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from syncer import sync

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

    # print('Tick! The time is: %s' % datetime.now())


@sync
async def _tick():
    # global bot_app
    print("tick")
    result = await bot_app.api().route(f'/guilds/{gid}').get()
    print(result)


@sync
async def _asd():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(_tick, 'interval', seconds=5)
    scheduler.start()


@sync
async def sad():
    await bot_app.start(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEyNDQ1NjcwMzUzMjk5NDU2MCIsImlhdCI6MTU5MTk1Mjg4M30.kSVY8QtlCFEDC-lJ6-EEjhVJrG4oHwd8NkQnpYi4vvc")
    # await bot_app.start_with_password("KZHIWEI#7479","A66871068a")


if __name__ == "__main__":
    bot_app = bot.Bot()
    gid = "124457012091162624"
    bot_app.on("READY", lambda: {
        asyncio.run(_asd())
    })
    asyncio.run(sad())
    # _asd()
    while (True):
        pass
