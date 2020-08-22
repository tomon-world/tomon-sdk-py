import asyncio
import threading

from .utils.observable import Observable
from .network import api
from .network import session


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
        self._api = api.Api()
        self._id = None
        self._name = None
        self._username = None
        self._discriminator = None

    def token(self):
        return self._token

    def session(self):
        return self._session

    def api(self):
        return self._api

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
            info = await self.api().route(path='/auth/login').post(data=credencials, auth=False)
            self._token = info.get('token')
            self._session.token = info.get('token')
            self._api.set_token(info.get('token'))
            self._id = info.get('id')
            self._name = info.get('name')
            self._username = info.get('username')
            self._discriminator = info.get('discriminator')

            print("🎫 Bot {}({}#{}) is authenticated.".format(
                info.get('name'), info.get('username'), info.get('discriminator')))

        except Exception as e:
            print("❌ Authentication failed. Please check your identity.")
            return
        print("🚢 Connecting...")
        self.once('READY', self.ready_test)
        try:
            self.session().open()
        except (KeyboardInterrupt, SystemExit):
            pass
        finally:
            print("Bot exit")
            pass

    def start(self, token):
        def callback():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            loop.run_until_complete(self._start(token=token))
            loop.close()

        processThread = threading.Thread(target=callback)
        processThread.start();
        # return await self._start(token=token)

    def start_with_password(self, fullname, password):
        def callback():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            loop.run_until_complete(self._start(full_name=fullname, password=password))
            loop.close()

        processThread = threading.Thread(target=callback)
        processThread.start()
        # return await self._start(full_name=fullname, password=password)
