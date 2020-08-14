from node_events import EventEmitter

class Observable:

    emitter = EventEmitter()

    def __init__(self):
        pass
    
    def on(self, event, listener):
        return self.emitter.on(event, listener)

    def off(self, event, listener):
        return self.emitter.off(event, listener)

    def once(self, event, listener):
        return self.emitter.once(event, listener)

    def emit(self, event, *args):
        return self.emitter.emit(event, *args)
