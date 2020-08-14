from ..utils.observable import Observable
from . import ws
import json
import enum
import zlib
from threading import Timer

class GatewayOp:
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    HELLO = 3
    HEARTBEAT_ACK = 4
    VOICE_STATE_UPDATE = 5


class Session(Observable):
    BASE_WS = 'wss://gateway.tomon.co/'
    #BASE_WS = 'wss://echo.websocket.org/'

    def __init__(self, zlib=False):
        self._zlib = zlib
        if self._zlib:
            self._url = self.BASE_WS + 'compress=zlib-stream'
        else:
            self._url = self.BASE_WS
        # self = Observable

        self._heartbeatTimer = None
        self._heartbeatInternal = 40000

        self._ws = ws.WS()
        self._ready = False
        self._connected = False

        self._sessionId = None
        self.token = None;
        self._buffer = bytearray()

        self._ws.onOpen = self.handleOpen
        self._ws.onClose = self.handleClose
        self._ws.onMessage = self.handleMessage
        self._ws.onReconnect = self.emit('NETWORK_RECONNECTING')

    def emit(self, event, *args):
        return super().emitter.emit(event, *args)

    def on(self, event, listener):
        return super().emitter.on(event, listener)

    def off(self, event, listener):
        return super().emitter.off(event, listener)

    def once(self, event, listener):
        return super().emitter.once(event, listener)

    def open(self):
        self._ws.open(self._url)

    def close(self, reason=None):
        self._ws.close(reason)

    def send(self, op, d=None):
        self._ws.send({"op":op, "d":d})

    def state(self):
        return self._ws.state

    def connected(self):
        return self._connected

    def ready(self):
        return self._ready

    def handleOpen(self):
        self._connected = True
        # import pdb; pdb.set_trace()
        self.emit('NETWORK_CONNECTED')

    def handleClose(self, reason=None):
        self.stopHeartbeat()
        self._sessionId = None
        self._connected = False
        self._ready = False
        self.emit('NETWORK_DISCONNECTED')

    def unpack(self, data):

        if (isinstance(data, str)):
            data = data.decode(encoding='UTF-8')


        return json.loads(data)

    def handleMessage(self, event):
        msg = event
        print(msg)
        if type(msg) is bytes:
            self._buffer.extend(msg)

            if len(msg) >= 4:
                if msg[-4:] == b'\x00\x00\xff\xff':
                    msg = zlib.decompressobj().decompress(self._buffer)
                    self._buffer = bytearray()

            
            try:
                msg = self.unpack(msg)
            except Exception as e:
                print(e)
        self.handlePacket(msg)

    def handlePacket(self, data):
        op = data.get("op")
        if op == GatewayOp.DISPATCH:
            self.emit(data.get('e'), data)
            self.emit('DISPATCH', data)
        elif op == GatewayOp.IDENTIFY:
            self._ready = True
            self.emit('READY', data)
        elif op == GatewayOp.HELLO:
            self._heartbeatInterval = data.get('d').get('heartbeat_interval')
            self._sessionId = data.get('d').get('session_id')
            self.heartbeat()
            self.emit('HELLO', data)
            self.send(GatewayOp.IDENTIFY, d={"token":self.token}
              
            )
        elif op == GatewayOp.HEARTBEAT:
            self.send(GatewayOp.HEARTBEAT_ACK)
        elif op == GatewayOp.HEARTBEAT_ACK:
            print(data)
            self.emit('HEARTBEAT_ACK')

    def heartbeat(self):
        def startHeartbeat():
            self.emit('HEARTBEAT')
            self.send(GatewayOp.HEARTBEAT)
        self._heartbeatTimer = Timer(self._heartbeatInterval, startHeartbeat)

    def stopHeartbeat(self):
        if self._heartbeatTimer:
            self._heartbeatTimer.cancel()
            self._heartbeatTimer = None
