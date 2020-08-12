import os
from urllib.parse import quote as _uriquote
import json
import aiohttp
from .utils.observable import Observable

import pdb


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

        # self.channel_id = parameters.get('channel_id')
        # self.guild_id = parameters.get('guild_id')

    def auth(self):
        if (self.token == None):
            return None

        return ('Bearer ' + self.token)

    async def request(self, method, url, *args):

        headers = {}
        payload = {}
        
        for arg in list(args):
            if 'auth' in arg and arg['auth'] == True:
                headers['authorization'] = self.auth()

            if 'data' in arg:
                payload = arg['data']
    
         
            if 'files' in arg:
                payload = aiohttp.FormData()
                if len(arg['files']) == 1:
                    filepath = arg['files'][0]
                    filename = os.path.basename(filepath)
                    payload.add_field('file', open(filepath, 'rb'), filename = filename)

                    if 'data' in arg:
                        payload.add_field('payload_json', json.dumps(arg['data']))

        try:
            async with aiohttp.request(method=method, url=url, data=payload, headers = headers) as r:
                if 300 > r.status >= 200:
                    return await r.json()
                elif (r.status == 404):
                    print("Not Found") 
                elif (r.status == 403):
                    print("Forbidden")
                else:
                    print(await r.json())

        except Exception as e:
            print(e)


    async def post(self, **kwargs):
        return await self.request('POST', self.url, kwargs)

    async def get(self, **kwargs):
        return await self.request('GET', self.url, kwargs)

    async def patch(self, **kwargs):
        return await self.request('PATCH', self.url, kwargs)

    async def put(self, **kwargs):
        return await self.request('PUT', self.url, kwargs)

    async def delete(self, **kwargs):
        return await self.request('DELETE', self.url, kwargs)



class Bot(Observable):

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
            # pdb.set_trace()
            info = await self.route(path='/auth/login', token=None).post(data=credencials, auth=False)

            # self.api.token = info.token
            # self.session.token = info.token
            self._id = info.get('id')
            self._name = info.get('name')
            self._username = info.get('username')
            self._discriminator = info.get('discriminator')
            print("🎫 Bot {}({}#{}) is authenticated.".format(
                info.get('name'), info.get('username'), info.get('discriminator')))

            guild_id = "124456710235492352"
            #/file = [('images', open(image_path))]

            
            msg = {"content":"test_image_upload"}

            uploads = await self.route(path='/channels/151217779805831168/messages', token=info.get('token')).post(data= msg, files = ['./example.jpg'],auth = True)
            ### get channels
            #channels = await self.route(path='/guilds/124456710235492352/channels', token=info.get('token')).get( auth = True)
            print(uploads)

        except Exception as e:
            print("❌ Authentication failed. Please check your identity.")

        # Session.open()
        print("🚢 Connecting...")

       # self.once('READY', self.ready_test(info.name, info.username, info.discriminator))

    async def start(self, token):
        return await self._start({'token': token})

    async def startWithPassword(self, fullname, password):
        return await self._start(full_name=fullname, password=password)
