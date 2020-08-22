import time
from enum import Enum
import json
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
            if self.onClose is not None:
                self.onClose(code, reason=None)

        def received_message(self, m):
            if self.onMessage is not None:
                self.onMessage(m.data)

        def unhandled_error(self, error):
            if self.onError is not None:
                self.onError(error)

    @staticmethod
    def retry_delay(times: int) -> float:
        if times == 0:
            return 0.5
        elif times <= 1:
            return 1
        elif times <= 2:
            return 3
        elif times <= 5:
            return 5
        else:
            return 10

    def __init__(self):
        self._url = None
        self._ws = None
        self._retryCount = 0
        self._reconnecting = False
        self._reconnectTimer = None
        self.state = WSState.CLOSED
        self._need_reconnect = False
        self._force_close = False

        self.onOpen = None
        self.onClose = None
        self.onReconnect = None
        self.onError = None
        self.onMessage = None

    def open(self, url: str):
        self._url = url
        if self.state != WSState.CLOSED:
            return
        self._need_reconnect = True
        self._force_close = False
        while self._need_reconnect and not self._force_close:
            self._connect(self._url)
            time.sleep(self.retry_delay(self._retryCount))

    def close(self, code: int, reason=None):
        self._need_reconnect = False
        self._force_close = True
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
        self._ws.onError = self._on_error()
        self._ws.onOpen = self._on_open()
        self._ws.onClose = self._on_close()
        self._ws.onMessage = self._on_message()
        self._ws.connect()
        self._ws.run_forever()

    def _reconnect(self, url: str):
        self._reconnecting = True
        self._need_reconnect = True
        self._retryCount += 1
        if self.onReconnect is not None:
            self.onReconnect(self._retryCount)

    def _close(self, code: int, reason=None):
        if self._ws is not None:
            self.state = WSState.CLOSED
            self._ws.close(code=code, reason=reason)

    def _stop_reconnect(self):
        self._need_reconnect = False
        if self._reconnectTimer is not None:
            self._reconnectTimer.cancel()
            self._reconnectTimer = None

    def _on_open(self):
        def onOpenFunc():
            self.state = WSState.OPEN
            self._retryCount = 0
            self._reconnecting = False
            self._stop_reconnect()
            if self.onOpen is not None:
                self.onOpen()

        return onOpenFunc

    def _on_close(self):
        def on_close_func(code: int, reason=None):
            self.state = WSState.CLOSED
            message = None
            if reason is not None:
                try:
                    data = json.loads(reason)
                    message = data
                except Exception as e:
                    message = reason
            if code == 1006 and not self._force_close:
                self._reconnect(self._url)
            else:
                self._force_close = True
                self._need_reconnect = False
            if self.onClose is not None:
                self.onClose(code, reason=message)

        return on_close_func

    def _on_message(self):
        def on_message_func(data):
            if self.onMessage is not None:
                self.onMessage(data)

        return on_message_func

    def _on_error(self):
        def on_error_func(error):
            self._force_close = True
            self._need_reconnect = False
            if self.onError is not None:
                self.onError(error)

        return on_error_func
