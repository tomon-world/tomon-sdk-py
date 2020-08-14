from enum import Enum
import websocket
import json
from threading import Timer

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


class WS:

    @staticmethod
    def retryDelay(times: int) -> int:
        if times <= 0:
            return 500
        elif times <= 1:
            return 1000
        elif times <= 2:
            return 3000
        elif times <= 5:
            return 5000
        else:
            return 100000

    def __init__(self):
        # websocket.enableTrace(True)
        self._ws = None
        self._retryCount = 0
        self._reconnecting = False
        self._reconnectTimer = None
        self.state = WSState.CLOSED
        self._connectError = None

        self.onOpen = None
        self.onClose = None
        self.onReconnect = None
        self.onError = None
        self.onMessage = None

    def open(self, url: str):
        if self.state != WSState.CLOSED:
            return
        self._connect(url)

    def close(self, reason: str):
        if self.state != WSState.CLOSED:
            self._reconnecting = False
            self._close(reason)

    def send(self, data):
        if self.state != WSState.OPEN:
            return
        if self._ws is not None:
            self._ws.send(json.dumps(data))

    def url(self):
        return self._ws.url

    def reconnecting(self):
        return self._reconnecting

    def _connect(self, url: str):
        websocket.enableTrace(True)
        self.state = WSState.CONNECTING
        self._ws = websocket.WebSocketApp(url, on_open=self._onOpen, on_close=self._onClose, on_error=self._onError,
                                          on_message=self._onMessage)

    def _reconnect(self, url: str):
        if self._reconnectTimer is not None:
            self._reconnectTimer.cancel()
        self._reconnecting = True
        self._connectError = None

        def retryFunc():
            self._retryCount += 1
            self._connect(url)
            if self.onReconnect is not None:
                self.onReconnect(count=self._retryCount)

        self.state = WSState.RECONNECTING
        self._reconnectTimer = Timer(self.retryDelay(self._retryCount), retryFunc),

    def _close(self, reason: str):
        if self._ws is not None:
            self.state = WSState.CLOSED
            self._ws.close(reason=reason)

    def _stopReconnect(self):
        if self._reconnectTimer is not None:
            self._reconnectTimer.cancel()
            self._reconnectTimer = None

    def _onOpen(self, ws):
        self.state = WSState.OPEN
        self._retryCount = 0
        self._reconnecting = False
        self._stopReconnect()
        if self.onOpen is not None:
            self.onOpen()

    def _onClose(self, ws):
        self.state = WSState.CLOSING
        if self._connectError is None:
            self._reconnect(self.url())
            if self.onClose is not None:
                self.onClose()
        else:
            if self.onClose is not None:
                self.onClose(reason=str(self._connectError))

    def _onMessage(self, ws, data):
        if self.onMessage is not None:
            self.onMessage(data)

    def _onError(self, ws, error):
        self._connectError = error
        if self.onError is not None:
            self.onError(message=str(error))
