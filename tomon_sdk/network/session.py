from ..utils.observable import Observable
from . import ws
import json
import zlib as zb
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

    def __init__(self, zlib=False):
        super().__init__()
        self._zlib = zlib
        if self._zlib:
            self._url = self.BASE_WS + '?compress=zlib-stream'
        else:
            self._url = self.BASE_WS

        self._heartbeatTimer = None
        self._heartbeatInterval = None

        self._ws = ws.WS()
        self._ready = False
        self._connected = False

        self._sessionId = None
        self.token = None
        self._buffer = bytearray()

        self._ws.onOpen = self.handle_open
        self._ws.onClose = self.handle_close
        self._ws.onMessage = self.handle_message
        self._ws.onError = lambda err: print("[ws] error: {}".format(err))
        self._ws.onReconnect = lambda _: (self.emit('NETWORK_RECONNECTING'), print("[ws] reconnecting"))

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

    def close(self, code: int, reason=None):
        self._ws.close(code, reason=reason)

    def send(self, op, d=None):
        self._ws.send({"op": op, "d": d})

    def state(self):
        return self._ws.state

    def connected(self):
        return self._connected

    def ready(self):
        return self._ready

    def handle_open(self):
        self._connected = True
        self.emit('NETWORK_CONNECTED')

    def handle_close(self, code, reason=None):
        self.stop_heartbeat()
        self._sessionId = None
        self._connected = False
        self._ready = False
        self.emit('NETWORK_DISCONNECTED')

    def handle_message(self, event):
        msg = event
        if type(msg) is bytes:
            self._buffer.extend(msg)
            if len(msg) >= 4:
                if self._buffer[-4:] == b'\x00\x00\xff\xff':
                    msg = zb.decompressobj().decompress(self._buffer)
                    msg = msg.decode(encoding='UTF-8')
                    self._buffer.clear()
                else:
                    return

        self.handle_packet(json.loads(msg))

    def handle_packet(self, data):
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
            self.send(GatewayOp.IDENTIFY, d={"token": self.token})
        elif op == GatewayOp.HEARTBEAT:
            self.send(GatewayOp.HEARTBEAT_ACK)
        elif op == GatewayOp.HEARTBEAT_ACK:
            self.emit('HEARTBEAT_ACK')

    def heartbeat(self):
        def start_heartbeat():
            self.emit('HEARTBEAT')
            self.send(GatewayOp.HEARTBEAT)
            self._heartbeatTimer = Timer(
                self._heartbeatInterval / 1000, start_heartbeat)
            self._heartbeatTimer.start()

        self._heartbeatTimer = Timer(
            self._heartbeatInterval / 1000, start_heartbeat)
        self._heartbeatTimer.start()

    def stop_heartbeat(self):
        if self._heartbeatTimer:
            self._heartbeatTimer.cancel()
            self._heartbeatTimer = None
