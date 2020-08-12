from node_events import EventEmitter


class Observable:

    emitter = EventEmitter()

    def __init__(self):
        pass

    def on(self, event, listener):
        return emitter.on(event, listener)

    def off(self, event, listener):
        return emitter.off(event, listener)

    def once(self, event, listener):
        return emitter.once(event, listener)

    def emit(self, event, *args):
        return emitter.emit(event, *args)
