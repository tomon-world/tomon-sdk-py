from . import route


class Api:

    def __init__(self):
        self._token = None

    def token(self):
        return self._token

    def setToken(self, token):
        self._token = token

    def route(self, path):
        return route.Route(path, self._token)
