import pdb
import aiohttp
import json
from urllib.parse import quote as _uriquote
import asyncio


async def json_or_text(response):
    text = await response.text(encoding='utf-8')
    try:
        if response.headers['content-type'] == 'application/json':
            return json.loads(text)
    except KeyError:
        pass

    return text


class Route:
    Base = "https://beta.tomon.co/api/v1"

    def __init__(self, path, token):

        self.path = path
        self.token = token
        url = (self.Base + str(self.path))
        self.url = url

        #self.channel_id = parameters.get('channel_id')
        #self.guild_id = parameters.get('guild_id')

    async def post(self, **kwargs):
        return await self.request('POST', self.url, kwargs)

    async def request(self, method, url, *args):
        for each in list(args):
            if 'data' in each:
                payload = each['data']

        headers = {}
        print(self.token)
        # if self.token is not None:
        #     headers['authorization'] = self.auth()

        headers['Content-Type'] = 'application/json'

        kwargs = {}
        kwargs['headers'] = headers
        kwargs['data'] = payload

        try:

            async with aiohttp.request(method=method, url=url, data=payload) as r:
                if r.status == 200:
                    print(await r.json())
                    return await r.json()
                else:
                    print('fail')

        except Exception as e:
            print(e)


class Bot:

    def __init__(self):

        self._route = None
    #    self._token = None
    #   self._session = Session
        self._id = None
        self._name = None
        self._username = None
        self._discriminator = None

    def route(self, path, token=None):
        self._route = Route(path, token)
        return self._route

    # def token(self, token):
    #     self._token = token
    #     return self._token

    def session(self):
        return self._session({zlib: true})

    def id(self):
        return self._id

    def name(self):
        return self._name

    def username(self):
        return self._username

    def discriminator(self):
        return self._discriminator

    def emit(self, event, *args):
        return self.emit(event, *args)

    def on(self, event, listener):
        return emitter.on(event, listener)

    def off(self, event, listener):
        return emitter.off(event, listener)

    def once(self, event, listener):
        return emitter.once(event, listener)

    def ready_test(self, name, username, discriminator):
        print("🤖️ Bot {}({}#{}) is ready to work!".format(
            name, username, discriminator))

    async def _start(self, **kwargs):

        if len(kwargs) == 0:
            print('no parameters')
        credencials = {}
        if len(kwargs) == 1 and 'token' in kwargs:
            credencials['token'] = kwargs['token']
        elif len(kwargs) == 2 and ('full_name' in kwargs) and ('password' in kwargs):
            credencials['full_name'] = kwargs['full_name']
            credencials['password'] = kwargs['password']
        print('⏳ Start authenticating...')
        try:
            info = await self.route(path='/auth/login', token=None).post(data=credencials)

            # self.api.token = info.token
            # self.session.token = info.token
            self._id = info.get('id')
            self._name = info.get('name')
            self._username = info.get('username')
            self._discriminator = info.get('discriminator')
            print("🎫 Bot {}({}#{}) is authenticated.".format(
                info.get('name'), info.get('username'), info.get('discriminator')))

            self.route(path=None, token=info.get('token'))

        except Exception as e:
            print("❌ Authentication failed. Please check your identity.")

        # Session.open()
        print("🚢 Connecting...")

       # self.once('READY', self.ready_test(info.name, info.username, info.discriminator))

    async def start(self, token):
        return await self._start({'token': token})

    async def startWithPassword(self, fullname, password):
        return await self._start(full_name=fullname, password=password)


bot = Bot()

loop = asyncio.get_event_loop()
result = loop.run_until_complete(
    bot.startWithPassword('xiao#8050', '***'))
