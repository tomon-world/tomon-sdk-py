import json
import aiohttp
from .utils.observable import Observable
from .network import route
import asyncio
# from events import EventType
from .network import session
import pdb


class OpCodeEvent:
    DISPATCH = 'DISPATCH'
    HEARTBEAT = 'HEARTBEAT'
    READY = 'READY'
    # IDENTIFY = 'IDENTIFY'1
    HELLO = 'HELLO'
    # HEARTBEAT_ACK = 'HEARTBEAT_ACK'
    # VOICE_STATE_UPDATE = 'VOICE_STATE_UPDATE'


class Bot(Observable):

    def __init__(self):
        super().__init__()
        self._route = None
        self._token = None
        self._session = session.Session(zlib=True)
        self._id = None
        self._name = None
        self._username = None
        self._discriminator = None

    def route(self, path, token=None):
        self._route = route.Route(path, token)
        return self._route

    def token(self):
        return self._token

    def session(self):
        return self._session

    def id(self):
        return self._id

    def name(self):
        return self._name

    def username(self):
        return self._username

    def discriminator(self):
        return self._discriminator

    def emit(self, event, *args):
        return super().emitter.emit(event, *args)

    def on(self, event, listener):
        return super().emitter.on(event, listener)

    def off(self, event, listener):
        return super().emitter.off(event, listener)

    def once(self, event, listener):
        return super().emitter.once(event, listener)

    def ready_test(self, data):
        name = self.name()
        username = self.username()
        discriminator = self.discriminator()
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
            # pdb.set_trace()
            info = await self.route(path='/auth/login', token=None).post(data=credencials, auth=False)
            self._token = info.get('token')
            self._session.token = info.get('token')
            self._id = info.get('id')
            self._name = info.get('name')
            self._username = info.get('username')
            self._discriminator = info.get('discriminator')

            print("🎫 Bot {}({}#{}) is authenticated.".format(
                info.get('name'), info.get('username'), info.get('discriminator')))

        except Exception as e:
            print("❌ Authentication failed. Please check your identity.")
            return

            # self.once ('READY', print)
        print("🚢 Connecting...")

        self.once('READY', self.ready_test)
        self.session().open()

    async def start(self, token):
        return await self._start({'token': token})

    async def startWithPassword(self, fullname, password):
        return await self._start(full_name=fullname, password=password)
