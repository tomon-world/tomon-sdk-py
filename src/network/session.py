from ..utils.observable import Observable
from .ws import WS
import json
import enum

class WSState(enum.Enum):
	CONNECTING = 1
  	OPEN = 2
 	CLOSING = 3
  	CLOSED = 4
  	RECONNECTING = 5


class GatewayOp(enum.Enum):
	DISPATCH = 0
	HEARTBEAT = 1
	IDENTIFY = 2
	HELLO = 3
	HEARTBEAT_ACK = 4
	VOICE_STATE_UPDATE = 5



class session:

	BASE_WS = 'wss://gateway.tomon.co'

	

	def __init__(self, _ws):

		self._url = self._zlib ? BASE_WS + 'compress=zlib-stream' : BASE_WS
		self._zlib = zlib.decompressobj()
		self._emitter = Observable

		self._ws = WS
		self._ready = False
		self._connected = False

		self._sessionId = None
		# self._inflate = None

		self.token = None;
		self._buffer = bytearray()




	

    def open(self):
    	self._ws.open(self.url)

    def close(self, code, reason):
    	self._ws.close(code, reason)

    def send(self, op, d):
    	self._ws.send({op, d})

    def state():
    	return self._ws.state

    def connected():
    	return self._connected

    def ready():
    	return self._ready

    def handleOpen():
    	self._connected = true
    	self._emitter.emit('NETWORK_CONNECTED')

    def handleClose(code, reason):
    	self.stopHeartbeat()
    	self._sessionId = None
    	self._connected = False
    	self._ready = False
    	self._emitter.emit('NETWORK_DISCONNECTED')


    def unpack(data):
    	if(type(data) not str):
    		data = data.decode('utf-8')
    	return json.loads(data)
    	

    async def close(self, code=4000):
        if self._keep_alive:
            self._keep_alive.stop()
            self._keep_alive = None

        self._close_code = code
        await self.socket.close(code=code)

    async def send(self, data):
    	self._dispatch('socket_raw_send', data)
    	await self._ws.send_str(data) 


    async def handleMessage(self, event):
    	msg = event.get("data")

    	if type(msg) is bytes:
    		self._buffer.extend(msg)

    		if len(msg) >= 4:
    			if msg[-4:] == b'\x00\x00\xff\xff':
    				msg = self._zlib.decompress(self._buffer)
    				self._buffer = bytearray()
    	
        try:
        	packet = self.unpack(msg)
        except Exception as e:
        	print(e)

        self.handlePacket(packet)



    async def handlePacket(self, data):
    	op = data.get("op")
    	if op == GatewayOp.DISPATCH:
    		self._emitter.emit(data.get('e'), data)
    		self._emitter.emit('DISPATCH', data)
    	elif op == GatewayOp.IDENTIFY:
    		self._ready = True
    		self._emitter.emit('READY', data)
    	elif op == GatewayOp.HELLO:
    		self._heartbeatInterval = data.get('d').get('heartbeat_interval')
    		self._sessionId = data.get('d').get('session_id')
    		self.heartbeat()
    		self._emitter.emit('HELLO', data)
    		self.send(GatewayOp.IDENTIFY, {
    			token: self.token
    			})
    	elif op == GatewayOp.HEARTBEAT:
    		self.send(GatewayOp.HEARTBEAT_ACK)
    	elif op == GatewayOp.HEARTBEAT_ACK:	
    		self._emitter.emit('HEARTBEAT_ACK')
    

    def heartbeat(self):
    	self._emitter.emit('HEARTBEAT')
    	self.send(self.HEARTBEAT)
    	# self._heartbeatTimer = settimeout

    def stopHeartbeat(self):
    	if (self._heartbeatTImer):
    		clearTimeout(self._heartbeatTImer)
    		self._hearbeatTimer = None



























