from enum import Enum
import json
from threading import Timer
from ws4py.client.threadedclient import WebSocketClient


class WSState(Enum):
    CONNECTING = 0
    OPEN = 1
    CLOSING = 2
    CLOSED = 3
    RECONNECTING = 4


class WS:
    class _Client(WebSocketClient):
        def __init__(self, url, protocols=None, extensions=None, heartbeat_freq=None,
                     ssl_options=None, headers=None, exclude_headers=None):
            super().__init__(url, protocols=None, extensions=None, heartbeat_freq=None, ssl_options=None, headers=None,
                             exclude_headers=None)
            self.onOpen = None
            self.onClose = None
            self.onError = None
            self.onMessage = None

        def opened(self):
            if self.onOpen is not None:
                self.onOpen()

        def closed(self, code, reason=None):
            print(code, reason)
            if self.onClose is not None:
                self.onClose(code, reason=None)

        def received_message(self, m):
            if self.onMessage is not None:
                self.onMessage(m.data)

        def unhandled_error(self, error):
            if self.onError is not None:
                self.onError(error)

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

    def close(self, code: int, reason=None):
        if self.state != WSState.CLOSED:
            self._reconnecting = False
            self._close(code, reason)

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
        self.state = WSState.CONNECTING
        self._ws = self._Client(url)
        self._ws.onError = self._onError()
        self._ws.onOpen = self._onOpen()
        self._ws.onError = self._onError()
        self._ws.onMessage = self._onMessage()
        self._ws.connect()
        self._ws.run_forever()

    def _reconnect(self, url: str):
        if self._reconnectTimer is not None:
            self._reconnectTimer.cancel()
        self._reconnecting = True

        def retryFunc():
            self._retryCount += 1
            self._connect(url)
            if self.onReconnect is not None:
                self.onReconnect(count=self._retryCount)

        self.state = WSState.RECONNECTING
        self._reconnectTimer = Timer(self.retryDelay(self._retryCount), retryFunc),

    def _close(self, code: int, reason=None):
        if self._ws is not None:
            self.state = WSState.CLOSED
            self._ws.close(code, reason)

    def _stopReconnect(self):
        if self._reconnectTimer is not None:
            self._reconnectTimer.cancel()
            self._reconnectTimer = None

    def _onOpen(self):
        def onOpenFunc():
            self.state = WSState.OPEN
            self._retryCount = 0
            self._reconnecting = False
            self._stopReconnect()
            if self.onOpen is not None:
                self.onOpen()

        return onOpenFunc

    def _onClose(self):
        def onCloseFunc(code: int, reason=None):
            self.state = WSState.CLOSED
            message = None
            if reason is not None:
                try:
                    data = json.loads(reason)
                    message = data
                except Exception as e:
                    message = reason
            if code == 1006:
                self._reconnect(self.url())
            if self.onClose is not None:
                self.onClose(code, message)

        return onCloseFunc

    def _onMessage(self):
        def onMessageFunc(data):
            if self.onMessage is not None:
                self.onMessage(data)

        return onMessageFunc

    def _onError(self):
        def onErrorFunc(error):
            self._connectError = error
            if self.onError is not None:
                self.onError(error)

        return onErrorFunc
