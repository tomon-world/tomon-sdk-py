import asyncio
import json
from enum import Enum

import websocket

try:
    import thread
except ImportError:
    import _thread as thread


class WSState(Enum):
    CONNECTING = 0
    OPEN = 1
    CLOSING = 2
    CLOSED = 3
    RECONNECTING = 4


class TomonWebsocket:
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    HELLO = 3
    HEARTBEAT_ACK = 4
    VOICE_STATE_UPDATE = 5

    class GatewayEvent:
        GUILD_CREATE = 'GUILD_CREATE'
        GUILD_DELETE = 'GUILD_DELETE'
        GUILD_UPDATE = 'GUILD_UPDATE'
        GUILD_POSITION = 'GUILD_POSITION'
        CHANNEL_CREATE = 'CHANNEL_CREATE'
        CHANNEL_DELETE = 'CHANNEL_DELETE'
        CHANNEL_UPDATE = 'CHANNEL_UPDATE'
        CHANNEL_POSITION = 'CHANNEL_POSITION'
        GUILD_ROLE_CREATE = 'GUILD_ROLE_CREATE'
        GUILD_ROLE_DELETE = 'GUILD_ROLE_DELETE'
        GUILD_ROLE_UPDATE = 'GUILD_ROLE_UPDATE'
        GUILD_ROLE_POSITION = 'GUILD_ROLE_POSITION'
        GUILD_MEMBER_ADD = 'GUILD_MEMBER_ADD'
        GUILD_MEMBER_REMOVE = 'GUILD_MEMBER_REMOVE'
        GUILD_MEMBER_UPDATE = 'GUILD_MEMBER_UPDATE'
        MESSAGE_CREATE = 'MESSAGE_CREATE'
        MESSAGE_DELETE = 'MESSAGE_DELETE'
        MESSAGE_UPDATE = 'MESSAGE_UPDATE'
        MESSAGE_REACTION_ADD = 'MESSAGE_REACTION_ADD'
        MESSAGE_REACTION_REMOVE = 'MESSAGE_REACTION_REMOVE'
        MESSAGE_REACTION_REMOVE_ALL = 'MESSAGE_REACTION_REMOVE_ALL'
        EMOJI_CREATE = 'EMOJI_CREATE'
        EMOJI_DELETE = 'EMOJI_DELETE'
        EMOJI_UPDATE = 'EMOJI_UPDATE'
        VOICE_STATE_UPDATE = 'VOICE_STATE_UPDATE'
        USER_TYPING = 'USER_TYPING'
        USER_PRESENCE_UPDATE = 'USER_PRESENCE_UPDATE'

    def _on_message(self, ws, msg):
        payload = json.loads(msg)
        op = payload.get('op')
        data = payload.get('d')
        event = payload.get('e')
        if op != self.DISPATCH:
            if op == self.HEARTBEAT_ACK:
                pass
            if op == self.HELLO:
                self._on_hello(data)
                pass

        if event == self.GatewayEvent.GUILD_CREATE:
            self._run_if_not_none(self.on_guild_create, data)
        if event == self.GatewayEvent.GUILD_DELETE:
            self._run_if_not_none(self.on_guild_delete, data)
        if event == self.GatewayEvent.GUILD_UPDATE:
            self._run_if_not_none(self.on_guild_update, data)
        if event == self.GatewayEvent.GUILD_POSITION:
            self._run_if_not_none(self.on_guild_position, data)
        if event == self.GatewayEvent.CHANNEL_CREATE:
            self._run_if_not_none(self.on_channel_create, data)
        if event == self.GatewayEvent.CHANNEL_DELETE:
            self._run_if_not_none(self.on_channel_delete, data)
        if event == self.GatewayEvent.CHANNEL_UPDATE:
            self._run_if_not_none(self.on_channel_update, data)
        if event == self.GatewayEvent.CHANNEL_POSITION:
            self._run_if_not_none(self.on_channel_position, data)
        if event == self.GatewayEvent.GUILD_ROLE_CREATE:
            self._run_if_not_none(self.on_guild_role_create, data)
        if event == self.GatewayEvent.GUILD_ROLE_DELETE:
            self._run_if_not_none(self.on_guild_role_delete, data)
        if event == self.GatewayEvent.GUILD_ROLE_UPDATE:
            self._run_if_not_none(self.on_guild_role_update, data)
        if event == self.GatewayEvent.GUILD_ROLE_POSITION:
            self._run_if_not_none(self.on_guild_role_position, data)
        if event == self.GatewayEvent.GUILD_MEMBER_ADD:
            self._run_if_not_none(self.on_guild_member_add, data)
        if event == self.GatewayEvent.GUILD_MEMBER_REMOVE:
            self._run_if_not_none(self.on_guild_member_remove, data)
        if event == self.GatewayEvent.GUILD_MEMBER_UPDATE:
            self._run_if_not_none(self.on_guild_member_update, data)
        if event == self.GatewayEvent.MESSAGE_CREATE:
            self._run_if_not_none(self.on_message_create, data)
        if event == self.GatewayEvent.MESSAGE_DELETE:
            self._run_if_not_none(self.on_message_delete, data)
        if event == self.GatewayEvent.MESSAGE_UPDATE:
            self._run_if_not_none(self.on_message_update, data)
        if event == self.GatewayEvent.MESSAGE_REACTION_ADD:
            self._run_if_not_none(self.on_message_reaction_add, data)
        if event == self.GatewayEvent.MESSAGE_REACTION_REMOVE:
            self._run_if_not_none(self.on_message_reaction_remove, data)
        if event == self.GatewayEvent.MESSAGE_REACTION_REMOVE_ALL:
            self._run_if_not_none(self.on_message_reaction_remove_all, data)
        if event == self.GatewayEvent.EMOJI_CREATE:
            self._run_if_not_none(self.on_emoji_create, data)
        if event == self.GatewayEvent.EMOJI_DELETE:
            self._run_if_not_none(self.on_emoji_delete, data)
        if event == self.GatewayEvent.EMOJI_UPDATE:
            self._run_if_not_none(self.on_emoji_update, data)
        if event == self.GatewayEvent.USER_TYPING:
            self._run_if_not_none(self.on_user_typing, data)
        if event == self.GatewayEvent.USER_PRESENCE_UPDATE:
            self._run_if_not_none(self.on_user_presence_update, data)

    def _on_close(self, ws):
        pass

    def _run_if_not_none(self, func, data):
        if func is not None:
            func(data)

    def _on_error(self, ws, error):
        pass

    def reconnect(self):
        self._open = False

        pass

    def _on_open(self, ws):
        payload = {
            "op": self.IDENTIFY,
            "d": {
                "token": self._token
            }
        }
        data = json.dumps(payload)
        ws.send(data)
        self._open = True

    def _on_hello(self, payload):
        self._heartbeat_interval = payload.heartbeat_interval
        self._session_id = payload.session_id

    def send(self, data):
        assert self._open, '连接尚未完成'
        self.ws.send(data)

    def _start_heartbeat(self):
        while self._open:
            try:
                await self.ws.send('ping')
                await asyncio.sleep(self._heartbeat_interval / 1000)
            except websocket.WebSocketException:
                print('Connection with server closed')
                break

    def __init__(self, url, token, enable_trace=True, on_error=None):
        self._url = url
        self._heartbeat_interval = None
        self._token = token
        self._enable_trace = enable_trace
        self._session_id = None
        self._open = False
        self._on_error_func = on_error if on_error is not None else self._on_error

        websocket.enableTrace(enable_trace)
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self._on_message,
                                         on_error=self._on_error_func,
                                         on_open=self._on_open,
                                         on_close=self._on_close)

        # 用户自定义handler
        self.on_identify = None
        self.on_guild_create = None
        self.on_guild_delete = None
        self.on_guild_update = None
        self.on_guild_position = None
        self.on_channel_create = None
        self.on_channel_delete = None
        self.on_channel_update = None
        self.on_channel_position = None
        self.on_guild_role_create = None
        self.on_guild_role_delete = None
        self.on_guild_role_update = None
        self.on_guild_role_position = None
        self.on_guild_member_add = None
        self.on_guild_member_remove = None
        self.on_guild_member_update = None
        self.on_message_create = None
        self.on_message_delete = None
        self.on_message_update = None
        self.on_message_reaction_add = None
        self.on_message_reaction_remove = None
        self.on_message_reaction_remove_all = None
        self.on_emoji_create = None
        self.on_emoji_delete = None
        self.on_emoji_update = None
        self.on_voice_state_update = None
        self.on_user_typing = None
        self.on_user_presence_update = None

    def set_on_error(self, onerror):
        self._on_error_func = onerror
        self.ws.on_error = onerror
