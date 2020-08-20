import asyncio
import time

import marshmallow_dataclass
from marshmallow_dataclass import dataclass
import nest_asyncio
from tomon_sdk import bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

nest_asyncio.apply()
bot_app = None


def on_dispatch(data):
    loop.run_until_complete(speak(data))

# @sync
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


# @sync
async def _tick():
    # global bot_app
    gid = "124457012091162624"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEyNDQ1NjcwMzUzMjk5NDU2MCIsImlhdCI6MTU5MTk1Mjg4M30.kSVY8QtlCFEDC-lJ6-EEjhVJrG4oHwd8NkQnpYi4vvc"
    bot_app.api().set_token(token)
    result = await bot_app.api().route(f'/guilds/{gid}').get()
    print(result)


# @sync
async def worker2():
    await asyncio.sleep(2)
    print("First Worker Executed")
    scheduler = AsyncIOScheduler()
    scheduler.add_job(_tick, trigger='interval', seconds=10,max_instances=10)
    scheduler.start()


# @sync
async def worker1():
    await asyncio.sleep(3)
    print("Second Worker Executed")
    await bot_app.start(
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEyNDQ1NjcwMzUzMjk5NDU2MCIsImlhdCI6MTU5MTk1Mjg4M30.kSVY8QtlCFEDC-lJ6-EEjhVJrG4oHwd8NkQnpYi4vvc")

    # # await bot_app.start_with_password("KZHIWEI#7479","A66871068a")


if __name__ == "__main__":
    # token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjEyNDQ1NjcwMzUzMjk5NDU2MCIsImlhdCI6MTU5MTk1Mjg4M30.kSVY8QtlCFEDC-lJ6-EEjhVJrG4oHwd8NkQnpYi4vvc"
    bot_app = bot.Bot()
    bot_app.on(bot.OpCodeEvent.DISPATCH, on_dispatch)
    #
    loop = asyncio.get_event_loop()
    # try:
    #     cors = asyncio.wait([worker1(),worker2()])
    #     # asyncio.ensure_future(worker2())
    #     loop.run_until_complete(cors)
    # except(KeyboardInterrupt, SystemExit):
    #     pass
    #
    loop.run_until_complete(worker1())
    # bot_app = bot.Bot()
    # gid = "124457012091162624"
    # # bot_app.on("READY", lambda: {
    # #     asyncio.run(_asd())
    # # })
    # asyncio.run(sad())
    # asyncio.run(_asd)
    # # _asd()
